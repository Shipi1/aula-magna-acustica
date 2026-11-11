# Reorientación del estudio hacia claridad musical y uniformidad

> **Documento archivado el 9 de noviembre de 2026.** Se conserva como antecedente de una etapa o estrategia sustituida; no es el protocolo vigente. Ubicación original: `informes/CRITERIOS-DE-CLARIDAD-MUSICAL-C80-D50.md`. Consultar el [plan actual](../../informes/PLAN-DE-ESTUDIO-D50-C80-Y-TRATAMIENTOS-POR-ZONA.md).


> **Plan vigente — D50 y C80:** el objetivo principal de continuación es estudiar D50 de 55–60 % a 1.000 Hz en P8/P9, con C80 de −2 a +2 dB como referencia conjunta a 500/1.000 Hz y controles en las demás zonas. Son metas de proyecto, no límites normativos. El [nuevo plan de referencia, simulación y revisión local](../../informes/PLAN-DE-ESTUDIO-D50-C80-Y-TRATAMIENTOS-POR-ZONA.md) prevalece sobre la jerarquía y las prioridades de ensayos de este documento. Los resultados históricos no se modifican.


**Teatro Aula Magna UTFSM — 9 de noviembre de 2026.**  
**Estado:** cambio de objetivo del estudio; evaluación inicial con respuestas ya disponibles, sin simulaciones nuevas.

## Objetivo actualizado

Se prioriza un balance de claridad musical adecuado y más uniforme en la platea alta, conservando la reverberación musical y evitando perjuicios en las zonas inferiores. C80 será el indicador principal y D50 un indicador complementario. La eliminación de flutter deja de ser condición necesaria para seleccionar una alternativa; los ecogramas y sus máximos se mantienen como controles de posibles retornos perjudiciales.

Esta actualización modifica la jerarquía de selección del [plan general](PLAN-DE-LOCALIZACION-Y-VALIDACION-DEL-TRATAMIENTO.md) y del [método de comparación](METODO-DE-COMPARACION-DE-DIFUSION.md). No cambia los resultados históricos ni convierte sus mejoras en evidencia de eliminación de ecos. Se mantienen las bandas 1, 2, 4 y 8 kHz; 16 kHz queda como antecedente.

## Qué se puede cuantificar

SPPS entrega ecogramas energéticos y permite obtener cocientes temporales como C80 y D50. También permite estudiar secuencias de retornos. Sin embargo, atribuir una percepción de flutter a una trayectoria y demostrar su desaparición exige más que una razón temprano/tardío: resolución suficiente, estabilidad de máximos, propiedades de reflexión y un criterio perceptual apropiado. La dificultad en este proyecto no implica que I-Simpa sea incapaz de representar reflexiones repetidas; implica que los ensayos actuales no bastan para certificar su percepción.

