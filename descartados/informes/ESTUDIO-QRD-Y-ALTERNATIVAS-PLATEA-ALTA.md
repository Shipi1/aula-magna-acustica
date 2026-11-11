# QRD y alternativas para la platea alta del Aula Magna

> **Documento archivado el 9 de noviembre de 2026.** Se conserva como antecedente de una etapa o estrategia sustituida; no es el protocolo vigente. Ubicación original: `informes/ESTUDIO-QRD-Y-ALTERNATIVAS-PLATEA-ALTA.md`. Consultar el [plan actual](../../informes/PLAN-DE-ESTUDIO-D50-C80-Y-TRATAMIENTOS-POR-ZONA.md).


**Fecha:** 21 de octubre de 2026.  
**Alcance:** investigación y predimensionamiento de alternativas; no es un diseño validado ni un plano de fabricación. No se ejecutaron simulaciones nuevas en este estudio.

## 1. Problema y criterio de selección

Este estudio desarrolla la [propuesta preliminar](informe-propuesta-acustica-refuerzo.md) y el [diagnóstico de la platea alta](../../analisis/diagnostico_platea_alta/INFORME.md).

En las octavas de 1, 2 y 4 kHz, la proporción media de energía posterior a 80 ms alcanza 46,0 % con parlante y 49,3 % con globo en P8/P9, frente a 25,2 % y 41,2 % en el piso abierto. Son diferencias relativas, sin calibración de SPL. La evidencia no demuestra que toda la cola sea más intensa en términos absolutos arriba ni identifica un par único de paredes responsable de flutter. P8/P9 tampoco representan todas las filas elevadas.

El objetivo será debilitar retornos concentrados y repetitivos, conservando las reflexiones musicales útiles y el carácter reverberante del conjunto. La banda inicial de estudio será 1–4 kHz; 8 kHz se mantiene como extensión por verificar. C80 será un indicador complementario: no diagnostica por sí solo flutter ni separa el directo de las reflexiones tempranas.

## 2. Qué aportaría un QRD

