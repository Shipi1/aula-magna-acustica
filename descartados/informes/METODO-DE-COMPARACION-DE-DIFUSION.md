# Método de comparación de difusión

> **Documento archivado el 9 de noviembre de 2026.** Se conserva como antecedente de una etapa o estrategia sustituida; no es el protocolo vigente. Ubicación original: `informes/METODO-DE-COMPARACION-DE-DIFUSION.md`. Consultar el [plan actual](../../informes/PLAN-DE-ESTUDIO-D50-C80-Y-TRATAMIENTOS-POR-ZONA.md).


> **Plan vigente — D50 y C80:** el objetivo principal de continuación es estudiar D50 de 55–60 % a 1.000 Hz en P8/P9, con C80 de −2 a +2 dB como referencia conjunta a 500/1.000 Hz y controles en las demás zonas. Son metas de proyecto, no límites normativos. El [nuevo plan de referencia, simulación y revisión local](../../informes/PLAN-DE-ESTUDIO-D50-C80-Y-TRATAMIENTOS-POR-ZONA.md) prevalece sobre la jerarquía y las prioridades de ensayos de este documento. Los resultados históricos no se modifican.


> **Actualización del objetivo — 9 de noviembre de 2026:** se priorizan el balance de claridad musical (C80), D50 como complemento y la uniformidad espacial, conservando la reverberación útil. La eliminación de flutter deja de ser condición de selección; los ecogramas se conservan como control. Esta actualización prevalece sobre los criterios previos relativos a eliminar ecos. Véase [Criterios de claridad musical](CRITERIOS-DE-CLARIDAD-MUSICAL-C80-D50.md).


**Proyecto:** Teatro Aula Magna UTFSM.  
**Fecha:** 21 de octubre de 2026.  
**Estado:** protocolo propuesto; este documento no incorpora nuevas simulaciones ni acredita eficacia de un tratamiento.

## 1. Objetivo y alcance

Evaluar si una intervención localizada en la platea alta reduce la concentración y repetición de retornos molestos, conservando la energía y el soporte musical útiles del recinto.

**Se prioriza dispersar con la menor absorción adicional posible.** La absorción localizada será una alternativa secundaria, que se incorporará solo si la dispersión resulta insuficiente. No se fija una reducción general del tiempo de reverberación como objetivo ni se supone que un mayor C80 sea siempre mejor para música orquestal.

El estudio desarrolla la [propuesta preliminar](informe-propuesta-acustica-refuerzo.md) y el [estudio de QRD y alternativas](ESTUDIO-QRD-Y-ALTERNATIVAS-PLATEA-ALTA.md). La evidencia de partida y sus límites están en el [diagnóstico de platea alta](../../analisis/diagnostico_platea_alta/INFORME.md).

Se distinguirán dos etapas: evaluar en I-Simpa superficies dispersoras equivalentes y justificar después si el QRD concreto puede proporcionar las propiedades y distribución angular requeridas. La primera etapa no valida automáticamente el diseño del panel.

## 2. Situación de referencia

Se conservará una copia de la base predictiva sin tratamiento. Entre base y variantes permanecerán iguales:

- Geometría, materiales fuera de los paños intervenidos y condiciones ambientales.
- Fuentes F1 y F2, calculadas por separado, con Lw global de 90 dB y el mismo espectro. El valor global no se asignará íntegro a cada banda.
- Posiciones y características de P1–P9, incluido su radio de captación.
- Duración de simulación, paso temporal, método energético, criterios de extinción y demás ajustes de cálculo.

La configuración documentada utiliza duración de 4 s, paso de 1 ms y radio de receptor de aproximadamente 0,31 m. Antes de ejecutar se comprobará que las variantes y la referencia emplean los mismos valores. Véase la [metodología de la base predictiva](../../informes/BASE-TEORICA-Y-METODOLOGIA-PREDICCION.md).

Se añadirán receptores virtuales en filas posteriores de la platea alta y próximos a los paños, identificados separadamente de los puntos medidos. Estos permitirán comprobar si la dispersión desplaza concentraciones de energía hacia otros asientos.

## 3. Localización de paños

Se subdividirán las superficies existentes en paños independientes, sin modificar inicialmente la forma del recinto. Cada paño tendrá identificación, límites y área registrados.

| Sector candidato | Pregunta de estudio |
|---|---|
| Laterales superiores | ¿La intervención interrumpe recorridos repetitivos que afectan a la platea alta? |
| Muro posterior alto | ¿Disminuye retornos asociados al recorrido candidato cielo–fondo? |
| Cielo superior | ¿Intercepta un recorrido relevante que no alcanza los paños murales disponibles? |