La [descripción oficial de SPPS](https://i-simpa-wiki.readthedocs.io/fr/latest/code_SPPS.html) identifica un método geométrico, energético y probabilístico cuya precisión depende del muestreo. Se priorizan aquí indicadores integrados más adecuados para comparar las respuestas disponibles; ello no los convierte en una evaluación completa de calidad musical.

## Definiciones y funciones

Si E representa energía integrada desde la llegada inicial:

\[
C_{80}=10\log_{10}\left(\frac{E_{0-80\,ms}}{E_{>80\,ms}}\right),\qquad
D_{50}=100\frac{E_{0-50\,ms}}{E_{total}}.
\]

C80 incluye directo y reflexiones de los primeros 80 ms. D50 indica qué porcentaje del total llega durante los primeros 50 ms; no se obtiene directamente de C80, porque emplea otro corte. D50 suele ser más útil en la evaluación de palabra que como objetivo principal de música. Véanse las [definiciones oficiales de REW](https://www.roomeqwizard.com/help/help/html/graph_clarity.html) y el tratamiento de criterios de palabra y música en el [apéndice técnico de EASERA](https://afmgd9.afmg.eu/sites/default/files/2021-09/EASERAAppendix.pdf).

En las respuestas SPPS se integran directamente las series energéticas, sin elevarlas otra vez al cuadrado. Se mantiene la referencia temporal, integración fraccional de intervalos y captura del frente directo de radio finito del estudio previo. El horizonte total es el disponible de 4 s. El contraste con medidas requiere igualar origen, filtrado, ancho de banda y tratamiento de ruido; el cálculo actual no resuelve automáticamente esas diferencias.

## Referencias de escucha musical

Como orientación inicial, ODEON presenta C80 entre **−1 y +3 dB** para música sinfónica. Es una referencia de diseño, no un límite normativo universal ni una banda de aceptación que debamos imponer por separado a 1, 2, 4 y 8 kHz. El repertorio, la ocupación, el criterio de promedio espectral y el asiento condicionan su uso. El [artículo de ODEON](https://odeon.dk/learn/articles/concert-hall-acoustics/) también destaca dimensiones como reverberación, fuerza y energía lateral; el [apéndice de EASERA](https://afmgd9.afmg.eu/sites/default/files/2021-09/EASERAAppendix.pdf) explica que no existe una regla normativa única de C80 óptimo.

No se fija por ahora un porcentaje D50 universal para música ni se adopta automáticamente un objetivo de inteligibilidad de palabra. Tampoco se propone maximizar C80 o D50: una respuesta con muy poca energía tardía puede perder mezcla, reverberancia o envolvimiento útiles.

Para fijar metas definitivas se deberá identificar qué posiciones realmente necesitan corrección, según las mediciones individuales y una referencia predictiva suficientemente contrastada. Los valores globales de orientación no sustituyen esa evaluación ni la condición de ocupación.

## Situación predictiva actual

Se derivó D50 de las respuestas existentes de las 40 corridas localizadas, sin volver a ejecutar SPPS. Se generaron 840 registros C80/D50. La referencia remallada con 150.000 partículas y una semilla da estos promedios descriptivos sobre F1/F2–P8/P9:

| Banda | C80 medio | D50 medio |
|---|---:|---:|
| 1 kHz | +0,26 dB | 43,2 % |
| 2 kHz | +0,06 dB | 41,1 % |
| 4 kHz | +0,11 dB | 39,5 % |
| 8 kHz | +5,17 dB | 65,7 % |

Estos datos no muestran una necesidad evidente de aumentar sistemáticamente el C80 medio de P8/P9 a 1–4 kHz. La banda de 8 kHz tiene mayor predominio temprano en esta base: no debe buscarse elevarla automáticamente, ni declararse inadecuada solo por superar una referencia general. Se revisarán las diferencias entre asientos, espectro y materiales antes de definir una corrección.

Los promedios no describen todos los asientos y no constituyen verificación perceptual. La base emplea fuentes omnidireccionales idealizadas; no reproduce la directividad real del parlante del estudio ni del line array. Este supuesto afecta la relación directo/reflexiones y la comparación absoluta de claridad, especialmente a frecuencias altas. Los materiales efectivos de 8 kHz también requieren cautela.

## Método de selección actualizado

1. Revisar C80 y D50 de referencia por fuente, receptor y banda, distinguiendo P8/P9, receptores virtuales y zonas inferiores. Separar resultados predictivos de medidos.
2. Identificar posiciones o bandas fuera del balance buscado y formular metas antes de seleccionar variantes. No imponer una subida en todos los puntos.
3. Revaluar R, C, RC y D con los nuevos indicadores; calcular diferencias de D50 en puntos porcentuales. El cambio de objetivo no altera la absorción ni justifica recalibrar la base para favorecer una variante.
4. Priorizar alternativas que acerquen posiciones deficientes al balance definido y reduzcan diferencias espaciales, conservando decaimiento y energía útil en las otras zonas. Una mayor uniformidad no basta si todos los asientos empeoran.
5. Repetir las alternativas pertinentes con 600.000 partículas y tres semillas. Antes de ejecutar se revisará la prioridad previa de C/RC según estos objetivos; no se traslada automáticamente un ranking de máximos al de claridad musical.
6. Confirmar las finalistas con 4,8 millones por fuente, banda y semilla, y propiedades físicas justificadas. Mantener los ecogramas como control, sin exigir demostrar eliminación de flutter para avanzar.

Un aumento de claridad por absorción puede ser compatible con el objetivo, pero debe compararse con la preferencia por mínima absorción adicional y la conservación musical. Un difusor puede redistribuir energía sin aumentar C80/D50 de manera general; por ello no se presupone que un QRD sea la solución necesaria para este objetivo actualizado.

## Resultados y archivos

- [C80 y D50 individuales: base y variantes](../../prediccion/estudio-difusion/localizado/resultados/claridad-c80-d50.csv).
- [Promedios descriptivos por zona](../../prediccion/estudio-difusion/localizado/resultados/resumen-claridad-c80-d50.json).
- [Preparación y resultados del ensayo localizado](PASO-3-ENSAYO-DE-PANOS-LOCALIZADOS.md).

Esta reorientación permite evaluar con más claridad lo que buscamos mejorar, pero todavía no acredita que haya una intervención necesaria ni un difusor específico que la consiga.
