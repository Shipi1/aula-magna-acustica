"""Vistas 3D de las geometrías efectivamente usadas en la comparación."""
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import proj3d
from matplotlib.collections import PolyCollection
from matplotlib.patches import Patch
import comparar_sala_propuesta as a
import preparar_reflectores as geom
B=a.B;O=a.O
models={'sin_tratamiento':json.loads((B/'malla-base.json').read_text()),'propuesta':json.loads((a.shared.O/'media_centro_a060/modelo-materiales.json').read_text())}
panels=json.loads((a.shared.O/'paneles-fijos.json').read_text());coords=json.loads((B/'reflectores/auditoria-posiciones.json').read_text())
def geometry(m):
    v=np.array(m['vertices']);t=v[np.array([f['v'] for f in m['faces']])];ids=np.array([f['idMat'] for f in m['faces']]);return t,ids
def draw3d(ax,m,treated=False,azim=-120):
    tri,ids=geometry(m)
    near=(np.ptp(tri[:,:,1],axis=1)<1e-5)&(tri[:,:,1].mean(1)<-11.5)
    keep=(ids!=108)&~near
    for selected,color,alpha in [((ids==113)&keep,'#9bb8c8',.95),(np.isin(ids,[110,111])&keep,'#c8b392',.95),((ids==112)&keep,'#83939b',.95),
        (~np.isin(ids,[108,110,111,112,113,201,301])&keep,'#bfc6cd',.08)]:
        if selected.any():
            if np.isin(ids[selected],201).all():color='#267e85'
            ax.add_collection3d(Poly3DCollection(tri[selected],facecolor=color,edgecolor='none',alpha=alpha,zsort='average'))
    if treated:
        for mat,color in [(301,'#d6a347'),(201,'#267e85')]:
            chosen=tri[ids==mat];ax.add_collection3d(Poly3DCollection(chosen,facecolor=color,edgecolor=color,linewidth=.3,alpha=1,zsort='average'))
    for name,p in coords['fuentes'].items():ax.scatter(*p,marker='^',c='#333',s=25);ax.text(p[0],p[1],p[2]+.4,name,fontsize=8)
    ax.text(3,0,.1,'Escenario',fontsize=9);ax.text(30,0,7.7,'Platea alta',fontsize=9,color='#355e74')
    ax.set(xlim=(0,41),ylim=(-12,12),zlim=(-1,13),xlabel='X (m)',ylabel='Y (m)',zlabel='Z (m)');ax.set_box_aspect((41,24,14));ax.view_init(elev=25,azim=azim);ax.grid(False)
    for axis in (ax.xaxis,ax.yaxis,ax.zaxis):axis.pane.fill=False
    if treated:
        for i,p in enumerate(panels,1):
            x,y,_=proj3d.proj_transform(*p['centro'],ax.get_proj());ax.annotate('R'+str(i),xy=(x,y),xytext=(-15 if i%2 else 10,17),textcoords='offset points',fontsize=9,color='#754a06',fontweight='bold',arrowprops=dict(arrowstyle='-',color='#97680f',lw=.7),zorder=100)
        x,y,_=proj3d.proj_transform(40.25,0,9.6,ax.get_proj());ax.annotate('A1 · 9,6 m²',xy=(x,y),xytext=(-20,24),textcoords='offset points',fontsize=9,color='#126169',fontweight='bold',arrowprops=dict(arrowstyle='-',color='#267e85',lw=.7),zorder=100)
fig=plt.figure(figsize=(17,7),layout='constrained')
for i,(c,m) in enumerate(models.items(),1):
    ax=fig.add_subplot(1,2,i,projection='3d');draw3d(ax,m,c=='propuesta');ax.set_title('Sala sin tratamiento propuesto' if c=='sin_tratamiento' else 'Propuesta: cuatro reflectores inclinados + paño absorbente',fontsize=12)
fig.suptitle('Comparación de los modelos 3D · misma cámara y escala\nVista abierta: cielos y muro lateral cercano omitidos solo en la imagen; las simulaciones conservan el recinto cerrado',fontsize=12)
fig.legend(handles=[Patch(facecolor='#d6a347',label='R1–R4 · reflectores'),Patch(facecolor='#267e85',label='A1 · absorción localizada'),Patch(facecolor='#9bb8c8',label='Superficies equivalentes de butacas')],loc='lower center',ncol=3,frameon=False)
fig.savefig(O/'modelos-3D-comparados.png',dpi=190);plt.close(fig)
fig=plt.figure(figsize=(12,7),layout='constrained');ax=fig.add_subplot(111,projection='3d');draw3d(ax,models['propuesta'],True,azim=-135)
ax.set_title('Propuesta mixta · segunda perspectiva del interior\nR1–R4: paneles rígidos inclinados · A1: paño posterior de 8 × 1,2 m',fontsize=12);fig.savefig(O/'detalle-propuesta-3D.png',dpi=190);plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(15,6),sharex=True,sharey=True,constrained_layout=True)
for ax,(c,m) in zip(axes,models.items()):
    tri,ids=geometry(m);mask=np.isin(ids,[110,111,112,113]);ax.add_collection(PolyCollection(tri[mask,:,:2],facecolor='#d6e0e4',edgecolor='none'))
    for name,p in coords['fuentes'].items():ax.scatter(p[0],p[1],marker='^',color='#333',s=30);ax.annotate(name,p[:2],xytext=(4,5),textcoords='offset points',fontsize=8)
    for name in a.TARGET:
        p=coords['receptores'][name];ax.scatter(p[0],p[1],c='#367a9e',s=25);ax.annotate(name,p[:2],xytext=(4,4),textcoords='offset points',fontsize=8)
    if c=='propuesta':
        for i,p in enumerate(panels,1):
            q=np.array(geom.corners(p))[4:8];ax.fill(q[:,0],q[:,1],color='#d6a347',edgecolor='#97680f',alpha=.8);ax.text(p['centro'][0],p['centro'][1],'R'+str(i),fontsize=9)
        ax.plot([40.25,40.25],[-4,4],color='#267e85',lw=5);ax.text(39.2,0,'A1',ha='right',fontsize=10,color='#126169')
    ax.set(xlim=(0,42),ylim=(-12,12),xlabel='X (m)',ylabel='Y (m)',title='Sala sin tratamiento' if c=='sin_tratamiento' else 'Propuesta mixta');ax.set_aspect('equal');ax.grid(alpha=.15)
fig.suptitle('Cambios geométricos en planta · puntos azules: seis receptores objetivo\nEl paño A1 se representa por su proyección; su altura es Z = 9,0–10,2 m')
fig.savefig(O/'modelos-planta.png',dpi=190);plt.close(fig)
print('Dos perspectivas 3D y comparación en planta generadas desde las mallas del estudio.')
