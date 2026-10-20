# C80 exploratorio del modelo D

C80=10log10(Etemprana/Etardia). Energía RECP lineal, sin volver a elevar al cuadrado. t0=distancia fuente-receptor/342 m/s; bins de 1 ms, centro (i+0.5) ms. Corte t0+80 ms; final de integración 4 s. Referencia geométrica presupone llegada directa no obstruida; revisar en puntos con sombra. Resultados exploratorios del modelo D, no validación del recinto.

Se procesaron las simulaciones espectrales ya existentes de F1 y F2. No se cambiaron materiales ni se ejecutaron simulaciones nuevas. El paso de 80 a 90 dB de potencia global no altera esta razón energética en el modelo lineal.

**El modelo aún no está calibrado en todo el espectro. Estos valores describen su predicción actual y no demuestran que la sala real tenga esa claridad.** La sensibilidad al corte ±1 ms se entrega en JSON; no representa toda la incertidumbre. Faltan comprobación de convergencia de C80, directividad real y contraste con C80 medido. Las bandas son tercios de octava aislados, no octavas ni un índice global.

El numerador incluye sonido directo y reflexiones durante los primeros 80 ms. C80 no separa directo/reflejado ni confirma por sí solo un eco flotante.

| Fuente | Punto | 250 Hz | 500 Hz | 1000 Hz | 2000 Hz | 4000 Hz |
|---|---|---:|---:|---:|---:|---:|
| F1 | P1 | -1.95 | -0.03 | +0.98 | -0.32 | +1.64 |
| F1 | P2 | -0.22 | +0.26 | +1.69 | +2.46 | +2.84 |
| F1 | P3 | -0.46 | +1.14 | +3.05 | +2.52 | +2.80 |
| F1 | P4 | -1.29 | -1.07 | +1.13 | +1.11 | +1.88 |
| F1 | P5 | -0.54 | +1.31 | +2.27 | +4.22 | +4.51 |
| F1 | P6 | +1.23 | +2.60 | +4.31 | +3.86 | +5.05 |
| F1 | P7 | -2.07 | -0.51 | +1.03 | +0.58 | +1.02 |
| F1 | P8 | -1.92 | -0.04 | +0.83 | +1.03 | +1.53 |
| F1 | P9 | -1.36 | -0.41 | +1.15 | +0.06 | +2.91 |
| F2 | P1 | -2.59 | -1.69 | -1.04 | -1.14 | +1.14 |
| F2 | P2 | +1.08 | +1.16 | +1.91 | +2.84 | +3.17 |
| F2 | P3 | +0.39 | +1.25 | +3.12 | +2.47 | +2.91 |
| F2 | P4 | -0.83 | -1.11 | +1.20 | +1.49 | +1.90 |
| F2 | P5 | +1.84 | +2.36 | +5.25 | +2.81 | +7.81 |
| F2 | P6 | +0.63 | +1.17 | +3.65 | +3.69 | +3.76 |
| F2 | P7 | -1.98 | -0.74 | +0.92 | +1.52 | +1.16 |
| F2 | P8 | -1.13 | +0.52 | +0.17 | +0.61 | +2.23 |
| F2 | P9 | -2.09 | -1.12 | -0.82 | -0.00 | +0.92 |

Valores en dB. P8 y P9 corresponden a platea alta. Las siete bandas completas (125–8000 Hz) se encuentran en C80-modelo-D.json.

Antes de comparar con REW hay que usar la misma banda, criterio de tiempo cero y tratamiento de cola/ruido. Un cálculo de partículas energético no reproduce la fase ni la vibración de una tarima: su efecto debe incorporarse mediante una curva de absorción equivalente respaldada.
