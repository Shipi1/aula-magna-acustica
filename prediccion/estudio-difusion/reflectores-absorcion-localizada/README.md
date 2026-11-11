# Estudio separado: cuatro reflectores inclinados y absorción localizada

**Inicio: 10 de noviembre de 2026.** La referencia es la configuración de cuatro reflectores con giro combinado del estudio de inclinaciones. Se mantiene fija y se agregan paños absorbentes al muro posterior, sin modificar el proyecto canónico ni los estudios anteriores.

- [Protocolo previo](../../../informes/ESTUDIO-MIXTO-REFLECTORES-Y-ABSORCION-LOCALIZADA.md).
- [Resultados del estudio](../../../informes/RESULTADOS-ESTUDIO-MIXTO-REFLECTORES-ABSORCION.md).

## Condiciones

| Carpeta | Área absorbente | Ubicación | α final a 1.000 Hz |
|---|---:|---|---:|
| `referencia` | 0 m² | Cuatro reflectores, sin absorción nueva | Muro existente |
| `superior_centro_a060` | 9,6 m² | X40,25; Y−4/+4; Z10,6/11,8 | 0,60 |
| `superior_completa_a060` | 19,2 m² | X40,25; Y−8/+8; Z10,6/11,8 | 0,60 |
| `superior_completa_a080` | 19,2 m² | Misma ubicación anterior | 0,80 |
| `media_centro_a060` | 9,6 m² | X40,25; Y−4/+4; Z9,0/10,2 | 0,60 |

Coordenadas globales en metros. Los reflectores conservan 48 m² de área frontal, 20 mm de espesor, α0,05 y dispersión 0,05. Se conserva la dispersión del muro en las zonas absorbentes. Los coeficientes son hipótesis efectivas de una banda; no son un producto seleccionado.

## Referencia y malla

Se subdivide coplanarmente el muro para delimitar áreas, se añaden los mismos cuatro paneles y se recalcula la referencia. Todas las variantes tienen vértices, caras y malla tetraédrica idénticos, salvo etiquetas de material en CBIN. El material 201 recibe el coeficiente del paño; el 301 corresponde a los reflectores. Se verifica la conservación de la sala, la igualdad de los paneles y las áreas tratadas.

La comparación con la referencia anterior se conserva como control de subdivisión/muestreo. Los efectos del tratamiento se calculan respecto de la nueva referencia común.

## Cálculo e indicadores

Treinta corridas principales nuevas y diez pilotos. Cada principal usa 600.000 partículas, una fuente, 1.000 Hz y una de tres semillas: 20261019/20261020/20261021. Duración 4 s, paso 1 ms, radio receptor 0,31 m y las condiciones ambientales/espectrales de la base. Lw es global de 90 dB, no nivel recibido ni potencia por banda. Fuentes omnidireccionales.

Se integran E0–50, E50–80 y E>80; se calculan D50, C80, EDT/T30 y cambios de energía total. Las energías lineales de las tres semillas se promedian antes de calcular los indicadores. El rango exploratorio es D50 45–55 % y C80 −2/+2 dB. No se exige perfección global ni se excluye F2–V08 de los conteos.

Cuando el límite geométrico de cualquier recorrido que toque el plano posterior demuestra que no puede llegar antes de 50 ms, se añade un diagnóstico con energía temprana fijada a la referencia. Se distingue de la respuesta simulada completa; sirve para examinar fluctuaciones de muestreo, no para reemplazar datos ni para imponer una mejoría.

## Archivos de consulta

- [Perfiles y caras](perfiles.json), [diseño del estudio](diseno-estudio.json), [objetivo](objetivo.json) y [paneles fijos](paneles-fijos.json).
- [Paños posteriores](resultados/panos-posteriores.png), [mapa F1](resultados/mapa-D50-F1.png), [mapa F2](resultados/mapa-D50-F2.png), [D50/C80](resultados/D50-C80-conjunto.png), [balance temporal](resultados/balance-ventanas.png) y [curvas energéticas](resultados/energia-V04-V08.png).
- [Respuestas medias](resultados/medias.csv), [semillas](resultados/semillas.csv), [comparaciones](resultados/comparaciones.csv), [zonas](resultados/resumen-zonas.csv) y [cambios por semilla](resultados/cambios-por-semilla.csv).
- [Control de subdivisión](resultados/control-subdivision.csv), [geometría](resultados/verificacion-geometria.json), [cálculos](resultados/verificacion-calculos.json) y [compactación íntegra](resultados/verificacion-compactacion.json).

Los OBJ/MTL permiten inspeccionar sala, paneles y paños coloreados. Se conservan configuraciones, registros, energías lineales y salidas nativas comprimidas sin pérdidas y verificadas. No se genera un nuevo `.proj` de interfaz. Los procedimientos están en los archivos `*_estudio_mixto.py` de la carpeta superior.
