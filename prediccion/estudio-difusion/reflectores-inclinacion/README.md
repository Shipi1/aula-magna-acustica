# Orientación y segmentación a igual área frontal

Este ciclo continúa el estudio del frente y la zona media de la platea alta. El objetivo son V01–V04 y V05/V08 con dos fuentes independientes: doce combinaciones. Los posteriores permanecen como controles.

## Comparaciones

Se mantienen 48 m² de área frontal, espesor de 20 mm, absorción α = 0,05 y dispersión 0,05 a 1.000 Hz. La referencia a igual área es la combinación de cuatro reflectores del primer ciclo, situada en `../reflectores/combinado/`.

| Carpeta | Cambio respecto de los cuatro originales |
|---|---|
| `vertical` | Giro vertical alrededor del eje u, con los mismos centros y dimensiones |
| `horizontal` | Giro alrededor de Z global, con los mismos centros y dimensiones |
| `combinada` | Ambos giros, primero horizontal y luego vertical, con los mismos centros y dimensiones |
| `segmentada` | Ocho módulos de 2 × 3 m derivados de la orientación combinada, con posiciones y orientaciones independientes |

Los giros se seleccionan por trayectorias geométricas visibles y tamaño finito; no por los indicadores que todavía se deben calcular. La búsqueda local usa pasos de 5° y hasta tres ciclos por coordenadas. La segmentación conserva área frontal pero cambia bordes, separaciones y tamaño finito; su comparación no aísla únicamente la orientación. SPPS no resuelve la difracción de borde de esos módulos y se registra el límite de esta aproximación.

## Simulación

Una fuente por corrida, solo 1.000 Hz, 600.000 partículas, semillas 20261019/20261020/20261021, 4 s, paso 1 ms, radio de receptor 0,31 m. Se conserva Lw global de 90 dB y el espectro de la base, fuentes omnidireccionales, posiciones originales, materiales efectivos de la sala, 18 °C, humedad 57 %, absorción del aire activada y transmisión de superficies desactivada.

Se ejecutan 24 corridas principales nuevas y ocho pilotos de 20.000 partículas. Se comparan con 18 corridas principales anteriores de sala sin paneles, cuatro originales y seis redistribuidos. Este último tiene 72 m² y sirve como comparador de desempeño, no como control a igual área.

Las energías lineales de las tres semillas se promedian antes de calcular los indicadores. Se informa también cada semilla, reparto temporal, EDT/T30, niveles relativos y controles fuera del objetivo.

## Resultados y modelos

- [Informe de orientación y segmentación](../../../informes/RESULTADOS-INCLINACION-Y-SEGMENTACION-REFLECTORES.md).
- [Geometrías en planta y perfil](resultados/geometrias.png), [objetivo](objetivo.json), [criterios de búsqueda](criterios.json), [variantes](variantes.json) y [detalles de segmentación](segmentacion.json).
- [Medias](resultados/medias.csv), [semillas](resultados/semillas.csv), [resumen por zonas](resultados/resumen-grupos.csv) y [cambios respecto de los cuatro originales](resultados/cambios-respecto-cuatro-originales.csv).
- [Verificación de mallas](resultados/verificacion-mallas.json), [configuraciones y cálculos](resultados/verificacion-calculos.json), [holguras](verificacion-espacial.json) e [inventario de compactación íntegra](resultados/verificacion-compactacion.json).

Cada carpeta de variante conserva `modelo.obj` y `modelo.mtl`, malla JSON, CBIN, MBIN, archivos de mallado y comprobaciones. Las configuraciones, registros y energías lineales se conservan por corrida junto a salidas nativas comprimidas sin pérdidas y verificadas. No se genera un nuevo `.proj` de interfaz ni se cambia el proyecto canónico.

Los procedimientos de preparación, ejecución, análisis, visualización, verificación e informe están en los archivos `*_inclinaciones_reflectores.py` de la carpeta superior; la segmentación usa `preparar_segmentacion_reflectores.py`.
