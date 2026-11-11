# Plan de localización y validación del tratamiento de la platea alta

> **Documento archivado el 9 de noviembre de 2026.** Se conserva como antecedente de una etapa o estrategia sustituida; no es el protocolo vigente. Ubicación original: `informes/PLAN-DE-LOCALIZACION-Y-VALIDACION-DEL-TRATAMIENTO.md`. Consultar el [plan actual](../../informes/PLAN-DE-ESTUDIO-D50-C80-Y-TRATAMIENTOS-POR-ZONA.md).


> **Plan vigente — D50 y C80:** el objetivo principal de continuación es estudiar D50 de 55–60 % a 1.000 Hz en P8/P9, con C80 de −2 a +2 dB como referencia conjunta a 500/1.000 Hz y controles en las demás zonas. Son metas de proyecto, no límites normativos. El [nuevo plan de referencia, simulación y revisión local](../../informes/PLAN-DE-ESTUDIO-D50-C80-Y-TRATAMIENTOS-POR-ZONA.md) prevalece sobre la jerarquía y las prioridades de ensayos de este documento. Los resultados históricos no se modifican.


> **Actualización del objetivo — 9 de noviembre de 2026:** se priorizan el balance de claridad musical (C80), D50 como complemento y la uniformidad espacial, conservando la reverberación útil. La eliminación de flutter deja de ser condición de selección; los ecogramas se conservan como control. Esta actualización prevalece sobre los criterios previos relativos a eliminar ecos. Véase [Criterios de claridad musical](CRITERIOS-DE-CLARIDAD-MUSICAL-C80-D50.md).


**Proyecto:** Teatro Aula Magna UTFSM.  
**Fecha:** 9 de noviembre de 2026.  
**Estado:** plan para continuar la investigación. Las etapas 1 y 2 resumen trabajo realizado; la etapa 3 ya tiene preparación geométrica y exploración inicial ejecutadas, y conserva repeticiones pendientes. Las etapas 4 y 5 siguen pendientes. Los resultados de continuación se documentan por separado; este plan no constituye una especificación de construcción.

## Objetivo y alcance

Determinar qué sectores de la platea alta conviene intervenir, con qué extensión y mediante qué tipo de superficie, para debilitar retornos concentrados y repetitivos en frecuencias altas. Se prioriza redistribuir la energía con la menor absorción adicional posible, conservando el soporte musical y el balance reverberante del recinto.

El éxito no se definirá solamente por un aumento de C80 o una disminución del tiempo de reverberación. Debe existir una mejora temporal verificable en las posiciones afectadas, sin trasladar el problema a otros asientos. La simulación permitirá evaluar sensibilidad y sustentar una propuesta; sin acceso al teatro, no certificará su resultado perceptual real.

El acondicionamiento se concentra en la platea alta. Los altavoces de apoyo bajo balcón se mantienen como una línea independiente de diseño: no se introducirán en estas comparaciones para evitar confundir cambios del recinto con cambios de refuerzo sonoro.

## Esquema general

| Etapa | Pregunta que resuelve | Producto | Estado |
|---|---|---|---|
| 1. Referencia | ¿Contra qué situación se comparan las intervenciones? | Base identificada, supuestos y reglas de comparación | Realizada como punto de partida; verificar en cada ensayo |
| 2. Exploración | ¿Qué superficies merecen investigarse primero? | Comparación de grandes paños y recorridos candidatos | Realizada; resultados iniciales |
| 3. Localización | ¿Qué sector y qué superficie mínima conviene tratar? | Paños menores, mapa de receptores y selección de ubicaciones | Preparación y exploración inicial realizadas; repetición pendiente |
| 4. Tratamiento físico | ¿Qué panel puede producir la redistribución requerida? | Alternativas de QRD u otras superficies, con propiedades justificadas | Pendiente |
| 5. Confirmación | ¿El beneficio persiste con más resolución y supuestos razonables? | Comparación final, incertidumbre y recomendación condicionada | Pendiente |

La secuencia admite retrocesos: si la caracterización física de la etapa 4 contradice la superficie equivalente favorable de la etapa 3, se revisará la selección antes de confirmar.

## 1. Referencia común

### 1.1 Modelo de partida

