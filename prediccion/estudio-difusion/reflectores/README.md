# Primer ciclo de reflectores orientados

Se generaron variantes geométricas reales con paneles sólidos cerrados de 4 × 3 m y 20 mm, material nominal α = 0,05 y s = 0,05 a 1.000 Hz. Son hipótesis para estudiar redistribución de energía, no propiedades ensayadas de un producto de madera ni especificaciones de montaje.

- `base/`: referencia sin paneles, nueva tetraedrización de la misma envolvente.
- `adelantado/` e `intermedio/`: dos paneles, 24 m² frontales por variante.
- `combinado/`: cuatro paneles, 48 m² frontales.
- `selectivo/`: adelantado del lado de P8 y ambos intermedios, 36 m² frontales.
- `exploracion-3x2/`: búsqueda geométrica inicial conservada, sin simulaciones SPPS de ese tamaño.
- `calculos/`: tres pilotos de 20.000 partículas, ocho corridas de exploración de 150.000 y 30 principales de 600.000. Cada condición principal usa ambas fuentes separadas y tres semillas.
- `resultados/`: energías procesadas, indicadores, diferencias, planos, gráficos, auditorías de entradas y compactación.

Cada geometría contiene CBIN, MBIN, OBJ, descripción de paneles y verificaciones de volumen, cierre y tetraedros. Los OBJ de tratamientos tienen material MTL contiguo para distinguir paneles en ocre; no son proyectos `.proj` preparados para la interfaz de I-Simpa. Los nativos y las configuraciones permiten las corridas documentadas. Los sólidos tienen huecos tetraédricos: no se propaga sonido dentro de la madera idealizada.

Las salidas nativas de las 41 corridas se conservaron sin pérdida en ZIP por carpeta tras verificar integridad y SHA256. Las series lineales, configuraciones, registros y metadatos siguen separados. El registro acumulativo se encuentra en `resultados/verificacion-compactacion.json`.

El [informe](../../../informes/RESULTADOS-INICIALES-REFLECTORES-PLATEA-ALTA.md) explica los resultados. Cuatro paneles acercan los pares prioritarios a la meta, pero solo 5/24 combinaciones virtuales cumplen ambos criterios y hay sectores centrales con disminución de D50. No se selecciona un tratamiento suficiente para toda la platea alta. No se calcularon otras bandas, sensibilidades de material ni combinación con absorción posterior. La siguiente etapa del [plan](../../../informes/PLAN-DE-ESTUDIO-DE-REFLECTORES-PLATEA-ALTA.md) es redistribuir cobertura.

El proyecto canónico y las mediciones originales no se modificaron. Los scripts de preparación, ejecución, análisis, visualización y generación del informe se conservan en la carpeta superior del estudio.
