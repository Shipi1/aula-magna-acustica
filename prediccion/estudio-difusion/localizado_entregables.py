"""Vista de localización y OBJ agrupado para revisión geométrica."""
from preparar_localizado import B,O
import json,collections,zipfile,xml.etree.ElementTree as ET,struct
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

m=json.loads((O/'malla-subdividida.json').read_text())
v=np.array(m['vertices']);patches=json.loads((O/'panos.json').read_text());rr=json.loads((O/'receptores-virtuales.json').read_text())
colors={'R':'#8951b0','C':'#278b99','D':'#d69936'}
fig,axs=plt.subplots(1,3,figsize=(15,5),constrained_layout=True)
for ax,k,axes in zip(axs,['R','C','D'],[[1,2],[0,1],[1,2]]):
    ids=patches[k]['faces'];polys=[v[m['faces'][i]['v']][:,axes] for i in ids]
    ax.add_collection(PolyCollection(polys,facecolor=colors[k],edgecolor='white',linewidth=.35));ax.autoscale();ax.set_aspect('equal')
    ax.set_title(f'{k}: '+{'R':'fondo alto','C':'cielo posterior','D':'control desplazado'}[k]+'\n19,2 m²');ax.set_xlabel(['X','Y','Z'][axes[0]]+' (m)');ax.set_ylabel(['X','Y','Z'][axes[1]]+' (m)');ax.grid(alpha=.15)
fig.savefig(O/'panos-localizados.png',dpi=160);plt.close(fig)
fig,ax=plt.subplots(figsize=(11,6),constrained_layout=True)
for r in rr:
    ax.scatter(r['x'],r['y'],c='#278b99');ax.annotate(r['nombre'],(r['x'],r['y']),xytext=(4,-15) if r['nombre']=='V01' else (4,5),textcoords='offset points',fontsize=8)
conf=ET.parse(B.parent/'convergencia-base-D/curva-espectral/G-F1-2000Hz/config.xml').getroot()
for rec in conf.find('recepteursp'):
    if rec.get('name') in ('P8','P9'):
        x,y=[float(rec.get(k)) for k in ('x','y')];ax.scatter(x,y,marker='x',c='#b34359',s=60);ax.annotate(rec.get('name'),(x,y),xytext=(8,5) if rec.get('name')=='P8' else (4,-14),textcoords='offset points')
ax.plot([40.25,40.25],[-8,8],color=colors['R'],lw=4,label='R y D: fondo, distintas alturas')
ax.fill([37,38.2,38.2,37],[-8,-8,8,8],color=colors['C'],alpha=.2,label='C: proyección del cielo')
ax.set(xlabel='X (m)',ylabel='Y (m)',title='Receptores virtuales en planta: 2 m sobre el piso local\nP8/P9 conservados; los virtuales no son mediciones',xlim=(23.5,41.5),ylim=(-12,12));ax.set_aspect('equal');ax.legend(loc='upper left',fontsize=8);ax.grid(alpha=.2)
fig.savefig(O/'receptores-localizados.png',dpi=160);plt.close(fig)

# Parent mapping keeps original surface-group names despite subdivision.
with zipfile.ZipFile(B.parent/'G_base_efectiva_espectral_Lw90.proj') as z:
    root=ET.fromstring(z.read('instance1/projet_config.xml'));offset=0;names={}
    for g in root.iter('gr'):
        if not g.get('facesFile'):continue
        data=z.read('instance1/'+g.get('facesFile'));n=struct.unpack('<i',data[:4])[0]
        for i in range(offset,offset+n):names[i]=g.get('name')
        offset+=n
membership={i:k for k,p in patches.items() for i in p['faces']}
groups=collections.defaultdict(list)
for i,f in enumerate(m['faces']):groups['PANO_'+membership[i] if i in membership else names[f['parent']]].append(f['v'])
with (O/'modelo-localizado.obj').open('w',encoding='utf8') as fp:
    fp.write('# Metros. Geometria de revision; R/C/D son grupos experimentales.\nmtllib modelo-localizado.mtl\n')
    for p in v:fp.write('v '+' '.join(f'{x:.9f}' for x in p)+'\n')
    for group,faces in groups.items():
        key=group[5:] if group.startswith('PANO_') else 'BASE'
        fp.write(f'g {group}\nusemtl {key}\n')
        for face in faces:fp.write('f '+' '.join(str(i+1) for i in face)+'\n')
with (O/'modelo-localizado.mtl').open('w') as fp:
    for name,rgb in [('BASE',(.65,.67,.7)),('R',(.54,.32,.69)),('C',(.15,.55,.60)),('D',(.84,.60,.21))]:
        fp.write('newmtl '+name+'\nKd '+' '.join(map(str,rgb))+'\nKa .2 .2 .2\nd 1\n\n')
print('Mapas y OBJ agrupado generados.')
