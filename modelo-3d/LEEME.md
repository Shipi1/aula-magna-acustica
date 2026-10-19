# Aula Magna UTFSM · modelo acústico revisado v2

Revisión del 19/10/2026 a partir de plantas, corte A de ARQ-01 y fotografías locales. **Geometría mejorada, todavía no un levantamiento exacto ni un modelo acústico calibrado.**

Abrir [el visor](visor.html). «Perfil del cielo» muestra su sección central con el techo oculto. «Cerrar techo y lateral» restaura las superficies ocultas. Las exportaciones siempre contienen la envolvente completa.

## Comparación y trazabilidad

- [Cambios, cotas, hipótesis y límites](revision/COMPARACION.md).
- [Superposición sobre planta alta](revision/comparacion-planta.png).
- [Sección de la malla sobre el corte A](revision/comparacion-corte.png).
- [Respaldo del modelo anterior](revision/modelo-anterior-v1.zip).
- `validacion.json`: controles del generador, volumen y áreas geométricas.
- `revision/verificacion-exportaciones.json`: comprobación independiente de exportaciones y puntos.

## Archivos para I-Simpa

**Empezar con `aula-magna.3ds`.** Contiene objetos separados por familia: escenario, platea, gradas, antepecho, pilares, embocadura, muros y planos del cielo. `grupos-isimpa.json` relaciona nombres y descripciones. Son categorías geométricas, no materiales acústicos asignados ni superficies definitivas de tratamiento.

`aula-magna.ply` contiene la misma geometría en PLY ASCII estándar, sin grupos. OBJ/MTL y DXF se mantienen para edición e intercambio general. El MTL solo contiene colores.

La [documentación de I-Simpa](https://i-simpa-wiki.readthedocs.io/fr/latest/menu_file.html) enumera 3DS y PLY como formatos de importación. Se comprobaron los archivos exportados, **pero no se ha ejecutado una importación ni un mallado dentro de I-Simpa**.

1. Crear un proyecto vacío e importar `aula-magna.3ds` mediante «Import new scene».
2. Verificar metros: ancho máximo 23,33 m; longitud 40,25 m; cota máxima +13,32 m. Z vertical. No convertir de centímetros.
3. Comprobar grupos, orientación y cierre. Ejecutar la comprobación/mallado recomendada por I-Simpa. Evitar una reconstrucción automática gruesa que borre pilares o balcón.
4. Guardar el proyecto. Esta entrega geométrica no incluye un archivo `.proj`.
5. Revisar las hipótesis importantes de la comparación y generar variantes de sensibilidad donde falte información.
6. Registrar fuentes/receptores y asignar absorción y dispersión por banda para el estado medido. Después calibrar contra las mediciones.

I-Simpa explica la comprobación en sus [recomendaciones de importación](https://i-simpa-wiki.readthedocs.io/fr/latest/import_file_recommandations.html).

## Coordenadas

Metros. X=0 en el muro posterior del escenario; X crece hacia el fondo del público. Y=0 en el eje central, Z=0 en el nivel arquitectónico +0,00.

`mediciones-originales.csv` conserva las coordenadas de `analisis/sala.py`. El registro XY con las marcas es aproximado y las alturas requieren revisión. P8/P9 son platea alta. P5 queda dentro del cierre revisado sin moverlo. Estar dentro de la malla no demuestra que una posición sea exacta.

## Regeneración

Python 3, `numpy`, `manifold3d` y `trimesh`; para figuras, `matplotlib` y `Pillow`. Versiones usadas en `revision/verificacion-exportaciones.json`.

```powershell
py -m pip install numpy manifold3d trimesh matplotlib Pillow
py -B modelo-3d/generar.py
py -B modelo-3d/comparar_plano.py
py -B modelo-3d/verificar_geometria.py
```

El generador conserva la procedencia de caras durante las operaciones booleanas. Une vértices a precisión de 0,000001 m y comprueba el cierre resultante. El visor se genera desde `visor.template.html`. Los renders de referencia están en `revision/`; no se modificaron los PDF.

## Alcance

Una región de aire conectada, con normales hacia su interior. Cuatro pilares unen piso e intradós: Euler=-6 es esperable y no constituye un hueco. Todas las aristas tienen dos caras incidentes y orientación coherente.

El volumen incluye escenario y circulaciones aproximadas; no sustituye la estimación del informe. Las superficies de butacas son equivalentes, sin asientos individuales; se deberán separar audiencia y pasillos antes de asignar materiales definitivos. No se añadieron tratamientos propuestos ni altavoces: se representa una hipótesis del estado existente.

**Las rutas del diagnóstico acústico anterior se calcularon con v1. Deben recalcularse antes de atribuir reflexiones a las nuevas superficies.**

Visor: Three.js 0.160.1, licencia MIT, incluido en `vendor/`.
