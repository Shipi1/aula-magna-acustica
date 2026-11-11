# Comparación directa: sala sin tratamiento y propuesta mixta

**Fecha: 10 de noviembre de 2026.** Este entregable compara el modelo del estado actual con cuatro reflectores de inclinación combinada y un paño central posterior de 9,6 m², α = 0,60 a 1.000 Hz, situado en Z = 9,0–10,2 m.

La alternativa se eligió por conservar los tres pares prioritarios de P8/P9 dentro de ambos rangos en las tres semillas del estudio mixto. No se declara óptima ni equivale al paño superior extendido de 19,2 m².

## Informe y figuras

- [Informe comparativo completo](../../../informes/INFORME-COMPARATIVO-SALA-SIN-TRATAMIENTO-Y-PROPUESTA-MIXTA.md).
- [Comparación de modelos 3D](modelos-3D-comparados.png), [perspectiva adicional](detalle-propuesta-3D.png) y [planta](modelos-planta.png).
- [Mapa D50 F1](mapa-D50-F1.png), [mapa D50 F2](mapa-D50-F2.png), [D50/C80](D50-C80.png) y [energías por ventanas](balance-ventanas.png).

Las vistas abiertas omiten cielos y el muro lateral cercano únicamente para visualizar el interior. Los modelos de simulación son cerrados. R1–R4 son reflectores y A1 es el paño absorbente. Los colores son una ayuda gráfica y no representan texturas reales.

## Datos adjuntos

- [Medias](medias.csv), [resultados por semilla](semillas.csv), [diferencias](diferencias.csv), [resumen por zona](resumen-zonas.csv) y [verificación de condiciones y entradas](verificacion.json).
- Las correspondientes versiones JSON conservan los mismos indicadores.

Se reutilizaron doce corridas principales: seis de `../reflectores/calculos/base-*` y seis de `../reflectores-absorcion-localizada/calculos/media_centro_a060-*`. No se realizaron nuevas simulaciones para esta comparación. Se mantuvieron fuentes, receptores, condiciones, 600.000 partículas y tres semillas; la banda calculada es 1.000 Hz.

La triangulación de las dos geometrías difiere por la subdivisión coplanar y la adición de sólidos. El informe distingue esta limitación de los efectos materiales. Las respuestas se promedian en energía lineal antes de calcular los indicadores. Los rangos entre semillas no son intervalos de confianza.

Los procedimientos de análisis, representación e informe son `comparar_sala_propuesta.py`, `visualizar_sala_propuesta.py` e `informar_sala_propuesta.py`, en la carpeta superior.
