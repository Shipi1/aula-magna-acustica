# Plan de estudio de D50, C80 y tratamientos por zona

**Alcance espacial vigente:** por decisión del usuario se optimizan frente y zona media de la platea alta —V01–V04 y V05/V08, doce combinaciones con F1/F2— y las posiciones posteriores quedan fuera del objetivo como controles. Se conservan los pares de campo prioritarios y F2–P9 secundario. La [revisión por franja](PRIORIDAD-FRENTE-Y-ZONA-MEDIA-PLATEA-ALTA.md) prevalece sobre las prioridades más amplias de los ensayos históricos.

**Etapa actual:** se completó el [primer ciclo de reflectores orientados](RESULTADOS-INICIALES-REFLECTORES-PLATEA-ALTA.md), según el [plan específico](PLAN-DE-ESTUDIO-DE-REFLECTORES-PLATEA-ALTA.md). F1–P8, F1–P9 y F2–P8 son prioritarios; F2–P9 pasa a control secundario por decisión del usuario. Los resultados se aproximan a la meta en los puntos prioritarios, pero requieren redistribuir cobertura en los virtuales altos. Las prioridades de fases anteriores se conservan como antecedentes, sin excluir de los controles el resto de la sala.

**Actualización de objetivo:** para la continuación de absorción posterior se adoptó D50 de 48–52 % a 1.000 Hz y C80 máximo +2 dB. La meta anterior de 55–60 % permanece como antecedente de las fases históricas. Se completaron pared completa y seis distribuciones localizadas con α = 0,80: [resultados actuales](RESULTADOS-ABSORCION-POSTERIOR-080.md). Ninguna cumplió ambos criterios en los cuatro pares F1/F2–P8/P9; no hay un tratamiento seleccionado como suficiente.

**Proyecto:** Teatro Aula Magna UTFSM.  
**Fecha:** 9 de noviembre de 2026.  
**Estado:** protocolo vigente; los avances de ejecución se registran al final y los resultados detallados se conservan en el informe actual.  
**Prioridad:** este documento actualiza la jerarquía de objetivos de los planes previos. Los resultados históricos se conservan con sus condiciones originales.

## 1. Propósito y alcance

Evaluar una propuesta teórica que mejore la definición temporal en la platea alta, especialmente P8/P9 a 1.000 Hz, manteniendo claridad musical, reverberación y condiciones de escucha apropiadas en las demás zonas. Se utilizará una base predictiva común para comparar el estado actual y las alternativas de tratamiento.

Se adopta **D50 como indicador principal de intervención a 1.000 Hz**, con **C80 como condición conjunta de balance** y controles de energía recibida, decaimiento y distribución espacial. La eliminación de flutter deja de ser requisito de éxito; los ecogramas se conservan para detectar efectos temporales y retornos perjudiciales.

La base no necesita coincidir exactamente con cada medición. Sí debe conservar una relación razonable con las observaciones, explicitar sus supuestos y producir diferencias estables ante repetición y variaciones plausibles. Una variación cualquiera del indicador no basta para respaldar una propuesta: importa su dirección, magnitud, distribución y robustez.

Se distinguirán dos afirmaciones:

- **Efecto dentro del modelo:** con una fuente, geometría y materiales declarados, una intervención modifica D50/C80 de cierta manera.
- **Prestación esperada del recinto:** el tratamiento físico produciría una mejora semejante en el teatro. Esta segunda afirmación requiere mayor justificación de fuentes, materiales y representatividad; no queda demostrada por la primera.

## 2. Objetivos del proyecto

| Indicador | Objetivo de trabajo | Cómo se evaluará |
|---|---|---|
| D50 a 1.000 Hz en P8/P9 | Explorar acercamiento al **55–60 %** | Valores de cada par F1/F2–P8/P9, media descriptiva y distribución en receptores virtuales |
| C80 a 500 y 1.000 Hz | Referencia de proyecto de **−2 a +2 dB** | Por fuente y receptor; compatibilidad con la meta D50 y límites de la comparación con medidas |
| Otras bandas | Conservar un balance razonable a 2, 4 y 8 kHz | No imponer automáticamente el mismo intervalo de C80 a todas las bandas |
| Reverberación | Conservar el carácter musical actual | Cambios de T30 y EDT por banda y zona respecto de la referencia |
| Zonas inferiores | Evitar perjuicios relevantes | Cambios individuales de claridad, definición, energía temprana, nivel integrado y decaimiento |

**55–60 % y −2 a +2 dB son metas adoptadas para esta investigación, no límites normativos universales de calidad orquestal.** Si resultan incompatibles en algunas posiciones, o exigen sacrificar energía musical, se informará el compromiso y se revisará la solución; no se ajustará artificialmente la base para cumplirlos.

