# Auditoría auxiliar del C80 medido a 1 kHz

Filtro Butterworth de tercio, prototipo orden 6, magnitud FFT fase cero de una pasada. t0 local en torno al pico de la señal de banda ancha; corte Lundeby. Resta de ruido integrada por segmento, con variante rectificada para diagnóstico. No replica el filtro Forward ni las preferencias internas de REW. El umbral en los 20 ms previos NO identifica de forma automática la llegada directa.

No sustituye la referencia REW. Sirve para comprobar si las diferencias entre campañas desaparecen al usar un procesamiento común. Los valores de fase cero no son una nueva certificación del C80. La sensibilidad ±2 ms desplaza solo el límite de 80 ms; no sustituye una selección manual del sonido directo.

| Método | Toma | REW Forward | Fase cero, ruido integrado | Cambio de corte ±2 ms | Adelanto de otro umbral (ms) |
|---|---|---:|---:|---|---:|
| Globo | F1-P1 | +2.08 | +1.45 | +1.43 / +1.63 | 6.35 |
| Globo | F1-P2 | -0.58 | -1.09 | -1.86 / -0.63 | 1.54 |
| Globo | F1-P3 (duplicado) | -0.58 | -1.11 | -1.88 / -0.65 | 1.54 |
| Globo | F1-P4 | -0.48 | -0.06 | -0.22 / +0.31 | 9.42 |
| Globo | F1-P5 | +3.53 | +5.29 | +5.15 / +5.34 | 19.73 |
| Globo | F1-P6 | +3.08 | +3.57 | +2.95 / +4.02 | 1.54 |
| Globo | F1-P7 | +3.42 | +2.91 | +2.90 / +2.94 | 1.81 |
| Globo | F1-P8 | +0.90 | +1.34 | +1.27 / +1.36 | 18.08 |
| Globo | F1-P9 | +0.11 | -1.06 | -1.19 / -0.96 | 18.29 |
| Globo | F2-P1 | +2.53 | +2.56 | +2.48 / +2.67 | 1.77 |
| Globo | F2-P2 | -0.53 | -0.28 | -0.71 / +0.30 | 0.65 |
| Globo | F2-P3 | +0.70 | +0.16 | +0.14 / +0.19 | 0.62 |
| Globo | F2-P4 | +1.73 | +1.41 | +1.29 / +1.75 | 0.71 |
| Globo | F2-P5 | +3.51 | +3.32 | +3.06 / +3.47 | 1.94 |
| Globo | F2-P6 (duplicado) | +1.73 | +1.41 | +1.29 / +1.75 | 0.71 |
| Globo | F2-P7 | -0.45 | -0.60 | -0.68 / -0.36 | 0.44 |
| Globo | F2-P8 | -0.29 | +0.62 | +0.57 / +0.65 | 19.40 |
| Globo | F2-P9 | +1.21 | +1.18 | +0.99 / +1.20 | 1.21 |
| Sweep | F2-P6 | +8.81 | +7.95 | +7.95 / +7.96 | 0.00 |
| Sweep | F2-P7 | +9.01 | +8.07 | +7.78 / +8.12 | 0.00 |
| Sweep | F1-P1 | +5.94 | +5.32 | +5.31 / +5.33 | 0.00 |
| Sweep | F1-P2 | +6.69 | +5.51 | +5.32 / +5.73 | 0.00 |
| Sweep | F1-P3 | +7.99 | +7.26 | +7.25 / +7.30 | 0.00 |
| Sweep | F1-P4 | +4.25 | +3.43 | +3.37 / +3.45 | 0.00 |
| Sweep | F1-P5 | +9.39 | +8.83 | +8.59 / +8.98 | 0.00 |
| Sweep | F1-P6 | +7.44 | +6.54 | +6.43 / +6.63 | 0.00 |
| Sweep | F1-P7 | +6.95 | +6.23 | +6.17 / +6.32 | 0.00 |
| Sweep | F1-P8 | -0.33 | -0.92 | -0.93 / -0.83 | 0.00 |
| Sweep | F1-P9 | +0.65 | +0.29 | +0.27 / +0.38 | 0.00 |
| Sweep | F2-P1 | +7.44 | +6.67 | +6.22 / +7.00 | 0.00 |
| Sweep | F2-P2 | +8.32 | +6.90 | +6.86 / +6.92 | 0.06 |
| Sweep | F2-P3 | +6.00 | +5.23 | +5.11 / +5.30 | 0.00 |
| Sweep | F2-P4 | +1.02 | +0.28 | +0.26 / +0.42 | 0.00 |
| Sweep | F2-P5 | +7.96 | +7.32 | +7.15 / +7.36 | 0.00 |
| Sweep | F2-P8 | +2.12 | +1.75 | +1.64 / +1.77 | 0.00 |
| Sweep | F2-P9 | +1.20 | +0.19 | +0.16 / +0.23 | 0.00 |

Se conserva cada resultado por toma. No se promedian ambas campañas como si fueran una misma fuente.
