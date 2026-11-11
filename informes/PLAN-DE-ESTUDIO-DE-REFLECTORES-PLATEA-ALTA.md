# Plan de estudio de reflectores orientados para la platea alta

**Proyecto:** Teatro Aula Magna UTFSM.  
**Fecha:** 9 de noviembre de 2026.  
**Estado:** primer ciclo y comparación de siete geometrías de cobertura ejecutados. Consultar la [comparación más reciente](RESULTADOS-GEOMETRIAS-COBERTURA-PLATEA-ALTA.md) y los [resultados iniciales](RESULTADOS-INICIALES-REFLECTORES-PLATEA-ALTA.md).  
**Tipo de estudio:** predicción comparativa con I-Simpa/SPPS y comprobación geométrica, sin nueva medición en terreno.

**Prioridad vigente:** frente y zona media sobre butacas; las posiciones posteriores quedan fuera de la función objetivo y se conservan como controles. La [revisión de alcance y relectura de resultados](PRIORIDAD-FRENTE-Y-ZONA-MEDIA-PLATEA-ALTA.md) prevalece sobre el objetivo espacial más amplio usado en los ciclos anteriores.

## 1. Objetivo y prioridad revisada

Investigar superficies reflectoras que redistribuyan energía hacia llegadas útiles anteriores a 50 ms respecto del sonido directo en la platea alta. La meta de trabajo a 1.000 Hz es **D50 de 48–52 % y C80 no mayor que +2 dB**, manteniendo como referencia de balance el intervalo de proyecto de −2 a +2 dB. Son criterios adoptados para este estudio, no límites normativos universales ni una garantía de calidad musical.

Por decisión del usuario, **F2–P9 pasa a ser un caso secundario de control y no un requisito excluyente que determine por sí solo el diseño**. Los pares primarios serán F1–P8, F1–P9 y F2–P8; F2–P9 se publicará siempre con su variación, aunque no alcance el rango objetivo. No se eliminará del promedio ni de los gráficos sin identificar la selección.

La optimización virtual utiliza **V01–V04 del frente y V05/V08 de la zona media: seis posiciones y doce combinaciones F1/F2**. Se evalúa el frente como prioridad y la zona media por separado, además del resumen conjunto. V09–V12 quedan fuera del objetivo; V10/V11 sobre butacas pasan a control, mientras V09/V12 ya eran controles sobre madera. V06/V07, también sobre madera, se mantienen como controles del tramo medio. P1–P7 siguen controlando platea baja y bajo balcón. El alcance se declara como frente y media, sin trasladar el cumplimiento a toda la platea alta.

## 2. Comprobación previa: distancia y correspondencia F2–P9

El usuario considera que F2–P9 representa la mayor separación fuente–receptor del estudio real. Esa interpretación **no coincide con las coordenadas actualmente usadas por las simulaciones**:

| Par de la base predictiva | Distancia recta tridimensional |
|---|---:|
| F2–P9 | 21,88 m |
| F1–P9 | 23,28 m |
| F1–P8 | 23,40 m |
| F2–P8 | 25,23 m |
| F2–P5 | 28,25 m |

Valores calculados desde las posiciones de los archivos `config.xml` de referencia F1/F2, 1.000 Hz, 600.000 partículas, semilla 20261019 del [estudio de absorción posterior](../prediccion/estudio-difusion/absorcion-posterior/README.md). Son distancias euclidianas: no demuestran línea de visión libre, recorridos reflejados ni exactitud del levantamiento real.

**Primera tarea:** contrastar etiquetas F1/F2 y P8/P9 con planos, fotografías, registros de campo y coordenadas. Si aparece un error documentado, corregirlo y recalcular la referencia afectada antes de optimizar reflectores. Si no se puede resolver, conservar las coordenadas y declarar la incertidumbre. No mover fuentes o receptores para hacer que los indicadores alcancen el objetivo.

Se respeta la prioridad secundaria de F2–P9 como decisión de alcance. No se justificará su menor D50 únicamente por distancia: también intervienen visibilidad, energía directa, reflexión y distribución temporal. Tampoco se afirmará que todo P9 quedó resuelto si F1–P9 mejora y F2–P9 continúa deficitario.

## 3. Antecedentes y mecanismo buscado

