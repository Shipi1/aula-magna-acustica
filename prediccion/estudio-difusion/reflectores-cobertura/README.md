# Comparación de geometrías de cobertura

**Alcance posterior revisado:** el usuario priorizó frente y media y retiró los puntos posteriores del objetivo. La [reevaluación por franja](../../../informes/PRIORIDAD-FRENTE-Y-ZONA-MEDIA-PLATEA-ALTA.md) usa las mismas respuestas, sin nuevas simulaciones. `objetivo-frente-media.json` declara los criterios de la próxima iteración. Los puntajes de búsqueda y los resultados originales de este ciclo se conservan con su alcance histórico.

Se compararon siete geometrías nuevas a 1.000 Hz, con el mismo material nominal de reflector (α = 0,05, s = 0,05) y las posiciones originales de fuentes/receptores.

| Carpeta | Geometría | Área frontal |
|---|---|---:|
| cobertura4 | Cuatro paneles 4 × 3 m elegidos por cobertura de rutas | 48 m² |
| equilibrio4 | Cuatro paneles 4 × 3 m con otra orientación central y criterio de profundidad | 48 m² |
| cobertura6 | cobertura4 más dos paneles | 72 m² |
| central5 | Cuatro anteriores más un panel central | 60 m² |
| retornos2 | Dos reflectores posteriores 4 × 3 m | 24 m² |
| retornos_compactos2 | Dos posteriores 6 × 2 m, eje largo horizontal | 24 m² |
| mixta6 | Cuatro anteriores y dos posteriores 6 × 2 m | 72 m² |

Se ejecutaron **42 corridas principales de 600.000 partículas** y **14 pilotos de 20.000**. Cada condición principal utiliza F1/F2 por separado y tres semillas: 20261019, 20261020 y 20261021. Se reutilizan doce corridas del [primer ciclo](../reflectores/README.md): referencia y combinación anterior de cuatro paneles.

Los resultados separan los tres pares prioritarios, F2–P9 como control, dieciséis combinaciones sobre bloques de butacas, ocho sobre madera y las zonas inferiores. Las medias se obtienen promediando primero energía lineal por semilla. No se cambian los puntos para mejorar los conteos.

El [informe](../../../informes/RESULTADOS-GEOMETRIAS-COBERTURA-PLATEA-ALTA.md) contiene tablas, mapas F1/F2, restricciones y diagnóstico temporal. La geometría cobertura6 logra el menor error medio respecto de D50 de 50 % en los virtuales sobre butacas; retornos_compactos2 logra el mayor número de cumplimientos nuevos, 5/16. Ninguna geometría reúne simultáneamente todos los objetivos en toda la zona muestreada.

`variantes.json` conserva posición, normal, dimensiones y rutas de los paneles. Cada carpeta geométrica incluye OBJ/MTL para inspección, CBIN/MBIN para cálculo y verificaciones de volumen/mallado. En `resultados/` quedan energías procesadas, comparaciones, holguras verticales y auditorías.

Las salidas nativas de las 56 corridas nuevas se archivaron sin pérdida y con verificación de CRC/SHA256. Las configuraciones, registros, metadatos y series lineales permanecen separados. La referencia canónica y las mediciones no se modificaron.

La preparación se conserva en los scripts de la carpeta superior: preparar_cobertura_reflectores.py, preparar_retornos_reflectores.py, preparar_retornos_compactos.py y preparar_mixta_reflectores.py, en ese orden. Ejecutar de nuevo una preparación puede regenerar geometrías: los archivos existentes representan las condiciones efectivamente calculadas. Las nuevas corridas usan ejecutar_cobertura_reflectores.py; el análisis y el informe usan analizar_cobertura_reflectores.py e informar_cobertura_reflectores.py.
