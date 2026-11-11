"""Informe del experimento dirigido al frente y a la zona media."""
import json,re
import analizar_frente_media_reflectores as a
O=a.O;OUT=a.OUT;ROOT=a.B.parents[1]
def f(x,n=2):return f'{x:.{n}f}'.replace('.',',')
def main():
    summary=json.loads((OUT/'resumen-grupos.json').read_text());means=json.loads((OUT/'medias.json').read_text());diff=json.loads((OUT/'comparaciones.json').read_text());checks=json.loads((OUT/'verificacion-calculos.json').read_text());geometry=json.loads((O/'verificacion-espacial.json').read_text())
    def group(c,g):return next(r for r in summary if r['variante']==c and r['grupo']==g)
    def row(c,s,p):return next(r for r in means if r['variante']==c and r['fuente']==s and r['receptor']==p)
    def delta(c,s,p):return next(r for r in diff if r['variante']==c and r['fuente']==s and r['receptor']==p)
    best=min(a.CASES,key=lambda c:group(c,'frente_media')['error_medio_a50']);bestnew=min(a.PROFILES,key=lambda c:group(c,'frente_media')['error_medio_a50'])
    good=[c for c in a.PROFILES if group(c,'frente_media')['cumplen']==12 and group(c,'campo_prioritario')['cumplen']==3]
    names=a.NAMES
    text=['# Reflectores laterales y combinaciones para frente y zona media',
        '**Aula Magna UTFSM — 9 de noviembre de 2026.**',
        '## 1. Resultado y decisión',
        f"Se calcularon **cinco condiciones nuevas** a 1.000 Hz: cuatro distribuciones físicas de paneles y un control numérico de material. Se ejecutaron 30 corridas principales y diez pilotos. La evaluación principal se limita a **seis posiciones virtuales del frente y la zona media, con dos fuentes: doce combinaciones**. Los puntos posteriores quedan fuera de la selección y permanecen como controles.",
        f"El menor error medio de D50 respecto de 50 % entre las ocho condiciones comparadas corresponde a **{names[best]}**, con {f(group(best,'frente_media')['error_medio_a50'])} puntos porcentuales y {group(best,'frente_media')['cumplen']}/12 respuestas dentro de D50 = 48–52 % y C80 = −2 a +2 dB. Entre las nuevas, el menor error es de **{names[bestnew]}**, con {f(group(bestnew,'frente_media')['error_medio_a50'])} puntos y {group(bestnew,'frente_media')['cumplen']}/12.",
        ('Una variante nueva cumple todos los criterios de esta banda.' if good else '**Ninguna de las condiciones nuevas resuelve simultáneamente las doce respuestas virtuales y los tres pares de campo prioritarios.** El ensayo permite separar mejoras locales de una mejora de cobertura; adelantar una trayectoria especular aislada no garantiza que mejore el balance energético completo.'),
        '## 2. Objetivo y controles',
        'Se mantiene D50 de 48–52 % a 1.000 Hz, con C80 entre −2 y +2 dB como criterio de proyecto. No se interpreta como un óptimo musical universal. El frente incluye V01–V04 (X = 26 m); la franja media incluye V05/V08 (X = 31 m). V06/V07 están sobre madera, no sobre los bloques de butacas; V09–V12 son posteriores. Todos esos controles se conservan sin penalizar sus indicadores al seleccionar el conjunto.',
        'Se observan también F1–P8, F1–P9 y F2–P8 como pares de campo prioritarios. F2–P9 se mantiene como control secundario. P1/P2/P4/P7 representan la platea baja abierta; P3/P5/P6, bajo balcón. Las coordenadas y sus límites de levantamiento son los del [mapa de receptores](MAPA-DE-RECEPTORES-VIRTUALES-PLATEA-ALTA.md).',
        '## 3. Hipótesis geométrica que se puso a prueba',
        'En el modelo existe un recorrido especular visible desde F2 al lateral opuesto (Y = −11,665 m) y luego a V08. El punto de reflexión [16,833; −11,665; 4,171] m pertenece a superficies de material 115 y sus dos tramos están libres en la envolvente original. Su retardo relativo al directo es **55,17 ms**. En V04 hay otro recorrido visible de **61,77 ms**. El retorno simple del plano posterior hacia F2–V08 tiene el primer tramo obstruido, de modo que no se lo identifica como una reflexión posterior visible.',
        'Se adelantó el plano lateral con paneles independientes para explorar si parte del retorno podía pasar a la ventana anterior a 50 ms:',
        '| Par | Muro actual | Panel Y = −9 m | Panel Y = −8 m |',
        '|---|---:|---:|---:|',
        '| F2–V04 | 61,77 ms | 48,44 ms | 43,62 ms |',
        '| F2–V08 | 55,17 ms | 42,72 ms | 38,27 ms |',
        'Estos tiempos proceden del método geométrico de fuente imagen y del tamaño finito del panel. **No identifican automáticamente un pico de la respuesta energética como perteneciente a ese muro.** Las salidas analizadas son histogramas de energía por receptor, no un registro etiquetado de todas las interacciones de cada partícula. La causalidad del efecto se evalúa comparando las variantes completas.',
        '![Hipótesis de recorrido lateral](../prediccion/estudio-difusion/reflectores-frente-media/resultados/hipotesis-retorno.png)',
        '## 4. Geometrías y materiales',
        'Los nuevos paneles laterales son verticales, de 6 × 3 m y 20 mm de espesor. Sus centros son X = 15,5 m, Z = 4,4 m y Y = ±9 o ±8 m. Ocupan X = 12,5–18,5 m y Z = 2,9–5,9 m. Son planos internos a la sala, separados del muro, no un cambio aplicado sobre el material del muro existente. Las combinaciones incorporan el par adelantado o el intermedio del primer ciclo, conservando sus posiciones y orientaciones.',
        '| Condición | Paneles | Área frontal | α a 1.000 Hz | Dispersión |',
        '|---|---:|---:|---:|---:|']
    for c,p in a.PROFILES.items():text.append(f"| {names[c]} | {p['paneles']} | {f(p['area_m2'],0)} m² | {f(p['alpha'],5)} | 0,05 |")
    text += ['', 'El reflector nominal usa α = 0,05 y dispersión = 0,05, con ley Lambert para la fracción dispersada. Se idealiza una superficie rígida sellada tipo tablero sobre bastidor; no se ha caracterizado un producto concreto. Se modelan ambas caras y cantos como sólidos opacos. El área tabulada corresponde a una cara principal, no a la suma de superficies expuestas ni al área de absorción equivalente.',
        'El control «Y±8 · α del muro» mantiene exactamente la malla de Y±8, pero asigna a sus paneles α = 0,24794628455412168, igual al muro efectivo 115 a 1.000 Hz; conserva dispersión 0,05. Es un control numérico, no la definición de un producto de madera. **Igualar el coeficiente por contacto no conserva la absorción total de la sala:** se añaden caras y se interceptan recorridos diferentes. La comparación con Y±8 nominal estudia la sensibilidad al material; la comparación con la referencia incluye geometría y superficie expuesta.',
        '![Distribuciones en planta y perfil](../prediccion/estudio-difusion/reflectores-frente-media/resultados/geometrias.png)',
        '## 5. Procedimiento y comprobaciones',
        'Se mantuvieron fuentes y receptores, materiales originales, potencia sonora global Lw = 90 dB y espectro de la base, fuentes omnidireccionales, 18 °C, humedad relativa 57 % y velocidad 342 m/s. La absorción del aire está activada y la transmisión de las superficies, desactivada. El espectro global de 90 dB no equivale a asignar 90 dB a la banda de 1.000 Hz ni a imponer ese nivel en las butacas. No se modela la directividad del line array.',
        'Se calculó una fuente por corrida, 600.000 partículas, tres semillas (20261019/20261020/20261021), duración 4 s, paso 1 ms y radio receptor 0,31 m. Se promediaron las respuestas energéticas lineales de las tres semillas y después se calcularon los indicadores. Los promedios de zona son medias de los indicadores por combinación, sin fusionar fuentes o posiciones.',
        'Las integraciones se refieren al tiempo directo distancia/342: D50 = 100·E(0–50 ms)/Etotal y C80 = 10·log10[E(0–80 ms)/E(>80 ms)]. Se incluye el frente directo captado por la esfera antes del centro geométrico del arribo. La energía nativa ya es lineal y no se vuelve a elevar al cuadrado. Los rangos entre semillas son descriptivos; no son intervalos de confianza.',
        f"Se reutilizaron 18 corridas principales de referencia, seis redistribuidos y dos posteriores, compatibles en sus condiciones. El análisis reúne **48 corridas principales, 336 respuestas medias y 1.008 respuestas individuales**. La fracción máxima de partículas perdidas de las 30 nuevas es {checks['max_fraccion_perdidas']:.3g}.",
        'Las cinco mallas conservan los 2.340 vértices y 4.692 caras originales como prefijo, tienen envolventes cerradas, volumen de aire consistente con los sólidos añadidos, fronteras marcadas y vecindades tetraédricas recíprocas. Ningún centro tetraédrico queda dentro de un panel. Los 42 segmentos directos de las dos fuentes a los 21 receptores permanecen libres. Se verificó que las esferas receptoras quedan fuera de los paneles y que no hay intersecciones mutuas.',
        '| Condición | Holgura vertical mínima muestreada | Volumen de aire |',
        '|---|---:|---:|']
    for c in a.PROFILES:
        gap=min(r['holgura_vertical']['minimo_m'] for r in geometry if r['variante']==c);tet=json.loads((O/c/'verificacion-tetra.json').read_text())
        text.append(f"| {names[c]} | {f(gap)} m | {f(tet['volumen_m3'],3)} m³ |")
    text += ['', 'Las holguras se muestrearon sobre los pisos del modelo; no son levantamientos del recinto. El modelo no incorpora todos los detalles de iluminación, escenografía ni equipos. Los OBJ y mallas nativas documentan las variantes calculadas; no se creó un nuevo proyecto `.proj` de interfaz.',
        '## 6. Resultados de cobertura: doce combinaciones objetivo',
        '«Cumplen» requiere ambos parámetros dentro de sus rangos. Un promedio de zona cercano a 50 % no implica que todos los puntos cumplan. Error significa media de |D50 − 50|, en puntos porcentuales.',
        '| Condición | D50 frente | D50 media | D50 conjunto | Error a 50 % | Cumplen /12 | C80 >+2 dB /12 |',
        '|---|---:|---:|---:|---:|---:|---:|']
    for c in a.CASES:
        r=group(c,'frente_media');text.append(f"| {names[c]} | {f(group(c,'frente')['D50_medio'])} % | {f(group(c,'media')['D50_medio'])} % | {f(r['D50_medio'])} % | {f(r['error_medio_a50'])} | {r['cumplen']} | {r['C80_sobre2']} |")
    text += ['', '![Mapa F1](../prediccion/estudio-difusion/reflectores-frente-media/resultados/mapa-D50-F1.png)',
        '![Mapa F2](../prediccion/estudio-difusion/reflectores-frente-media/resultados/mapa-D50-F2.png)',
        '## 7. Casos deficitarios y energía temporal',
        'Cada celda muestra D50 (%) / C80 (dB). Los dos puntos siguientes están dentro del objetivo, no son controles posteriores.',
        '| Condición | F2–V04, frente lateral | F2–V08, media lateral |',
        '|---|---:|---:|']
    for c in a.CASES:
        text.append('| '+names[c]+' | '+' | '.join(f"{f(row(c,'F2',p)['D50_pct'])} / {f(row(c,'F2',p)['C80'])}" for p in ('V04','V08'))+' |')
    text += ['', 'Para F2–V08 se separan variaciones de energía absoluta respecto de la referencia. ΔE en dB corresponde a un cociente de energías, no a la diferencia de D50. La fracción 50–80 ms se expresa respecto de la energía total de cada variante.',
        '| Condición | ΔE 0–50 ms | ΔE 50–80 ms | ΔE 80–300 ms | ΔE total | Fracción 50–80 ms |',
        '|---|---:|---:|---:|---:|---:|']
    for c in a.CASES:
        d=delta(c,'F2','V08');text.append('| '+names[c]+' | '+' | '.join(f"{f(d[k])} dB" for k in ('delta_E0_50_dB','delta_E50_80_dB','delta_E80_300_dB','delta_total_dB'))+f" | {f(d['fraccion_50_80_pct'])} % |")
    text += ['', '![Respuestas energéticas comparadas](../prediccion/estudio-difusion/reflectores-frente-media/resultados/energia-V04-V08.png)',
        'Las curvas usan la misma normalización por la energía total de referencia. El suavizado de 3 ms solo facilita la lectura; los parámetros se integran sin suavizar. Un panel puede adelantar una reflexión candidata, interceptar otras, aumentar retornos posteriores y cambiar la energía total captada. Por eso la mejora no se deduce del retardo aislado ni se suma algebraicamente entre tratamientos.',
        'En Y±8 nominal, F2–V08 pierde 0,72 dB de energía anterior a 50 ms y aumenta 0,23 dB en 80–300 ms. El cambio de una trayectoria candidata hacia antes de 50 ms no compensa el resto de las modificaciones. Con el material equivalente al muro, D50 queda en 27,46 %: el déficit tampoco se resuelve igualando el coeficiente de absorción. Estos son efectos netos de las variantes, no una identificación etiquetada de cada reflexión.',
        '## 8. Puntos de campo prioritarios',
        '| Condición | F1–P8 | F1–P9 | F2–P8 | F2–P9, control | Cumplen prioritarios /3 |',
        '|---|---:|---:|---:|---:|---:|']
    for c in a.CASES:text.append('| '+names[c]+' | '+' | '.join(f"{f(row(c,s,p)['D50_pct'])} / {f(row(c,s,p)['C80'])}" for s,p in [('F1','P8'),('F1','P9'),('F2','P8'),('F2','P9')])+f" | {group(c,'campo_prioritario')['cumplen']} |")
    text += ['', '## 9. Efectos sobre otras zonas',
        'Cambios medios respecto de referencia. Se informa ΔT30 de las mismas respuestas energéticas, con los ajustes y valores individuales conservados en los datos. Una diferencia pequeña frente a la dispersión entre semillas no permite declarar un efecto estable.',
        '| Condición | Zona | ΔD50 (puntos) | ΔC80 (dB) | ΔT30 (s) | ΔEDT (s) | Δenergía total (dB) |',
        '|---|---|---:|---:|---:|---:|---:|']
    for c in a.PROFILES:
        for g,label in [('platea_baja','Platea baja'),('bajo_balcon','Bajo balcón'),('posterior_control','Posteriores sobre butacas')]:
            r=group(c,g);text.append('| '+names[c]+' | '+label+' | '+' | '.join(f(r[k]) for k in ('delta_D50_pct','delta_C80','delta_T30','delta_EDT','delta_total_dB'))+' |')
    text += ['', '## 10. Incertidumbre y decisión de continuación',
        'En los siguientes casos se conserva el rango mínimo–máximo entre semillas junto al indicador de la respuesta media. No se usa el número de cumplimientos como una prueba estadística independiente.',
        '| Condición | F2–V08 D50 medio | Rango D50 entre semillas | C80 medio | Rango C80 entre semillas |',
        '|---|---:|---:|---:|---:|']
    for c in a.CASES:
        r=row(c,'F2','V08');text.append(f"| {names[c]} | {f(r['D50_pct'])} % | {f(r['min_semilla_D50'])}–{f(r['max_semilla_D50'])} % | {f(r['C80'])} dB | {f(r['min_semilla_C80'])}–{f(r['max_semilla_C80'])} dB |")
    text += ['', 'El ensayo evalúa cinco condiciones concretas a una banda y con la resolución indicada. Un resultado negativo no descarta todas las orientaciones ni todos los reflectores laterales. Tampoco justifica trasladar puntos porcentuales de la predicción a las mediciones reales como una corrección lineal.',
        'La siguiente búsqueda deberá conservar el objetivo frente/media y comparar **orientaciones segmentadas o curvas de reflectores adelantados/intermedios**, con atención específica a V04/V08 y al posible sombreado de reflexiones útiles. Los retornos posteriores anteriores se conservan como referencia de redistribución, aunque los receptores posteriores ya no sean objetivo. No conviene añadir área de forma indiscriminada ni elegir una variante por un único promedio.',
        'Antes de ampliar bandas o aumentar partículas, se debe seleccionar una geometría con mejora espacial consistente. Después corresponderá sensibilidad a posición/orientación y material, confirmación con mayor resolución y evaluación a 500 Hz y 1/2/4/8 kHz. No se atribuye este resultado a un QRD físico ni se ha simulado una combinación nueva con absorción posterior.',
        '## 11. Datos y documentos relacionados',
        '- [Medias por receptor](../prediccion/estudio-difusion/reflectores-frente-media/resultados/medias.csv), [resultados por semilla](../prediccion/estudio-difusion/reflectores-frente-media/resultados/semillas.csv) y [comparaciones energéticas](../prediccion/estudio-difusion/reflectores-frente-media/resultados/comparaciones.csv).',
        '- [Resumen por zona](../prediccion/estudio-difusion/reflectores-frente-media/resultados/resumen-grupos.csv), [verificación de cálculos](../prediccion/estudio-difusion/reflectores-frente-media/resultados/verificacion-calculos.json) y [verificación de mallas](../prediccion/estudio-difusion/reflectores-frente-media/resultados/verificacion-mallas.json).',
        '- [Carpeta del experimento](../prediccion/estudio-difusion/reflectores-frente-media/README.md): geometrías, parámetros, configuraciones y salidas nativas.',
        '- [Prioridad frente/media](PRIORIDAD-FRENTE-Y-ZONA-MEDIA-PLATEA-ALTA.md), [siete geometrías anteriores](RESULTADOS-GEOMETRIAS-COBERTURA-PLATEA-ALTA.md), [plan de reflectores](PLAN-DE-ESTUDIO-DE-REFLECTORES-PLATEA-ALTA.md), [base teórica](BASE-TEORICA-Y-METODOLOGIA-PREDICCION.md) y [documento central de avances](AVANCES-Y-ESTADO-DEL-ESTUDIO-ACUSTICO.md).', '']
    report=ROOT/'informes/RESULTADOS-REFLECTORES-LATERALES-FRENTE-MEDIA.md';report.write_text('\n\n'.join(text),encoding='utf8')
    # Markdown tables require contiguous lines, not blank lines between rows.
    report.write_text(re.sub(r'\n{3,}','\n\n',re.sub(r'(?m)(^\|[^\n]*)\n\n(?=\|)',r'\1\n',report.read_text())),encoding='utf8')
    print('Informe:',report)
if __name__=='__main__':main()
