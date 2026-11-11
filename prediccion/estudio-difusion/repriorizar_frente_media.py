"""Relectura de cálculos existentes al delimitar el objetivo a frente y media."""
from pathlib import Path
import json,csv,numpy as np
B=Path(__file__).resolve().parent;O=B/'reflectores-cobertura/resultados'
rows=json.loads((O/'medias.json').read_text())
objective=json.loads((O.parent/'objetivo-frente-media.json').read_text())
names={'base':'Referencia','combinado':'Cuatro anteriores','cobertura4':'Cobertura 4','equilibrio4':'Equilibrio 4','cobertura6':'Cobertura 6','central5':'Anterior + central 5','retornos2':'Posteriores 4 × 3 m','retornos_compactos2':'Posteriores 6 × 2 m','mixta6':'Mixta 6'}
groups={'frente':objective['frente_butacas'],'media':objective['media_butacas'],'posterior_butacas_control':objective['posterior_butacas_control'],'frente_media':objective['frente_butacas']+objective['media_butacas']}
summaries=[]
for case in names:
    for group,recs in groups.items():
        rr=[r for r in rows if r['variante']==case and r['receptor'] in recs];ds=[float(r['D50_pct']) for r in rr];cs=[r['C80'] for r in rr]
        summaries.append(dict(variante=case,grupo=group,n=len(rr),D50_medio=float(np.mean(ds)),C80_medio=float(np.mean(cs)),
            error_medio_a50=float(np.mean([abs(x-50) for x in ds])),D50_min=min(ds),D50_max=max(ds),C80_min=min(cs),C80_max=max(cs),
            cumplen=sum(48<=float(r['D50_pct'])<=52 and -2<=r['C80']<=2 for r in rr),
            D50_bajo48=sum(d<48 for d in ds),D50_sobre52=sum(d>52 for d in ds),C80_sobre2=sum(c>2 for c in cs)))
