# Ensayo localizado: paso 3

Bandas del estudio: **1000, 2000, 4000 y 8000 Hz**. Los 16000 Hz no se incluyen.

- `base`: referencia remallada, sin tratamiento.
- `R`: franja superior del fondo, 19,2 m².
- `C`: paño del cielo posterior, 19,2 m².
- `RC`: combinación de ambos, 38,4 m².
- `D`: control desplazado en el fondo, 19,2 m².

Todos los escenarios comparten topología, malla tetraédrica y 21 receptores. La exploración utiliza 150.000 partículas por fuente y banda, semilla 20261019. Es sensibilidad a dispersión Lambert, no un QRD validado.

`modelo-localizado.obj` y `.mtl` muestran los grupos de superficies y colores. No contienen el proyecto acústico completo. Los `.cbin` y `tetramesh.mbin` son entradas nativas para SPPS. Cada carpeta de corrida contiene su configuración XML, resultados energéticos, log y metadatos. El piloto de 20.000 partículas solo comprueba funcionamiento y no entra en las tablas exploratorias.

El informe se encuentra en [Paso 3: ensayo de paños localizados](../../../descartados/informes/PASO-3-ENSAYO-DE-PANOS-LOCALIZADOS.md).

## Continuación de las repeticiones

El ejecutor permite elegir condiciones, fuentes, bandas, partículas y semillas. Para repetir los candidatos que se seleccionen se usarán 600.000 partículas y las semillas 20261019, 20261020 y 20261021. La confirmación final será de 4.800.000 por fuente, banda y semilla. Esta preparación no significa que esas repeticiones se hayan ejecutado.
