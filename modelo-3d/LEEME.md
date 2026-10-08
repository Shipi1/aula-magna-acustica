# Aula Magna UTFSM: base geométrica preliminar para acústica

Modelo creado el 8 de octubre de 2026 a partir de la lámina ARQ-01 (24/09/2025), de su copia marcada y del corte A. No es un levantamiento as-built, un modelo calibrado ni una simulación. Se entrega para revisión y preparación de una futura simulación en un programa aún no elegido.

## Archivos

- `visor.html`: inspección 3D local. Abrir en un navegador; conservar `vendor/three.min.js`. No necesita conexión.
- `aula-magna.dxf`: caras triangulares 3DFACE, familias en capas, unidades de cabecera en metros. Comprobar unidades y convención de normales al importar.
- `aula-magna.obj` y `aula-magna.mtl`: misma geometría, grupos de superficies y colores. El MTL solo define apariencia; **no contiene propiedades acústicas**. OBJ no impone unidades: importar como metros, Z vertical.
- `geometria.json`: vértices, caras, grupos, dimensiones y controles.
- `validacion.json`: controles geométricos y áreas por familia.
- `mediciones-originales.csv`: coordenadas heredadas de `analisis/sala.py`, SIN registrar con el origen arquitectónico de este modelo. No deben importarse como posiciones verificadas.
- `generar.py`: generador editable, usa Python estándar. Ejecutar `py -B modelo-3d/generar.py` desde la raíz para regenerar salidas.

## Sistema de coordenadas

Metros, Z arriba. X crece desde el muro posterior del escenario hacia el fondo de la sala; Y es transversal, con origen en el eje; Z=0 corresponde al nivel +0.00 del plano. Este sistema NO se ha demostrado equivalente al sistema XY heredado del análisis. El visor permite superponer ese XY solo como diagnóstico y lo muestra apagado por defecto.

## Cotas usadas

| Elemento | Valor | Procedencia / confianza |
|---|---:|---|
| Ancho general | 23.33 m | Cota 2333 en la planta |
| Escenario hasta borde central | 11.55 m | Cota 1155 de planta |
| Borde escenario a frente central del balcón | 12.48 m | Cota 1248 de planta |
| Frente central balcón a cierre de platea | 8.52 m | Cota 852 de planta |
| Profundidad gradería inferior | 7.96 m | Cota 796 de planta superior |
| Profundidad gradería superior | 8.26 m | Cota 826 de planta superior |
| Piso posterior / delantero del escenario | +0.50 / +0.14 m | Niveles del plano |
| Inicio / término gradería inferior | +3.80 / +5.54 m | Niveles del corte |
| Término gradería superior | +8.53 m | Nivel del corte |
| Techo global simplificado | +13.32 m | Deducido de +0.50 + 12.82 m en caja escénica |

Los encadenamientos dan frente central del balcón X=24.03, cierre central de platea X=32.55, final inferior X=31.99 y final superior X=40.25 m. Son cotas sobre el eje, no distancias constantes a todo lo ancho de los frentes curvos.

## Simplificaciones que deben revisarse antes de simular

1. **Curvaturas:** aproximación parabólica de los frentes, con flecha 0.90 m en proscenio, 2.80 m en balcón y aproximadamente 1.65–1.75 m en su zona posterior. Son trazados visuales, no radios acotados. Se discretizan en 24 franjas transversales.
2. **Platea:** piso lineal de -0.80 m junto al escenario a +0.00 m al fondo; la cota -0.80 es inferida visualmente del corte. Confirmar pendiente y desniveles.
3. **Balcón:** intradós horizontal a +3.30 m, inferido del corte. Frente desde +3.30 hasta +3.80 m; no incluye antepecho ornamental, baranda ni molduras. Es una simplificación relevante para las reflexiones.
4. **Gradas:** reparto uniforme de alturas en 13 módulos inferiores y 19 superiores, guiado por las numeraciones de planta; debe confirmarse la relación exacta entre filas, huellas y contrahuellas. No modela pasillos ni descansos reales.
5. **Gradería superior:** se extiende provisionalmente al ancho general de 23.33 m. La planta muestra una zona central más estrecha (cota 14.49 m) y circulaciones laterales a otra altura. Esta simplificación afecta volumen y reflexiones; debe sustituirse por la geometría exacta antes de usar resultados cuantitativos.
6. **Cielo:** cierre horizontal único. No reproduce los planos escalonados/acústicos del corte ni el artesonado de las fotografías. La cota superior de caja escénica no equivale a la altura acústica local de toda la sala.
7. **Caja escénica:** simplificada al ancho general, con dos niveles de piso; no reproduce la embocadura, estrechamientos, telones, paneles ni torres laterales. La comunicación escenario-sala queda completamente abierta.
8. **Muros:** cierres continuos simplificados. No se han trazado puertas, corredores, pilares, cabinas ni recintos externos. No se deben usar las áreas por grupo como mediciones reales de materiales.
9. **Butacas:** no se representan asientos individuales. Los grupos `platea` y `gradas` reservan superficies para un futuro tratamiento equivalente; incluyen áreas que luego deberán separarse entre audiencia y pasillos. No se asigna absorción ni dispersión.
10. **Mediciones:** P5 de XY queda más atrás que el cierre central obtenido por cotas; las fuentes también requieren registrar el origen. No se movieron puntos ni muros para forzar concordancia. Revisar las marcas del plano y las notas de terreno. P8/P9 usan Z heredada, no altura recalculada sobre las gradas.

## Cierre y normales

Se modela la frontera del volumen de aire como una sola envolvente con la gradería formando una intrusión conectada al cierre posterior. El corte de visualización no corta la malla exportada.

El generador exige dos caras por arista, orientación consistente, triángulos con área positiva y característica de Euler 2. Exporta normales implícitas hacia el interior. El volumen se obtiene de la malla completa e incluye la caja escénica; no es directamente comparable con los 8.000 m³ del informe, que excluyen esa caja y tienen gran incertidumbre. Los controles topológicos no prueban fidelidad arquitectónica ni sustituyen el chequeo de geometría del simulador.

## Preparación de la simulación

1. Elegir simulador y verificar aceptación de DXF 3DFACE u OBJ; no se afirma compatibilidad nativa con un programa concreto.
2. Corregir las simplificaciones de mayor influencia: cielo, embocadura, gradería superior, curvatura e intradós del balcón.
3. Registrar origen, escala y alturas de fuentes y receptores con el plano y la bitácora.
4. Dividir audiencia/pasillos y asignar coeficientes de absorción por banda y dispersión a partir de fuentes justificadas; definir sala vacía u ocupada.
5. Incorporar directividad y potencia de la fuente. No calibrar C80 del parlante como si fuera una fuente omnidireccional.
6. Verificar fugas, normales y escala dentro del programa elegido. Comparar T30 y EDT por banda y por zona con las mediciones, preservando puntos independientes para validación.

No se entrega un cálculo de T30, claridad, mapas acústicos ni un ajuste a las mediciones: esos pasos requieren completar y validar la geometría y las condiciones acústicas.

Motor del visor: Three.js 0.160.1, licencia MIT. Distribución local en `vendor/`.