La meta se estudia primero en P8/P9 y se verifica en las posiciones virtuales. Un promedio dentro del intervalo con varios asientos desfavorables no constituye éxito general de la platea alta.

## 3. Valores de partida disponibles

### 3.1 Predicción actual

La referencia localizada, con 150.000 partículas y una semilla, da estos promedios descriptivos sobre F1/F2–P8/P9:

| Banda | C80 | D50 |
|---|---:|---:|
| 1.000 Hz | +0,26 dB | 43,2 % |
| 2.000 Hz | +0,06 dB | 41,1 % |
| 4.000 Hz | +0,11 dB | 39,5 % |
| 8.000 Hz | +5,17 dB | 65,7 % |

Esta referencia usa fuentes omnidireccionales idealizadas y no es la reproducción de la directividad del parlante del estudio. La matriz localizada todavía no incluye 500 Hz y no tiene repetición de tres semillas. Por tanto, estos números son un punto de partida, no una base final declarada convergente.

### 3.2 Mediciones que orientan el objetivo

Los exportes REW, tomando los tercios centrados exactamente en 500 y 1.000 Hz y promediando los cuatro pares altos de cada excitación, dan:

| Banda | Fuente | C80 | D50 |
|---|---|---:|---:|
| 500 Hz | Parlante | +2,40 dB | 47,3 % |
| 500 Hz | Globo | −0,68 dB | 34,7 % |
| 1.000 Hz | Parlante | +0,91 dB | 47,8 % |
| 1.000 Hz | Globo | +0,48 dB | 39,0 % |

Son tercios de octava exportados por REW, no octavas reconstruidas. No deben compararse con promedios globales de todos los puntos ni equipararse automáticamente a otro procesamiento temporal. El barrido y el globo son dos condiciones de excitación, no dos verdades intercambiables sobre la sala. La diferencia de claridad no se atribuye exclusivamente a directividad sin revisar también integración, origen temporal y ruido.

### 3.3 Porcentaje relativo y puntos porcentuales

Desde el D50 predictivo medio de 43,2 %:

- Subir **10 % relativo** llevaría aproximadamente a 47,5 %.
- Subir **10 puntos porcentuales** llevaría a 53,2 %.
- Llegar a **55–60 %** exige aproximadamente **+11,8 a +16,8 puntos porcentuales**.

Desde el valor medido con parlante a 1.000 Hz de aproximadamente 47,8 %, la diferencia hasta la meta sería de unos +7,2 a +12,2 puntos. No se trasladará automáticamente una mejora porcentual del modelo a ese valor medido como si ambas respuestas fueran idénticas.

Las variantes pequeñas ya calculadas no alcanzaron esa magnitud en su promedio P8/P9 a 1.000 Hz: R dio aproximadamente +1,61 puntos, C −1,62, RC −0,21 y D +0,77. Son resultados de una sola semilla, sin certeza de que persistan al repetir. El nuevo objetivo no convierte esos ensayos en una solución suficiente.

## 4. Compatibilidad entre D50 y C80

Se empleará energía integrada con un mismo origen y horizonte:

\[
D_{50}=100\frac{E_{0-50}}{E_{total}},\qquad
D_{80}=100\frac{E_{0-80}}{E_{total}},\qquad
C_{80}=10\log_{10}\frac{D_{80}}{100-D_{80}}.
\]

Como D80 no puede ser menor que D50, **D50 = 55 % exige C80 ≥ +0,87 dB** y **D50 = 60 % exige C80 ≥ +1,76 dB**. Si además se limita C80 a +2 dB, D80 no puede superar aproximadamente 61,3 %.

Por tanto, con D50 = 55 %, la fracción de energía entre 50 y 80 ms puede ser como máximo unos 6,3 puntos porcentuales del total; con D50 = 60 %, solo unos 1,3 puntos. No es imposible cumplir ambas metas, pero el extremo de 60 % deja poco margen. Estos límites se aplican a cada respuesta individual; no se deduce la energía de una respuesta promedio a partir de promedios separados de C80 y D50.

Esto también evita confundir una mejora de C80 causada por energía entre 50 y 80 ms con una mejora de D50: esa energía entra en el numerador de C80, pero queda fuera del de D50.

## 5. Etapa A: establecer una referencia comparable

### A1. Fijar las condiciones

Se conservarán la geometría localizada, sus 21 receptores y los parámetros existentes: F1/F2 por separado; Lw global de 90 dB con el espectro conservado; 4 s; paso de 1 ms; radio 0,31 m; 18 °C y 57 % de humedad; absorción atmosférica activada y transmisión desactivada. Se identificarán versión, materiales y huellas de los archivos.

