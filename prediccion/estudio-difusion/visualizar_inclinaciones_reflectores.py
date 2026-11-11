"""Geometrías y rotaciones a igual área para inspección del experimento."""
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import preparar_inclinaciones_reflectores as p
O=p.O;OUT=O/'resultados';OUT.mkdir(exist_ok=True)
cases={'original':p.original,**json.loads((O/'variantes.json').read_text())}
names={'original':'Originales','vertical':'Giro vertical','horizontal':'Giro horizontal','combinada':'Ambos ejes','segmentada':'Ocho módulos'}
vv=np.array(p.h.g.MODEL['vertices']);faces=p.h.g.MODEL['faces'];tri=vv[np.array([f['v'] for f in faces])]
mask=np.array([f['idMat'] in (110,112,113) for f in faces])&(tri[:,:,2].min(1)>3.5)&(abs(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0])[:,2])>1e-7)
fig,axs=plt.subplots(2,5,figsize=(20,8),constrained_layout=True)
for col,(case,ps) in enumerate(cases.items()):
    axs[0,col].add_collection(PolyCollection(tri[mask,:,:2],facecolor='#dcecef',edgecolor='none'))
    for i,panel in enumerate(ps,1):
        face=np.array(p.h.g.corners(panel))[4:8];q=np.array(panel['centro']);n=np.array(panel['normal'])
        for row,dims in enumerate(((0,1),(0,2))):
            ax=axs[row,col];cc=face[:,dims];ax.fill(cc[:,0],cc[:,1],facecolor='#d9a84b',edgecolor='#97680f',alpha=.65)
            ax.text(*q[list(dims)],str(i),fontsize=7)
            ax.quiver(q[dims[0]],q[dims[1]],n[dims[0]],n[dims[1]],angles='xy',scale_units='xy',scale=.5,color='#9b382b',width=.007)
    for row,dims in enumerate(((0,1),(0,2))):
        ax=axs[row,col]
        for name,r in p.h.R.items():
            if name.startswith('V'):ax.scatter(r[dims[0]],r[dims[1]],marker='o' if name in p.TARGET else 'x',color='#216b9a' if name in p.TARGET else '#999',s=18)
            elif name in ('P8','P9'):ax.scatter(r[dims[0]],r[dims[1]],marker='*',c='#b44236',s=45)
        for r in p.h.S.values():ax.scatter(r[dims[0]],r[dims[1]],marker='^',c='#333',s=25)
        ax.set(xlim=(0,41),ylim=(-12.5,12.5) if row==0 else (0,13.5),xlabel='X (m)',ylabel='Y (m)' if row==0 else 'Z global (m)');ax.set_aspect('equal');ax.grid(alpha=.15)
    axs[0,col].set_title(names[case]+' · 48 m²',fontsize=11)
fig.suptitle('Orientación y segmentación · planta y perfil\nOcre: paneles · flechas: normales de la cara útil · círculos: objetivos · cruces: controles')
fig.savefig(OUT/'geometrias.png',dpi=170);fig.savefig(OUT/'geometrias.svg');plt.close(fig)
for case in cases:
    if case=='original':continue
    folder=O/case;m=json.loads((folder/'malla-subdividida.json').read_text());obj=(folder/'modelo.obj').read_text()
    obj='mtllib modelo.mtl\n'+'\n'.join(s for s in obj.splitlines() if not s.startswith(('mtllib ','usemtl ')))+'\n'
    for mat in set(f['idMat'] for f in m['faces']):obj=obj.replace(f'g material_{mat}\n',f'g material_{mat}\nusemtl '+('reflector' if mat==301 else 'sala')+'\n')
    (folder/'modelo.obj').write_text(obj);(folder/'modelo.mtl').write_text('newmtl sala\nKd 0.72 0.74 0.76\nnewmtl reflector\nKd 0.86 0.57 0.15\n')
print('Geometrías comparadas y cuatro OBJ coloreados listos.')
