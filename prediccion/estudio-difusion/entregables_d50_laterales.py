"""Paños y geometría de revisión del ensayo de D50."""
from preparar_localizado import B
import json,collections,csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
O=B/'d50-laterales'
m=json.loads((O/'malla-subdividida.json').read_text());v=np.array(m['vertices']);panos=json.loads((O/'panos.json').read_text());keys=('R','Lneg','Lpos')
colors={'R':'#8951b0','Lneg':'#278b99','Lpos':'#c17b25'}
fig,axs=plt.subplots(1,3,figsize=(15,5),constrained_layout=True)
for ax,k in zip(axs,keys):
    axes=[1,2] if k=='R' else [0,2];p=panos[k]
    polygons=[v[m['faces'][i]['v']][:,axes] for i in p['faces']]
    ax.add_collection(PolyCollection(polygons,facecolor=colors[k],edgecolor='white',linewidth=.5));ax.autoscale();ax.set_aspect('equal')
    ax.set(title=f'{k} · '+{'R':'Fondo alto','Lneg':'Lateral Y negativo','Lpos':'Lateral Y positivo'}[k]+f'\n{p["area_m2"]:.2f} m²',xlabel=('Y' if k=='R' else 'X')+' (m)',ylabel='Z (m)');ax.grid(alpha=.15)
fig.savefig(O/'panos-d50.png',dpi=160);plt.close(fig)
membership={i:k for k in keys for i in panos[k]['faces']};groups=collections.defaultdict(list)
for i,f in enumerate(m['faces']):groups['PANO_'+membership[i] if i in membership else f'MATERIAL_{f["idMat"]}'].append(f['v'])
with (O/'modelo-panos-d50.obj').open('w') as fp:
    fp.write('# Metros; grupos de revisión geométrica, no materiales acústicos.\nmtllib modelo-panos-d50.mtl\n')
    for p in v:fp.write('v '+' '.join(f'{x:.9f}' for x in p)+'\n')
    for g,faces in groups.items():
        fp.write(f'g {g}\nusemtl '+(g[5:] if g.startswith('PANO_') else 'BASE')+'\n')
        for face in faces:fp.write('f '+' '.join(str(i+1) for i in face)+'\n')
with (O/'modelo-panos-d50.mtl').open('w') as fp:
    for name,rgb in [('BASE',(.65,.67,.7)),('R',(.54,.32,.69)),('Lneg',(.15,.55,.60)),('Lpos',(.76,.48,.15))]:
        fp.write('newmtl '+name+'\nKd '+' '.join(map(str,rgb))+'\nKa .2 .2 .2\nd 1\n\n')

# Record candidate paths; no amplitude or causal attribution is inferred.
paths=[]
with (B/'resultados/recorridos-candidatos-malla-vigente.csv').open(encoding='utf-8-sig') as fp:
    for r in csv.DictReader(fp):
        if r['orden']!='1' or 'lateral' not in r['superficies']:continue
        p=json.loads(r['rebotes_xyz'])[0]
        r['interceptado_por_laterales_altos']=26<=p[0]<=34 and 8<=p[2]<=10.4
        paths.append(r)
assert len(paths)==8 and not any(x['interceptado_por_laterales_altos'] for x in paths)
(O/'recorridos-laterales-tempranos.json').write_text(json.dumps(paths,indent=2,ensure_ascii=False),encoding='utf8')
print('Paños, OBJ y contraste geométrico de retornos laterales preparados.')
