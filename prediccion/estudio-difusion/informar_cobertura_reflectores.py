"""Informe de seis geometrías comparadas; criterios y restricciones explícitos."""
from pathlib import Path
import json,math
import analizar_cobertura_reflectores as a
O=a.O;OUT=a.OUT
def f(x,n=2):return f'{x:.{n}f}'.replace('.',',')
def main():
    means=json.loads((OUT/'medias.json').read_text());diff=json.loads((OUT/'comparaciones.json').read_text());summary=json.loads((OUT/'resumen-grupos.json').read_text());checks=json.loads((OUT/'verificacion-calculos.json').read_text())
    variants=json.loads((O/'variantes.json').read_text());gaps=json.loads((OUT/'holguras-verticales.json').read_text())
    assert len(variants)==7 and checks['nuevas']==42
    def result(c,grp):return next(r for r in summary if r['variante']==c and r['grupo']==grp)
    best=min(variants,key=lambda c:result(c,'butacas_virtuales')['error_medio_a50'])
    counts=max(variants,key=lambda c:result(c,'butacas_virtuales')['cumplen'])
    complete=[c for c in variants if result(c,'butacas_virtuales')['cumplen']==16 and result(c,'prioritarios')['cumplen']==3]
    names=a.NAMES
    text=['# Comparación de geometrías para la cobertura acústica de platea alta',
        '**Teatro Aula Magna UTFSM — 9 de noviembre de 2026.**',
        '## 1. Resultado principal',
        f"Se compararon **siete geometrías nuevas** a 1.000 Hz. La menor distancia media de D50 respecto de 50 % en las dieciséis combinaciones virtuales sobre butacas corresponde a **{names[best]}**, con {f(result(best,'butacas_virtuales')['error_medio_a50'])} puntos de error absoluto medio y {result(best,'butacas_virtuales')['cumplen']}/16 respuestas dentro de ambos rangos. La mayor cantidad de cumplimientos entre las nuevas corresponde a **{names[counts]}**, con {result(counts,'butacas_virtuales')['cumplen']}/16. Ambos criterios se muestran porque una media más cercana y un mayor número dentro de un intervalo estrecho pueden favorecer geometrías diferentes.",
        'El objetivo se mantiene en **D50 de 48–52 % y C80 entre −2 y +2 dB** como criterios de proyecto. Los pares prioritarios son F1–P8, F1–P9 y F2–P8; F2–P9 permanece como control secundario. No se modificaron las metas para seleccionar una variante.',
        ('Ninguna de las siete variantes reúne ambos rangos en los tres pares prioritarios y las dieciséis combinaciones virtuales sobre butacas a la vez. Los resultados se interpretan como avances y diferencias de cobertura.' if not complete else 'Cumplimiento nominal en los tres pares y dieciséis combinaciones virtuales: '+', '.join(names[c] for c in complete)+'. Los rangos por semilla permiten revisar su estabilidad.'),
        '## 2. Muestreo y comparación',
        'Se mantienen los 21 receptores y las dos fuentes calculadas por separado. Los virtuales se separan según la superficie del modelo: **ocho posiciones sobre butacas × dos fuentes = 16 combinaciones**; **cuatro posiciones sobre madera expuesta × dos fuentes = 8 controles**. El antiguo conteo de 24 mezclaba ambos grupos; no se interpreta como porcentaje de público.',
        'Se ejecutaron **42 corridas principales nuevas de 600.000 partículas y tres semillas por fuente y geometría**, más **14 pilotos de 20.000 partículas**. Se reutilizaron doce corridas del estudio anterior: seis de referencia sin paneles y seis de su combinación de cuatro paneles. En total se analizan 54 corridas principales, de las cuales doce son reutilizadas, con 21 receptores por corrida.',
        'Las semillas son 20261019, 20261020 y 20261021. Se promedian energías lineales antes de recalcular D50/C80 y decaimientos. Se conservan Lw global 90 dB y espectro de referencia, fuente omnidireccional idealizada, radio receptor 0,31 m, duración 4 s, paso 1 ms, 18 °C, 57 % HR y absorción atmosférica activa. El material de los reflectores permanece en α = 0,05 y s = 0,05 a 1.000 Hz, con transmisión desactivada. La comparación aísla cambios geométricos sin reajustar los materiales de la sala.',
        'La envolvente original y sus materiales se conservan en todas las variantes. Cada panel es un sólido cerrado de 20 mm, con su volumen excluido del aire tetraédrico. La referencia utiliza la misma representación original y cadena de exportación que el estudio anterior; se conserva su identidad por huellas de archivos y no se vuelve a calibrar para cada geometría.',
        '## 3. Geometrías comparadas',
        '| Identificador | Distribución | Paneles | Dimensiones por panel | Área frontal total |',
        '|---|---|---:|---|---:|',
        '| cobertura4 | Selección de rutas tempranas sobre los sectores de butacas, dando mayor peso a déficits de referencia | 4 | 4 × 3 m | 48 m² |',
        '| equilibrio4 | Selección con recompensa de equilibrio entre franjas delantera, intermedia y posterior | 4 | 4 × 3 m | 48 m² |',
        '| cobertura6 | Misma geometría cobertura4, con dos módulos adicionales | 6 | 4 × 3 m | 72 m² |',
        '| central5 | Cuatro paneles del estudio anterior más un módulo elegido para aportar a V02/V03 | 5 | 4 × 3 m | 60 m² |',
        '| retornos2 | Dos reflectores elevados en el sector posterior, adelantados respecto del muro | 2 | 4 × 3 m | 24 m² |',
        '| retornos_compactos2 | Dos paneles posteriores más anchos y menos altos, con el eje largo horizontal | 2 | 6 × 2 m | 24 m² |',
        '| mixta6 | Cuatro paneles anteriores más los dos posteriores compactos | 6 | Cuatro de 4 × 3 m y dos de 6 × 2 m | 72 m² |',
        'Las cuatro primeras variantes proceden de una búsqueda de posiciones X = 12–28 m, Y = −7/0/+7 m y Z = 8/9/10 m. Se conservaron 468 propuestas de posición y orientación con rutas útiles y compatibilidad geométrica. El puntaje pondera las posiciones deficitarias y equilibra profundidad según el caso; es una herramienta de selección geométrica, no una predicción de D50/C80.',
        'Se puntuaron rutas especulares con retardo relativo menor que 45 ms y corte conservador de reflector finito no mayor que 1.000 Hz. Se incluyó la ocultación de rutas entre paneles al seleccionar conjuntos. Las posiciones, normales y puntos de reflexión quedan en los archivos de geometría. La ley geométrica de cada panel cambia realmente: no se representa la nueva forma aumentando un coeficiente de difusión.',
        'Las dos variantes posteriores se añadieron para estudiar otra familia de recorridos. En retornos2 se exploraron 516 propuestas y quedaron 69 al aplicar la reserva vertical descrita más abajo. En retornos_compactos2 se conservaron 75 propuestas y se forzó que el primer módulo tuviera una ruta útil hacia V10/V11. Se mantuvo el área de 12 m² por módulo al pasar de 4 × 3 a 6 × 2 m, aunque también cambian posición y orientación; no se atribuye el resultado exclusivamente a la relación de aspecto.',
        'La variante mixta se añadió al observar efectos diferentes entre grupos: la cobertura6 acercó más el promedio virtual a 50 %, mientras los posteriores compactos consiguieron más respuestas dentro de ambos rangos. La mixta prueba esa distribución con los cuatro paneles anteriores, usando los mismos 72 m² de cobertura6. Es una elección adaptativa, no una validación independiente de una geometría preseleccionada.',
        '![Geometrías comparadas](../prediccion/estudio-difusion/reflectores-cobertura/resultados/geometrias-comparadas.png)',
        '![Geometrías en proyección longitudinal](../prediccion/estudio-difusion/reflectores-cobertura/resultados/geometrias-perfil.png)',
        '## 4. Restricciones espaciales verificadas',
        'Se comprobaron paneles dentro de la envolvente, cajas sin intersección mutua, continuidad de la envolvente original, esferas receptoras fuera de los paneles y conservación de los segmentos directos de F1/F2 hacia los 21 receptores. Los reflejos entre paneles pueden ocultarse: esa comprobación es distinta de la de sonido directo y se conserva en el registro de rutas.',
        'La holgura vertical se muestreó en 50 puntos de ambas caras de cada panel, buscando el piso modelado más alto bajo cada muestra. Los valores siguientes son **mínimos muestreados sobre el modelo**, no alturas globales Z ni una medición del recinto. Para las variantes posteriores se utilizó una reserva geométrica de 2,31 m = 2 m de altura de receptor + 0,31 m de radio. Es una condición de este estudio, no una exigencia normativa.',
        '| Variante | Holgura vertical mínima muestreada | Tetraedros | Volumen de aire |',
        '|---|---:|---:|---:|']
    for c in variants:
        t=json.loads((O/c/'verificacion-tetra.json').read_text());h=min(r['minimo_m'] for r in gaps if r['variante']==c)
        text.append(f"| {names[c]} | {f(h)} m | {t['tetraedros']} | {f(t['volumen_m3'],3)} m³ |")
    text += ['', 'Los elementos de iluminación, escenografía y line array que no estén representados por geometría identificada no forman parte de esta prueba de colisiones. Las comprobaciones anteriores corresponden al volumen modelado y a las fuentes del estudio. Los [datos de holgura](../prediccion/estudio-difusion/reflectores-cobertura/resultados/holguras-verticales.json) identifican cada punto de control y su piso.',
        '## 5. Cobertura en los puntos virtuales sobre butacas',
        'Todos los conteos siguientes usan el mismo denominador: **16 respuestas, ocho posiciones y dos fuentes**. La media no sustituye el cumplimiento por posición; el error medio es la distancia absoluta de D50 respecto de 50 %, en puntos porcentuales.',
        '| Geometría | D50 medio | Error medio respecto de 50 % | D50 mínimo–máximo | Cumplen D50 y C80 | D50 <48 % | D50 >52 % | C80 >+2 dB |',
        '|---|---:|---:|---:|---:|---:|---:|---:|']
    for c in a.CASES:
        r=result(c,'butacas_virtuales')
        text.append('| '+names[c]+f" | {f(r['D50_medio'])} % | {f(r['error_medio_a50'])} puntos | {f(r['D50_min'])}–{f(r['D50_max'])} % | {r['cumplen']}/16 | {r['bajo48']}/16 | {r['sobre52']}/16 | {r['C80_sobre2']}/16 |")
    text += ['', '![Mapa D50 con F1](../prediccion/estudio-difusion/reflectores-cobertura/resultados/mapa-D50-butacas-F1.png)',
        '![Mapa D50 con F2](../prediccion/estudio-difusion/reflectores-cobertura/resultados/mapa-D50-butacas-F2.png)',
        '## 6. Puntos prioritarios y F2–P9',
        'Cada celda muestra **D50 (%) / C80 (dB)**. F2–P9 se conserva visible, aunque no es un requisito excluyente para estos conjuntos.',
        '| Geometría | F1–P8 | F1–P9 | F2–P8 | F2–P9, control | Cumplen prioritarios |',
        '|---|---:|---:|---:|---:|---:|']
    for c in a.CASES:
        cells=[]
        for pair in a.PRIMARY+[('F2','P9')]:
            r=next(r for r in means if r['variante']==c and (r['fuente'],r['receptor'])==pair);cells.append(f"{f(r['D50_pct'])} / {f(r['C80'])}")
        text.append('| '+names[c]+' | '+' | '.join(cells)+f" | {result(c,'prioritarios')['cumplen']}/3 |")
    text += ['', '![Comparación de pares prioritarios](../prediccion/estudio-difusion/reflectores-cobertura/resultados/comparacion-prioritarios.png)',
        'Las barras y los archivos individuales muestran el rango entre tres semillas, no un intervalo de confianza. Un exceso de unas décimas sobre 52 % se distingue de un déficit espacial de diez o veinte puntos; el conteo estricto conserva los umbrales sin convertirlos en fronteras perceptuales.',
        '## 7. Diagnóstico temporal: el caso F2–V08',
        'En la referencia, F2–V08 tiene D50 ≈ 27,98 %, C80 ≈ −0,05 dB y **21,73 % de energía entre 50 y 80 ms**. Parte importante de la energía que no contribuye a D50 sí pertenece al numerador de C80. Esto ayuda a explicar por qué mejorar ambos parámetros requiere mirar tres ventanas y no simplemente añadir más reflexiones.',
        'Como balance algebraico, si solo se añadiera energía anterior a 50 ms y todo lo demás permaneciera fijo, llevar ese D50 a 50 % daría C80 cercano a **+2,7 dB**. Ese balance no es una nueva simulación ni una imposibilidad para cualquier tratamiento: señala la necesidad de cambiar también la distribución de 50–80 ms y/o la energía posterior. Las variantes posteriores buscan investigar cambios de recorrido; no se presume que hayan eliminado una reflexión concreta de la referencia.',
        '| Geometría | D50 F2–V08 | C80 F2–V08 | Δenergía 0–50 ms | Δenergía 50–80 ms | Δenergía 80–300 ms |',
        '|---|---:|---:|---:|---:|---:|']
    for c in a.CASES:
        r=next(r for r in diff if r['variante']==c and r['fuente']=='F2' and r['receptor']=='V08')
        text.append('| '+names[c]+f" | {f(r['D50'])} % | {f(r['C80'])} dB | {f(r['delta_E0_50_dB'])} dB | {f(r['delta_E50_80_dB'])} dB | {f(r['delta_E80_300_dB'])} dB |")
    text += ['', '## 8. Controles y efectos en otras zonas',
        'Los controles sobre madera se conservan separados de la audiencia. Los cambios se expresan como medias de diferencias individuales frente a la referencia, a 1.000 Hz; los CSV mantienen los extremos y cada receptor.',
        '| Variante | Grupo | ΔD50 (puntos) | ΔC80 (dB) | ΔT30 (s) | ΔEDT (s) | Δnivel de banda (dB) |',
        '|---|---|---:|---:|---:|---:|---:|']
    groupnames={'madera_virtual':'Madera alta, control','platea_baja':'Platea baja','bajo_balcon':'Bajo balcón'}
    for c in variants:
        for grp in groupnames:
            r=result(c,grp);text.append('| '+names[c]+' | '+groupnames[grp]+' | '+' | '.join(f(r[k]) for k in ('delta_D50_pct','delta_C80','delta_T30','delta_EDT','delta_total_dB'))+' |')
    text += ['', '## 9. Lectura del resultado y continuación',
        'La geometría de seis paneles redistribuidos logra **50,12 % / +1,59 dB en F1–P8**, **50,35 % / +1,40 dB en F1–P9** y **54,60 % / +1,84 dB en F2–P8**. F2–P9, mantenido como control, llega a **50,28 % / +1,73 dB**. El efecto sobre ese control confirma que su déficit no debe considerarse una consecuencia inevitable de la distancia.',
        'Los dos paneles posteriores de 6 × 2 m consiguen cinco cumplimientos virtuales y elevan el mínimo virtual a 36,57 %, frente a 27,98 % de referencia, pero sus tres pares prioritarios permanecen por debajo de 48 %. La mezcla con los cuatro anteriores no suma simplemente sus ventajas: F1–P9 pasa a 54,55 % y +2,42 dB, y cuatro combinaciones virtuales exceden +2 dB. Ese ensayo conserva la misma área de 72 m² de cobertura6 y permite distinguir el efecto de distribución del mero aumento de superficie.',
        'La comparación debe conservar conjuntamente tres lecturas: acercamiento de D50 a 50 %, C80 por posición y distribución espacial. Una geometría que ayuda a P8/P9 puede seguir dejando sectores virtuales por debajo de 48 % o sobrepasar 52 % en otros. Los mapas permiten identificar ese patrón sin reducirlo a una media global.',
        'La selección geométrica basada en rutas no garantizó el resultado energético: los paneles también interceptan trayectorias existentes y cambian las reflexiones de orden superior. Por eso se calcularon las variantes completas con SPPS, en lugar de sumar respuestas de paneles individuales.',
        'El diagnóstico de F2–V08 indica una línea de continuación concreta: examinar qué superficies alimentan 50–80 ms y contrastar una redistribución de esas llegadas, además del aporte 0–50 ms. Cualquier complemento posterior de absorción debe compararse por separado y combinado, conservando la claridad y la energía de las demás posiciones. No se atribuye causalidad a una pared solo por el valor de D50.',
        'Estos resultados corresponden a 1.000 Hz, material nominal y las fuentes idealizadas actuales. No se han calculado aquí otras bandas, variantes de material ni una nueva confirmación de 4,8 millones de partículas. La variación entre semillas y las hipótesis físicas permanecen en el registro, y los cambios predictivos no se suman automáticamente a las mediciones.',
        '## 10. Datos y modelos',
        f"Se verificaron las {checks['nuevas']} corridas principales nuevas y las doce reutilizadas: fuentes, receptores, parámetros comunes, materiales y huellas de entrada. Las series son finitas y no negativas. La pérdida máxima en las nuevas fue {f(checks['max_fraccion_perdidas']*100,4)} %. También se verificaron cierre y volumen de las mallas.",
        '- [Variantes: posición, orientación, dimensiones y rutas](../prediccion/estudio-difusion/reflectores-cobertura/variantes.json).',
        '- [Criterios de selección geométrica](../prediccion/estudio-difusion/reflectores-cobertura/criterios-geometricos.json).',
        '- [Indicadores medios y rangos por semilla](../prediccion/estudio-difusion/reflectores-cobertura/resultados/medias.csv).',
        '- [Comparación individual](../prediccion/estudio-difusion/reflectores-cobertura/resultados/comparaciones.csv).',
        '- [Resumen por grupo](../prediccion/estudio-difusion/reflectores-cobertura/resultados/resumen-grupos.csv).',
        '- [Verificación de las corridas](../prediccion/estudio-difusion/reflectores-cobertura/resultados/verificacion-calculos.json).',
        '- [Verificación geométrica](../prediccion/estudio-difusion/reflectores-cobertura/resultados/verificacion-geometrias.json).',
        '- [Archivo nativo verificado](../prediccion/estudio-difusion/reflectores-cobertura/resultados/verificacion-compactacion.json).',
        '- [Primer estudio de reflectores](RESULTADOS-INICIALES-REFLECTORES-PLATEA-ALTA.md).',
        '- [Documento central de avances](AVANCES-Y-ESTADO-DEL-ESTUDIO-ACUSTICO.md).']
    for c in variants:text.append(f"- [Modelo OBJ: {names[c]}](../prediccion/estudio-difusion/reflectores-cobertura/{c}/modelo.obj).")
    text += ['Los OBJ tienen MTL contiguo con los paneles diferenciados. Se conservan CBIN, MBIN, geometría JSON, configuraciones, registros y energías lineales, junto con las salidas nativas archivadas sin pérdida. El proyecto de referencia y las mediciones se conservan sin cambios.']
    target=O.parents[2]/'informes/RESULTADOS-GEOMETRIAS-COBERTURA-PLATEA-ALTA.md';target.write_text('\n\n'.join(text).replace('|\n\n|','|\n|')+'\n',encoding='utf8');print(target)
if __name__=='__main__':main()
