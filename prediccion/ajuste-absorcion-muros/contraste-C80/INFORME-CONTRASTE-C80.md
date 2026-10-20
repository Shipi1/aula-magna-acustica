# Contraste del C80 predicho con las mediciones

Se compara el modelo D con los valores C80 ya calculados por REW y exportados en los 36 archivos de datos de globos y barridos. No se modifican los originales ni se ejecutan nuevas simulaciones. Se usa el mismo centro de tercio de octava (125, 250, 500, 1000, 2000, 4000 y 8000 Hz), sin reconstruir octavas ni combinar fuentes.

Hay 252 pares de comparación; 238 entran en los resúmenes. Se excluyen los siete valores de Globo F1-P3 y los siete de Globo F2-P6 por duplicación conocida de WAV. La etiqueta correcta de cada par no está confirmada: F1-P2/P3 y F2-P4/P6 siguen marcados como ambiguos. Los valores negativos y cero de C80 son válidos; no se filtran usando el coeficiente de regresión del RT, que no certifica la calidad de C80.

## Resultado por frecuencia

Promedios emparejados de ambas posiciones de fuente. MAE = media del error absoluto; no es incertidumbre ni tolerancia normativa.

| Método | Hz | n | Modelo (dB) | REW (dB) | Sesgo (dB) | MAE (dB) |
|---|---:|---:|---:|---:|---:|---:|
| Globo | 125 | 16 | -2.49 | -3.19 | +0.69 | 1.87 |
| Globo | 250 | 16 | -0.84 | -0.76 | -0.08 | 1.51 |
| Globo | 500 | 16 | +0.17 | +0.93 | -0.76 | 1.52 |
| Globo | 1000 | 16 | +1.51 | +1.28 | +0.23 | 1.60 |
| Globo | 2000 | 16 | +1.48 | +1.09 | +0.39 | 1.48 |
| Globo | 4000 | 16 | +2.66 | +1.73 | +0.93 | 1.58 |
| Globo | 8000 | 16 | +5.87 | +4.80 | +1.07 | 1.94 |
| Sweep | 125 | 18 | -2.37 | +0.74 | -3.11 | 4.09 |
| Sweep | 250 | 18 | -0.74 | +1.69 | -2.43 | 2.45 |
| Sweep | 500 | 18 | +0.28 | +3.44 | -3.16 | 3.16 |
| Sweep | 1000 | 18 | +1.71 | +5.60 | -3.89 | 4.10 |
| Sweep | 2000 | 18 | +1.66 | +3.59 | -1.94 | 2.17 |
| Sweep | 4000 | 18 | +2.73 | +4.56 | -1.83 | 2.41 |
| Sweep | 8000 | 18 | +5.89 | +8.28 | -2.39 | 2.91 |

## Interpretación

**El modelo D todavía no reproduce de forma suficiente la claridad medida.** A 1 kHz su media frente a globos se aproxima (+1,51 frente a +1,28 dB), pero el error absoluto medio punto a punto es 1,60 dB. La coincidencia de medias oculta diferencias espaciales. Frente a barridos, el error absoluto medio sube a 4,10 dB y el modelo subestima C80 en promedio 3,89 dB.

La diferencia entre globo y barrido no debe atribuirse automáticamente a un cambio de la sala: puede incluir directividad y orientación del parlante, tiempo cero, excitación y procesamiento. Las medias de ambos métodos en la tabla usan distinto conjunto de puntos por las exclusiones. Deben compararse también las filas individuales, sin fusionar ambas referencias en una sola curva objetivo.

En platea alta, las mediciones presentan menor C80 que bajo balcón en los tercios de 500, 1000, 2000, 4000 y 8000 Hz, con ambos métodos. A 4 kHz, por ejemplo, la media de platea alta es −0,18 dB con globos y +1,25 dB con barridos. Esto respalda un mayor peso relativo de energía posterior a 80 ms en esa zona respecto de las otras zonas; no demuestra que su nivel absoluto de agudos sea mayor ni identifica las paredes responsables.

Bajo balcón no aparece un déficit de C80 a 1 kHz: las medias medidas son +2,71 dB (globo) y +7,93 dB (barrido). Es compatible con que el balcón reduzca parte de la energía tardía, pero no prueba la causa. Una claridad alta no garantiza nivel recibido, cobertura ni balance espectral adecuados: la necesidad de altavoces de apoyo debe justificarse además con esas variables.

El modelo D muestra cambios de C80 de hasta 1,34 dB al pasar de 300.000 a 1.200.000 partículas en F1 a 1 kHz. Por tanto, parte de las diferencias pequeñas aún puede deberse al muestreo. No corresponde afinar materiales por décimas de dB con esta convergencia.

La exclusión adicional de ambos pares de etiquetas ambiguas deja a 1 kHz un MAE frente a globos de 1,62 dB (14 puntos fuente-receptor), parecido al de 1,60 dB con la convención principal. La conclusión de falta de concordancia espacial no depende solo de esos duplicados.

Siguiente trabajo recomendado: comprobar el origen temporal en las IR de las mediciones, representar la orientación/directividad del parlante en una variante separada y aumentar/confrontar el muestreo de C80; después revisar absorción y dispersión con objetivos simultáneos de RT, EDT y claridad. No aumentar absorción indiscriminadamente ni ajustar el modelo a una media única.