El [ensayo de absorción α = 0,80](RESULTADOS-ABSORCION-POSTERIOR-080.md) comparó toda la pared posterior alta y seis distribuciones localizadas. La pared completa mejoró D50, pero superó +2 dB de C80 en tres pares altos; F2–P9 quedó en D50 de 46,94 % y C80 de +1,76 dB. Ninguna de las siete configuraciones cumplió ambos criterios en los cuatro pares.

Ese ensayo se evaluó con una prioridad distinta, que exigía cumplimiento en los cuatro pares. Sus resultados se conservan; la nueva prioridad no convierte retrospectivamente una configuración en solución demostrada.

Ahora se probará un mecanismo diferente: **redistribuir energía hacia 0–50 ms**, conservando suficiente energía posterior para el balance musical, en vez de reducir indiscriminadamente la cola. D50 y C80 usan ventanas diferentes; sus definiciones energéticas se pueden consultar en el [manual de ODEON, sección de parámetros acústicos](https://odeon.dk/download/Version17/OdeonManual.pdf).

Un balance algebraico anterior mostró que añadir solamente energía anterior a 50 ms, conservando todo lo demás, permitiría llevar D50 a 50 % con C80 de aproximadamente +1,3 a +1,5 dB en los cuatro pares de referencia. **No fue una simulación de reflectores:** un panel pasivo redistribuye energía, puede interceptar trayectorias útiles y cambiar llegadas posteriores. El balance solo acredita compatibilidad matemática entre los objetivos.

## 4. Cómo se modificará el modelo 3D

**Sí: se crearán variantes geométricas del modelo y se predecirá sobre ellas.** No basta con cambiar el coeficiente de difusión de una pared para representar un reflector orientado.

Se conservará intacto el [proyecto canónico](../prediccion/G_base_efectiva_espectral_Lw90.proj). Las variantes se guardarán en un estudio independiente, con identificación de paneles, dimensiones, posición, normal, material y condición ensayada. La envolvente original, butacas y tratamientos existentes permanecerán como referencia, salvo los cambios geométricos expresamente necesarios para instalar cada panel.

Se considerarán dos familias:

1. **Facetas rígidas adosadas a superficies existentes.** Su orientación podrá diferir de la pared o cielo originales. Si sustituyen una parte de la envolvente, se recortará esa parte y se cerrarán encuentros, evitando una pared original duplicada detrás de la nueva cara reflectora en el mismo plano.
2. **Paneles rígidos suspendidos o separados de la envolvente.** Se incorporarán sus dimensiones, dos caras y espesor mediante una representación compatible con el motor y el mallado. Se comprobará primero un caso piloto de incidencia por ambas caras y paso de rayos por los bordes. No se asumirá que una lámina abierta es compatible con la cadena actual de tetraedrización.

Si una familia no se puede representar correctamente con la instalación disponible, se documentará la limitación y se continuará con la familia compatible. No se sustituirá silenciosamente un panel suspendido por un techo continuo.

Cada variante requiere comprobar orientación de caras, intersecciones, caras duplicadas, cierre de envolvente, calidad de malla y funcionamiento del cálculo. Si los paneles se representan como sólidos, su volumen desplazado se registrará y se distinguirá del volumen acústico útil; no se exigirá igualdad de volumen exacta con la sala vacía de paneles.

## 5. Localización, orientación y dimensiones

Se buscarán primero sectores del **cielo y laterales adelantados o intermedios**, con visión geométrica desde la fuente y hacia la platea alta. Son zonas candidatas, no ubicaciones ya seleccionadas. La pared posterior ensayada no puede aportar reflexiones anteriores a 50 ms en P8/P9 bajo la geometría actual.

Para cada fuente S, punto de reflexión Q y receptor R se calculará:

`retardo relativo = (|S−Q| + |Q−R| − |S−R|) / c`

Se usará el valor de c coherente con la referencia, aproximadamente 342 m/s. Para llegar antes de 50 ms, el recorrido reflejado debe exceder al directo en menos de unos **17,1 m**. Se buscará margen respecto del corte de 50 ms y se publicará el retardo exacto: no se optimizará una llegada justo en el umbral para obtener un beneficio numérico frágil.

Se comprobarán la ley de reflexión especular, la intersección dentro del panel finito y la ausencia de obstáculos en ambos segmentos. Una trayectoria temporalmente corta no acredita por sí sola que exista una reflexión físicamente orientada hacia el receptor.

La orientación inicial se obtendrá de la geometría especular fuente–panel–zona objetivo; después se probarán pequeñas variaciones de inclinación y ubicación. Se evaluarán F1 y F2 por separado. Un panel orientado a una fuente puntual no necesariamente cubre la otra ni una orquesta distribuida.

Se comenzará con caras **planas**, distribuidas en varios paños cuando sea necesario. No se introducirán superficies cóncavas para concentrar energía. Una curvatura convexa suave o una disposición facetada podrán estudiarse después si la cobertura de los paneles planos resulta estrecha.

Como tamaños iniciales de exploración se podrán usar módulos de **2 × 1,5 m** y **3 × 2 m**, comparando cambios de área y número de módulos de forma separada. Son dimensiones propuestas para investigar, no un predimensionamiento validado ni un mínimo acústico garantizado.

La eficacia de un reflector finito depende también de distancias, incidencia y difracción de borde. No se aceptará como prueba de eficacia que el panel sea simplemente mayor que una longitud de onda. Se hará una estimación independiente de pérdida por tamaño finito siguiendo el método descrito por [Arup/Strutt para superficies reflectoras finitas](https://strutt.arup.com/help/Auditorium_Acoustics/Reflector.htm). La limitación de los métodos geométricos ante paneles finitos está discutida por [Rathsam, Wang, Rindel y Christensen, DAGA 2007](https://digitalcommons.unl.edu/archengfacpub/24/).

No se atribuirán automáticamente a SPPS las correcciones de difracción que incorpora otro programa. Una discrepancia importante entre la estimación de reflector finito y la respuesta geométrica deberá resolverse o quedar explícita antes de recomendar dimensiones.

## 6. Material propuesto e hipótesis acústica

La familia constructiva inicial será **un panel de contrachapado de madera, de cara continua y sellada, rigidizado mediante bastidor**. Se propone por permitir construir facetas con orientación definida y acabado compatible con una sala de uso musical. No se propone madera perforada, ranurada o con cara porosa para esta primera prueba reflectora.

Como hipótesis preliminar de construcción se podrán considerar espesores de **18–21 mm**, sujetos a tamaño libre, rigidización y revisión del montaje. Ese espesor no acredita por sí solo rigidez acústica, respuesta a 500 Hz, aislamiento o resistencia de una suspensión. No se ha definido todavía producto, masa superficial ni sistema de anclaje.

En el primer cálculo se separará material físico e hipótesis del motor:

| Propiedad | Hipótesis inicial de sensibilidad | Qué significa |
|---|---|---|
| Absorción a 1.000 Hz | α = 0,05; contrastar 0,02 y 0,10 | Valores de ensayo de una cara muy reflectante; no datos certificados del contrachapado elegido |
| Dispersión a 1.000 Hz | s = 0,05; contrastar 0 y 0,10 si la alternativa resulta favorable | Comprobar dependencia del resultado respecto de una reflexión casi especular |
| Ley | Especular para s = 0; ley disponible del motor para la fracción dispersa cuando s > 0 | Mantener separada la orientación geométrica del reparto disperso |
| Transmisión | Panel opaco en la primera hipótesis | Simplificación que requiere revisar masa, rigidez, montaje y banda inferior |

Estos intervalos **no son propiedades atribuidas a un producto**. Se ensayará primero la geometría con la hipótesis nominal; las sensibilidades se reservarán a las candidatas para evitar multiplicar indiscriminadamente todas las combinaciones.

Antes de recomendar un panel constructivo se buscarán datos de absorción por banda y montaje, y se revisará si su masa/rigidez permiten la aproximación opaca. No se copiarán los coeficientes del muro efectivo calibrado al reflector. Tampoco se extenderá α = 0,05 a todo el espectro y se presentará esa extensión como dato medido.

## 7. Secuencia de estudio

| Paso | Trabajo | Resultado revisable y condición de avance |
|---|---|---|
| 0. Referencia | Comprobar etiquetas, posiciones, distancia y condiciones de fuente; contrastar nueva referencia si se corrige algo | Coordenadas y alcance aceptados; F2–P9 identificado como control secundario |
| 1. Búsqueda geométrica | Localizar planos candidatos, retardos, visibilidad y cobertura para F1/F2 y toda la zona alta | Plano de candidatos, normales y trayectorias; descarte de ubicaciones inviables |
| 2. Variantes 3D | Introducir paneles planos y probar dimensiones, orientaciones y compatibilidad de mallado | Geometrías verificadas y piloto funcional; todavía sin declarar eficacia acústica |
| 3. Exploración a 1 kHz | Comparar referencia, cada familia reflectora sola y variaciones controladas | Magnitud, distribución espacial y reparto temporal; preselección razonada |
| 4. Confirmación | Repetir candidatas con tres semillas y resolución suficiente para distinguir el rango objetivo | Estabilidad del resultado y sensibilidad a orientación y material |
| 5. Espectro y combinación | Revisar 500 Hz y 1, 2, 4, 8 kHz; solo después valorar absorción posterior limitada | Balance por banda y comparación de reflector solo, absorción sola y combinación |
| 6. Propuesta | Elegir una candidata o concluir insuficiencia | Plano, material supuesto, incertidumbre y mejoras/perjuicios por zona |

No se iniciarán muchas variantes sin completar la comprobación de posiciones y la búsqueda geométrica. La franja posterior de 19,2 m² constituye un antecedente para una eventual combinación, no una cantidad de absorción fijada de antemano.

## 8. Condiciones y precisión de las predicciones

Se conservarán las condiciones de la referencia: F1/F2 independientes, Lw global 90 dB y espectro actual, 21 receptores, posiciones y alturas documentadas, 4 s, paso 1 ms, radio receptor 0,31 m y ambiente supuesto de 18 °C y 57 % HR. Las fuentes seguirán siendo omnidireccionales idealizadas mientras no exista una directividad real documentada. No se presentará el resultado como predicción de un line array concreto.

La referencia se calculará mediante la misma cadena de preparación y validación que las variantes. Al incorporar obstáculos internos puede cambiar la malla: se comprobará que el procesamiento de la base no introduce por sí solo cambios importantes respecto de la referencia anterior. No se confundirá un cambio de mallado o de fuente con un beneficio del reflector.

Se podrá usar una exploración de 150.000 partículas para comprobar funcionamiento y efectos grandes, sin decidir cumplimiento por diferencias pequeñas. La comparación de candidatas partirá de **600.000 partículas × tres semillas** (20261019, 20261020, 20261021) tanto en variante como en su referencia compatible. Se promediarán energías lineales antes de recalcular indicadores.

Si la variación entre realizaciones impide distinguir una mejora o el rango de ±2 puntos de D50, se aumentará la resolución por etapas, hasta contrastar **4,8 millones de partículas por semilla** si hace falta y resulta viable. Ese número no garantiza convergencia: se compararán niveles de resolución y estabilidad de efectos. No se declarará cumplimiento por un promedio aislado que cruce el umbral dentro de una dispersión amplia.

Los controles anteriores que fijaban la energía previa a 50 ms **no pueden aplicarse automáticamente a los reflectores nuevos**: precisamente se busca modificar esa energía. Se analizarán las respuestas completas de cada geometría y se distinguirá efecto físico de fluctuación mediante repetición, inspección temporal y geometría.

## 9. Indicadores y decisión

Se evaluarán D50, C80 y energías 0–20, 20–50, 50–80, 80–300 y 300–1.000 ms, además de energía total, EDT, T20/T30 y calidad de sus ajustes. Los ecogramas servirán para detectar si el beneficio procede de una llegada útil o de concentrar una reflexión dominante. Se conservarán resultados por fuente y receptor; no se sumarán fuentes para fabricar un caso promedio.

Una candidata favorable deberá:

- Acercar los tres pares primarios al rango D50 de 48–52 % manteniendo C80 ≤ +2 dB, con atención al límite inferior de balance de −2 dB.
- Mostrar una mejora distribuida en los virtuales altos; informar número y ubicación de receptores beneficiados y perjudicados, no solo su media.
- Mantener F2–P9 como control visible. No exige alcanzar la misma meta, pero cualquier empeoramiento importante o nueva reflexión concentrada deberá discutirse; su condición secundaria no autoriza ignorar perjuicios.
- Conservar un balance razonable de nivel, EDT y T30 en platea alta y zonas inferiores. Se señalarán cambios de magnitud comparable o superior a 2 puntos de D50, 1 dB de C80/nivel o 5 % de T30 para revisión, sin presentarlos como límites perceptuales universales ni como cambios físicos confirmados si domina el muestreo.
- Mantener la conclusión frente a pequeñas variaciones de orientación y propiedades del panel. No se elegirá una solución cuyo beneficio dependa de una dirección puntual o un coeficiente ideal exacto.

Si no se cumple, el informe podrá concluir mejora parcial o insuficiencia. No se forzará el objetivo modificando las propiedades efectivas de la sala para cada tratamiento.

## 10. Entregables y siguiente acción concreta

Se entregarán un plano de ubicación y cobertura, vistas 3D con dimensiones y orientaciones, descripción del panel supuesto, geometrías nativas y configuraciones de cálculo, curvas energéticas y gráficos comparativos por fuente/receptor, y un informe con límites y decisión. La exportación de una variante a un proyecto `.proj` revisable en la interfaz se comprobará antes de presentarla como lista para abrir; generar solo una malla o un archivo de motor no equivale a ese proyecto.

**La acción inmediata es comprobar la correspondencia de fuentes/receptores y elaborar el mapa geométrico de candidatos y retardos.** Después se incorporarán al modelo únicamente los paños viables y se iniciarán las predicciones. Este documento no autoriza a afirmar que ya existe un reflector capaz de mantener D50 = 50 % y C80 ≤ +2 dB, ni constituye un diseño estructural o de instalación.

## 11. Avance del primer ciclo

Se verificó la coherencia de etiquetas XY con registros y plano existentes, sin certificar el levantamiento físico. Se conservaron posiciones y alturas. Se prepararon referencia y cuatro geometrías con paneles sólidos de 4 × 3 m y 20 mm: par adelantado, par intermedio, cuatro paneles y tres selectivos. El tamaño se amplió respecto de las primeras dimensiones exploratorias por el filtro conservador de reflector finito; no se atribuye esta necesidad a cualquier ubicación posible.

Se ejecutaron tres pilotos, ocho corridas exploratorias y 30 corridas principales a 1.000 Hz, estas últimas de 600.000 partículas con tres semillas. Cuatro paneles producen D50 de 48,65 %, 52,43 % y 52,42 % en los pares prioritarios, con C80 medio de +1,14, +1,69 y +1,55 dB. No se declara cumplimiento estricto ni estabilidad de todos los umbrales por esos promedios. Solo 5/24 combinaciones virtuales cumplen ambos criterios y aparecen disminuciones en sectores centrales.

**Siguiente acción:** redistribuir cobertura y revisar qué reflexiones útiles se interceptan en los sectores deficitarios. No se ha ejecutado todavía esa optimización espacial, sensibilidad de material, confirmación de mayor resolución, otras bandas ni combinación con absorción posterior. Las geometrías OBJ y archivos nativos permiten inspeccionar lo calculado; no se ha generado un nuevo `.proj` de interfaz. Véase el [informe completo](RESULTADOS-INICIALES-REFLECTORES-PLATEA-ALTA.md).

La siguiente iteración incorporará también las restricciones espaciales de los paneles: holguras con cielo y superficies, visuales, iluminación, escenografía y relación con el sistema sonoro según los datos disponibles. Las cotas iniciales, los hitos y la secuencia de trabajo se reúnen en [Avances y estado del estudio acústico](AVANCES-Y-ESTADO-DEL-ESTUDIO-ACUSTICO.md), documento central de consulta.

## 12. Comparación de siete geometrías de cobertura completada

Se ejecutaron 42 corridas principales nuevas a 1.000 Hz y 14 pilotos. Las variantes mantienen el material y cambian posición, orientación, cantidad y, en los posteriores compactos, relación de aspecto. Se verificaron envolvente, mallado, conservación de los segmentos directos y holguras verticales muestreadas. Se conservan separados los virtuales sobre butacas (16 combinaciones) y sobre madera (8 controles).

Los seis paneles redistribuidos dan el menor error absoluto medio de D50 respecto de 50 % en las butacas virtuales: 4,83 puntos, frente a 7,34 de la referencia y 6,50 de los cuatro anteriores. Los dos posteriores de 6 × 2 m dan más cumplimientos conjuntos, 5/16, pero no cumplen en los tres pares prioritarios. La mezcla con los cuatro anteriores se calculó completa y mostró aumentos excesivos de C80 en algunas posiciones, sin sumar de forma automática las ventajas de sus componentes.

La continuación se centra en examinar las trayectorias que alimentan 50–80 ms en posiciones deficitarias, junto con el reparto 0–50 ms y la cola. En F2–V08, el 21,73 % de la energía de referencia está en esa ventana intermedia; un balance que solo añadiera energía temprana hasta D50 de 50 % llevaría C80 a unos +2,7 dB. Ese diagnóstico orienta la siguiente iteración y no identifica todavía una superficie causal. Los [resultados completos](RESULTADOS-GEOMETRIAS-COBERTURA-PLATEA-ALTA.md) conservan las geometrías, mapas, controles y valores individuales.

## 13. Alcance revisado: frente y media

Por decisión del usuario se retiran las posiciones posteriores de la función objetivo. Sus indicadores permanecen en el registro como controles y no se les exige alcanzar D50 de 48–52 % y C80 ≤ +2 dB para seleccionar una geometría. Esta decisión no presupone que la proximidad al muro produzca siempre un C80 mayor; se distingue el alcance elegido de esa explicación física.

## 14. Ensayo dirigido de retornos laterales

La continuación prueba dos planos laterales internos, a Y = ±9 y ±8 m, y combina la segunda distribución con los pares adelantados e intermedios. Se añade un control con la misma geometría y coeficiente de absorción igual al muro efectivo a 1.000 Hz. Se estudia si adelantar un recorrido candidato desde 50–80 ms mejora el balance completo, sin deducir el resultado únicamente del tiempo especular.

El [informe del ensayo frente/media](RESULTADOS-REFLECTORES-LATERALES-FRENTE-MEDIA.md) documenta las 30 corridas principales nuevas, diez pilotos y 18 corridas principales reutilizadas. Este ciclo conserva los doce pares virtuales objetivo y los controles posteriores; sus resultados y decisiones de continuación sustituyen la acción inmediata descrita en las etapas históricas anteriores.

## 15. Comparación de inclinaciones y segmentación a igual área

Se toma como control la combinación original de cuatro reflectores de 4 × 3 m, 48 m² en total. Se comparan giros verticales, horizontales y combinados, manteniendo centros, dimensiones y material; los giros se seleccionan geométricamente en pasos de 5°, sin usar todavía los indicadores resultantes. Después se compara una variante de ocho módulos de 2 × 3 m derivados de la orientación combinada. La segmentación conserva área frontal, pero también cambia tamaño finito, bordes, separaciones y posiciones de los módulos.

Se mantienen como indicadores principales D50 y C80 por posición/fuente, junto con energía 0–50/50–80/>80 ms, nivel relativo, EDT/T30 y rangos entre semillas. La cobertura se evalúa en doce combinaciones delanteras/intermedias y tres pares de campo prioritarios, con controles en las demás zonas. Los [resultados de inclinación y segmentación](RESULTADOS-INCLINACION-Y-SEGMENTACION-REFLECTORES.md) reúnen las 24 corridas principales nuevas, ocho pilotos, parámetros y geometrías de este ciclo.

## 16. Continuación documentada como estudio independiente

Por solicitud del usuario, la combinación de los cuatro paneles inclinados con absorción localizada se documenta aparte: [protocolo del estudio mixto](ESTUDIO-MIXTO-REFLECTORES-Y-ABSORCION-LOCALIZADA.md) y [resultados](RESULTADOS-ESTUDIO-MIXTO-REFLECTORES-ABSORCION.md). Su referencia es la configuración inclinada, no la sala sin tratamiento. El rango exploratorio es D50 de 45–55 % y C80 de −2 a +2 dB. Los estudios anteriores mantienen sus criterios históricos y no se reescriben sus conteos.

El nuevo estudio examina área, absorción y altura de paños posteriores, descompone E0–50/E50–80/E>80 y conserva F2–V08 como caso crítico visible, sin convertir su cumplimiento en requisito único para reconocer una demostración parcial del método.

Se reevaluaron las simulaciones existentes con doce combinaciones virtuales delanteras/intermedias, sin nuevos cálculos. Seis paneles redistribuidos dan D50 medio frontal de 50,70 %, pero el medio queda en 41,65 %. Los dos posteriores de 4 × 3 m dan el menor error frente + media entre los casos ensayados, unos 4,36 puntos. Los resultados y la [definición de objetivo](../prediccion/estudio-difusion/reflectores-cobertura/objetivo-frente-media.json) están en la [revisión de prioridades](PRIORIDAD-FRENTE-Y-ZONA-MEDIA-PLATEA-ALTA.md). El diagnóstico de F2–V08 permanece vigente porque corresponde a una posición de la franja media.
