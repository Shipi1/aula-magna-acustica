"""Informe trazable de la continuación autorizada alfa .80."""
from analizar_absorcion_080 import O,OUT,CASES,LABELS
from pathlib import Path
import json

def f(x,n=2):return f'{x:.{n}f}'.replace('.',',')

def main():
    comparisons=json.loads((OUT/'comparaciones.json').read_text(encoding='utf8'))
    means=json.loads((OUT/'respuestas-medias.json').read_text(encoding='utf8'))
    zones=json.loads((OUT/'resumen-zonas.json').read_text(encoding='utf8'))
    specs=json.loads((O/'escenarios.json').read_text(encoding='utf8'))
    checks=json.loads((OUT/'verificacion.json').read_text(encoding='utf8'))
    names=dict(zip(CASES,LABELS))
    full=next(r for r in comparisons if r['variante']=='total_a080' and r['fuente']=='F2' and r['receptor']=='P9')
    local=[r for r in comparisons if r['variante'] in CASES[2:] and r['fuente']=='F2' and r['receptor']=='P9']
    winners=[c for c in CASES[1:] if all(r['cumple_conjunto'] for r in comparisons if r['variante']==c and r['receptor'] in ('P8','P9'))]
    report=['# Absorción posterior α = 0,80: pared completa y paneles localizados',
        '**Teatro Aula Magna UTFSM — 9 de noviembre de 2026.**',
        '## 1. Pregunta y alcance',
        'Se estudió si reducir energía posterior mediante absorción en el fondo de la platea alta permite acercarse a **D50 de 48–52 % a 1.000 Hz**, conservando **C80 entre −2 y +2 dB** como criterio de proyecto. Este rango no se presenta como un requisito normativo universal ni como garantía perceptual.',
        (f"**Resultado principal:** ninguna configuración ensayada cumple el objetivo conjunto en los cuatro pares F1/F2–P8/P9. La pared completa α = 0,80 deja F2–P9 en D50 = {f(full['D50'])} % y C80 = {f(full['C80'])} dB; los otros pares y los paños locales se detallan a continuación. Se cuantifica un beneficio parcial, sin seleccionar un tratamiento suficiente." if not winners else '**Resultado principal:** se encontraron configuraciones candidatas en las respuestas medias; véanse los resultados por posición y sus rangos antes de seleccionar un tratamiento.'),
        'La pared completa con α = 0,80 sirve de límite de cobertura para ese coeficiente en el modelo. Los seis paños parciales permiten comparar sensibilidad a posición y superficie. No se supone una relación lineal entre área y D50.',
        '## 2. Método y condiciones',
        'Se ejecutaron **42 nuevas corridas**: siete tratamientos × dos fuentes independientes × tres semillas. Se reutilizaron las seis referencias sin tratamiento sobre la misma geometría. Cada corrida usa **600.000 partículas**, semillas **20261019, 20261020 y 20261021**, una banda activa de **1.000 Hz**, 21 receptores, radio 0,31 m, 4 s de duración y paso 1 ms. Las energías lineales de las tres realizaciones se promedian antes de recalcular los indicadores.',
        'Se conservaron las fuentes omnidireccionales idealizadas, Lw global de 90 dB y su espectro, posiciones, altura, malla común y condiciones ambientales de 18 °C y 57 % HR. La absorción atmosférica permanece activa y la transmisión desactivada. La dispersión del paño permanece aproximadamente en 0,05 y conserva su ley: aquí se aísla absorción, sin introducir simultáneamente una nueva hipótesis de difusión.',
        'El coeficiente **α = 0,80 es el valor final de las superficies seleccionadas a 1.000 Hz**, no un incremento de 0,80 ni un valor impuesto en todas las bandas. El muro efectivo de referencia tiene α ≈ 0,24795 a esa frecuencia. Esta referencia es una calibración efectiva, no un ensayo del concreto real. No se ha seleccionado todavía un material comercial ni un montaje con espectro acreditado.',
        '## 3. Ubicación y superficie',
        'Todos los tratamientos se encuentran en X = 40,25 m. La franja superior ocupa Z = 10,6–11,8 m; la media, Z = 9,0–10,2 m. En cada altura, el sector central ocupa Y = −4 a +4 m; los exteriores son dos paños separados, Y = −8 a −4 y +4 a +8 m. La franja completa reúne central y exteriores. Las coordenadas Z son cotas globales del modelo, no alturas medidas desde cada grada.',
        '| Distribución | Superficie | Aumento de absorción equivalente a 1 kHz |',
        '|---|---:|---:|']
    for c in CASES[1:]:
        area=specs[c]['area_m2'];report.append(f'| {names[c]} | {f(area)} m² | {f(area*(.8-.24794628455412168))} m² |')
    report += ['', 'La absorción equivalente se presenta solo para dimensionar el cambio; no reemplaza la propagación calculada ni permite deducir la eficacia local mediante Sabine.',
        '![Distribuciones posteriores comparadas](../prediccion/estudio-difusion/absorcion-posterior/resultados-a080/distribuciones-a080.png)',
        '## 4. Resultados por fuente y posición',
        'Cada celda presenta **D50 (%) / C80 (dB)**. No se mezclan fuentes ni asientos para evaluar cumplimiento.',
        '| Condición | F1–P8 | F1–P9 | F2–P8 | F2–P9 | Cumplen ambos criterios |',
        '|---|---:|---:|---:|---:|---:|']
    for c in CASES:
        row=[];passed=0
        for src,rec in [('F1','P8'),('F1','P9'),('F2','P8'),('F2','P9')]:
            m=next(r for r in means if r['variante']==c and r['fuente']==src and r['receptor']==rec)
            row.append(f"{f(m['D50_pct'])} / {f(m['C80'])}")
            passed+=48<=m['D50_pct']<=52 and -2<=m['C80']<=2
        report.append('| '+names[c]+' | '+' | '.join(row)+f' | {passed}/4 |')
    report += ['', 'El único par que cumple en cada escenario localizado es F2–P8, que ya cumplía en la referencia. Ese 1/4 no significa que se haya incorporado una posición previamente deficitaria al rango objetivo.',
        '![D50 y C80 por posición](../prediccion/estudio-difusion/absorcion-posterior/resultados-a080/D50-C80-por-posicion.png)',
        'Las barras muestran el rango de las tres realizaciones, no intervalos de confianza. Se evita atribuir a un tratamiento diferencias pequeñas del mismo orden que el muestreo.',
        '### Control de la energía temprana en P8/P9',
        'El análisis geométrico anterior establece que las trayectorias que tocan este plano posterior no pueden contribuir antes de 50 ms en P8/P9, considerando el radio receptor y el paso temporal. Por tanto, las diferencias de energía anterior a 50 ms entre cálculos se interpretan como variación de muestreo. Como diagnóstico secundario se fija esa energía al valor de referencia y se conserva la energía posterior de cada tratamiento. No se sustituye el resultado bruto ni se extiende esta propiedad a todos los virtuales.',
        '| Distribución | F2–P9 D50 bruto | F2–P9 control temprano | Rango entre semillas del control |',
        '|---|---:|---:|---:|']
    for c in CASES[1:]:
        r=next(r for r in comparisons if r['variante']==c and r['fuente']=='F2' and r['receptor']=='P9')
        report.append(f"| {names[c]} | {f(r['D50'])} % | {f(r['D50_control_temprano'])} % | {f(r['min_semilla_control'])}–{f(r['max_semilla_control'])} % |")
    report += ['', 'El control no hace invariante la energía de 50–80 ms: parte de las llegadas posteriores puede situarse en esa ventana. Los datos individuales incluyen también C80 de control, calculado con E0–50 de referencia y E50–80 y E>80 del tratamiento. No se conserva sin comprobar toda la energía anterior a 80 ms ni se atribuye una certeza estadística a esta corrección.',
        '## 5. Efectos en las tres zonas y receptores virtuales',
        'Los siguientes cambios son medias descriptivas de diferencias individuales frente a la referencia, a 1.000 Hz. Pueden esconder efectos mayores en un asiento: los archivos individuales se conservan.',
        '| Tratamiento | Zona | ΔD50 (puntos) | ΔC80 (dB) | ΔEDT (s) | ΔT30 (s) | Δnivel de banda (dB) | Máximo cambio absoluto D50 (puntos) |',
        '|---|---|---:|---:|---:|---:|---:|---:|']
    zn={'P8_P9':'P8/P9','virtuales':'Virtuales altos','platea_baja':'Platea baja','bajo_balcon':'Bajo balcón'}
    for r in zones:
        report.append('| '+names[r['variante']]+' | '+zn[r['zona']]+' | '+' | '.join(f(r[k]) for k in ('delta_D50_pp','delta_C80','delta_EDT','delta_T30','delta_total_dB','max_abs_delta_D50'))+' |')
    report += ['', '## 6. Interpretación y decisión',
        f"**Resultado del límite a α = 0,80:** F2–P9 alcanza D50 = {f(full['D50'])} % y C80 = {f(full['C80'])} dB. El control de energía temprana da {f(full['D50_control_temprano'])} %. Los seis paños locales producen D50 bruto de {f(min(r['D50'] for r in local))} a {f(max(r['D50'] for r in local))} % en ese caso, con valores de control de {f(min(r['D50_control_temprano'] for r in local))} a {f(max(r['D50_control_temprano'] for r in local))} %.",
        f"Como balance energético, manteniendo fija E0–50 de F2–P9, llegar a D50 = 48 % requeriría reducir su energía total de referencia aproximadamente un {f(100*(1-full['base_D50']/48))} %; llegar a 50 %, un {f(100*(1-full['base_D50']/50))} %. El tratamiento completo α = 0,80 produce aproximadamente un {f(100*(1-full['base_D50']/full['D50_control_temprano']))} % de reducción en ese control. Es una identidad del reparto energético, no una conversión de esa diferencia a metros cuadrados ni una predicción de otro material.",
        ('**Ninguna de las siete configuraciones ensayadas cumple ambos criterios en los cuatro pares F1/F2–P8/P9.** No se selecciona un área ni un material como solución suficiente. Los tratamientos locales pueden aportar una mejora parcial; su utilidad debe valorarse frente a su magnitud, incertidumbre y efectos sobre los demás asientos.' if not winners else '**Configuraciones candidatas con cumplimiento en los cuatro pares:** '+', '.join(names[c] for c in winners)+'. El cumplimiento se refiere a respuestas medias de este modelo y debe contrastarse con el muestreo y el espectro real.'),
        'La selección se debe basar en el caso deficitario y la cobertura, no solo en el promedio de P8/P9. Que un paño reduzca energía posterior y aumente D50 no basta para afirmar que alcanza el objetivo, conserva C80 o mejora la percepción de toda la audiencia.',
        'La pared completa ofrece una referencia de máxima eliminación para α = 0,80 en P8/P9 bajo estas hipótesis: la energía previa a 50 ms permanece físicamente invariable y aumentar la superficie absorbente no aumenta la energía posterior esperada. La comparación Monte Carlo puede presentar fluctuaciones; no se usa para declarar una imposibilidad universal en el recinto real.',
        'Los paños ensayados no abarcan todas las distribuciones posibles. Si el límite completo no alcanza la meta en un caso, no se prometerá que un paño menor del mismo coeficiente la alcance. Si una distribución local se aproxima a los criterios, seguirá siendo una candidata predictiva a contrastar, no una solución instalada validada.',
        'Estos cálculos no verifican el comportamiento a 500 Hz, 2, 4 u 8 kHz ni los ecos audibles. Para seleccionar un absorbente hace falta introducir su espectro ensayado con el montaje previsto y estudiar el balance musical en todas las zonas. No se transfieren los incrementos de D50 a las mediciones mediante suma de puntos porcentuales.',
        '## 7. Datos, verificación y conservación',
        f"Se verificaron las 48 entradas de cálculo utilizadas, incluidos los seis controles reutilizados: banda activa, Lw global, receptores y fuentes idénticos a la referencia, parámetros de simulación conservados, dispersión sin cambios, absorción modificada solo a 1.000 Hz y huellas de configuración y mallas. Las series son finitas y no negativas. La fracción máxima de partículas perdidas fue {f(checks['max_fraccion_perdidas']*100,4)} %. Esto comprueba la ejecución; no constituye por sí solo una prueba de convergencia estadística o validación física.",
        '- [Comparaciones individuales y controles](../prediccion/estudio-difusion/absorcion-posterior/resultados-a080/comparaciones.csv).',
        '- [Indicadores por realización](../prediccion/estudio-difusion/absorcion-posterior/resultados-a080/indicadores-por-semilla.csv).',
        '- [Respuestas medias y rangos de semillas](../prediccion/estudio-difusion/absorcion-posterior/resultados-a080/respuestas-medias.csv).',
        '- [Resumen por zonas](../prediccion/estudio-difusion/absorcion-posterior/resultados-a080/resumen-zonas.csv).',
        '- [Verificación de entradas y ejecución](../prediccion/estudio-difusion/absorcion-posterior/resultados-a080/verificacion.json).',
        '- [Escenarios y mallas utilizadas](../prediccion/estudio-difusion/absorcion-posterior/escenarios.json).',
        '- [Ensayo ideal anterior](RESULTADOS-LIMITE-ABSORCION-POSTERIOR.md).',
        'No se modificaron el proyecto canónico ni las mediciones originales. Se conservaron configuraciones, registros del motor, metadatos y energías lineales. Las salidas nativas de las 42 corridas nuevas se archivaron sin pérdida en ZIP por corrida, verificando contenido y SHA256 antes de retirar las copias sueltas; el registro queda en [verificación de compactación](../prediccion/estudio-difusion/absorcion-posterior/resultados-a080/verificacion-compactacion.json).']
    target=O.parents[2]/'informes/RESULTADOS-ABSORCION-POSTERIOR-080.md'
    assert target.parent.is_dir(),target
    target.write_text('\n\n'.join(report)+'\n',encoding='utf8')
    # Consecutive table lines must be adjacent in Markdown.
    text=target.read_text(encoding='utf8').replace('|\n\n|','|\n|')
    target.write_text(text,encoding='utf8')
    print(target)

if __name__=='__main__':main()