Se utilizará el [proyecto base predictivo](../../prediccion/G_base_efectiva_espectral_Lw90.proj), sin tratamiento, y su malla nativa vigente de 2.340 vértices y 4.692 caras. Se conservará una copia independiente y se registrarán versión, huella del archivo, materiales y ajustes utilizados.

La base es una aproximación calibrada del recinto: una coincidencia razonable de decaimiento no garantiza que cada reflexión ni cada material estén representados de forma única. Sus coeficientes efectivos de absorción no deben confundirse con ensayos del revestimiento real.

### 1.2 Condiciones comunes

| Variable | Condición de referencia |
|---|---|
| Fuentes | F1 y F2, en procesos separados y posiciones existentes |
| Potencia | Lw global de 90 dB por fuente, conservando el espectro; no 90 dB por banda |
| Receptores originales | P1–P9, sin desplazar; P8 y P9 pertenecen a platea alta |
| Duración y paso | 4 s y 1 ms |
| Radio de receptor | 0,31 m |
| Ambiente | 18 °C y 57 % de humedad relativa, según configuración existente |
| Motor | SPPS de I-Simpa, método energético; absorción atmosférica activada y transmisión desactivada |
| Extinción | Exponente 5, conservado entre condiciones |
| Semillas | 20261019, 20261020 y 20261021 en las repeticiones |
| Bandas prioritarias | 1, 2, 4 y 8 kHz |

Las alturas de partida proceden de las indicaciones del estudio: fuentes aproximadamente 1 m sobre el escenario y receptores aproximadamente 2 m sobre el piso local. No se reinterpretarán como alturas topográficas medidas con precisión. Esta etapa utiliza las fuentes del estudio, no una simulación validada del line array instalado.

Los receptores virtuales nuevos deberán existir también en la referencia que se vuelva a calcular. No es válido comparar un asiento nuevo con una respuesta histórica de otra posición.

## 2. Evidencia que orienta la localización

La [investigación inicial](RESULTADOS-INICIALES-DISPERSION-PLATEA-ALTA.md) comprende 42 simulaciones: exploración de ambos laterales y fondo alto, sensibilidad de dispersión, repetición intermedia y control separado de absorción.

El fondo alto fue el candidato más prometedor. A 2 kHz, con 600.000 partículas por corrida y tres semillas, la comparación de las respuestas medias de F1/F2–P8/P9 dio aproximadamente:

- Energía de 80–300 ms: **−0,58 dB**.
- C80: **+0,62 dB**.
- Concentración relativa del máximo de 10 ms en la ventana tardía: prácticamente sin cambio medio.

Esto justifica continuar, pero no demuestra eliminación de flutter. El cambio medio del piso abierto fue pequeño; bajo balcón se observaron diferencias de decaimiento que deben revisarse, por lo que no se supone independencia acústica entre zonas.

Los recorridos geométricos candidatos cielo posterior → fondo alto → receptores superiores presentan retardos de aproximadamente 79,5–85,1 ms respecto del directo. Los rebotes en el muro posterior se sitúan cerca de Z = 11,22–11,26 m y Y = −5,85; −4,52; +5,76 y +7,08 m. Los rebotes previos en cielo están cerca de X = 37,5–37,7 m y Z = 12,12 m.

Estas coordenadas permiten proponer paños de prueba. No aportan amplitudes de reflexión ni prueban que esos recorridos sean los responsables dominantes de la molestia. Además, algunos retornos laterales atraviesan superficies ajenas a los paños altos ya estudiados.

Hay otra limitación decisiva: conservar la absorción efectiva del muro al aumentar la dispersión produjo un resultado más favorable que el control exploratorio de baja absorción. Por ello, una superficie equivalente favorable no se transferirá directamente a un QRD rígido de poca absorción.

## 3. Localización y reducción de superficie: siguiente trabajo

### 3.1 Preguntas e hipótesis

Se comprobarán tres hipótesis separadas:

1. Un paño alto del fondo que intercepte los recorridos candidatos conserva parte del beneficio del tratamiento de toda la pared.
2. Intervenir el sector correspondiente del cielo puede modificar esos retornos con igual o menor superficie.
3. Tratar ambos extremos produce un beneficio adicional suficiente para justificar el área adicional.