(O/'resumen-frente-media.json').write_text(json.dumps(summaries,indent=2),encoding='utf8')
with (O/'resumen-frente-media.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(summaries[0]));w.writeheader();w.writerows(summaries)
def fr(x,n=2):return f'{x:.{n}f}'.replace('.',',')
def get(case,group):return next(r for r in summaries if r['variante']==case and r['grupo']==group)
text=['# Prioridad de estudio: frente y zona media de la platea alta',
    '**Actualización:** 9 de noviembre de 2026. **Origen:** decisión del usuario de concentrar el objetivo en las filas delanteras y medias. Se reinterpretan resultados ya calculados; no se ejecutaron nuevas simulaciones ni se cambiaron posiciones o respuestas.',
    '## 1. Alcance vigente',
    'La optimización se concentra en **la zona delantera como prioridad y la zona media como parte del objetivo**, manteniendo D50 de 48–52 % y C80 máximo +2 dB a 1.000 Hz, con la referencia de balance −2 a +2 dB. Las posiciones posteriores dejan de exigir el cumplimiento de esos rangos para seleccionar una geometría. Se mantienen como controles separados, fuera de la función objetivo.',
    '| Sector | Posiciones | Combinaciones con F1/F2 | Papel |',
    '|---|---|---:|---|',
    '| Delantero, X = 26 m | V01, V02, V03 y V04 | 8 | Prioridad principal de optimización |',
    '| Medio sobre butacas, X = 31 m | V05 y V08 | 4 | Objetivo espacial, evaluado por separado del frente |',
    '| Posterior sobre butacas, X = 36 m | V10 y V11 | 4 | Control, fuera del objetivo |',
    '| Madera expuesta alta | V06, V07, V09 y V12 | 8 | Control, fuera del objetivo |',
    'El nuevo conjunto virtual de optimización tiene **seis posiciones y doce combinaciones**. V09–V12 quedan fuera del objetivo: V09/V12 ya eran controles sobre madera y V10/V11 dejan de ser exigencias de cobertura. V06/V07 son controles sobre madera del tramo medio y no se incorporan como butacas.',
    'Se conservan los pares de campo prioritarios F1–P8, F1–P9 y F2–P8, y F2–P9 como control secundario. P1–P7 siguen separando platea baja y bajo balcón. Los posteriores no penalizan el incumplimiento de D50/C80 en la selección; se muestran para registrar qué cambia en el resto de la sala.',
    '## 2. Alcance y explicación física son decisiones distintas',
    'Priorizar frente y media es una decisión de alcance. **La cercanía al muro posterior no garantiza que C80 siempre sea mayor:** una reflexión puede llegar antes o después de 80 ms respecto del directo, y el indicador depende de la energía de ambas ventanas y de los demás recorridos. No se presume una claridad posterior inevitablemente excesiva.',
    'La referencia a 1.000 Hz presenta este patrón descriptivo:',
    '| Sector de butacas virtuales | D50 medio | C80 medio | Rango de C80 |',
    '|---|---:|---:|---:|']
for group,label in [('frente','Delantero'),('media','Medio'),('posterior_butacas_control','Posterior')]:
    r=get('base',group);text.append(f"| {label} | {fr(r['D50_medio'])} % | {fr(r['C80_medio'])} dB | {fr(r['C80_min'])} a {fr(r['C80_max'])} dB |")
text+=['', 'En promedio el C80 posterior es mayor, pero todos los valores posteriores de referencia están entre +0,63 y +1,48 dB. Además, F1–V10 (posterior) tiene C80 de aproximadamente +0,63 dB, menor que F1–V08 (medio), aproximadamente +1,17 dB. El patrón medio no permite afirmar que cada punto trasero tenga más claridad que cualquier punto delantero.',
    '## 3. Reevaluación de las geometrías ya calculadas',
    'Los siguientes valores utilizan solo las doce combinaciones delanteras e intermedias. Se promedian parámetros individuales calculados sobre las respuestas energéticas medias de tres semillas. No se mezclan fuentes actuando simultáneamente. La media conjunta da a cada combinación el mismo peso, no a cada metro cuadrado de audiencia.',
    '| Geometría | D50 frente | D50 medio | D50 frente + media | C80 frente + media | Distancia media a D50 de 50 % | Cumplen ambos rangos |',
    '|---|---:|---:|---:|---:|---:|---:|']
for case,label in names.items():
    r=get(case,'frente_media');front=get(case,'frente');mid=get(case,'media')
    text.append(f"| {label} | {fr(front['D50_medio'])} % | {fr(mid['D50_medio'])} % | {fr(r['D50_medio'])} % | {fr(r['C80_medio'])} dB | {fr(r['error_medio_a50'])} puntos | {r['cumplen']}/12 |")
text+=['', '### Cómo cambia la comparación',
    '- **Seis paneles redistribuidos:** el frente alcanza D50 medio de 50,70 % y C80 medio de +1,56 dB, pero la zona media queda en 41,65 % de D50. La media frontal no significa que sus ocho combinaciones cumplan: lo hacen dos de ocho.',
    '- **Dos posteriores de 4 × 3 m:** proporcionan el menor error medio frente + media entre los casos ensayados, aproximadamente 4,36 puntos, y mejoran la zona media a 45,13 % de D50. La ubicación del tratamiento y la del público objetivo son cosas distintas: una superficie posterior puede enviar energía hacia el frente y el centro.',
    '- **Dos posteriores de 6 × 2 m:** su resultado anterior de 5/16 en butacas pasa a 3/12 en el nuevo objetivo. Dos de aquellos cumplimientos pertenecían a V10/V11 con alguna fuente y ahora son controles.',
    '- **F2–V08 permanece dentro del objetivo:** está en la franja media, X = 31 m, Y = +9 m. Su D50 de referencia es 27,98 % y el 21,73 % de su energía está entre 50 y 80 ms. El déficit principal no desaparece al sacar la franja posterior de la optimización.',
    'Ninguna de las geometrías ya ensayadas cumple ambos rangos en las doce combinaciones nuevas a la vez. El cambio de alcance modifica la comparación y las prioridades; no transforma retrospectivamente los cálculos en cumplimiento de una meta distinta sin identificarlo.',
    '## 4. Consecuencia para la próxima búsqueda',
    '1. Puntuar cobertura útil hacia V01–V05 y V08, con los pares de campo prioritarios conservados; retirar V10/V11 del puntaje objetivo.',
    '2. Comparar frente y media por separado, además de su resumen de doce combinaciones. Una mejora frontal no compensa automáticamente un déficit medio.',
    '3. Mantener las posiciones posteriores en las salidas como control, sin exigir que alcancen el mismo D50/C80. Conservar los datos históricos y su antiguo denominador de dieciséis.',
    '4. Examinar los recorridos que aportan 50–80 ms en la zona media, especialmente F2–V08, y probar cómo la geometría puede redistribuirlos junto con los aportes 0–50 ms.',
    '5. Mantener las restricciones geométricas, el material de comparación y los controles de las zonas inferiores. La ubicación de un reflector podrá ser adelantada, intermedia o posterior si beneficia la zona objetivo.',
    '## 5. Referencias y datos',
    '- [Resumen frente/media/posterior CSV](../prediccion/estudio-difusion/reflectores-cobertura/resultados/resumen-frente-media.csv).',
    '- [Resumen frente/media/posterior JSON](../prediccion/estudio-difusion/reflectores-cobertura/resultados/resumen-frente-media.json).',
    '- [Definición del objetivo revisado](../prediccion/estudio-difusion/reflectores-cobertura/objetivo-frente-media.json).',
    '- [Mapa y coordenadas de receptores](MAPA-DE-RECEPTORES-VIRTUALES-PLATEA-ALTA.md).',
    '- [Comparación de siete geometrías, con alcance histórico de dieciséis combinaciones sobre butacas](RESULTADOS-GEOMETRIAS-COBERTURA-PLATEA-ALTA.md).',
    '- [Plan de reflectores](PLAN-DE-ESTUDIO-DE-REFLECTORES-PLATEA-ALTA.md).',
    '- [Documento central de avances](AVANCES-Y-ESTADO-DEL-ESTUDIO-ACUSTICO.md).']
report=B.parents[1]/'informes/PRIORIDAD-FRENTE-Y-ZONA-MEDIA-PLATEA-ALTA.md';report.write_text('\n\n'.join(text).replace('|\n\n|','|\n|')+'\n',encoding='utf8');print(report)
