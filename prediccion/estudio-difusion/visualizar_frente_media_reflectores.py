"""Mapa del ensayo frente/media y su hipótesis de recorrido especular."""
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import preparar_frente_media_reflectores as p
O=p.O;OUT=O/'resultados';OUT.mkdir(exist_ok=True)
cases=json.loads((O/'variantes.json').read_text())
names={'lateral9':'Laterales Y±9 · 36 m²','lateral8':'Laterales Y±8 · 36 m²','lateral8_adel':'Laterales + adelantados · 60 m²','lateral8_inter':'Laterales + intermedios · 60 m²'}
vv=np.array(p.h.g.MODEL['vertices']);faces=p.h.g.MODEL['faces'];tri=vv[np.array([f['v'] for f in faces])]
mask=np.array([f['idMat'] in (110,112,113) for f in faces])&(tri[:,:,2].min(1)>3.5)&(abs(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0])[:,2])>1e-7)
fig,axs=plt.subplots(2,4,figsize=(18,9),constrained_layout=True)
for col,(case,title) in enumerate(names.items()):
    axs[0,col].add_collection(PolyCollection(tri[mask,:,:2],facecolor='#dcecef',edgecolor='none'))
    for panel in cases[case]:
        face=np.array(p.h.g.corners(panel))[4:8]
        for row,dims in enumerate(((0,1),(0,2))):
            q=face[:,dims];ax=axs[row,col]
            ax.fill(q[:,0],q[:,1],facecolor='#d9a84b',edgecolor='#97680f',alpha=.85,lw=2)
    for row,dims in enumerate(((0,1),(0,2))):
        ax=axs[row,col]
        for name,r in p.h.R.items():
            if name.startswith('V'):
                target=name in p.TARGET
                ax.scatter(r[dims[0]],r[dims[1]],marker='o' if target else 'x',c='#216b9a' if target else '#888888',s=23)
            elif name in ('P8','P9'):ax.scatter(r[dims[0]],r[dims[1]],marker='*',c='#b44236',s=55)
        for source in p.h.S.values():ax.scatter(source[dims[0]],source[dims[1]],marker='^',c='#333333',s=30)
        ax.set(xlim=(0,41),ylim=(-12.5,12.5) if row==0 else (-1,13.5),xlabel='X (m)',ylabel='Y (m)' if row==0 else 'Z global (m)');ax.set_aspect('equal');ax.grid(alpha=.15)
    axs[0,col].set_title(title,fontsize=11)
fig.suptitle('Ensayo dirigido a frente y zona media · planta y perfil\nOcre: paneles · círculos: objetivos virtuales · cruces: controles · estrellas: P8/P9')
fig.savefig(OUT/'geometrias.png',dpi=170);fig.savefig(OUT/'geometrias.svg');plt.close(fig)

diag=json.loads((O/'hipotesis-retorno-lateral.json').read_text())
d=next(r for r in diag if r['fuente']=='F2' and r['receptor']=='V08' and r['muro_y_m']<0)
s=p.h.S['F2'];r=p.h.R['V08'];fig,ax=plt.subplots(figsize=(10,7),constrained_layout=True)
ax.add_collection(PolyCollection(tri[mask,:,:2],facecolor='#edf3f5',edgecolor='none'))
for name,path,color in [('Muro actual',d['muro_actual'],'#666666'),('Plano Y=−9',d['paneles']['lateral9'],'#278c9d'),('Plano Y=−8',d['paneles']['lateral8'],'#b27720')]:
    q=np.array(path['punto']);route=np.array([s,q,r]);ax.plot(route[:,0],route[:,1],label=f"{name}: {path['retardo_ms']:.1f} ms",color=color,lw=2,marker='o',ms=3)
for y in (-11.665,11.665):ax.plot([0,40.25],[y,y],color='#aaa',lw=1)
for case in ('lateral9','lateral8'):
    for panel in cases[case]:
        center=panel['centro'];ax.plot([12.5,18.5],[center[1],center[1]],lw=4,color='#278c9d' if case=='lateral9' else '#b27720')
ax.annotate('F2',s[:2],xytext=(6,8),textcoords='offset points');ax.annotate('V08',r[:2],xytext=(6,8),textcoords='offset points')
ax.set(xlim=(0,41),ylim=(-12.5,12.5),xlabel='X (m)',ylabel='Y (m)',title='Hipótesis geométrica F2–V08: adelantar un retorno lateral\nLos retardos son relativos al sonido directo; no identifican por sí solos picos de la simulación')
ax.set_aspect('equal');ax.legend(loc='upper left');ax.grid(alpha=.15);fig.savefig(OUT/'hipotesis-retorno.png',dpi=170);plt.close(fig)

for case in cases:
    folder=O/case;obj=(folder/'modelo.obj').read_text();obj='mtllib modelo.mtl\n'+'\n'.join(s for s in obj.splitlines() if not s.startswith(('mtllib ','usemtl ')))+'\n'
    m=json.loads((folder/'malla-subdividida.json').read_text())
    for mat in set(f['idMat'] for f in m['faces']):obj=obj.replace(f'g material_{mat}\n',f'g material_{mat}\nusemtl '+('reflector' if mat==301 else 'sala')+'\n')
    (folder/'modelo.obj').write_text(obj);(folder/'modelo.mtl').write_text('newmtl sala\nKd 0.72 0.74 0.76\nnewmtl reflector\nKd 0.86 0.57 0.15\n')
print('Mapas geométricos y cinco modelos OBJ con materiales listos.')
