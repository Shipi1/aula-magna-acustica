# Extensión de las pruebas de dispersión a 8 y 16 kHz

> **Documento archivado el 9 de noviembre de 2026.** Se conserva como antecedente de una etapa o estrategia sustituida; no es el protocolo vigente. Ubicación original: `informes/RESULTADOS-DISPERSION-8-Y-16-KHZ.md`. Consultar el [plan actual](../../informes/PLAN-DE-ESTUDIO-D50-C80-Y-TRATAMIENTOS-POR-ZONA.md).


**Proyecto:** Teatro Aula Magna UTFSM.  
**Fecha:** 9 de noviembre de 2026.  
**Alcance:** ampliación espectral de los ensayos de grandes paños de platea alta. No constituye validación de un QRD físico ni sustituye los ensayos localizados del paso 3.

## Motivo de la ampliación

La molestia observada por el usuario corresponde a persistencia de agudos. Esa observación justifica investigar 8 kHz y explorar 16 kHz, sin asignar de antemano la molestia a una banda concreta.

El análisis previo de las mediciones ya contiene una octava de 8 kHz. La proporción media de energía posterior a 80 ms, con el horizonte de integración y tratamiento del ruido de aquel análisis, es:

| Excitación | Platea alta P8/P9 | Piso abierto | Bajo balcón |
|---|---:|---:|---:|
| Parlante | 28,61 % | 14,81 % | 11,24 % |
| Globo | 35,61 % | 26,13 % | 24,29 % |

Son promedios de proporciones por toma, no niveles absolutos de presión sonora. El análisis conserva las exclusiones documentadas y no todas las zonas tienen igual cantidad de mediciones. Esto respalda estudiar 8 kHz; no demuestra por sí solo flutter ni una causa superficial única.

Fuente: [resumen medido por zona](../../analisis/diagnostico_platea_alta/resumen_zonas.csv) y [método del diagnóstico](../../analisis/diagnostico_platea_alta/INFORME.md). Los 36 archivos RT60 exportados de globo y parlante revisados no contienen una fila de 16 kHz. No se ha procesado aquí una nueva banda de 16 kHz sobre las respuestas WAV; su contraste medido permanece pendiente.

## Simulaciones ejecutadas

Se amplía la investigación existente con **40 procesos SPPS nuevos**:

| Ensayo | Condiciones | Procesos |
|---|---|---:|
| Exploración | Base, lateral Y negativo, lateral Y positivo y fondo alto; F1/F2; 8 y 16 kHz; 150.000 partículas; semilla 20261019 | 16 |
| Repetición intermedia | Base y fondo alto; F1/F2; 8 y 16 kHz; 600.000 partículas; semillas 20261019, 20261020 y 20261021 | 24 |

Se conservan los nueve receptores originales, geometría, potencia global Lw = 90 dB por fuente, espectro, duración de 4 s, paso de 1 ms, radio 0,31 m, ambiente de 18 °C y 57 % de humedad, absorción atmosférica y demás condiciones del [estudio inicial](RESULTADOS-INICIALES-DISPERSION-PLATEA-ALTA.md). F1 y F2 se calculan separadamente. No se ejecutó en esta ampliación el protocolo final de 4,8 millones.

Los paños son los grandes sectores existentes: unos 112,66 m² en Y negativo, 92,35 m² en Y positivo y 112,47 m² en el fondo. No son comparaciones a igual área ni superficies prescritas para construir. No se han creado todavía las franjas R/C/D ni los receptores virtuales del plan localizado.

En los paños tratados se mantiene la absorción de referencia y se cambia la dispersión aproximadamente de 0,05 a 0,60, ley Lambert, en la frecuencia activa. No se ha introducido geometría de pozos ni caracterización de un QRD.

## Cómo se comparan los resultados

Se conserva el procedimiento energético y temporal del estudio inicial. Las tres realizaciones se promedian en energía lineal por fuente y receptor; después se recalculan los indicadores. Los promedios por zona resumen cambios de posiciones individuales, no respuestas mezcladas.

Los rangos entre semillas son descriptivos y no intervalos de confianza. Las trayectorias pueden divergir entre condiciones aunque compartan identificador de semilla. C80 no prueba por sí solo reducción de ecos; se revisan también energía integrada, máximo de 10 ms en 80–300 ms y concentración de ese máximo respecto de la ventana.

