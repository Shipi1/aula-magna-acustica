# Ensayo dirigido a frente y zona media

Continuación del estudio de reflectores con el objetivo revisado: V01–V04 y V05/V08, dos fuentes independientes, doce combinaciones. Los receptores posteriores se conservan como controles. No se cambia el proyecto canónico ni se recalibran los materiales originales de la sala.

## Condiciones calculadas

| Carpeta | Geometría | Área frontal | Material a 1 kHz |
|---|---|---:|---|
| `lateral9` | Dos paneles verticales 6 × 3 m, centros (15,5; ±9; 4,4) m | 36 m² | α = 0,05; dispersión 0,05 |
| `lateral8` | Mismos tamaños, Y = ±8 m | 36 m² | α = 0,05; dispersión 0,05 |
| `lateral8_adel` | Laterales Y±8 y par adelantado del primer ciclo | 60 m² | α = 0,05; dispersión 0,05 |
| `lateral8_inter` | Laterales Y±8 y par intermedio del primer ciclo | 60 m² | α = 0,05; dispersión 0,05 |
| `lateral8_equiv` | Geometría idéntica a Y±8; control de material | 36 m² | α = 0,24794628455412168; dispersión 0,05 |

El espesor es 20 mm; ambas caras y cantos son opacos. El control iguala el coeficiente de absorción del muro efectivo a 1 kHz, no el área de absorción total de la sala. No representa un producto ensayado.

## Método

SPPS de I-Simpa, 1.000 Hz, Lw global 90 dB y espectro original de la base, 600.000 partículas por corrida, semillas 20261019/20261020/20261021, 4 s, paso 1 ms, receptor de radio 0,31 m. Dos fuentes calculadas por separado; 30 corridas principales nuevas y diez pilotos de 20.000 partículas. Se reutilizan 18 corridas principales compatibles de referencia, seis redistribuidos y dos posteriores. Las medias energéticas preceden al cálculo de indicadores.

Se conservan configuraciones, registros, metadatos, resultados energéticos lineales y salidas nativas en ZIP verificado. No se generó un nuevo `.proj` de interfaz. Los OBJ coloreados y mallas nativas corresponden a las variantes realmente calculadas.

## Archivos

- [Informe de resultados](../../../informes/RESULTADOS-REFLECTORES-LATERALES-FRENTE-MEDIA.md).
- [Objetivo](objetivo.json), [perfiles](perfiles.json), [paneles y rutas](variantes.json), [hipótesis geométrica](hipotesis-retorno-lateral.json).
- [Holguras y segmentos directos](verificacion-espacial.json), [verificación de mallas](resultados/verificacion-mallas.json), [verificación de cálculos](resultados/verificacion-calculos.json).
- [Medias](resultados/medias.csv), [semillas](resultados/semillas.csv), [diferencias energéticas](resultados/comparaciones.csv), [resumen por zonas](resultados/resumen-grupos.csv).
- [Geometrías](resultados/geometrias.png), [hipótesis lateral](resultados/hipotesis-retorno.png), [mapa F1](resultados/mapa-D50-F1.png), [mapa F2](resultados/mapa-D50-F2.png), [curvas temporales](resultados/energia-V04-V08.png).

Cada carpeta geométrica incluye `modelo.obj` con `modelo.mtl`, `mesh.cbin`, `tetramesh.mbin`, la malla JSON y comprobaciones geométricas/tetraédricas. Las coordenadas son metros en el sistema global del modelo.

## Preparación y análisis

Los procedimientos están en la carpeta superior: `preparar_frente_media_reflectores.py`, `ejecutar_frente_media_reflectores.py`, `analizar_frente_media_reflectores.py`, `visualizar_frente_media_reflectores.py`, `verificar_frente_media_reflectores.py` e `informar_frente_media_reflectores.py`. La compactación íntegra usa `compactar_reflectores.py --estudio reflectores-frente-media` y conserva un inventario acumulativo de archivos con SHA-256.