Una cuarta condición de control verificará si importa la ubicación: se comparará un paño de igual área desplazado respecto de los puntos de rebote. No se presumirá que dicho control carece de influencia sobre otras trayectorias.

### 3.2 Preparación geométrica

Primero se superpondrán los puntos de rebote a la malla vigente y a las gradas. Se comprobarán ejes, unidades, distancias a oyentes, obstáculos y disponibilidad física aparente. Las coordenadas siguientes son **envolventes propuestas para el experimento**, no límites constructivos verificados en terreno.

| Código | Región nominal propuesta | Área nominal |
|---|---|---:|
| R | Fondo: X = 40,25 m; Y entre −8 y +8 m; Z entre 10,6 y 11,8 m | 19,2 m² |
| C | Último cielo horizontal: Z = 12,12 m; X entre 37,0 y 38,2 m; Y entre −8 y +8 m | 19,2 m² |
| R+C | Unión de los dos sectores anteriores | 38,4 m² |
| D | Control desplazado en el fondo, con la misma área efectiva que R | Por definir geométricamente |

El ancho de R abarca los cuatro rebotes posteriores identificados y su altura deja margen alrededor de la cota nominal. C incluye el intervalo longitudinal de los rebotes de cielo; antes de fijarlo se comprobarán también sus coordenadas transversales completas. Si alguno queda fuera, se ajustará el polígono y se igualará de nuevo el área de la comparación R–C.

El control D se situará preferentemente por debajo de R, si existe un paño continuo disponible sin superposición ni obstáculos. Su ubicación definitiva quedará registrada antes de calcular. No se elegirá retrospectivamente según el resultado.

Los triángulos actuales no coinciden con estos límites. Se subdividirán las caras que crucen los bordes, conservando exactamente el plano y la envolvente del recinto; no se usarán solo centroides ni triángulos enteros que cambien inadvertidamente el área. Se verificará cierre, normales, ausencia de solapes y calidad de malla.

Si la subdivisión requiere regenerar la malla de cálculo, la nueva base y todas las variantes se calcularán con esa misma malla. Una comparación previa entre las dos referencias permitirá detectar cambios numéricos introducidos por la remalla.

### 3.3 Cobertura de receptores

Se conservarán P1–P9. Se añadirán inicialmente **doce receptores virtuales en platea alta**: tres filas representativas —frontal, intermedia y posterior— por cuatro posiciones transversales distribuidas entre ambos lados. Sus coordenadas se obtendrán de las superficies transitables del modelo; no se colocarán sobre un plano horizontal único ni dentro de gradas o paredes.

Estos receptores estarán aproximadamente 2 m sobre el piso local, para conservar el criterio del estudio. Se registrará distancia al paño y se revisarán las posiciones cercanas al fondo. Se comprobará que las esferas de captación no intersecten superficies. Si una posición es inviable, se ajustará y documentará antes de ejecutar toda la matriz.

Los virtuales se identificarán como V01–V12, sin presentarlos como mediciones reales. Los controles inferiores seguirán siendo P1, P2, P4 y P7 para piso abierto, y P3, P5 y P6 para bajo balcón.

### 3.4 Matriz de ensayos y recursos

En esta etapa se mantendrá la absorción efectiva de la base y se cambiará únicamente la dispersión del paño seleccionado a **s = 0,60 con ley Lambert**, a 1, 2, 4 y 8 kHz. Este valor mantiene continuidad con el ensayo anterior; no es un óptimo demostrado ni una propiedad del QRD.

| Fase | Condiciones | Resolución | Cantidad de procesos |
|---|---|---|---:|
| Exploración localizada | Base, R, C, R+C y D; F1/F2; 1, 2, 4 y 8 kHz | 150.000 partículas; semilla 20261019 | 40 |
| Repetición intermedia | Base y hasta dos candidatos; F1/F2; 1, 2, 4 y 8 kHz | 600.000 partículas; tres semillas | Hasta 72 |

Cada proceso corresponde a una condición, fuente, banda y semilla. Las 72 corridas intermedias son adicionales a las exploratorias. No se sumarán respuestas de diferentes fuentes para obtener una supuesta respuesta única.