No se cambiarán materiales ni potencia para hacer que el D50 alcance la meta. Cambiar el nivel global de una fuente lineal no modifica por sí solo estos cocientes energéticos.

### A2. Revisar la comparación con las medidas

Se contrastarán las mismas posiciones y condiciones de emisión, verificando inicio de integración, ancho de banda, horizonte y ruido. Los resultados del parlante serán la referencia empírica para la condición con parlante; los del globo se conservarán como contraste independiente.

Se revisará la disponibilidad de datos de directividad y orientación del parlante. Si existen, se preparará una condición que los represente. Si faltan, se conservará la referencia omnidireccional y se ensayarán hipótesis direccionales explícitas, físicamente plausibles y separadas; no se presentará una directividad ajustada a nueve puntos como identificación única de la fuente real.

La evaluación orquestal acústica y la evaluación de refuerzo sonoro deberán distinguirse. Un parlante único no reproduce por sí solo la distribución y radiación de una orquesta ni del line array.

### A3. Repetir la referencia y añadir 500 Hz

La primera repetición priorizará 500 y 1.000 Hz: **600.000 partículas × tres semillas × dos fuentes × dos bandas = 12 procesos** por condición de emisión. Las semillas serán 20261019, 20261020 y 20261021.

La referencia se ampliará después a 2, 4 y 8 kHz, otros 18 procesos, para un total de 30 por condición de emisión. Si se estudia una segunda directividad, su matriz se contará separadamente. Los 16 kHz quedan fuera del protocolo.

Se promediarán energías lineales por fuente, receptor y banda antes de recalcular indicadores. Se informarán también resultados individuales y variación entre semillas. Una referencia se considerará utilizable para comparar cuando la variación sea suficientemente menor que el efecto que interesa detectar; no por alcanzar un número fijo de partículas.

### A4. Producto de esta etapa

Tabla base de D50/C80 por posición, mapas de distribución, relación con los datos medidos, supuestos de fuente y variabilidad. Si hay desajustes relevantes que condicionen el signo o tamaño de la mejora, se declararán antes de interpretar el tratamiento. No se exige identidad exacta con la realidad, pero tampoco se ignoran diferencias que invaliden el objetivo absoluto de 55–60 %.

## 6. Etapa B: comparar superficies del fondo y laterales

### B1. Localizaciones iniciales

Se mantendrá R, franja alta del fondo de 19,2 m², como referencia de localización ya preparada. Se incorporarán ambos laterales por separado, inicialmente con áreas comparables. Como envolvente geométrica para revisar se propone X = 26–34 m y Z = 8–10,4 m en cada muro Y ≈ ±11,665 m: área nominal de 19,2 m² por lado. Estos laterales **todavía no están delimitados ni verificados**; se comprobarán sobre la malla y se corregirán antes de calcular.

La posición definitiva se apoyará también en recorridos que puedan aportar energía antes de 50 ms. No se elegirá exclusivamente por proximidad a P8/P9. La franja posterior y el cielo ya ensayados interceptan recorridos alrededor de 80 ms respecto del directo: dispersar esas llegadas no garantiza que se conviertan en contribuciones anteriores a 50 ms.

Se compararán las condiciones base, fondo, lateral Y negativo y lateral Y positivo. El cielo C se conservará como alternativa si su respuesta D50 o sus recorridos justifican retomarlo. Las combinaciones de paños se ensayarán después de los casos individuales y se identificarán por su mayor área total.

### B2. Familias de intervención

| Familia | Pregunta | Control necesario |
|---|---|---|
| Dispersión equivalente con absorción fija | ¿Redistribuir la reflexión aumenta D50 en las posiciones objetivo? | Variar s por banda como sensibilidad, sin atribuirlo a un QRD validado |
| Reflexión orientada o superficie facetada/convexa | ¿Puede aportar energía útil antes de 50 ms? | Calcular recorridos, dirección de salida y efectos en otros asientos |
| Absorción localizada limitada | ¿Reducir contribuciones posteriores mejora D50 con pérdida aceptable de energía? | Separar aumento del cociente de conservación de nivel y reverberación |
| Solución mixta | ¿Combinar redistribución y absorción ofrece un compromiso mejor? | Comparación contra cada intervención aislada y área total |

Se prioriza mínima absorción adicional. No se presupone que difusión aumente D50: puede aumentarlo, disminuirlo o apenas cambiarlo según la redistribución. Tampoco un coeficiente Lambert favorable valida la distribución angular de un QRD físico, particularmente a 8 kHz.