La simulación activa una frecuencia central de la configuración espectral. El análisis WAV citado utiliza filtros de octava. No se presenta una equivalencia cuantitativa exacta entre ambos anchos de banda ni se declara calibración de 8/16 kHz por comparar sus cifras sin unificar el procesamiento.

## Resultados de la ampliación

### Exploración de ubicación: 150.000 partículas y una semilla

Cambios medios descriptivos en los cuatro pares F1/F2–P8/P9. Los laterales no cuentan todavía con repetición de tres semillas en estas bandas.

| Banda | Paño | ΔE 80–300 ms | ΔC80 |
|---|---|---:|---:|
| 8 kHz | lateral_Yneg | +0.03 dB | +0.30 dB |
| 8 kHz | lateral_Ypos | +0.15 dB | -0.31 dB |
| 8 kHz | fondo_alto | +0.01 dB | +0.28 dB |
| 16 kHz | lateral_Yneg | -0.66 dB | +0.85 dB |
| 16 kHz | lateral_Ypos | -0.10 dB | +0.45 dB |
| 16 kHz | fondo_alto | -0.26 dB | +0.82 dB |

La exploración a 8 kHz, por sí sola, no mostró una reducción clara de la energía tardía en los grandes paños. Al aumentar el muestreo, el resultado del fondo cambia: no corresponde declarar que el tratamiento sea inútil basándose en aquella única realización.

### Fondo alto: 600.000 partículas y tres semillas

| Banda | Par | ΔE 80–300 ms | Rango entre semillas | ΔC80 | Δmáximo 10 ms |
|---|---|---:|---|---:|---:|
| 8 kHz | F1–P8 | -0.54 dB | -0.76 a -0.32 dB | +0.54 dB | -0.53 dB |
| 8 kHz | F1–P9 | -0.39 dB | -0.50 a -0.17 dB | +0.48 dB | -0.64 dB |
| 8 kHz | F2–P8 | -0.25 dB | -0.43 a -0.16 dB | +0.24 dB | -0.28 dB |
| 8 kHz | F2–P9 | -0.36 dB | -0.49 a -0.11 dB | +0.51 dB | -0.13 dB |
| 16 kHz | F1–P8 | -0.15 dB | -0.48 a +0.06 dB | +0.07 dB | -0.59 dB |
| 16 kHz | F1–P9 | -0.63 dB | -1.08 a -0.36 dB | +0.57 dB | -1.10 dB |
| 16 kHz | F2–P8 | -0.68 dB | -1.06 a -0.27 dB | +0.61 dB | -1.29 dB |
| 16 kHz | F2–P9 | -0.56 dB | -0.91 a -0.26 dB | +0.79 dB | -0.94 dB |

| Banda | Zona | ΔE 80–300 ms | ΔC80 | Δmáximo 10 ms |
|---|---|---:|---:|---:|
| 8 kHz | alta | -0.38 dB | +0.44 dB | -0.39 dB |
| 8 kHz | piso | -0.05 dB | -0.02 dB | -0.06 dB |
| 8 kHz | bajo | -0.07 dB | -0.08 dB | -0.22 dB |
| 16 kHz | alta | -0.50 dB | +0.51 dB | -0.98 dB |
| 16 kHz | piso | -0.08 dB | +0.06 dB | -0.09 dB |
| 16 kHz | bajo | +0.06 dB | -0.12 dB | +0.21 dB |

**A 8 kHz**, el fondo reduce aproximadamente 0,38 dB la energía de 80–300 ms y aumenta C80 unos 0,44 dB, en promedio descriptivo de los cuatro pares altos. La reducción de energía mantiene el signo en las doce comparaciones individuales de semilla y par. La concentración relativa del máximo apenas cambia en promedio: todavía no se demuestra eliminación de flutter.

**A 16 kHz**, los cambios medios son aproximadamente −0,50 dB de energía tardía, +0,51 dB de C80 y −0,98 dB del máximo de 10 ms. La concentración relativa baja unos 0,034 en escala de 0 a 1, es decir, 3,4 puntos porcentuales. Sin embargo, F1–P8 cambia de signo en energía tardía entre semillas; no todos los efectos son consistentes. Estos resultados son exploratorios y dependen de materiales y propagación aún no validados en esta banda.

