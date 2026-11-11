"""Geometrías comparadas y auditoría de rutas con todos los paneles presentes."""
from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import preparar_cobertura_reflectores as prep
O=prep.O;OUT=O/'resultados';OUT.mkdir(exist_ok=True)
cases=json.loads((O/'variantes.json').read_text());audit=json.loads((prep.old/'auditoria-posiciones.json').read_text())
fig,plans=plt.subplots(int(np.ceil(len(cases)/4)),4,figsize=(18,8),constrained_layout=True)
fig_elev,elevs=plt.subplots(int(np.ceil(len(cases)/4)),4,figsize=(18,5.5),constrained_layout=True)
axs=np.array([list(plans.flat)[:len(cases)],list(elevs.flat)[:len(cases)]])
checks=[]
model=prep.g.MODEL;vv=np.array(model['vertices']);tri=vv[np.array([f['v'] for f in model['faces']])]
mask=np.array([f['idMat'] in (110,112,113) for f in model['faces']])&(tri[:,:,2].min(1)>3.5)&(abs(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0])[:,2])>1e-7)
for col,(case,panels) in enumerate(cases.items()):
    axs[0,col].add_collection(PolyCollection(tri[mask,:,:2],facecolor='#dcecef',edgecolor='none'))
    for i,p in enumerate(panels):
        cc=np.array(prep.g.corners(p));face=cc[4:8]
        for row,dims in enumerate(((0,1),(0,2))):
            q=face[:,dims];axs[row,col].fill(q[:,0],q[:,1],color='#d9a84b',edgecolor='#97680f',alpha=.8)
            axs[row,col].text(*q.mean(0),str(i+1),fontsize=8)
        for r in p['rutas_utiles']:
            s=prep.S[r['fuente']];target=prep.R[r['receptor']];q=np.array(r['punto'])
            clear=not any(prep.blocks(other,s,q) or prep.blocks(other,q,target) for j,other in enumerate(panels) if j!=i)
            checks.append(dict(variante=case,panel=i+1,fuente=r['fuente'],receptor=r['receptor'],retardo_ms=r['retardo_ms'],corte_finito_estimado_Hz=r['corte_finito_estimado_Hz'],visible_con_todos=clear))
            if clear and (r['fuente'],r['receptor']) in prep.PRIMARY:
                path=np.array([s,q,target])
                for row,dims in enumerate(((0,1),(0,2))):axs[row,col].plot(path[:,dims[0]],path[:,dims[1]],color='#258c9d',alpha=.3,lw=.7)
    for row,dims in enumerate(((0,1),(0,2))):
        ax=axs[row,col]
        for name,p in prep.R.items():
            if name.startswith('V'):
                ax.scatter(p[dims[0]],p[dims[1]],color='#216b9a' if name in prep.SEATS else '#888888',marker='o' if name in prep.SEATS else 'x',s=16)
            elif name in ('P8','P9'):
                ax.scatter(p[dims[0]],p[dims[1]],color='#b44236',marker='*',s=60)
        for name,p in prep.S.items():ax.scatter(p[dims[0]],p[dims[1]],c='#333333',marker='^',s=35)
        ax.set(xlim=(0,41),ylim=(-12.5,12.5) if row==0 else (0,13.5),xlabel='X (m)',ylabel='Y (m)' if row==0 else 'Z global (m)');ax.grid(alpha=.15);ax.set_aspect('equal')
        if row==0:ax.set_title(case+f' · {len(panels)*12} m² frontales',fontsize=11)
    folder=O/case;obj=(folder/'modelo.obj').read_text();obj='mtllib modelo.mtl\n'+'\n'.join(s for s in obj.splitlines() if not s.startswith(('mtllib ','usemtl ')))+'\n'
    m=json.loads((folder/'malla-subdividida.json').read_text())
    for mat in set(f['idMat'] for f in m['faces']):obj=obj.replace(f'g material_{mat}\n',f'g material_{mat}\nusemtl '+('reflector' if mat==301 else 'sala')+'\n')
    (folder/'modelo.obj').write_text(obj);(folder/'modelo.mtl').write_text('newmtl sala\nKd 0.72 0.74 0.76\nnewmtl reflector\nKd 0.86 0.57 0.15\n')
for collection in (plans,elevs):
    for ax in list(collection.flat)[len(cases):]:ax.axis('off')
fig.suptitle('Variantes de orientación y distribución · vista en planta\nOcre: paneles · azul: virtuales sobre butacas · gris: controles sobre madera · estrellas: P8/P9')
fig.savefig(OUT/'geometrias-comparadas.png',dpi=170);fig.savefig(OUT/'geometrias-comparadas.svg');plt.close(fig)
fig_elev.suptitle('Geometrías · proyección longitudinal · cotas globales del modelo')
fig_elev.savefig(OUT/'geometrias-perfil.png',dpi=170);plt.close(fig_elev)
(OUT/'rutas-visibles.json').write_text(json.dumps(checks,indent=2),encoding='utf8')
print('Geometrías dibujadas; rutas útiles visibles:',sum(r['visible_con_todos'] for r in checks),'de',len(checks))
