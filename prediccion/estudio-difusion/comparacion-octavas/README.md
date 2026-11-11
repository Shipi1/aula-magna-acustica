# Sala sin tratamiento frente a propuesta: bandas de octava

Este estudio amplía la comparación a 63/125/250/500/1.000/2.000/4.000/8.000 Hz, manteniendo las mismas geometrías. La propuesta corresponde a cuatro reflectores con inclinación combinada y el paño central posterior de 9,6 m², con el espectro efectivo definido antes del cálculo.

- [Protocolo y fuente de los coeficientes](../../../informes/PROTOCOLO-COMPARACION-POR-OCTAVAS.md).
- [Informe de resultados](../../../informes/RESULTADOS-COMPARACION-POR-OCTAVAS.md).
- [Espectros y supuestos](espectros.json), [reutilización de 1.000 Hz](reutilizadas-1000Hz.json) y matrices de cálculo en esta carpeta.

Se mantienen 600.000 partículas, tres semillas, dos fuentes por separado, 21 receptores, 4 s y paso de 1 ms. Hay 84 corridas principales nuevas y doce reutilizadas de 1.000 Hz, además de 28 pilotos excluidos del análisis principal. Las energías lineales se promedian antes de calcular indicadores.

Los modelos de `modelos/` son copias verificadas de los utilizados en la comparación anterior. El proyecto canónico y los estudios previos permanecen sin cambios. En `calculos/` se conservan configuraciones, registros, metadatos, energías lineales y salidas nativas verificadas.

La curva de A1 es una hipótesis escalada a 0,60 en 1.000 Hz a partir de un ensayo publicado; no es una ficha ensayada del tratamiento. 63 y 8.000 Hz incluyen extrapolaciones. Los reflectores se idealizan con α y dispersión 0,05 constantes. Las bandas bajas requieren cautela por tamaño finito, difracción y propiedades efectivas de la base.

El rango de trabajo de 1.000 Hz no se convierte en un óptimo obligatorio para todas las frecuencias. Las bandas y los receptores críticos permanecen visibles aun cuando una condición empeore.

## Resultados adjuntos

- [Indicadores medios por receptor, fuente y banda](resultados/medias.csv), [resultados por semilla](resultados/semillas.csv), [diferencias](resultados/diferencias.csv) y [resumen por zona](resultados/resumen-zonas.csv).
- [Verificación de entradas](resultados/verificacion.json), [corridas verificadas](resultados/corridas-verificadas.csv) y [coeficientes efectivos utilizados](resultados/coeficientes-usados.csv).
- [D50 por zona](resultados/D50-por-zona.png), [C80 por zona](resultados/C80-por-zona.png), [T30 por zona](resultados/T30-por-zona.png) y [EDT por zona](resultados/EDT-por-zona.png).
- [Cambios de D50 por posición](resultados/delta_D50_pct.png), [cambios de C80](resultados/delta_C80.png), [P8/P9](resultados/P8-P9-por-octava.png) y [energía por ventanas](resultados/energias-por-octava.png).

El archivo `AVANCE.md` muestra el estado del cálculo. Las tablas finales reúnen 672 respuestas medias y 2.016 resultados por semilla; los pilotos no forman parte de esas tablas.
