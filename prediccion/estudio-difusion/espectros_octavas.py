"""Coeficientes efectivos usados y curva comparativa de las hipótesis."""
import json,csv,xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
import ejecutar_octavas_propuesta as s
O=s.O;out=O/'resultados';out.mkdir(exist_ok=True)
root=ET.parse(next((s.B/'reflectores/calculos').glob('base-F1-1000Hz-N600000-seed20261019*/config.xml'))).getroot();mats={m.get('id'):m for m in root.find('surface_absorption_enum')}
base=json.loads((s.B/'malla-base.json').read_text());proposed=json.loads((s.B/'reflectores-absorcion-localizada/media_centro_a060/modelo-materiales.json').read_text());rows=[]
for case,model in [('sin_tratamiento',base),('propuesta',proposed)]:
    for mat in sorted({str(f['idMat']) for f in model['faces']},key=int):
        for hz in s.FREQS:
            b=next(b for b in mats[mat] if int(b.get('freq'))==hz);alpha=float(b.get('absorb'));diff=float(b.get('diffusion'));law=b.get('loi')
            if mat=='201':alpha=s.ABS[hz]
            if mat=='301':alpha=.05;diff=.05;law='2'
            rows.append(dict(estado=case,material_id=int(mat),frecuencia=hz,absorcion=alpha,dispersion=diff,ley=law))
with (out/'coeficientes-usados.csv').open('w',newline='',encoding='utf-8-sig') as fp:w=csv.DictWriter(fp,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(out/'coeficientes-usados.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
x=np.arange(len(s.FREQS));wall=[next(r['absorcion'] for r in rows if r['estado']=='sin_tratamiento' and r['material_id']==115 and r['frecuencia']==hz) for hz in s.FREQS]
fig,ax=plt.subplots(figsize=(10,5),constrained_layout=True)
ax.plot(x,wall,'o-',color='#617b90',label='Muro efectivo de la base');ax.plot(x,[s.ABS[f] for f in s.FREQS],'s-',color='#23877d',label='Paño A1 · hipótesis escalada');ax.plot(x,[.05]*len(x),'^-',color='#c59b42',label='Reflectores · hipótesis rígida')
ax.scatter([0,7],[s.ABS[63],s.ABS[8000]],s=160,facecolors='none',edgecolors='#23877d',label='Extremos extrapolados de A1')
ax.set(xticks=x,xticklabels=s.FREQS,ylim=(0,1.02),xlabel='Banda de octava (Hz)',ylabel='Coeficiente de absorción α',title='Coeficientes usados en la comparación espectral\nA1 es una hipótesis efectiva; el muro de base es una calibración equivalente')
ax.grid(alpha=.18);ax.legend();fig.savefig(out/'espectros-materiales.png',dpi=180);plt.close(fig)
print('Coeficientes usados y gráfico espectral listos.')
