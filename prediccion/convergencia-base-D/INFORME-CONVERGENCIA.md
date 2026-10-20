# Convergencia numérica del modelo base D

Se mantiene la geometría y todos los materiales. Los cálculos son de F1, nueve receptores y tercio de octava de 1 kHz. La potencia de referencia es Lw global 80 dB como en D; C80, EDT y RT son independientes del cambio a 90 dB en este modelo lineal. Los originales D y E se conservan.

De trabajo, no normativos: cambio C80 <0.5 dB y T20/T30 <5% entre niveles N con semilla 20261019. Para tres semillas al N mayor: rango max-min C80 <0.5 dB y rango RT/media <5%. Tres semillas solo describen variación observada, no garantizan intervalos de confianza.

## Ejecuciones completadas

| Partículas | Semilla | Origen | Tiempo de cálculo (s) |
|---:|---:|---|---:|
| 1,200,000 | 20261019 | Confirmación D reutilizada | — |
| 2,400,000 | 20261019 | Nuevo cálculo SPPS | 350 |
| 4,800,000 | 20261019 | Nuevo cálculo SPPS | 677 |
| 4,800,000 | 20261020 | Nuevo cálculo SPPS | 683 |
| 4,800,000 | 20261021 | Nuevo cálculo SPPS | 661 |

## Cambio al aumentar partículas

| Partículas | Máx. cambio C80 | Puntos C80 <0,5 dB | Máx. cambio T20 | Máx. cambio T30 |
|---|---:|---:|---:|---:|
| 1,200,000 → 2,400,000 | 0.229 dB | 9/9 | 3.47 % | 3.32 % |
| 2,400,000 → 4,800,000 | 0.203 dB | 9/9 | 1.81 % | 1.71 % |

## Repeticiones con distintas semillas al nivel mayor

Nivel: 4,800,000 partículas por repetición. Semillas completadas: 20261019, 20261020, 20261021.

| Punto | C80 medio (dB) | Rango C80 (dB) | T20 medio (s) | Rango T20 (s) | T30 medio (s) |
|---|---:|---:|---:|---:|---:|
| P1 | +0.688 | 0.065 | 1.690 | 0.018 | 1.777 |
| P2 | +1.744 | 0.055 | 1.674 | 0.015 | 1.744 |
| P3 | +2.329 | 0.274 | 1.731 | 0.015 | 1.771 |
| P4 | +0.877 | 0.225 | 1.660 | 0.039 | 1.751 |
| P5 | +3.447 | 0.392 | 1.663 | 0.036 | 1.706 |
| P6 | +4.310 | 0.311 | 1.701 | 0.026 | 1.749 |
| P7 | +0.912 | 0.085 | 1.709 | 0.017 | 1.746 |
| P8 | +0.478 | 0.437 | 1.727 | 0.088 | 1.774 |
| P9 | +0.469 | 0.311 | 1.741 | 0.069 | 1.776 |

## Respuesta energética media de las repeticiones

Se promedian las energías lineales de las realizaciones con igual N y se recalculan los parámetros. Esta respuesta reduce el ruido de muestreo y mantiene la potencia de una fuente; no representa varias fuentes sonando a la vez. Los parámetros pueden diferir ligeramente del promedio de parámetros de la tabla anterior.

| Punto | C80 de energía media (dB) | T20 de energía media (s) | T30 de energía media (s) | EDT (s) |
|---|---:|---:|---:|---:|
| P1 | +0.688 | 1.689 | 1.775 | 1.582 |
| P2 | +1.744 | 1.673 | 1.744 | 1.762 |
| P3 | +2.330 | 1.731 | 1.768 | 1.493 |
| P4 | +0.877 | 1.660 | 1.750 | 1.579 |
| P5 | +3.449 | 1.661 | 1.706 | 1.490 |
| P6 | +4.312 | 1.700 | 1.749 | 1.373 |
| P7 | +0.912 | 1.709 | 1.746 | 1.629 |
| P8 | +0.479 | 1.727 | 1.774 | 1.620 |
| P9 | +0.468 | 1.740 | 1.777 | 1.637 |

## Evaluación

No se cumplen todos los criterios de trabajo en los nueve puntos. Debe conservarse la variación observada y evitar interpretar cambios pequeños como efectos físicos.

Puntos que cumplen C80 entre los dos últimos niveles de partículas: 9/9. Puntos con rango C80 <0,5 dB entre semillas: 9/9. Puntos con rango T20 y T30 <5 % entre semillas: 7/9.

Esta evaluación se limita a F1 y 1 kHz. No prueba convergencia de F2 ni del resto del espectro, ni valida la absorción efectiva de paredes.

## Uso para comparar tratamientos

Comparar estado actual y tratado con igual configuración numérica y varias semillas; usar diferencias por receptor, banda y zona. El rango entre semillas observado aquí no incluye incertidumbre de materiales, geometría o directividad. Un cambio del tratamiento menor que ese rango no es una evidencia robusta por sí solo. La variación entre varios modelos base plausibles debe evaluarse además de la numérica.

El origen de C80 es distancia/342 m/s; el corte se fija a 80 ms después de esa llegada. No se vuelve a elevar al cuadrado la energía RECP. El resultado integra hasta 4 s. Las semillas se controlan con una sola banda por proceso, manteniendo radio 0,31 m y paso 1 ms.

[Documentación de configuración SPPS](https://i-simpa-wiki.readthedocs.io/fr/latest/code_configuration_SPPS.html).