Primero se estudiará cada ubicación por separado. No se tratará una pared solo por su proximidad al receptor. Algunos rebotes candidatos ocurren fuera del alcance superior, y una intervención que no los intercepte puede ser ineficaz.

## 4. Matriz de comparación y prioridad de conservación de energía

| Variante | Modificación | Función |
|---|---|---|
| B0 | Ninguna | Referencia común |
| D | Variar dispersión en un paño manteniendo su absorción de referencia | Aislar el efecto de redistribuir energía |
| A | Variar absorción localizada manteniendo la dispersión de referencia | Control de comparación; cuantificar el efecto de retirar energía |
| DA | Combinar dispersión y absorción documentadas | Evaluar una alternativa física mixta, solo si hace falta |

La prioridad de desarrollo será D. Las variantes A y DA no representan una decisión de añadir absorción desde el inicio: permiten evaluar cuánto se necesita y si puede evitarse.

En ausencia de datos del QRD, se ensayarán escenarios de dispersión baja, intermedia y alta, con coeficientes explícitos por banda y claramente declarados como supuestos. No se etiquetarán como prestaciones calculadas del panel. Se registrará la ley angular utilizada.

La variante D es un experimento de sensibilidad, no necesariamente un material fabricable. La evaluación final deberá representar tanto la dispersión como la absorción real del producto, incluidas las pérdidas de los pozos. Si falta información se informará un rango, sin asumir absorción nula.

Seleccionada una ubicación, se aumentará progresivamente la superficie tratada conservando las otras variables. Después se estudiarán combinaciones de paños. Se buscará la menor intervención eficaz.

## 5. Identificación de picos y atribución de reflexiones

### 5.1 Qué permiten los resultados disponibles

Los archivos `Sound level.recp` contienen resultados temporales por banda en cada receptor. Los ecogramas por fuente permiten separar F1 de F2. En los cálculos espectrales revisados se empleó un paso de 1 ms, pero esa discretización no implica exactitud física de 1 ms: también influyen el radio receptor, la geometría, el número de partículas y las aproximaciones del método.

La revisión de archivos del 21/10/2026 encontró `nbparticules_rendu=0` en las ocho configuraciones espectrales G de 250, 500, 2.000 y 4.000 Hz para F1/F2; tampoco se encontraron archivos `.pbin` en la carpeta de predicción ni dentro del proyecto principal. No se dispone de una colección guardada de trayectorias para reconstruir retrospectivamente cada llegada.

Un ecograma integra contribuciones que llegan en cada intervalo. **No identifica por sí solo qué pared ni qué secuencia de rebotes originó un pico.** La cola tardía puede sumar numerosas trayectorias.

### 5.2 Procedimiento de atribución

1. Extraer los ecogramas por fuente, receptor y banda, trabajando con energías lineales. No elevar al cuadrado de nuevo un resultado que ya representa energía o presión cuadrática.
2. Expresar los tiempos respecto de la llegada directa, usando el mismo criterio entre base, variantes y mediciones. No confundir tiempo desde la emisión con retardo respecto del directo.
3. Detectar ventanas con concentraciones o secuencias repetitivas que sean estables entre semillas. Registrar banda, receptor, tiempo, ancho de ventana y energía.
4. Calcular recorridos candidatos con la geometría. Para una longitud de recorrido L y distancia directa Ld, el retardo esperado es Δt = (L − Ld)/c. Verificar que los puntos de reflexión pertenecen a los paños y que el recorrido no queda obstruido.
5. Contrastar la coincidencia temporal en distintas fuentes y receptores. Una coincidencia aislada no basta para identificar una superficie.
6. Ejecutar pruebas que modifiquen un solo paño. Una prueba diagnóstica de absorción muy alta puede ayudar a evaluar su influencia, aunque no represente una solución de obra ni el objetivo de baja absorción. Interpretar cambios de energía por ventanas y su estabilidad, no solo diferencias entre picos individuales.
7. Si hace falta, estudiar un registro adicional de trayectorias con las opciones de salida disponibles. Una animación de una muestra de partículas sirve para explorar recorridos, pero no equivale automáticamente a una descomposición completa de la energía recibida por historial de paredes.

Una reducción al modificar un paño indica sensibilidad del resultado a esa superficie dentro del modelo. No prueba que toda la energía desaparecida pertenezca a una reflexión única: el paño puede participar en muchas trayectorias y modificar el campo posterior.

