# Dispersión de reflexiones en la platea alta a 4 y 8 kHz

El ensayo estudia si las reflexiones dominantes pueden repartirse en el tiempo y entre butacas, conservando el aporte temprano a 1 kHz de la [propuesta mixta](INFORME-COMPARATIVO-SALA-SIN-TRATAMIENTO-Y-PROPUESTA-MIXTA.md). A 8 kHz, el C80 medio del frente y la zona media sube de +5,35 a +5,72 dB con la propuesta. La mayor variación individual ocurre en F1–V04, de +5,29 a +6,77 dB. El C80 se sigue como control del balance temporal. [Comparación original por octavas](RESULTADOS-COMPARACION-POR-OCTAVAS.md).

## Método

- **Referencia.** Cuatro reflectores inclinados y el paño absorbente posterior A1. Se mantienen la geometría, la absorción de cada superficie, la absorción del aire, las fuentes omnidireccionales y los 21 receptores. Cada variante cambia la dispersión de una superficie a la vez a 0,60 con ley Lambert, solo en la banda de prueba. El valor es una hipótesis de sensibilidad para la simulación geométrica.
- **Barrido inicial.** Ocho corridas de F1 a 8 kHz, con 120.000 partículas y la misma semilla. Incluyen la referencia, R1–R4, fondo alto sin A1 y ambos laterales altos. Se seleccionaron R2 y el lateral alto del lado Y negativo para verificar el efecto observado en F1–V04. R2 es el reflector adelantado en Y positivo, centrado en (12, 4, 8,2) m. El lateral negativo abarca 112,7 m² de la malla, por lo que su resultado representa la sensibilidad de una zona amplia.
- **Verificación.** Para cada una de las dos superficies se corren F1 y F2 a 8 kHz y F1 a 4 kHz, con 600.000 partículas y tres semillas por combinación. La comparación reutiliza las respuestas de la propuesta mixta con esas mismas semillas. Se incorpora una comprobación independiente de R2 con F1 a 1 kHz, banda en que el coeficiente sigue en 0,05.
- **Comparación temporal.** Tiempo cero en el arribo geométrico del directo, a unos 68 ms desde la emisión para F1–V04. Se usa el máximo de energía acumulada en 5 ms dentro de la ventana 3–16 ms, tanto en nivel relativo al directo como respecto al nivel del mismo pico en la propuesta. La concentración es la fracción de energía de 3–16 ms contenida en esos 5 ms. Los ecogramas usan una referencia común para que se aprecien los cambios de nivel entre casos.
- **Comparación espacial.** En 3–80 ms se compara el máximo de 5 ms y la energía integrada por separado, para detectar una reducción local o un traslado del máximo a otra butaca. Se usan como prioridad V01–V04, V05 y V08 y se conservan P8, P9 y los puntos de las otras zonas. C80, D50, EDT y la energía posterior a 80 ms acompañan la comparación.

En F1–V04, los recorridos especulares candidatos de primer orden desde R4 y R2 tienen retardos geométricos de aproximadamente 3,6 y 5,8 ms. La ventana permite estudiar ambos junto con otras llegadas cercanas. El nivel de una llegada en SPPS se interpreta como energía por intervalo temporal. Su coincidencia con una trayectoria geométrica sirve para plantear una hipótesis sobre el origen de la reflexión.

## Resultados a 8 kHz

En F1–V04, la propuesta mixta produce un pico más intenso en los primeros milisegundos que la sala base. Entre 3 y 16 ms la energía total aumenta 2,95 dB y el máximo de 5 ms aumenta 2,16 dB. La energía posterior a 80 ms cambia solo −0,02 dB. El aumento de C80 en este receptor se explica principalmente por el incremento temprano de la propuesta.

| Configuración en F1–V04 | Pico respecto al directo (dB) | Cambio de nivel del pico frente a la propuesta (dB) | Energía en los 5 ms más intensos (% de 3–16 ms) | Cambio de energía de 3–16 ms (dB) | C80 (dB) |
|---|---:|---:|---:|---:|---:|
| Sala sin tratamiento | −0,21 | −2,16 | 59,7 | −2,95 | +5,29 |
| Propuesta mixta | +1,47 | 0,00 | 49,8 | 0,00 | +6,77 |
| R2 con dispersión 0,60 | +0,44 | −0,58 | 52,6 | −0,82 | +6,62 |
| Lateral negativo con dispersión 0,60 | +1,07 | −0,53 | 48,3 | −0,40 | +6,52 |

En R2 el nivel del pico de F1–V04 baja en las tres semillas, entre −1,29 y −0,15 dB. La fracción concentrada sube de 49,8 a 52,6 %. El resultado indica una reducción local del pico, con menor energía en el conjunto de la ventana. En el lateral negativo el pico también baja en las tres semillas, entre −0,55 y −0,24 dB. La fracción concentrada baja ligeramente en la respuesta media, con signos mixtos al comparar semillas.

| Superficie | Fuente | Cambio medio del máximo de 5 ms en 3–80 ms (dB) | Puntos con reducción en las tres semillas | Mayor aumento entre las seis butacas (dB) |
|---|---|---:|---:|---:|
| R2 | F1 | −0,45 | 4 de 6 | −0,05 |
| R2 | F2 | −0,08 | 1 de 6 | +0,55 |
| Lateral negativo | F1 | −0,26 | 2 de 6 | +0,24 |
| Lateral negativo | F2 | +0,04 | 2 de 6 | +1,29 |