La combinación R+C usa el doble de área nominal; su comparación con R o C mide el beneficio de añadir superficie, no una superioridad a igual área. R frente a C y R frente a D sí permiten comparar localización con igual área efectiva.

Solo después se reducirá o desplazará el paño ganador, por ejemplo dividiéndolo en dos mitades y comparando cada mitad por separado. Se recalcularán sus recorridos y áreas. Estas pruebas adaptativas tendrán una matriz y criterios escritos antes de ejecutarse; no están incluidas en las cantidades de la tabla.

### 3.5 Análisis temporal y espacial

Por cada fuente, banda y receptor se entregarán:

- Ecogramas con una referencia de nivel común base–variante, conservando las series de 1 ms y mostrando suavizados de 5 y 10 ms.
- Energía de 0–20, 0–80, 80–300 y 300–1.000 ms respecto de la llegada directa, además de energía total.
- Máximo móvil de 10 ms entre 80 y 300 ms y su cociente respecto de la energía de esa ventana.
- Inspección de picos recurrentes y sus separaciones temporales. Una posible periodicidad se contrastará con los recorridos y con su sensibilidad al paño; no se atribuirá a una pared por coincidencia temporal aislada.
- C80 y T30; EDT y T20 cuando la respuesta y el rango útil permitan un ajuste fiable, mostrando calidad y tramo de ajuste.
- Mapas de diferencias por posición y resultados individuales, junto con el promedio descriptivo por zona.

Se prestará atención a **60–120 ms**, porque los recorridos candidatos están cerca del límite de 80 ms. Se compararán también máximos móviles dentro de ese intervalo, sin desplazar ventanas para favorecer un resultado. El corte convencional de C80 no debe convertir una llegada de 79,5 ms en una conclusión opuesta a otra de 82,7 ms sin examinar ambas.

Se conservará el procedimiento temporal del estudio inicial: origen basado en distancia/342 m/s, integración fraccional de los intervalos y captura completa del frente directo de radio finito en la energía temprana. Los valores C80 así calculados se identificarán como comparaciones internas; su contraste con mediciones exige revisar el mismo criterio de origen e integración. Las salidas energéticas no se elevarán al cuadrado nuevamente.

Las respuestas de tres semillas se promediarán **en energía lineal**, recalculando después los indicadores. Se mostrarán también diferencias de cada realización. Los rangos entre semillas serán descriptivos, no intervalos de confianza. Usar el mismo número de semilla no garantiza trayectorias idénticas después de modificar las reflexiones.

### 3.6 Reglas para seleccionar una ubicación

Antes de las nuevas simulaciones se adoptan las siguientes reglas de decisión. Son criterios internos del proyecto, no umbrales normativos ni garantías de audibilidad:

1. **Consistencia:** una mejora debe mantener su dirección al repetir semillas y aparecer en varias posiciones altas. Un resultado de una sola fuente o un solo asiento se informará como beneficio localizado.
2. **Concentración temporal:** reducir energía integrada sin reducir el máximo o la recurrencia de retornos no bastará para declarar control de ecos flotantes. C80 será complementario.
3. **Incertidumbre:** cuando la magnitud del efecto sea comparable con la variación entre corridas o cambie de signo, se declarará inconclusa y se aumentará resolución antes de seleccionar.
4. **Conservación musical:** pérdidas de energía temprana, cambios de balance o nuevos máximos en otras posiciones deberán revisarse individualmente. No se compensará un deterioro de un asiento con el promedio favorable de otros.
5. **Extensión:** se preferirá el paño menor si su ventaja o desventaja frente al grande no resulta distinguible con la resolución obtenida; la ausencia de diferencia detectable no se presentará como equivalencia física demostrada.

Como alarmas para revisión, se marcarán aumentos de máximos o pérdidas de energía temprana de aproximadamente 1 dB en cualquier posición y cambios de T30 superiores al 5 % respecto de su referencia. Las diferencias menores también se informarán: estas alarmas no convierten automáticamente lo inferior en aceptable ni sustituyen el análisis de variabilidad. Se fijan ahora para evitar elegir límites a posteriori.

**Salida de la etapa 3:** uno o dos sectores prioritarios con coordenadas y área verificadas, mapas de beneficio y perjuicio, variación entre corridas y una explicación de qué aspecto temporal cambia. Si no aparece una mejora suficientemente clara, la conclusión será revisar las hipótesis de recorrido y ampliar localización; no seleccionar un QRD por anticipado.

