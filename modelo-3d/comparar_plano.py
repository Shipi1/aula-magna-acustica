"""Láminas de revisión, usando renders de los PDF locales (no altera planos)."""
from pathlib import Path
import json
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

BASE=Path(__file__).resolve().parent
R=BASE/'revision'
g=json.loads((BASE/'geometria.json').read_text(encoding='utf8'))
v=np.asarray(g['vertices'])
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11})

fig,ax=plt.subplots(figsize=(15,10))
im=Image.open(R/'planta-alta.png')
ax.imshow(im,alpha=.72)
def planline(x,y,**kw):
 ax.plot(145+56.9*np.asarray(x),962.5-56.9*np.asarray(y),**kw)
ys=np.linspace(-11.665,11.665,97)
planline(24.03-3.15*(ys/11.665)**2,ys,color='#007a87',lw=2.4,label='Frente curvo del balcón · v2')
edge=np.array(g['revision']['upper_edge'])
for sign in [-1,1]:
 planline(edge[:,0],sign*edge[:,1],color='#bb4e14',lw=2.5,label='Límite del bloque posterior · v2' if sign==1 else None)
planline([40.25,40.25],[-7.245,7.245],color='#bb4e14',lw=2.5)
planline([31.99,40.25,40.25,31.99],[-11.665,-11.665,11.665,11.665],color='#a1284f',ls='--',lw=1.4,label='Extensión anterior del bloque · v1')
planline([6.35,6.35],[-7.965,7.965],color='#3261bc',lw=2.4,label='Abertura de embocadura · 15,93 m')
planline([40.25,40.25],[-11.665,11.665],color='#555555',ls=':',lw=1.8,label='Cierre exterior retenido · hipótesis')
ax.set_title('Platea alta: contraste del trazado con la planta ARQ-01',loc='left',fontsize=17,pad=15)
ax.legend(loc='lower left',framealpha=.96,fontsize=10)
ax.set_axis_off()
fig.text(.08,.035,'Registro gráfico aproximado: 56,9 px/m. Curvas interpoladas; las líneas no representan un levantamiento en terreno.',fontsize=10)
fig.savefig(R/'comparacion-planta.png',dpi=150,bbox_inches='tight');plt.close(fig)

segments=[]
for f in g['faces']:
 pts=v[f['v']]; hits=[]
 for a,b in zip(pts,np.roll(pts,-1,axis=0)):
  if abs(a[1])<1e-7: hits.append(a)
  if a[1]*b[1]<-1e-12: hits.append(a+(b-a)*(-a[1]/(b[1]-a[1])))
 if len(hits)>=2:
  p=np.unique(np.round(hits,6),axis=0)
  if len(p)==2: segments.append(p[:,[0,2]])
fig,ax=plt.subplots(figsize=(16,7))
ax.imshow(Image.open(R/'corte.png'),alpha=.65)
converted=[np.column_stack((98+56.7*s[:,0],818-56.7*s[:,1])) for s in segments]
ax.add_collection(LineCollection(converted,colors='#007a87',linewidths=1.8,label='Intersección real de la malla v2 con Y=0'))
ax.plot([98,98+40.25*56.7],[818-13.32*56.7]*2,'--',color='#a1284f',lw=2,label='Cielo único de v1')
ax.set_title('Corte central: modelo revisado sobre el corte A del plano',loc='left',fontsize=17,pad=15)
ax.legend(loc='lower right',framealpha=.97)
ax.set_axis_off()
fig.text(.1,.05,'El corte proyecta elementos laterales: no todo su contorno pertenece al plano central. Cielo v2 = cierre equivalente, con retornos inferidos.',fontsize=10)
fig.savefig(R/'comparacion-corte.png',dpi=150,bbox_inches='tight');plt.close(fig)
print('Comparaciones gráficas exportadas.')