Cada promedio corresponde a los seis receptores prioritarios de esa fuente. Se calcula cada indicador a partir de la respuesta energética media de tres semillas y después se promedia entre receptores. El conteo usa las tres comparaciones individuales y describe consistencia de signo, sin imponer un umbral de audibilidad.

Los cambios medios de nivel total a 8 kHz en platea baja y bajo balcón están entre −0,04 y +0,12 dB en las dos variantes y fuentes. El mayor cambio medio de C80 en estos controles es +0,39 dB, en bajo balcón con F1 al aumentar la dispersión del lateral.

## Resultados a 4 kHz

En F1–V04, R2 reduce el pico en 1,04 dB y la energía de 3–16 ms en 1,06 dB. El cambio del pico es negativo en las tres semillas (−1,39 a −0,61 dB). La concentración de los 5 ms más intensos apenas cambia, de 49,6 a 49,8 %. En el conjunto prioritario de F1, el máximo de 3–80 ms cambia −0,02 dB de media y solo se reduce en las tres semillas en una de las seis butacas. El lateral negativo aumenta el máximo de 3–80 ms en +0,23 dB de media. La verificación de esta banda se limita a F1.

## Control a 1 kHz

La comprobación de R2 con F1 y la semilla 20261019 reproduce exactamente el D50 y el C80 de la propuesta mixta en los 21 receptores. En esta banda, ambos modelos usan la misma absorción y dispersión de R2. En total se verificaron 27 corridas nuevas, con una fracción máxima de pérdidas numéricas del 0,018 %.

## Mediciones disponibles

| Fuente y punto | C80 medido con sweep a 4 kHz (dB) | C80 medido con sweep a 8 kHz (dB) | C80 de la base simulada a 8 kHz (dB) |
|---|---:|---:|---:|
| F1–P8 | +0,90 | +3,76 | +5,32 |
| F1–P9 | +0,68 | +3,53 | +5,27 |
| F2–P8 | +1,16 | +4,18 | +5,45 |
| F2–P9 | +0,74 | +4,43 | +4,42 |

Los valores medidos proceden del análisis de los WAV por octavas, con corrección de ruido y truncado según el decaimiento. En los cuatro pares, la tendencia medida hacia mayor C80 a 8 kHz es clara. El modelo base excede en 1,27–1,74 dB el sweep en tres pares y queda a 0,01 dB en F2–P9. Las fuentes y los métodos de obtención de las respuestas difieren, por lo que estos valores se usan para contrastar magnitudes y tendencias. [Energía por ventanas de las mediciones](../analisis/diagnostico_platea_alta/energia_por_ventanas.csv).

El análisis exploratorio de periodicidad de los sweeps y globos de P8 y P9 encuentra retardos dominantes variables entre fuentes, puntos y bandas. En particular, en 8 kHz no aparece un intervalo recurrente en las cuatro respuestas de sweep. Esto deja abierta la hipótesis de reflexiones perceptibles y da poco respaldo a atribuirlas a un único patrón repetitivo. V04 es un receptor virtual. [Datos de periodicidad de las mediciones](../analisis/diagnostico_platea_alta/periodicidad_flutter.csv).

## Conclusión

R2 es la superficie candidata para estudiar cómo repartir el rebote temprano en el frente de la platea alta. El aumento de dispersión Lambert reduce el pico local de F1–V04 en ambas bandas y el efecto general entre butacas es pequeño y dependiente de la fuente. La concentración temporal en F1–V04 permanece cerca del 50 % o sube ligeramente. El lateral negativo tampoco ofrece una mejora repetible entre butacas. La evidencia permite seleccionar una superficie para seguir estudiando y todavía es insuficiente para elegir un difusor o especificar un tratamiento del muro.

Una comparación posterior podría ensayar un cambio leve de orientación de R2 y una variante que reparta el reflejo en un abanico más ancho. La comparación debería exigir menos picos altos en ambas fuentes, una pérdida pequeña de energía reflejada útil y conservación del D50 a 1 kHz. Las variantes de geometría deberán volver a verificar 1 kHz porque cambiarán los recorridos también en esa banda.

## Datos y gráficos

- [Ecogramas de F1–V04 a 4 y 8 kHz](../prediccion/estudio-difusion/dispersion-agudos/resultados/ecogramas-F1-V04.png).
- [Cambios por butaca a 8 kHz](../prediccion/estudio-difusion/dispersion-agudos/resultados/cambios-por-butaca-8k.png).
- [Indicadores por banda, fuente y receptor](../prediccion/estudio-difusion/dispersion-agudos/resultados/medias.csv) y [resultados por semilla](../prediccion/estudio-difusion/dispersion-agudos/resultados/por-semilla.csv).
- [Resumen por zonas, incluido bajo balcón](../prediccion/estudio-difusion/dispersion-agudos/resultados/por-zona.csv) y [verificación de entradas y corridas](../prediccion/estudio-difusion/dispersion-agudos/resultados/verificacion.json).
- [Superficies y caras modificadas](../prediccion/estudio-difusion/dispersion-agudos/superficies.json), [preparación y simulación](../prediccion/estudio-difusion/probar_dispersion_agudos.py) y [análisis de ecogramas](../prediccion/estudio-difusion/analizar_dispersion_agudos.py).
