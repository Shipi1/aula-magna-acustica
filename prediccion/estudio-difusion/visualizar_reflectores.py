"""Vistas y comprobación de rutas en la geometría conjunta real."""
from pathlib import Path
import json,itertools
import numpy as np
import matplotlib.pyplot as plt
import preparar_reflectores as g
O=g.O;OUT=O/'resultados';OUT.mkdir(exist_ok=True)
chosen=json.loads((O/'paneles-elegidos.json').read_text())
audit=json.loads((O/'auditoria-posiciones.json').read_text());sources=audit['fuentes'];receivers=audit['receptores']
checks=[]
fig,axs=plt.subplots(2,len(chosen),figsize=(5.3*len(chosen),9),constrained_layout=True)
base=(g.A,g.E1,g.E2)
for col,(case,panels) in enumerate(chosen.items()):
    m=json.loads((O/case/'malla-subdividida.json').read_text());v=np.array(m['vertices']);tri=v[np.array([f['v'] for f in m['faces']])]
    g.A=tri[:,0];g.E1=tri[:,1]-g.A;g.E2=tri[:,2]-g.A
    visible_paths=[]
    for i,p in enumerate(panels):
        cc=np.array(g.corners(p));face=cc[4:8]
        for row,dims in enumerate(((0,1),(0,2))):
            ax=axs[row,col];poly=face[:,dims];poly=np.vstack([poly,poly[0]])
            ax.fill(poly[:,0],poly[:,1],color='#d29323',alpha=.7);ax.plot(poly[:,0],poly[:,1],color='#9a6710')
            ax.text(*np.mean(poly[:-1],axis=0),str(i+1),fontsize=9)
        for r in p['rutas']:
            s=np.array(sources[r['fuente']]);target=np.array(receivers[r['receptor']]);hit=np.array(r['punto'])
            clear=g.visible(s,hit) and g.visible(hit,target)
            checks.append(dict(variante=case,panel=i+1,**r,visible_con_todos_los_paneles=clear))
            if clear and (r['fuente'],r['receptor']) in [('F1','P8'),('F1','P9'),('F2','P8')]:
                visible_paths.append(r)
                pts=np.array([s,hit,target])
                for row,dims in enumerate(((0,1),(0,2))):axs[row,col].plot(pts[:,dims[0]],pts[:,dims[1]],color='#277d92',alpha=.4,lw=.9)
    for row,dims in enumerate(((0,1),(0,2))):
        ax=axs[row,col]
        for name,p in receivers.items():
            if not (name.startswith('V') or name in ('P8','P9')):continue
            ax.scatter(p[dims[0]],p[dims[1]],s=12 if name.startswith('V') else 40,color='#377e45')
            if name in ('P8','P9'):ax.annotate(name,(p[dims[0]],p[dims[1]]),xytext=(5,-14 if row==1 and name=='P8' else 9),textcoords='offset points',fontsize=8)
        for name,p in sources.items():
            ax.scatter(p[dims[0]],p[dims[1]],s=40,color='#b6503a',marker='x')
            ax.annotate(name,(p[dims[0]],p[dims[1]]),xytext=(-14,-13 if row==1 and name=='F1' else 10),textcoords='offset points',fontsize=8)
        ax.set(xlabel='X (m)',ylabel='Y (m)' if row==0 else 'Z global (m)',xlim=(0,41))
        ax.grid(alpha=.15)
        if row==0:ax.set_ylim(-13,13);ax.set_aspect('equal');ax.set_title(f'{case} · {12*len(panels)} m² frontales')
        else:
            ax.set_ylim(0,14);ax.set_aspect('equal')
    # Export materials for OBJ viewers; panel faces retain a distinct group.
    folder=O/case;obj='\n'.join(line for line in (folder/'modelo.obj').read_text().splitlines() if not line.startswith(('mtllib ','usemtl ')))+'\n';obj='mtllib modelo.mtl\n'+obj
    for mat in sorted(set(f['idMat'] for f in m['faces'])):
        obj=obj.replace(f'g material_{mat}\n',f'g material_{mat}\nusemtl '+('reflector' if mat==301 else 'sala')+'\n')
    (folder/'modelo.obj').write_text(obj)
    (folder/'modelo.mtl').write_text('newmtl sala\nKd 0.72 0.74 0.76\nnewmtl reflector\nKd 0.86 0.57 0.15\n')
g.A,g.E1,g.E2=base
(OUT/'rutas-con-obstaculos.json').write_text(json.dumps(checks,indent=2),encoding='utf8')
fig.suptitle('Reflectores: planta y proyección longitudinal\nOcre: paneles · azul: rutas primarias visibles · verde: receptores altos · rojo: fuentes')
fig.savefig(OUT/'ubicaciones-y-rutas.png',dpi=160);plt.close(fig)
print('Rutas comprobadas:',len(checks),'ocultas por otros paneles:',sum(not x['visible_con_todos_los_paneles'] for x in checks))