### B3. Matriz escalonada

El primer barrido comprenderá base y tres localizaciones individuales, F1/F2 y 500/1.000 Hz: **16 procesos de 150.000 partículas y una semilla** por condición de emisión. Será exploratorio, sin declaración de convergencia.

Las dos alternativas pertinentes, junto con la base, se repetirán a 600.000 partículas y tres semillas en 500/1.000 Hz: **36 procesos**. Se verificará después su balance a 2/4/8 kHz: **54 procesos adicionales** si se mantienen las tres condiciones. Las sensibilidades de material, tamaño, orientación o fuente tendrán matrices adicionales registradas antes de ejecutarse.

Las corridas previas podrán usarse como antecedentes, pero solo se reutilizarán como referencia de una comparación nueva si coinciden malla, receptores, fuente y demás condiciones necesarias. No se compararán directamente una variante remallada y una referencia histórica diferente como si solo cambiara el tratamiento.

## 7. Etapa C: localizar y reducir el tratamiento

Después del barrido por superficies se revisará **cada zona localmente**, para identificar qué área específica conviene tratar y con qué método:

1. Platea alta: subdividir el paño candidato en sectores, comparar mitades o módulos y evaluar variación por asiento, altura y fuente.
2. Platea general: comprobar preservación del balance existente y localizar cualquier efecto secundario de los tratamientos altos. No se prescribe acondicionamiento adicional sin una necesidad identificada.
3. Bajo balcón: comprobar definición, claridad, energía útil y cobertura. Los apoyos electroacústicos se estudiarán en una condición de refuerzo separada; no se incorporarán a una comparación de acondicionamiento como si fueran el mismo mecanismo.

Se dibujarán mapas de beneficio y perjuicio, coordenadas, áreas y distancias a oyentes. Se preferirá la intervención menor que produzca una mejora demostrable bajo el protocolo, sin confundir ausencia de diferencia detectable con equivalencia física probada.

Si ningún paño da el cambio buscado, se revisará ubicación, mecanismo y viabilidad de las metas; no se escogerá automáticamente el de mayor C80 ni se aumentará indefinidamente la dispersión.

## 8. Cómo se decidirá si una propuesta tiene respaldo

Una alternativa será candidata cuando:

- Aumente D50 a 1.000 Hz en las posiciones objetivo de manera consistente, reduciendo su distancia a 55–60 % sin ocultar diferencias entre fuentes o asientos.
- Mantenga C80 dentro del balance adoptado a 500/1.000 Hz, o permita explicar y valorar un compromiso si ambas metas no se cumplen simultáneamente.
- Muestre un efecto distinguible de la variación numérica y conserve su interpretación ante incertidumbres plausibles de fuente y material.
- Evite perjuicios relevantes en las zonas inferiores y conserve el soporte musical, no solo los cocientes de claridad.

Se conservarán como alarmas internas de revisión cambios de aproximadamente 1 dB en energía temprana o nivel integrado, 5 puntos porcentuales en D50 de zonas de control y 5 % en T30; no son límites normativos ni autorizan a ignorar cambios menores. Se examinarán magnitud, signo, posición y variabilidad, no solo medias de zona. Los máximos y ecogramas seguirán como controles de nuevos retornos perjudiciales.

Se integrarán por separado las ventanas 0–20, 20–50, 50–80, 80–300 y 300–1.000 ms, además del total. Eso permitirá distinguir una mejora por aporte temprano de otra obtenida por reducción de energía posterior.

Como orden de magnitud, partiendo de D50 ≈ 43,2 %, si la energía anterior a 50 ms permaneciera constante, alcanzar 55–60 % exigiría reducir la energía total recibida aproximadamente 21–28 %. Es una reducción en ese receptor, no necesariamente absorción global del recinto. Ilustra por qué una mejora de 12–17 puntos no debe suponerse pequeña ni gratuita en nivel o balance.

## 9. Confirmación y tratamiento físico

La base y las alternativas finalistas se confirmarán con **4.800.000 partículas por fuente, banda y semilla**, usando las tres semillas del protocolo y revisando convergencia real de los indicadores. Aumentar el número de partículas no resuelve por sí solo la incertidumbre de fuente, geometría o materiales.

Se definirán después tipo de panel, absorción y dispersión por frecuencia, orientación, montaje y extensión. Un QRD, una superficie facetada o un sistema mixto solo se especificarán cuando su comportamiento físico pueda relacionarse con el equivalente favorable del modelo. La comparación final incluirá sensibilidad a esas propiedades.

