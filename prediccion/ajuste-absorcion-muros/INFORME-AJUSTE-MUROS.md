# Ajuste efectivo de absorción de paredes

Se toma B (cortinas de audiencia solo junto al escenario). Se mantiene exactamente su geometría y se aumenta únicamente la absorción de los grupos 05_muros, 10_laterales_altos y 11_fondo_alto. Cielos, pilares, paneles, butacas, cortinas, piso y dispersión conservan sus valores.

**Es un ajuste inverso efectivo: no identifica la absorción real del concreto ni demuestra por sí solo que el modelo esté calibrado.**

Objetivo: T20 de P1–F1 en el tercio de octava de 1000 Hz = 1,70 s, con tolerancia de ±0,05 s. Resultado de confirmación con 1.200.000 partículas: 1.650 s.
Absorción efectiva a 1 kHz: α=0.24795, frente a α=0,03 inicial. Incremento aplicado: 0.21795.

En la misma confirmación, T30 de P1–F1 es 1.733 s y EDT 1.588 s. R² del ajuste T20=0.99829; R² del ajuste T30=0.99845. Estos parámetros no fueron forzados al objetivo de T20.

## Curva fijada antes de validar otras frecuencias

Se añade ese mismo incremento a la curva original, con límite α=0,99. Las otras bandas no se reajustan para acercarlas a REW. No se impone 1,7 s a todo el espectro.

| Frecuencia (Hz) | α original | α efectivo |
|---|---:|---:|
| 125 | 0.013 | 0.23095 |
| 250 | 0.015 | 0.23295 |
| 500 | 0.020 | 0.23795 |
| 1000 | 0.030 | 0.24795 |
| 2000 | 0.040 | 0.25795 |
| 4000 | 0.050 | 0.26795 |
| 8000 | 0.050 (extrapolado) | 0.26795 |

## Búsqueda ejecutada

| Ejecución | Partículas | α a 1 kHz | T20 P1–F1 (s) |
|---|---:|---:|---:|
| busqueda-00-base | 100000 | 0.03000 | 2.873 |
| busqueda-01-superior | 100000 | 0.30000 | 1.420 |
| busqueda-02-interpolada | 100000 | 0.24795 | 1.647 |
| busqueda-03-interpolada | 100000 | 0.22615 | 1.828 |
| busqueda-04-interpolada | 100000 | 0.24157 | 1.479 |
| busqueda-05-interpolada | 100000 | 0.23180 | 1.999 |
| confirmacion-00 | 1200000 | 0.24795 | 1.650 |

## Validación por frecuencia

Medias emparejadas: cada promedio simulado usa exactamente los receptores con referencia REW aceptada. Se excluyen duplicados de globo y ajustes REW con |r|<0,99. Las filas pueden tener distinto número de puntos. La prueba de P1–F1 a 1 kHz fue usada para ajustar, y no es una validación independiente.

| Fuente | Hz | Referencia | n | T20 sim. (s) | T20 REW (s) | Error medio (s) |
|---|---:|---|---:|---:|---:|---:|
| F1 | 125 | Globo | 4 | 3.938 | 1.835 | +2.102 |
| F1 | 125 | Sweep | 6 | 3.883 | 1.532 | +2.351 |
| F1 | 250 | Globo | 6 | 2.466 | 1.577 | +0.889 |
| F1 | 250 | Sweep | 9 | 2.465 | 1.460 | +1.006 |
| F1 | 500 | Globo | 8 | 2.052 | 1.586 | +0.466 |
| F1 | 500 | Sweep | 8 | 2.059 | 1.539 | +0.520 |
| F1 | 1000 | Globo | 8 | 1.702 | 1.714 | -0.012 |
| F1 | 1000 | Sweep | 9 | 1.720 | 1.648 | +0.071 |
| F1 | 2000 | Globo | 8 | 1.582 | 1.742 | -0.160 |
| F1 | 2000 | Sweep | 9 | 1.573 | 1.705 | -0.131 |
| F1 | 4000 | Globo | 8 | 1.344 | 1.566 | -0.222 |
| F1 | 4000 | Sweep | 9 | 1.347 | 1.527 | -0.180 |
| F1 | 8000 | Globo | 8 | 0.861 | 0.949 | -0.088 |
| F1 | 8000 | Sweep | 9 | 0.862 | 0.933 | -0.070 |
| F2 | 125 | Globo | 3 | 3.175 | 1.742 | +1.433 |
| F2 | 125 | Sweep | 4 | 3.139 | 1.544 | +1.595 |
| F2 | 250 | Globo | 7 | 2.519 | 1.555 | +0.964 |
| F2 | 250 | Sweep | 8 | 2.532 | 1.446 | +1.087 |
| F2 | 500 | Globo | 8 | 2.032 | 1.620 | +0.411 |
| F2 | 500 | Sweep | 9 | 2.026 | 1.549 | +0.477 |
| F2 | 1000 | Globo | 8 | 1.733 | 1.720 | +0.013 |
| F2 | 1000 | Sweep | 9 | 1.726 | 1.665 | +0.061 |
| F2 | 2000 | Globo | 8 | 1.561 | 1.754 | -0.193 |
| F2 | 2000 | Sweep | 9 | 1.566 | 1.703 | -0.137 |
| F2 | 4000 | Globo | 8 | 1.382 | 1.588 | -0.206 |
| F2 | 4000 | Sweep | 9 | 1.376 | 1.545 | -0.169 |
| F2 | 8000 | Globo | 8 | 0.856 | 0.964 | -0.108 |
| F2 | 8000 | Sweep | 9 | 0.857 | 0.949 | -0.092 |

