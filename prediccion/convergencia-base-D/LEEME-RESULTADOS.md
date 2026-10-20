# Base predictiva: convergencia y primer ajuste espectral

Se completaron 18 cálculos SPPS nuevos y se reutilizó una confirmación previa de D. Se conservó toda la geometría. El resultado es una base numérica más estable a 1 kHz y un candidato espectral G más cercano a los tiempos medidos, especialmente en 500–4000 Hz. **No se ha simulado todavía un tratamiento de platea alta ni se declara una calibración global del recinto.**

## Qué abrir

- **G_base_efectiva_espectral_Lw90.proj**: candidato de trabajo con una curva efectiva de absorción por frecuencia para los tres grupos de pared ya ajustados en D. Incluye los ocho cálculos G: F1/F2, tercios de 250, 500, 2000 y 4000 Hz, 600.000 partículas por cálculo. Es una hipótesis equivalente NO MEDIDA, no la absorción real del concreto. Su limitación principal es C80 a 250 Hz.
- **F_base_D_convergencia_Lw90.proj**: control que conserva todos los materiales de D y contiene los cinco ensayos de convergencia a 1 kHz. Permite comparar los efectos del número de partículas y la semilla.

Ambos proyectos mantienen las fuentes a **Lw global 90 dB**, con F1 activa y F2 desactivada inicialmente. La configuración de cálculo principal selecciona **solo 1 kHz, 4.800.000 partículas y semilla 20261019**. Para una prueba reproducible, cambiar una banda cada vez. Los cálculos almacenados se realizaron con la referencia anterior de Lw global 80 dB y están rotulados `Lw80`; esto no altera RT, C80, EDT o los cocientes energéticos del modelo lineal. No son resultados de 90 dB SPL en butacas. La respuesta energética media de las tres semillas se entrega en JSON; los gráficos nativos de los proyectos muestran realizaciones individuales.

Los archivos D y E originales se conservaron. Se verificaron estructura ZIP/XML, mallas, grupos, fuentes, receptores y materiales; únicamente G modifica el material efectivo 115. No se abrió la interfaz gráfica de I-Simpa para verificar su presentación.

## Convergencia conseguida

F1, nueve puntos, tercio de octava de 1 kHz, radio de receptor 0,31 m, paso de 1 ms y duración 4 s:

| Comprobación | Resultado |
|---|---|
| 1,2 → 2,4 millones, misma semilla | Máximo cambio C80: 0,229 dB |
| 2,4 → 4,8 millones, misma semilla | Máximo cambio C80: 0,203 dB |
| Tres semillas con 4,8 millones | Máximo rango C80: 0,437 dB; nueve puntos bajo 0,5 dB |
| T20/T30 entre 2,4 y 4,8 millones | Cambios máximos de 1,81 % y 1,71 % |
| RT entre tres semillas | Siete de nueve puntos cumplen rango/media <5 % para ambos parámetros |

Las excepciones son P6 en T30 (rango/media 5,19 %) y P8 en T20 (5,07 %). Se conservan, sin relajar retrospectivamente el criterio. Son umbrales de trabajo de esta investigación, no tolerancias normativas. La media de las energías lineales de las tres realizaciones reduce el ruido de muestreo; las tres semillas no bastan para construir una garantía estadística de precisión.

Esta prueba demuestra estabilidad de C80 bajo las condiciones ensayadas de F1 y 1 kHz. No se extrapola automáticamente a F2, otras bandas, nuevas geometrías o materiales tratados.

## Acercamiento del espectro a los globos

T20 medio de F1, emparejado con los puntos que tienen referencia REW aceptada:

| Centro del tercio | D, 600k (s) | G, 600k (s) | Globo REW (s) |
|---|---:|---:|---:|
| 250 Hz | 2,486 | 1,750 | 1,577 |
| 500 Hz | 2,048 | 1,626 | 1,586 |
| 2000 Hz | 1,580 | 1,787 | 1,742 |
| 4000 Hz | 1,352 | 1,628 | 1,566 |

Las medias de 250 Hz usan seis puntos, y las otras filas ocho: se excluye F1-P3 por duplicación conocida y se exige |r_T20|≥0,99 en la referencia. Son comparaciones de tercios aislados, no octavas reconstruidas. En el informe se entregan también los datos individuales y F2.

En F2, G obtiene 1,628 s frente a 1,620 s medidos a 500 Hz; 1,798 frente a 1,754 s a 2 kHz; y 1,614 frente a 1,588 s a 4 kHz. En las ocho combinaciones de fuente y banda, el error del T20 medio queda dentro de ±15 %. Esto no implica que todos los puntos cumplan ese margen.