Una propuesta podrá respaldarse como mejora teórica condicionada aun sin alcanzar exactamente el valor objetivo, siempre que su efecto y limitaciones estén claros. No se afirmará que el teatro alcanzará D50 = 55–60 % únicamente porque un escenario numérico lo produzca.

## 10. Entregables y siguiente acción

Se prepararán referencia por fuente y zona, inventario de hipótesis, tablas C80/D50, gráficos y mapas base–tratamiento, variación entre semillas, comparación de áreas y una recomendación por sector. El informe distinguirá resultados calculados, supuestos de materiales, metas de proyecto y pendientes de validación.

**Siguiente acción:** repetir la referencia a 500 y 1.000 Hz, revisar la sensibilidad a la fuente y delimitar ambos laterales. Después se realizará el barrido de localizaciones. La selección previa de C/RC por máximos no se traslada automáticamente a este nuevo objetivo de D50.

### Antecedentes y datos de partida

- [Criterios de claridad y definición anteriores](../descartados/informes/CRITERIOS-DE-CLARIDAD-MUSICAL-C80-D50.md).
- [Preparación y ensayos localizados](../descartados/informes/PASO-3-ENSAYO-DE-PANOS-LOCALIZADOS.md).
- [C80/D50 de las respuestas existentes](../prediccion/estudio-difusion/localizado/resultados/claridad-c80-d50.csv).
- [Resumen predictivo por zona](../prediccion/estudio-difusion/localizado/resultados/resumen-claridad-c80-d50.json).
- [Contraste REW de fuentes a 500/1.000 Hz](../prediccion/estudio-difusion/localizado/resultados/contraste-fuentes-REW-500-1000.json).

**Estado al redactar:** metas y protocolo definidos; históricos conservados; nueva repetición de referencia, nuevos paños laterales y matrices de este plan pendientes de ejecución.

## Actualización de ejecución: primera tanda completada

Se prepararon los paños laterales Lneg/Lpos y una nueva malla común para base, fondo y laterales. Se completaron 34 corridas de investigación: 16 exploratorias a 500/1.000 Hz, 12 de referencia a 600.000 partículas con tres semillas y 6 de repetición del fondo a 1.000 Hz. El piloto de funcionamiento se contabiliza aparte.

La referencia repetida de esta tanda da en promedio F1/F2–P8/P9 **D50 = 43,65 % y C80 = +0,49 dB a 1.000 Hz**, y **D50 = 50,10 % y C80 = +1,73 dB a 500 Hz**. Esta referencia sustituye para las nuevas comparaciones la estimación exploratoria anterior de otra discretización; no representa un cambio físico del teatro.

El fondo repetido llega a D50 medio de 44,15 % a 1.000 Hz, aproximadamente +0,50 puntos, con efectos individuales positivos y negativos. No alcanza la meta ni muestra mejora uniforme. Los laterales altos tampoco proporcionan una alternativa suficiente en el barrido inicial. La siguiente prioridad es revisar el mecanismo y la localización de las contribuciones útiles antes de 50 ms, no seleccionar todavía un QRD. Se mantienen pendientes la revisión de fuente, los ensayos más localizados, las bandas de control y la confirmación final.

Véase el [informe de fondo y laterales, con resultados, mapas y limitaciones](../descartados/informes/RESULTADOS-D50-FONDO-Y-LATERALES-PLATEA-ALTA.md).

## Actualización: laterales más bajos y adelantados

Se completaron 46 corridas de estudio y un piloto independiente. Se compararon dos paños de 17,229 m² entre X = 19–27 m y Z = 4,2–6,6 m, cada lado por separado y ambos juntos. Las tres alternativas se repitieron a 1.000 Hz con 600.000 partículas y tres semillas; 500 Hz quedó como control exploratorio de los tratamientos, con referencia repetida.

En P8/P9, D50 medio de referencia es aproximadamente 43,58 % a 1.000 Hz. Los cambios medios son −2,32 puntos con Lneg, −1,13 con Lpos y −3,61 con ambos. No se alcanza la meta 55–60 %. Los cambios medios en platea baja son mucho menores, pero no nulos ni iguales en todas las posiciones. Estos resultados no respaldan aumentar la dispersión en esos paños para elevar D50.

La siguiente línea de investigación deberá conservar las reflexiones tempranas útiles y evaluar reflexión orientada, otra ubicación o una solución mixta justificada. No se selecciona todavía un QRD ni se declara validación instalada. Véase el [informe vigente de laterales bajos y adelantados](RESULTADOS-LATERALES-BAJOS-Y-ADELANTADOS.md). Los ensayos anteriores se mantienen como antecedentes en descartados.
