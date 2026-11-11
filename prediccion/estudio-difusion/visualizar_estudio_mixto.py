"""Ubicación de paños en el muro posterior, separada de los reflectores."""
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import analizar_estudio_mixto as a
O=a.O;OUT=a.OUT;m=json.loads((O/'referencia/modelo-materiales.json').read_text());vv=np.array(m['vertices']);tri=vv[np.array([f['v'] for f in m['faces']])]
rear=(abs(tri[:,:,0]-40.25).max(1)<1e-5)&np.array([f['idMat']==115 for f in m['faces']])
fig,axes=plt.subplots(1,4,figsize=(16,5),sharex=True,sharey=True,constrained_layout=True)
for ax,c in zip(axes,list(a.PROFILES)[1:]):
    p=a.PROFILES[c];ax.add_collection(PolyCollection(tri[rear,:,1:3],facecolor='#e2e5e7',edgecolor='none'))
    ax.add_collection(PolyCollection(tri[p['caras'],:,1:3],facecolor='#26838c' if p['alpha']==.6 else '#174c57',edgecolor='none'))
    ax.set(xlim=(-12,12),ylim=(6.5,12.5),xlabel='Y (m)',ylabel='Z global (m)',title=a.NAMES[c].replace(' · ','\n'));ax.set_aspect('equal');ax.grid(alpha=.15)
fig.suptitle('Absorción localizada · elevación del muro posterior X = 40,25 m\nSe conservan los cuatro reflectores inclinados en todas las condiciones')
fig.savefig(OUT/'panos-posteriores.png',dpi=170);fig.savefig(OUT/'panos-posteriores.svg');plt.close(fig)
print('Mapa de cuatro tratamientos posteriores listo.')
