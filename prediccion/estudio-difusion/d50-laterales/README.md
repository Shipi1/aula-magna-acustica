# Comparación de D50 en fondo y laterales

Esta carpeta es independiente de `localizado/` y conserva su propia referencia remallada. Se utilizan los mismos nueve receptores originales y doce virtuales, con fuentes omnidireccionales idealizadas.

- `R`: fondo alto, 19,20 m².
- `Lneg` y `Lpos`: laterales altos entre X = 26–34 m y Z ≈ 8–10,4 m, 19,20 m² cada uno.
- `base`: sin tratamiento, con la misma geometría de cálculo.

Los materiales tratados mantienen la absorción efectiva del muro y elevan s de aproximadamente 0,05 a 0,60 con ley Lambert. No representan un QRD físico validado. Los archivos C/RC/D también se generan por reutilización de la preparación, pero no forman parte de las corridas acústicas de esta tanda.

Matrices: 16 exploraciones de 150.000 partículas; 12 referencias de 600.000 con tres semillas; 6 repeticiones del fondo a 1.000 Hz, también a 600.000 y tres semillas. El piloto de 20.000 partículas está separado. La matriz inicial de 28 figura en `matriz-tanda-inicial.json`; las seis repeticiones adicionales se identifican en `matriz-repeticion-fondo.json`.

`modelo-panos-d50.obj` y `.mtl` son geometría y colores de revisión, sin propiedades acústicas, fuentes o receptores. Las condiciones completas de cada corrida están en su `config.xml`, con resultados, log y metadatos en la misma carpeta. No se ha creado un proyecto .proj de interfaz.

El [informe](../../../descartados/informes/RESULTADOS-D50-FONDO-Y-LATERALES-PLATEA-ALTA.md) distingue exploración, repetición, incertidumbre y conclusiones.