En algunas respuestas a 16 kHz, especialmente en la ventana 300–1.000 ms, aparecen energías exactamente nulas. Las razones logarítmicas con numerador o denominador nulo se registran como no evaluables, sin sustituirlas por reducciones arbitrarias. Incluso cuando la energía es positiva, las diferencias grandes de una cola casi extinguida no se consideran evidencia robusta de eficacia. Los resúmenes indican cuántas comparaciones son válidas por indicador.

### Decisión para continuar

Se mantiene el fondo alto como candidato para la etapa localizada y se incorpora 8 kHz como banda prioritaria. Por decisión posterior del usuario, 16 kHz queda solo como antecedente exploratorio y no se incluirá en las siguientes matrices. No se ha demostrado que el fondo sea el mejor paño en estas bandas, porque la repetición intermedia no incluye los laterales, ni se ha validado el QRD físico. Las franjas de muro y cielo permitirán evaluar la localización con menor superficie y más posiciones de escucha.

Los efectos medios sobre las zonas inferiores son pequeños para varios indicadores, pero no se declara desacoplamiento ni ausencia de perjuicios en cada receptor. Las tablas individuales permiten revisarlos antes de seleccionar una alternativa.

## Límites específicos de estas frecuencias

### Materiales de la base

Los archivos contienen valores a 8 y 16 kHz, pero no existe en esta ampliación una caracterización independiente que los valide. Varios materiales repiten los valores de 4 kHz. El muro efectivo utiliza α ≈ 0,26795 tanto a 8 como a 16 kHz, frente a 0,11 a 4 kHz. No debe interpretarse ese salto como una propiedad medida del concreto.

Las comparaciones muestran la sensibilidad de esta base bajo esos supuestos. Antes de elegir un tratamiento se deberá revisar la absorción y dispersión de los materiales en las bandas altas y la respuesta/directividad de la fuente de medición. Un resultado favorable a 16 kHz es especialmente dependiente de esa revisión.

### Propagación atmosférica y muestreo

Se mantiene la absorción del aire. La [documentación física oficial de SPPS](https://i-simpa-wiki.readthedocs.io/fr/latest/code_SPPS_modelling.html) explica que se calcula a la frecuencia central, con límites de aproximación dependientes del recorrido y del ancho de banda. A 16 kHz los recorridos reflejados largos exigen especial cautela; una cola corta de la simulación no acredita por sí sola el decaimiento real de toda la banda.

La estadística de partículas absorbidas por el aire describe terminación de partículas, no el porcentaje de energía recibida perdido por ese mecanismo. Tampoco la resolución temporal de 1 ms garantiza exactitud física de cada pico. Se conserva esta distinción al interpretar las salidas.

### Consecuencias para el QRD

El [QRD preliminar](ESTUDIO-QRD-Y-ALTERNATIVAS-PLATEA-ALTA.md) tiene pozos de 30 mm y un límite orientativo de modelo de pozo de unos 5,7 kHz. No tiene eficacia acreditada a 8 ni a 16 kHz. Si esas bandas son determinantes, habrá que revisar el ancho de pozo, la distribución angular, las pérdidas y el conjunto completo.

La relación orientativa w ≤ c/(2f), con c = 343 m/s, daría unos 21,4 mm a 8 kHz y 10,7 mm a 16 kHz. Es una condición aproximada, no una garantía de difusión uniforme ni una receta de fabricación. Las pruebas Lambert de esta ampliación no validan esos diseños.

## Archivos y continuidad

- [Exploración por fuente y receptor](../../prediccion/estudio-difusion/resultados/agudos-8-16kHz/exploracion.csv).
- [Repetición por fuente y receptor](../../prediccion/estudio-difusion/resultados/agudos-8-16kHz/repeticion.csv).
- [Resumen de cambios por zona](../../prediccion/estudio-difusion/resultados/agudos-8-16kHz/resumen.json).
- [Ecogramas a 8 kHz](../../prediccion/estudio-difusion/resultados/agudos-8-16kHz/ecogramas-8000Hz.png).
- [Ecogramas a 16 kHz](../../prediccion/estudio-difusion/resultados/agudos-8-16kHz/ecogramas-16000Hz.png).
- [Plan actualizado de cinco etapas](PLAN-DE-LOCALIZACION-Y-VALIDACION-DEL-TRATAMIENTO.md).

La base principal y los datos medidos no se modifican. Las nuevas configuraciones y salidas se guardan en carpetas independientes de corrida dentro del estudio de difusión.
