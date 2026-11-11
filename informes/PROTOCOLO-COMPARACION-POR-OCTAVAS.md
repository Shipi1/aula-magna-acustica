# Extensión de la comparación a bandas de octava

**Fecha: 10 de noviembre de 2026.** Protocolo de la ampliación espectral de la comparación entre sala sin tratamiento y propuesta de cuatro reflectores inclinados más paño posterior central de 9,6 m². Se mantienen posiciones y geometrías; no se recalibra la sala.

**Estado:** cálculo completado. La interpretación y los resultados por banda están en el [informe de octavas](RESULTADOS-COMPARACION-POR-OCTAVAS.md).

## Bandas y condiciones

Se calculan **63, 125, 250, 500, 1.000, 2.000, 4.000 y 8.000 Hz**. La banda de 63 Hz se añade como exploratoria. Se conserva el criterio anterior de no priorizar 16 kHz.

Se mantienen 600.000 partículas por corrida, tres semillas (20261019/20261020/20261021), una fuente por proceso, 4 s, paso 1 ms, receptor de radio 0,31 m, Lw global de 90 dB con el espectro original, fuentes omnidireccionales y las condiciones ambientales del estudio anterior. Las fuentes y los 21 receptores permanecen iguales.

Se ejecutan 84 corridas principales nuevas en las siete bandas distintas de 1.000 Hz. Las doce corridas anteriores de 1.000 Hz se reutilizan después de verificar compatibilidad de geometría, configuración y coeficientes activos. El conjunto reúne 96 condiciones banda/estado/fuente/semilla y 2.016 respuestas individuales de receptores. Se hacen además 28 pilotos de 20.000 partículas, excluidos de los promedios finales.

## Hipótesis espectral del tratamiento

El usuario autorizó utilizar un espectro de referencia documentado. La curva del absorbente a 1.000 Hz era un coeficiente efectivo de 0,60; no existía una ficha de producto de la propuesta. Se conserva ese valor y se utiliza la forma de una curva publicada para definir una **hipótesis espectral efectiva**, no un producto ya caracterizado.

La fuente es el [ensayo CSTB AC14-26051052/7, publicado por Ecophon](https://www.ecophon.com/globalassets/old-structure/01.ecophon-master/technical-documentation/absorption_iso/akusto-wall/akusto_wall_wall_panel_a_super_g_ods43_octave.pdf/), de 1 de octubre de 2014, correspondiente a Akusto Wall A/Super G de 40 mm y profundidad total de montaje de 43 mm. Se usan sus coeficientes prácticos publicados de 125–4.000 Hz como forma espectral. No se asignan directamente sus prestaciones al paño propuesto.

La transformación declarada antes de los cálculos es:

\[
\alpha_{A1}(f)=0,60\,\frac{\alpha_{\mathrm{referencia}}(f)}{\alpha_{\mathrm{referencia}}(1.000)}.
\]

| Banda | Coeficiente publicado de referencia | Coeficiente efectivo usado en A1 | Procedencia |
|---|---:|---:|---|
| 63 Hz | Sin dato | 0,09 | Se mantiene el valor de 125 Hz; extrapolación |
| 125 Hz | 0,15 | 0,09 | Curva de referencia escalada |
| 250 Hz | 0,65 | 0,39 | Curva de referencia escalada |
| 500 Hz | 1,00 | 0,60 | Curva de referencia escalada |
| 1.000 Hz | 1,00 | 0,60 | Conserva el ensayo anterior |
| 2.000 Hz | 1,00 | 0,60 | Curva de referencia escalada |
| 4.000 Hz | 1,00 | 0,60 | Curva de referencia escalada |
| 8.000 Hz | Sin dato | 0,60 | Se mantiene el valor de 4.000 Hz; extrapolación |

El escalado es una hipótesis de estudio; no demuestra un montaje físico capaz de realizar exactamente esa curva ni representa automáticamente una mezcla de áreas. La dispersión de A1 se conserva como la del muro original. Los reflectores rígidos mantienen α = 0,05 y dispersión = 0,05 en todas las bandas; esta idealización no identifica su comportamiento resonante real en bajas frecuencias.

## Materiales originales y lectura física

Se conserva la absorción efectiva espectral de la base. En particular, el muro original tiene α ≈ 0,231 a 63/125 Hz y α = 0,60 a 250 Hz: son valores superiores a los asignados al paño nuevo en esas bandas. Por tanto, sustituir ese sector puede disminuir su absorción efectiva calculada. No se reajustan los coeficientes para forzar un beneficio en todas las frecuencias.

La base posee limitaciones de calibración, especialmente de claridad a 250 Hz. Los extremos de 63 y 8.000 Hz incorporan extrapolaciones. El tamaño finito de los reflectores y la difracción no resuelta limitan especialmente la interpretación en bandas bajas. Estos cálculos son exploratorios y no validan por sí solos una intervención física multibanda.

## Procesamiento y presentación

Se promedian las energías lineales de tres semillas antes de calcular parámetros. Se comparan D50, C80, EDT, T30, energía total y ventanas E0–50/E50–80/E>80 por receptor, fuente y banda. Los cambios de D50 se expresan en puntos porcentuales y los cambios de energía en dB. Se conserva la integración temporal del estudio anterior.

Los gráficos usarán la misma escala entre estados. En mapas de diferencias, el color representará la magnitud absoluta y las anotaciones conservarán el signo. Las bandas se mostrarán en orden de octava, sin aparentar mediciones en frecuencias intermedias.

D50 de 45–55 % y C80 de −2 a +2 dB siguen siendo los rangos exploratorios usados a 1.000 Hz. Se pueden mostrar como guías de comparación, pero no se impondrá el mismo óptimo como requisito universal para todas las bandas. Se mantendrán visibles F2–V08 y los controles de las otras zonas.

Los rangos entre semillas describen muestreo, no intervalos de confianza. Se examinará la calidad de los ajustes de decaimiento antes de interpretar EDT/T30 y no se confundirá un valor extrapolado con una caída observada de 60 dB.

## Archivos

- [Carpeta y configuración espectral](../prediccion/estudio-difusion/comparacion-octavas/README.md).
- [Informe comparativo anterior a 1.000 Hz](INFORME-COMPARATIVO-SALA-SIN-TRATAMIENTO-Y-PROPUESTA-MIXTA.md).
- [Resultados multibanda](RESULTADOS-COMPARACION-POR-OCTAVAS.md).