La atribución se clasificará como: coincidencia temporal candidata, recorrido geométricamente válido, influencia respaldada por pruebas controladas o trayectoria identificada cuando exista información suficiente. No se asignarán porcentajes de responsabilidad a una pared sin una descomposición que los sustente.

## 6. Indicadores y comparación espacial

Las bandas prioritarias serán 1, 2, 4 y 8 kHz, manteniendo otras bandas como control del balance espectral. Los 16 kHz quedan solo como antecedente exploratorio, fuera de las siguientes matrices, según el alcance acordado el 9 de noviembre de 2026. Se revisarán:

- Ecogramas y persistencia de concentraciones o secuencias de retornos.
- Energía en 80–300 ms y 300–1.000 ms, con idéntica referencia temporal.
- Energía temprana y nivel integrado, para detectar pérdida de aportes útiles o redistribución perjudicial.
- C80, EDT y T20/T30 como indicadores complementarios.
- Efectos por receptor y fuente en platea alta, piso abierto y bajo balcón.

No se promediarán fuentes antes de revisar sus resultados individuales. Tampoco se presentará el aumento de C80 como demostración suficiente de eliminación de flutter. Las medidas actuales respaldan una diferencia relativa de energía tardía, pero no identifican un par único de superficies causante.

## 7. Convergencia y criterio de decisión

La exploración inicial podrá utilizar menos partículas, manteniendo condiciones comparables. La base y alternativas finalistas se recalcularán con **4.800.000 partículas por fuente y banda**, con las semillas **20261019, 20261020 y 20261021**. Se mantendrá la ejecución por fuente y banda conforme al protocolo documentado.

Se obtendrán respuestas medias a partir de energías lineales, además de informar la variación entre ejecuciones. La comparación no se basará en promediar directamente niveles en dB. Se aplicará el mismo estimador a base y variantes.

La reducción buscada deberá superar la variación entre semillas y conservarse ante supuestos razonables de material y ubicación. Si es comparable con la variación numérica, se declarará inconclusa. La convergencia de RT o C80 no garantiza por sí sola la estabilidad de picos de 1 ms: las ventanas temporales relevantes también deberán comprobarse.

Se preferirá una alternativa que reduzca retornos problemáticos sin generar otros, conserve energía temprana y balance musical, limite los cambios en las zonas inferiores y necesite poca absorción adicional. Los umbrales de aceptación se definirán antes de seleccionar la alternativa final; no se ajustarán retrospectivamente para favorecer un resultado.

## 8. Relación con el QRD físico

SPPS utiliza acústica geométrica y energética. El coeficiente de dispersión no equivale al índice de uniformidad de difusión, y una ley Lambert no reproduce la distribución principalmente horizontal de un QRD unidimensional.

Dibujar los pozos como pequeñas caras rígidas no representa automáticamente las interferencias de fase que generan la respuesta del QRD. Para justificar el panel se requerirán ensayos o modelación ondulatoria local, con respuesta por frecuencia, incidencia, montaje y disposición del conjunto. Esa información permitirá valorar la representación equivalente y sus limitaciones en I-Simpa.

El estudio inicial podrá concluir que una ubicación se beneficia de dispersión bajo ciertos supuestos. La atribución de esa mejora al QRD concreto requerirá el paso adicional de caracterización. No se garantiza eficacia por introducir un coeficiente alto de dispersión.

## 9. Entregables previstos

Registro de variantes y paños; propiedades y supuestos por banda; gráficos temporales base–tratamiento; indicadores por fuente, receptor y banda; variación entre semillas; tabla de recorridos candidatos y evidencia de atribución; recomendación de ubicación, superficie y absorción adicional mínima, con límites de interpretación.

## 10. Referencias técnicas

- [I-Simpa: configuración y resultados de SPPS](https://i-simpa-wiki.readthedocs.io/fr/latest/code_configuration_SPPS.html). Describe los ecogramas por fuente, salidas temporales y opciones de partículas.
- [I-Simpa: modelación física de SPPS](https://i-simpa-wiki.readthedocs.io/fr/latest/code_SPPS_modelling.html). Describe captación por receptores y diferencia entre dispersión y difusión.
- [COMSOL: Schroeder Diffuser in 2D](https://doc.comsol.com/6.3/doc/com.comsol.help.models.aco.diffuser_schroeder_2d/diffuser_schroeder_2d.html). Referencia para caracterización ondulatoria local y efecto de la respuesta angular.