Fuera del punto y banda usados para ajustar, el error absoluto medio frente a las referencias aceptadas es 0.456 s y el RMSE 0.728 s. Son resúmenes descriptivos de comparaciones correlacionadas, no una certificación de exactitud.

## Interpretación de la comprobación

A 1 kHz, las medias simuladas emparejadas con globos son 1,702 s para F1 y 1,733 s para F2, frente a 1,714 y 1,720 s en REW. El ajuste del punto objetivo también se aproxima a las medias de esa banda.
La curva no se generaliza a todo el espectro: a 250 Hz se obtienen aproximadamente 2,47–2,53 s frente a 1,45–1,58 s medidos; a 500 Hz persiste exceso de reverberación. A 2–4 kHz, por el contrario, el incremento uniforme produce tiempos menores que las referencias.
Esto no justifica elegir el valor efectivo como coeficiente del concreto. La siguiente hipótesis debe distinguir el comportamiento por frecuencia y las construcciones que el modelo está representando de forma equivalente; no basta un único aumento de absorción en toda la curva.
A 125 Hz, algunas regresiones simuladas T20 tienen R²≈0,94–0,96 y son claramente menos lineales. Sus cifras se conservan como diagnóstico, pero necesitan más partículas y revisión de las curvas y duración antes de considerarlas una estimación precisa de RT. El RMSE global incluye esas cifras y queda muy influido por ellas. A 8 kHz también debe recordarse la extrapolación de materiales y la sensibilidad ambiental.

## Verificación espacial a 1 kHz

| Fuente | Receptor | T20 (s) | T30 (s) | EDT (s) |
|---|---|---:|---:|---:|
| F1 | P1 | 1.645 | 1.862 | 1.588 |
| F1 | P2 | 1.680 | 1.758 | 1.782 |
| F1 | P3 | 1.859 | 1.888 | 1.595 |
| F1 | P4 | 1.619 | 1.640 | 1.541 |
| F1 | P5 | 1.585 | 1.752 | 1.598 |
| F1 | P6 | 1.981 | 1.853 | 1.457 |
| F1 | P7 | 1.652 | 1.666 | 1.711 |
| F1 | P8 | 1.648 | 1.687 | 1.732 |
| F1 | P9 | 1.808 | 1.908 | 1.603 |
| F2 | P1 | 1.648 | 1.948 | 1.697 |
| F2 | P2 | 1.738 | 1.759 | 1.759 |
| F2 | P3 | 1.724 | 1.695 | 1.478 |
| F2 | P4 | 1.787 | 1.720 | 1.628 |
| F2 | P5 | 1.763 | 1.539 | 1.603 |
| F2 | P6 | 1.674 | 1.693 | 1.425 |
| F2 | P7 | 1.882 | 1.833 | 1.590 |
| F2 | P8 | 1.685 | 1.623 | 1.518 |
| F2 | P9 | 1.634 | 1.708 | 1.821 |

## Alcance y archivos

Pérdida máxima por mallado: 0.0270 %. Geometría nativa y tetraedros conservados. Solo 195 caras de muro reciben el nuevo identificador de material. Las validaciones espectrales usan 300.000 partículas por banda; la confirmación del ajuste usa 1.200.000.
Abrir D_muros_ajuste_1kHz.proj. Incluye el nuevo material AM_Muros_ajuste_efectivo_NO_MEDIDO y los resultados de confirmación y validación. La escena, fuentes y receptores conservan la configuración de B. La estructura ZIP/XML y las referencias se verificaron; no se abrió la interfaz gráfica.
La curva nueva puede compensar errores de otros elementos. Si exige absorción elevada, no debe explicarse solo por una textura rugosa. Una coincidencia en el punto objetivo no garantiza EDT, C80 o estructura de ecos correctos.
La búsqueda con 100.000 partículas mostró variación y respuestas no monótonas entre algunos ensayos; se utilizó únicamente para acotar el parámetro. El objetivo se confirmó con 1.200.000 partículas. Las validaciones con 300.000 pueden diferir en el punto objetivo y requieren mayor convergencia antes de interpretar diferencias pequeñas.
Los coeficientes extremos de 8 kHz siguen siendo una extrapolación de la curva inicial. Faltan temperatura/humedad medidas y directividad del altavoz de ensayo. No utilizar el nivel absoluto de estas simulaciones para dimensionar el refuerzo sonoro.
