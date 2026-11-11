# Estudio independiente: reflectores inclinados y absorción localizada

**Inicio: 10 de noviembre de 2026.** Este documento define el estudio antes de revisar sus resultados. La referencia es la sala con los cuatro paneles de inclinación combinada, no la sala sin tratamiento. Los resultados se documentarán en un informe separado, enlazado al final.

**Estado:** cálculo completado. Se conserva este protocolo previo y se remite al [informe de resultados](RESULTADOS-ESTUDIO-MIXTO-REFLECTORES-ABSORCION.md) para las conclusiones.

## Pregunta y alcance

¿Puede una cantidad limitada de absorción en el muro posterior de la platea alta mejorar el reparto temporal de energía de la configuración con cuatro reflectores, conservando el balance musical y los avances en P8/P9?

Se busca una demostración de mejora parcial, repartida y consistente, sin exigir que todas las posiciones alcancen un valor idéntico. Se conservarán todos los resultados. F2–V08 se identificará como caso crítico y no como requisito único de éxito; tampoco se eliminará de los conteos ni se declarará imposible de mejorar.

Esta etapa estudia paños del **muro posterior**, no absorción en todos los muros de la platea alta. Las conclusiones se limitarán a esas ubicaciones y a 1.000 Hz.

## Referencia fija

Cuatro reflectores de 4 × 3 m, 48 m² de área frontal total, 20 mm de espesor, α = 0,05 y dispersión = 0,05 a 1.000 Hz. Se mantienen las posiciones y orientaciones de la variante `combinada` del [estudio de inclinación](RESULTADOS-INCLINACION-Y-SEGMENTACION-REFLECTORES.md).

El muro posterior se subdivide coplanarmente para delimitar paños. Se genera una malla común para referencia y tratamientos; las variantes solo cambian etiquetas y coeficiente de absorción de las caras elegidas. El mallado tetraédrico es idéntico entre condiciones. La nueva referencia se contrasta también con las simulaciones anteriores para cuantificar diferencias asociadas a esa subdivisión/mallado.

## Condiciones

| Condición | Área absorbente | Coordenadas del paño, en metros globales | α final a 1.000 Hz |
|---|---:|---|---:|
| Referencia | 0 m² | Sin paños nuevos | Material actual del muro |
| Superior central | 9,6 m² | X = 40,25; Y = −4 a +4; Z = 10,6 a 11,8 | 0,60 |
| Superior extendido | 19,2 m² | X = 40,25; Y = −8 a +8; Z = 10,6 a 11,8 | 0,60 |
| Superior extendido, mayor absorción | 19,2 m² | Misma ubicación anterior | 0,80 |
| Medio central | 9,6 m² | X = 40,25; Y = −4 a +4; Z = 9,0 a 10,2 | 0,60 |

Las dos áreas superiores permiten estudiar el efecto de cobertura con el mismo coeficiente. El paño superior extendido compara α = 0,60/0,80 a igual geometría. Los dos paños centrales comparan altura con igual área y coeficiente. La dispersión y la ley de reflexión se mantienen como en el muro original. Los coeficientes son hipótesis efectivas, no un producto seleccionado ni un espectro extrapolado.

## Método de predicción

Una fuente por corrida, 1.000 Hz, Lw global de 90 dB con el espectro original, fuentes omnidireccionales, 600.000 partículas y semillas 20261019/20261020/20261021. Duración 4 s, paso 1 ms, radio receptor 0,31 m, 18 °C, humedad 57 %, velocidad 342 m/s, absorción del aire activada y transmisión de superficies desactivada.

Se ejecutarán diez pilotos de 20.000 partículas y treinta corridas principales nuevas: cinco condiciones, dos fuentes y tres semillas. Se promedian las energías lineales antes de calcular los indicadores. Los rangos entre semillas son descriptivos, no intervalos de confianza.

Se conserva el proyecto canónico y los estudios anteriores. Esta etapa no reproduce la directividad del line array ni representa todavía un producto absorbente en todas las bandas.

## Indicadores y criterios

Se informarán por separado E0–50, E50–80 y E>80, referidas al arribo directo; también energía total, D50, C80, EDT y T30. Las diferencias energéticas se expresarán en dB y las diferencias de D50 en puntos porcentuales.

El rango exploratorio será **D50 de 45–55 % y C80 de −2 a +2 dB**, conservando 50 % como referencia. Es un criterio de este proyecto, no un óptimo universal de música orquestal. No se ampliará después de ver los resultados para incluir una variante.

La comparación principal usa V01–V04 y V05/V08 con ambas fuentes: doce combinaciones. Se separarán frente y media. F1–P8, F1–P9 y F2–P8 serán controles prioritarios de conservación de los avances. F2–P9, los posteriores, los puntos sobre madera, platea baja y bajo balcón permanecerán visibles como controles.

Se evaluará la reducción del déficit respecto del rango, además del número de respuestas dentro de ambos límites. Una mejora fuera de rango podrá constituir evidencia parcial; no se convertirá en cumplimiento. Se distinguirá un beneficio en uno o dos puntos de una mejora distribuida. La consistencia se examinará por semilla, sin suponer que usar la misma semilla asegura trayectorias idénticas entre materiales.

## Lectura física

Absorber únicamente energía posterior a 80 ms eleva D50, pero también tiende a elevar C80 si se conserva la energía temprana. El análisis algebraico previo indica que F2–V08 no puede alcanzar 45 % mediante ese mecanismo aislado sin superar C80 de +2 dB. Esto no es un límite para todos los tratamientos: pueden cambiar también E50–80 y E0–50.

Los paños reales no absorben solo después de un tiempo programado; afectan las trayectorias que los alcanzan. El registro de ventanas permite verificar su efecto neto, pero no identifica por sí solo cada pico con una superficie causal. La cercanía de un receptor a un muro no implica siempre mayor C80 ni determina el resultado.

## Entregables

- [Informe de resultados](RESULTADOS-ESTUDIO-MIXTO-REFLECTORES-ABSORCION.md).
- [Carpeta del experimento](../prediccion/estudio-difusion/reflectores-absorcion-localizada/README.md), con configuraciones, energías lineales, geometrías y verificaciones.
- Comparaciones por punto/fuente, mapas D50/C80, reparto temporal, controles por zona y variación entre semillas.
- Decisión sobre la utilidad de la combinación y sus límites, manteniendo F2–V08 explícito.