## Comparación por receptor a 1 kHz

| Fuente | Punto | Modelo (dB) | Globo REW (dB) | Sweep REW (dB) |
|---|---|---:|---:|---:|
| F1 | P1 | +0.98 | +2.08 | +5.94 |
| F1 | P2 | +1.69 | -0.58 * | +6.69 |
| F1 | P3 | +3.05 | Excluido | +7.99 |
| F1 | P4 | +1.13 | -0.48 | +4.25 |
| F1 | P5 | +2.27 | +3.53 | +9.39 |
| F1 | P6 | +4.31 | +3.08 | +7.44 |
| F1 | P7 | +1.03 | +3.42 | +6.95 |
| F1 | P8 | +0.83 | +0.90 | -0.33 |
| F1 | P9 | +1.15 | +0.11 | +0.65 |
| F2 | P1 | -1.04 | +2.53 | +7.44 |
| F2 | P2 | +1.91 | -0.53 | +8.32 |
| F2 | P3 | +3.12 | +0.70 | +6.00 |
| F2 | P4 | +1.20 | +1.73 * | +1.02 |
| F2 | P5 | +5.25 | +3.51 | +7.96 |
| F2 | P6 | +3.65 | Excluido | +8.81 |
| F2 | P7 | +0.92 | -0.45 | +9.01 |
| F2 | P8 | +0.17 | -0.29 | +2.12 |
| F2 | P9 | -0.82 | +1.21 | +1.20 |

* Etiqueta ambigua del par duplicado. P8 y P9 son platea alta, según confirmación del usuario.

## Resumen por zona a 1 kHz

| Método | Zona | n | Modelo (dB) | REW (dB) | MAE (dB) |
|---|---|---:|---:|---:|---:|
| Globo | Platea general | 8 | +0.98 | +0.96 | 1.91 |
| Globo | Bajo balcón | 4 | +3.73 | +2.71 | 1.66 |
| Globo | Platea alta | 4 | +0.33 | +0.48 | 0.90 |
| Sweep | Platea general | 8 | +0.98 | +6.20 | 5.27 |
| Sweep | Bajo balcón | 6 | +3.61 | +7.93 | 4.32 |
| Sweep | Platea alta | 4 | +0.33 | +0.91 | 1.41 |

## Convergencia del modelo D a 1 kHz

Se procesó también la confirmación existente de F1 con 1.200.000 partículas y se comparó con la validación de 300.000. Geometría y materiales corresponden a D. No es una comparación entre el modelo anterior de 4 s y D.

| Punto | C80 300k (dB) | C80 1200k (dB) | Cambio (dB) |
|---|---:|---:|---:|
| F1-P1 | +0.98 | +0.39 | -0.59 |
| F1-P2 | +1.69 | +1.57 | -0.13 |
| F1-P3 | +3.05 | +2.25 | -0.81 |
| F1-P4 | +1.13 | +0.83 | -0.30 |
| F1-P5 | +2.27 | +3.61 | +1.34 |
| F1-P6 | +4.31 | +4.49 | +0.18 |
| F1-P7 | +1.03 | +0.95 | -0.08 |
| F1-P8 | +0.83 | +0.60 | -0.23 |
| F1-P9 | +1.15 | +0.41 | -0.74 |

## Límites de la comparación

- Los valores medidos son los C80 exportados por REW, no una repetición propia del filtrado. Los 252 pares indican filtrado Forward. El modelo entrega energía geométrica por banda sin la respuesta temporal del filtro. Esta diferencia importa especialmente en las bandas bajas; la comparación es exploratoria y no certifica concordancia ISO.
- El inicio de SPPS se referencia a distancia/342 m/s; los exportes REW sitúan el pico en tiempo cero. No se modificó ese origen ni el tratamiento de ruido almacenado en REW. Si el pico dominante fuera una reflexión, ambos criterios no coincidirían. Hay que verificarlo antes de una atribución fina a superficies.
- El modelo integra 4 s de energía y usa intervalos de 1 ms. Los barridos tienen 131072 muestras a 48 kHz y pico en torno a 1 s: conservan aproximadamente 1,73 s después del pico. Una cola recortada puede sesgar la claridad; los globos aportan una comprobación con registro más largo. No se inventa una corrección de cola.
- La fuente simulada es omnidireccional. El parlante real y la explosión del globo no tienen necesariamente esa directividad, sobre todo a alta frecuencia. C80 es sensible a esa diferencia y a orientación, geometría y dispersión.
- El material de pared de D es un ajuste efectivo para acercar RT a 1 kHz. No se ajustó con C80. Un RT coincidente no valida la distribución temporal de energía.
- C80 positivo indica más energía en los primeros 80 ms que después. No separa el sonido directo de las primeras reflexiones y no demuestra ni descarta flutter echo. No debe maximizarse indiscriminadamente para uso orquestal.

## Fuentes y trazabilidad

El JSON incluye cada archivo de medición, valores emparejados, exclusiones y sensibilidad del corte temporal del modelo. No se altera el informe web ni los proyectos I-Simpa.

[REW: definición de claridad y exportación](https://www.roomeqwizard.com/help/help_en-GB/html/graph_clarity.html). [REW: filtrado e influencia del truncamiento](https://www.roomeqwizard.com/help/help_en-GB/html/graph_rt60.html).