## 4. Definición del tratamiento físico

### 4.1 Alternativas que se compararán

La primera candidata seguirá siendo el [QRD preliminar de 13 pozos](ESTUDIO-QRD-Y-ALTERNATIVAS-PLATEA-ALTA.md): frecuencia de diseño de 850 Hz, pozos de 30 mm y profundidad máxima aproximada de 186 mm. Son dimensiones de estudio, todavía no una solución validada para el teatro.

Se comparará su orientación de acuerdo con los planos de incidencia y salida de los recorridos seleccionados. No se trasladará automáticamente la disposición de ranuras verticales de un lateral al fondo alto: el recorrido que incluye el cielo puede necesitar redistribución en otro plano.

También se estudiarán superficies convexas o facetadas rígidas si permiten una redirección mejor controlada. La absorción porosa puntual o una solución híbrida quedarán como alternativas secundarias si la redistribución de baja absorción resulta insuficiente.

### 4.2 Información necesaria

Para cada alternativa se documentarán dimensiones, área cubierta, distancia a oyentes, orientación, montaje, absorción por banda y respuesta angular de dispersión. Debe distinguirse el coeficiente de dispersión de un índice de uniformidad de difusión.

Las propiedades procederán de ensayos del conjunto o de una modelación ondulatoria local suficientemente justificada. Si solo se dispone de intervalos plausibles, se simularán como sensibilidad y se mantendrá la conclusión condicionada a esos supuestos. No se asignará s = 0,60 a un QRD simplemente porque ese valor haya sido favorable en la etapa 3.

Los pozos de un QRD no se validarán dibujando pequeñas caras rígidas y aplicando acústica geométrica: ese procedimiento no reproduce por sí mismo el mecanismo de fase. Una representación Lambert tampoco valida su direccionalidad. Si el motor o la caracterización disponible no permiten representarla de forma adecuada, se declarará el límite y se evitará seleccionar una orientación como si estuviera comprobada.

### 4.3 Absorción efectiva y mínima absorción adicional

Se separarán dos preguntas:

- **Sensibilidad de ubicación:** conservar la absorción calibrada y variar dispersión, como en la etapa 3.
- **Intervención física:** reemplazar las propiedades del área cubierta por las del conjunto panel–muro–montaje que realmente se propone.

La segunda comparación puede cambiar tanto absorción como dispersión, incluso si el panel se concibe como poco absorbente. Se ensayarán valores centrales y límites justificados; no se conservará una absorción efectiva elevada del muro sin explicar qué representa bajo el revestimiento.

Si solo una solución con absorción adicional controla los retornos, se comparará una pequeña fracción absorbente en el sector relevante con la alternativa dispersora. Se documentará el aumento de absorción equivalente por banda y la consecuencia en las tres zonas. No se impondrá absorción generalizada como ajuste de calibración.

**Salida de la etapa 4:** ficha de una o dos alternativas físicamente plausibles, propiedades y procedencia, orientación, superficie y límites de representación. Anclajes, cargas y detalles de instalación requerirán comprobación específica antes de construir.

## 5. Confirmación numérica y recomendación

### 5.1 Protocolo final

Se recalcularán la base y las alternativas finalistas con **4.800.000 partículas por fuente, banda y semilla**, utilizando **20261019, 20261020 y 20261021**. Se mantendrán los ajustes de la etapa 1 y el mismo conjunto ampliado de receptores.

La comparación principal abarcará 1, 2, 4 y 8 kHz. Con base y dos finalistas serían 72 procesos; con una finalista serían 48. Los 16 kHz quedan fuera del protocolo de continuación por decisión del usuario; sus ensayos previos se conservan como antecedente. Se añadirán 250 y 500 Hz como controles del balance, siempre con propiedades justificadas: hasta otros 36 procesos para dos finalistas. Ninguna de estas corridas valida automáticamente difusión útil de un QRD en esas bandas.