Un QRD emplea pozos rígidos de profundidades distintas para producir diferencias de fase y redistribuir la reflexión. Puede interrumpir una secuencia especular sin absorber gran parte de su energía. No garantiza reducir la energía tardía integrada ni aumentar C80 en todos los asientos. [COMSOL explica y modela este mecanismo](https://doc.comsol.com/6.3/doc/com.comsol.help.models.aco.diffuser_schroeder_2d/diffuser_schroeder_2d.html).

Para el Aula Magna es un candidato coherente cuando interesa conservar energía musical. Si el problema exige reducir la energía que permanece en un recorrido, la absorción localizada puede resultar más directa. La distribución de la absorción importa: absorber superficies ajenas al recorrido puede hacer más perceptible un flutter que antes quedaba enmascarado. Véase [AKUTEK: Echoes and flutter-echoes](https://www.akutek.info/research_files/echoes.htm).

## 3. Predimensionamiento propuesto

### 3.1 Geometría inicial

Se propone comparar un **QRD unidimensional de 13 pozos, frecuencia de diseño de 850 Hz y ancho libre de pozo de 30 mm**, con las ranuras verticales para dispersar principalmente en el plano horizontal.

Las relaciones de diseño son:

\[
r_n=n^2\bmod N,\qquad d_n=\frac{r_n c}{2Nf_0},\qquad n=0,\ldots,N-1.
\]

Se usa c = 343 m/s como valor de cálculo, N = 13 y f₀ = 850 Hz. La ley de profundidades se describe, por ejemplo, en la [investigación de QRD publicada en Ultrasound in Medicine & Biology](https://www.sciencedirect.com/science/article/abs/pii/S0301562906014864); aquí se aplica a dimensiones para sonido audible.

| Pozo, desde n = 0 | Residuo | Profundidad desde el plano frontal (mm) |
|---:|---:|---:|
| 0 | 0 | 0,0 |
| 1 | 1 | 15,5 |
| 2 | 4 | 62,1 |
| 3 | 9 | 139,7 |
| 4 | 3 | 46,6 |
| 5 | 12 | 186,2 |
| 6 | 10 | 155,2 |
| 7 | 10 | 155,2 |
| 8 | 12 | 186,2 |
| 9 | 3 | 46,6 |
| 10 | 9 | 139,7 |
| 11 | 4 | 62,1 |
| 12 | 1 | 15,5 |

El pozo de profundidad cero queda cerrado al ras del frente. Los demás tienen fondo rígido; las profundidades no son alturas de bloques medidas desde la trasera.

| Parámetro | Propuesta para estudiar |
|---|---|
| Ancho libre de cada pozo | 30 mm |
| Separadores y dos laterales | 3 mm, sujetos a rigidez y fabricación |
| Ancho exterior por módulo | 13 × 30 + 14 × 3 = 432 mm |
| Altura modular inicial | 1.200 mm, elección constructiva por verificar |
| Profundidad acústica máxima | 186,2 mm |
| Fondo rígido ilustrativo | 12 mm; proyección total cercana a 200 mm antes de herrajes |
| Material | Contrachapado o sistema rígido equivalente; acabado y soporte por especificar |

La altura, el espesor del fondo y los separadores son propuestas constructivas, no resultados de optimización. Deben comprobarse rigidez, tolerancias, masa, anclajes y reacción al fuego del conjunto. No se debe cubrir la boca de los pozos con una placa ni rellenarlos con absorbente suponiendo que se conservará la misma respuesta.

### 3.2 Banda útil y límites

La condición aproximada de propagación plana dentro del pozo da f ≈ c/(2w), que para w = 30 mm resulta **5.717 Hz**. Es un límite orientativo del modelo de pozo, no una garantía de difusión uniforme hasta esa frecuencia. El tamaño finito, la incidencia y el montaje también importan. La teoría y las limitaciones constructivas se desarrollan en [Acoustic Diffuser Optimization, capítulo 6](https://arqen.com/wp-content/docs/Acoustic-Diffuser-Optimization-Arqen.pdf).

La selección de 850 Hz pretende dar margen bajo el centro de 1 kHz. No acredita toda su octava ni una respuesta continua y uniforme entre 850 y 5.717 Hz. Para extender el estudio hacia 8 kHz, el mismo criterio exige w ≤ 21,4 mm; eso incrementa la dificultad constructiva y hace necesario revisar pérdidas y prestaciones. No priorizaría esa extensión antes de comprobar 1–4 kHz.

Como sensibilidad de profundidad, manteniendo N = 13: f₀ = 700 Hz requiere unos 226 mm máximos; f₀ = 1.000 Hz requiere unos 158 mm. Cambiar profundidad también cambia la respuesta, no solo el volumen del panel.

La ida y vuelta en el pozo más profundo del diseño de 850 Hz añade aproximadamente **1,09 ms**. Por tanto, su mecanismo no consiste en convertir una llegada de 150 ms en una temprana: redistribuye el campo reflejado y puede cambiar los recorridos posteriores.

### 3.3 Conjunto de módulos y distancia a oyentes

Debe evaluarse el paño completo, sus bordes y su distancia a los asientos. No hay una distancia mínima universal que podamos certificar para este módulo sin conocer su respuesta y montaje.

No se propone llenar una pared con copias idénticas sin analizar el conjunto. La repetición puede reforzar lóbulos y dejar direcciones poco cubiertas; se compararán agrupaciones limitadas y, si procede, modulaciones calculadas. Tampoco se garantiza una mejora por alternar módulos al azar. El [ejemplo de COMSOL](https://doc.comsol.com/6.3/doc/com.comsol.help.models.aco.diffuser_schroeder_2d/diffuser_schroeder_2d.html) muestra cómo cambia la respuesta angular con la periodicidad.

## 4. Ubicación en este teatro

**Laterales superiores:** estudiar ranuras verticales en los paños que efectivamente intercepten los recorridos candidatos. Los retornos laterales tempranos pueden aportar soporte musical, por lo que no se tratará todo el lateral cercano por su proximidad a P8/P9.

**Fondo alto:** comparar difusión y solución mixta en el recorrido candidato cielo–muro posterior. El diagnóstico previo no respalda atribuir el problema a una reflexión simple del fondo: esa trayectoria queda bloqueada por las gradas en la geometría nominal.

**Cielo superior:** mantenerlo como alternativa si intercepta un recorrido relevante que los muros disponibles no alcanzan. La orientación del tratamiento se elegirá según ese recorrido, sin trasladar automáticamente las ranuras verticales de los muros al cielo.

Algunos rebotes laterales identificados en el diagnóstico ocurren fuera del sector superior. Si el paño tratado no intercepta el recorrido, añadir más difusores allí no corrige esa limitación. No se fija todavía cantidad ni superficie total.

## 5. Otras soluciones que conviene comparar

| Alternativa | Aporte esperado | Límite y aplicación propuesta |
|---|---|---|
| Absorción porosa localizada | Reduce la energía que continúa por los rebotes interceptados | Paneles de 40–50 mm, directos o con cámara de 30–50 mm, en un extremo del recorrido; comprobar pérdida de energía musical |
| Paneles convexos o policilíndricos rígidos | Redistribuyen reflexiones sin depender de pozos estrechos | Comparar radios, anchuras y orientaciones; una curva decorativa no asegura difusión uniforme |
| Facetas rígidas inclinadas | Desvían una reflexión para romper su recurrencia | Comprobar dónde llega la energía desviada; no crear un retorno concentrado en otra zona |
| Tratamiento híbrido ensayado | Combina absorción y dispersión en un mismo conjunto | Útil si ambas funciones son necesarias; no equivale a un QRD rígido con idéntica conservación de energía |
| Paneles reversibles o absorción regulable | Permiten distintas condiciones de operación | Comparar ambas posiciones y resolver montaje; preferibles si los usos requieren balances diferentes |
| Apoyos y ajuste de cobertura | Mejoran llegada útil en usos amplificados | Complementan el acondicionamiento; no eliminan flutter en conciertos acústicos |

Como referencia de absorción localizada, existe [ensayo de Akusto Wall A/Super G de 40 mm con montaje total de 43 mm](https://www.ecophon.com/globalassets/old-structure/01.ecophon-master/technical-documentation/absorption_iso/akusto-wall/akusto_wall_wall_panel_a_super_g_ods43_octave.pdf/). Sus coeficientes corresponden a ese sistema, no a cualquier fibra de igual espesor.

Como referencia de solución híbrida, el [BAD 2.0 de RPG](https://www.rpgacoustic.com/product/bad-2-0-panel/) combina absorción y dispersión. No se selecciona como producto definitivo ni se transfieren sus prestaciones a un panel casero perforado.

Los resonadores de membrana o Helmholtz orientados a 250–500 Hz no serían mi primera solución a esta persistencia aguda. Su eventual necesidad debe surgir de un problema distinto en esas bandas, sin confundir el ajuste de la base predictiva con un tratamiento que deba instalarse.

## 6. Cómo evaluar las alternativas en I-Simpa

1. Conservar la base predictiva y delimitar los mismos paños disponibles para cada comparación.
2. Separar tres ensayos: difusión equivalente, absorción localizada y combinación. Comparar después curvas o facetas si la geometría ofrece una ventaja.
3. Usar absorción y dispersión por banda documentadas. Si faltan, realizar sensibilidad con valores declarados como hipótesis; no presentarlos como prestaciones calculadas del QRD.
4. Mantener fuentes, receptores, duración, número de partículas y protocolo de semillas constantes entre base y tratamiento. Añadir receptores virtuales junto a los paños y en las filas altas posteriores, diferenciándolos de P1–P9 medidos.
5. Revisar ecogramas por banda, persistencia de secuencias y energía de 80–300 y 300–1.000 ms; complementar con C80, EDT y T20/T30 en las tres zonas.
6. Exigir que los cambios superen la variabilidad entre ejecuciones y persistan ante supuestos razonables de material y ubicación. No fijar retrospectivamente un criterio para favorecer una alternativa.

**Limitación de representación:** SPPS distingue absorción y dispersión; su coeficiente s cuantifica la fracción no especular y no equivale al índice de uniformidad de difusión. Una ley Lambert reparte energía de forma distinta de un QRD unidimensional. Véase la [documentación oficial de SPPS](https://i-simpa-wiki.readthedocs.io/fr/latest/code_SPPS_modelling.html).

Modelar los pozos como pequeñas caras rígidas y lanzar partículas no reproduce por sí solo las interferencias que generan su respuesta. Para validar el módulo se necesitan ensayos o una simulación ondulatoria del panel; después puede trasladarse una caracterización equivalente al estudio del recinto. El modelo ondulatorio local es mucho más acotado que resolver toda la sala con ese método. Esta limitación impide declarar que una mejora con dispersión Lambert demuestra la eficacia específica del QRD calculado.

## 7. Recomendación

Desarrollar en paralelo el QRD de 13 pozos propuesto y una alternativa mixta con absorción puntual. Mantener una alternativa de paneles convexos o facetas cuando resulte más sencillo interceptar el recorrido mediante su geometría. Elegir la menor intervención que reduzca retornos problemáticos sin degradar el soporte musical de las demás zonas.

El QRD queda predimensionado como candidato para investigar; su ubicación final, extensión y prestaciones aún deben demostrarse. Este documento no modifica la geometría ni los materiales de la base predictiva.
