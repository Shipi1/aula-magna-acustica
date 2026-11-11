"""Muro del límite ideal y módulos preparados para una posible fase local."""
from preparar_localizado import B
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
O=B/'absorcion-posterior';m=json.loads((O/'malla-subdividida.json').read_text());v=np.array(m['vertices']);patches=json.loads((O/'panos-absorcion.json').read_text())
fig,axs=plt.subplots(1,2,figsize=(15,5),constrained_layout=True)
polygons=[v[m['faces'][i]['v']][:,[1,2]] for i in patches['total']['faces']]
for ax in axs:
    ax.add_collection(PolyCollection(polygons,facecolor='#dedede',edgecolor='white',linewidth=.4));ax.autoscale();ax.set_aspect('equal');ax.set_xlabel('Y (m)');ax.set_ylabel('Z (m)');ax.grid(alpha=.15)
axs[0].add_collection(PolyCollection(polygons,facecolor='#a54b6a',edgecolor='white',linewidth=.4,alpha=.8));axs[0].set_title('Límite ideal: todo el muro posterior alto\n112,47 m² · α = 1 a 1.000 Hz')
for prefix,color,z in [('sup','#8951b0',11.2),('med','#278b99',9.6)]:
    for j,y in enumerate((-6,-2,2,6),1):
        ids=patches[f'{prefix}_{j}']['faces'];pp=[v[m['faces'][i]['v']][:,[1,2]] for i in ids]
        axs[1].add_collection(PolyCollection(pp,facecolor=color,edgecolor='white',linewidth=.4));axs[1].text(y,z,f'{prefix.upper()}{j}\n4,8 m²',ha='center',va='center',fontsize=8,color='white')
axs[1].set_title('Paños preparados para búsqueda localizada\nSu cálculo depende de la factibilidad de la etapa A')
fig.savefig(O/'muro-y-modulos.png',dpi=160);plt.close(fig)
print('Vista posterior generada.')