**C80 permite discriminar dónde la mejora de RT es suficiente y dónde no:**

- A 2 y 4 kHz, G combina RT cercano con errores absolutos medios de C80 de aproximadamente 1,01–1,54 dB frente a globos. Es el resultado más prometedor para estudiar la intervención en agudos.
- A 500 Hz, el RT mejora mucho; el error medio absoluto de C80 es 1,55 dB en F1 y 2,23 dB en F2.
- A 250 Hz, el RT se acerca, pero C80 empeora: errores absolutos medios de 2,76 y 3,80 dB. **No se acepta como banda calibrada para claridad.**

G mantiene el ajuste de 1 kHz y todos los demás materiales. La dispersión no se modificó. La curva efectiva de muro alcanza α=0,60 a 250 Hz: puede representar pérdidas no resueltas de varias construcciones, pero no debe identificarse como concreto rugoso ni utilizarse para deducir un material real. No se tocaron las referencias de 125 y 8000 Hz; esas bandas no se recalcularon en G.

## Lo que mostró la prueba del escenario

Se mantuvo el resto de D y se probó α=1 exclusivamente en el piso del escenario, como control ideal, no como propuesta de material. A 250 Hz el promedio emparejado baja de 2,486 a aproximadamente 2,15 s, todavía por encima de 1,577 s medidos. A 500 Hz pasa de 2,048 a aproximadamente 1,79 s, frente a 1,586 s medidos.

Esto hace poco plausible corregir todo el desajuste cambiando solo la tarima. No identifica su resonancia ni constituye una demostración matemática de monotonía del T20. El escenario ya estaba representado mediante una curva de piso de madera; su cámara real, masa, apoyos y amortiguamiento siguen sin conocerse.

## Cómo usar esta base para evaluar el tratamiento

1. Mantener G como candidato provisional y F/D como referencia de sensibilidad. La base de G es más cercana en RT, especialmente en medios/agudos; no debe presentarse como una reconstrucción física única del teatro.
2. Antes de cuantificar diferencias pequeñas del tratamiento, repetir la comprobación de partículas y semillas en 2 y 4 kHz con G: los ocho ensayos espectrales actuales usan 600.000 partículas. La convergencia a 1 kHz no certifica esas bandas.
3. Comparar estados actual y tratado con iguales fuentes, receptores, bandas, número de partículas y conjunto de semillas. Evaluar cambios por punto y por zona, sin depender solo de medias espaciales.
4. Usar curvas de absorción y dispersión del montaje de tratamiento concreto. Si se reemplaza una superficie, no sumar su absorción sobre la efectiva de la base sin definir qué sistema está representando. Comparar varias bases plausibles si esa equivalencia es incierta.
5. Para ecos flotantes, revisar además la energía-tiempo y la persistencia de picos repetidos. RT y C80 no demuestran por sí solos su desaparición. Las limitaciones del cálculo geométrico energético y la directividad desconocida siguen presentes.

El objetivo de esta etapa se cumplió como ensayo: mejoró la estabilidad numérica y se obtuvo un candidato de RT más cercano sin rehacer la geometría. La evidencia de eficacia de un tratamiento requiere todavía la comparación actual/tratado en sus bandas de interés. Ningún resultado de esta entrega se presenta como verificación de una intervención instalada.

## Documentación y datos

- `INFORME-CONVERGENCIA.md`: todos los ensayos, variación por punto y parámetros de la energía media.
- `ENSAYOS-BASELINE.md`: control del escenario, curva G y contraste de RT/C80 con globos.
- `AUDITORIA-MEDICIONES-C80.md`: reproceso auxiliar a 1 kHz con filtro común y sensibilidad del corte temporal; no reemplaza REW.
- `resumen-convergencia.json`, `respuesta-media-semillas.json`, `ensayos-baseline.json`: datos numéricos y comparaciones.
- `verificacion-proyecto-F.json` y `verificacion-proyecto-G.json`: integridad y huellas de los proyectos.
- Las carpetas de cada cálculo conservan configuración nativa, registro SPPS y respuestas de los nueve receptores.

La auditoría de mediciones mantiene diferencias entre globos y barridos al usar un procesamiento común: las medias a 1 kHz son aproximadamente +1,29 y +4,82 dB, frente a +1,28 y +5,60 dB en los exportes REW. No se fuerza una curva única que mezcle ambas fuentes. El cambio de método, origen temporal y directividad deben seguir separados del ajuste de materiales.