Una corrida de 4,8 millones no se considerará convergente solo por su tamaño. Se comparará con la resolución intermedia cuando coincidan configuración y propiedades; si cambia el material físico, se calculará primero un punto intermedio comparable. Se comprobarán estabilidad de energía integrada, máximos temporales y variación entre semillas. Si los picos siguen inestables, la conclusión sobre ellos permanecerá abierta o se ampliará el muestreo.

### 5.2 Robustez y alcance de la conclusión

Además del cálculo nominal, se comprobarán las incertidumbres con mayor efecto: absorción y dispersión del conjunto, posición dentro del paño y cercanía de receptores. Los intervalos se fijarán a partir de la caracterización y las tolerancias disponibles antes de ejecutar esa sensibilidad; no se inventará una precisión de montaje que no conocemos.

Las corridas adicionales de sensibilidad tendrán presupuesto propio. El estudio no sustituirá las fuentes medidas por un line array hipotético sin identificar esa modificación como otra condición de operación.

El contraste con las mediciones servirá para recordar dónde la base representa razonablemente el recinto y dónde mantiene diferencias. No se reajustará la base en paralelo para hacer favorable el tratamiento. Una predicción base–tratamiento robusta respaldará un efecto esperado, no una verificación experimental de una instalación inexistente.

### 5.3 Entregables y cierre

Se entregarán:

1. Plano o vista 3D con paños, coordenadas, áreas y receptores.
2. Registro de variantes, propiedades por banda y ajustes de simulación.
3. Ecogramas y mapas base–tratamiento, con resultados individuales y variabilidad.
4. Tabla de energía temprana, tardía, máximos, concentración temporal, C80 y decaimiento en las tres zonas.
5. Comparación entre alternativas y superficie requerida, incluyendo perjuicios o resultados inconclusos.
6. Recomendación de tratamiento, condicionada por su caracterización física y los límites del modelo.

Solo se afirmará control numérico de una secuencia de retornos si sus indicadores temporales lo respaldan. Si únicamente se reduce la energía tardía integrada, esa será la conclusión. La confirmación perceptual e instalada quedará pendiente de una futura comprobación en el recinto.

## Documentos de referencia del proyecto

- [Base teórica y metodología de predicción](../../informes/BASE-TEORICA-Y-METODOLOGIA-PREDICCION.md).
- [Método de comparación de difusión](METODO-DE-COMPARACION-DE-DIFUSION.md).
- [Resultados iniciales: evidencia de las etapas 1 y 2](RESULTADOS-INICIALES-DISPERSION-PLATEA-ALTA.md).
- [QRD y alternativas: predimensionamiento y referencias técnicas](ESTUDIO-QRD-Y-ALTERNATIVAS-PLATEA-ALTA.md).
- [Recorridos candidatos en la malla vigente](../../prediccion/estudio-difusion/resultados/recorridos-candidatos-malla-vigente.csv).

**Estado operativo actualizado:** se subdividieron los polígonos R, C y D, se incorporaron V01–V12 y se ejecutó la matriz de 40 corridas exploratorias con referencia remallada. La siguiente acción será revisar los resultados y repetir las variantes pertinentes antes de seleccionar. Véase [Paso 3: preparación y exploración localizada](PASO-3-ENSAYO-DE-PANOS-LOCALIZADOS.md).

## Ampliación espectral acordada el 9 de noviembre de 2026

Se incorpora 8 kHz a la localización. Los ensayos iniciales de 16 kHz se conservan como antecedente exploratorio; por decisión posterior del usuario, esa banda no forma parte de las siguientes matrices. La percepción de agudos no fija por sí sola la banda del problema. A 8 kHz existe análisis medido previo; a 16 kHz la comparación requiere procesar y verificar las respuestas originales y el margen sobre ruido. Los valores de materiales de la base en ambas bandas no constituyen caracterización validada. Se mantendrá la absorción atmosférica y se revisarán sus limitaciones en recorridos largos. El QRD preliminar de pozos de 30 mm no tiene eficacia acreditada a 8 kHz; será necesario revisar su diseño si esa banda resulta determinante.

La ampliación inicial de grandes paños se documenta separadamente en [Resultados a 8 y 16 kHz](RESULTADOS-DISPERSION-8-Y-16-KHZ.md). Los ensayos localizados R/C/D ya tienen una primera exploración ejecutada; sus repeticiones y la selección definitiva siguen pendientes.
