# Absorción posterior: etapa de factibilidad

Se calcularon base y absorción ideal α = 1 a 1.000 Hz sobre 112,4666 m² del muro posterior alto, con dispersión de base conservada. Se usaron 21 receptores, F1/F2 separadas y 600.000 partículas con tres semillas: 12 corridas de estudio, más dos pilotos.

La continuación aprobada revisó la meta a D50 de 48–52 % y C80 máximo +2 dB. Se calcularon toda la pared y seis distribuciones locales con α = 0,80 a 1.000 Hz: 42 corridas nuevas, conservando 600.000 partículas y tres semillas por fuente y condición. Los otros coeficientes locales preparados en `escenarios.json` no se calcularon. No hay un producto comercial seleccionado.

El [informe actualizado](../../../informes/RESULTADOS-ABSORCION-POSTERIOR-080.md) y `resultados-a080/` contienen las comparaciones, los rangos de semillas, el control de energía temprana y los efectos en las tres zonas. Ninguna configuración ensayada satisface los dos indicadores en los cuatro pares F1/F2–P8/P9. Las 42 salidas nativas nuevas están archivadas sin pérdida y verificadas; su registro se mantiene separado de la etapa ideal.

El [informe](../../../informes/RESULTADOS-LIMITE-ABSORCION-POSTERIOR.md) explica la mejora media, el caso limitante F2–P9, los controles de muestreo y los efectos en otras zonas. Las salidas nativas están archivadas sin pérdida por corrida; configuración, log, metadatos y energías lineales se conservan aparte.

No se modificaron el proyecto principal ni las mediciones. No se ha generado un nuevo proyecto .proj de interfaz ni se han simulado reflexión orientada o combinaciones.
