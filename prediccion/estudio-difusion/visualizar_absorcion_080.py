"""Ubicaciones comparadas; geometría exacta de los paños del estudio .80."""
from analizar_absorcion_080 import O,OUT,CASES,LABELS
import json,numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
m=json.loads((O/'malla-subdividida.json').read_text());v=np.array(m['vertices'])
p=json.loads((O/'panos-absorcion.json').read_text())
specs=json.loads((O/'escenarios.json').read_text())
def polygons(ids):return [v[m['faces'][i]['v']][:,[1,2]] for i in ids]
fig,axs=plt.subplots(4,2,figsize=(13,13),constrained_layout=True)
for ax,case,label in zip(axs.flat,CASES,LABELS):
    ax.add_collection(PolyCollection(polygons(p['total']['faces']),facecolor='#dddddd',edgecolor='white',linewidth=.25))
    if case!='base':
        name=case.removesuffix('_a080')
        ax.add_collection(PolyCollection(polygons(p[name]['faces']),facecolor='#277d92',edgecolor='white',linewidth=.25))
    ax.autoscale();ax.set_aspect('equal');ax.set(xlabel='Y (m)',ylabel='Z global (m)',
        title=label+f" · {specs[case]['area_m2']:.2f} m²".replace('.',','))
fig.suptitle('Paños posteriores comparados · α = 0,80 a 1.000 Hz\nAzul: superficie tratada · gris: muro de referencia')
fig.savefig(OUT/'distribuciones-a080.png',dpi=160);plt.close(fig)
