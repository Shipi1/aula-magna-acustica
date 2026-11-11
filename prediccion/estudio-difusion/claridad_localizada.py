"""Añade D50 a las respuestas existentes; no ejecuta ni modifica SPPS."""
from preparar_localizado import O
from analizar import win
import csv,json,xml.etree.ElementTree as ET
import numpy as np

out=O/'resultados'
previous={(r['variante'],r['fuente'],int(r['frecuencia']),r['receptor']):r for r in csv.DictReader((out/'indicadores.csv').open(encoding='utf-8-sig'))}
rows=[]
for meta in sorted((O/'calculos').glob('*/ejecucion.json')):
    d=json.loads(meta.read_text())
    if d['N']!=150000:continue
    root=ET.parse(meta.parent/'config.xml').getroot();s=root.find('sources')[0];source=np.array([float(s.get(k)) for k in ('x','y','z')])
    positions={r.get('name'):np.array([float(r.get(k)) for k in ('x','y','z')]) for r in root.find('recepteursp')}
    result=json.loads((meta.parent/'resultados-lineales.json').read_text())
    for name,cols in result['receptores'].items():
        energy=np.array(next(iter(cols.values())),float);t0=float(np.linalg.norm(positions[name]-source)/342)
        d50=100*win(energy,0,t0+.05)/energy.sum();assert 0<=d50<=100
        old=previous[(d['variante'],d['fuente'],d['frecuencia'],name)]
        rows.append(dict(variante=d['variante'],fuente=d['fuente'],frecuencia=d['frecuencia'],receptor=name,N=d['N'],semilla=d['semilla'],C80_dB=float(old['C80']),D50_pct=float(d50)))
assert len(rows)==840
base={(r['fuente'],r['frecuencia'],r['receptor']):r for r in rows if r['variante']=='base'}
for row in rows:
    ref=base[(row['fuente'],row['frecuencia'],row['receptor'])]
    row['delta_C80_dB']=row['C80_dB']-ref['C80_dB'];row['delta_D50_puntos_porcentuales']=row['D50_pct']-ref['D50_pct']
with (out/'claridad-c80-d50.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
summary=[]
for variant in ('base','R','C','RC','D'):
    for freq in (1000,2000,4000,8000):
        for zone,names in [('P8_P9',['P8','P9']),('virtuales',[f'V{i:02}' for i in range(1,13)]),('piso',['P1','P2','P4','P7']),('bajo',['P3','P5','P6'])]:
            rr=[r for r in rows if r['variante']==variant and r['frecuencia']==freq and r['receptor'] in names]
            summary.append(dict(variante=variant,frecuencia=freq,zona=zone,n=len(rr),**{k:float(np.mean([r[k] for r in rr])) for k in ('C80_dB','D50_pct','delta_C80_dB','delta_D50_puntos_porcentuales')}))
(out/'resumen-claridad-c80-d50.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
for r in summary:
    if r['variante']=='base' and r['zona']=='P8_P9':print(r)
print('840 registros de claridad derivados de respuestas existentes; ninguna simulación nueva.')
