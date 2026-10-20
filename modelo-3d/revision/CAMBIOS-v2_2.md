# v2.2: cortinas y superficies equivalentes de audiencia

Se conserva la envolvente de v2.1 y se subdividen superficies para asignar materiales. El volumen sigue siendo 9550,48 m³, dentro del redondeo del modelo. Las butacas se representan por superficies equivalentes, sin añadir sillas individuales ni una segunda capa superpuesta al piso.

## Grupos nuevos

| Grupo | Área geométrica aproximada | Asignación inicial |
|---|---:|---|
| butacas_platea | 430,04 m² | AM_Butacas_cuero_vacias |
| butacas_alta_frontal | 132,69 m² | AM_Butacas_cuero_vacias |
| butacas_alta_posterior | 100,01 m² | AM_Butacas_cuero_vacias |
| pasillos_alfombra | 153,68 m² | AM_Alfombra_sin_bajoalfombra |
| madera_expuesta | 208,09 m² | AM_Parquet_soporte_rigido |
| cortinas_fondo | 78,00 m² | AM_Cortina_media_plegada_HIPOTESIS |

La delimitación de audiencia es una aproximación de bloques, no un recuento de butacas. Se usa pasillo central de 1,30 m y límites laterales aproximados; los sectores de circulación no identificados como alfombra quedan como madera. El bloque posterior usa una delimitación central conservadora. Las fracciones de cobertura y áreas pueden revisarse con el plano sin representar cada asiento. Las contrahuellas siguen separadas de las huellas de audiencia.

Por indicación del usuario, todo el cierre posterior bajo balcón se representa con cortinas cubriendo puertas cerradas. Se cambia el material de esa frontera, sin crear una abertura hacia el exterior ni otro volumen acoplado. La puerta/muro queda implícita como respaldo rígido: la curva de cortina es una aproximación al conjunto, no a tela suspendida en campo libre. Pilares e intradós conservan sus superficies rígidas. La foto muestra dos pilares visibles; se conservan los cuatro pilares de la planta/modelo anterior, sin inferir que los restantes hayan desaparecido.

El archivo 3DS incluye ahora colores visuales por grupo, independientes de los coeficientes acústicos. Para verlos en I-Simpa seleccionar View → Material color → Original. Para ver colores de materiales acústicos, usar Material y definir sus colores en Display.

## Reimportar sin perder la configuración de puntos

Guardar una copia del proyecto actual. Dentro de esa copia usar File → Import new scene con `aula-magna-v2_2.3ds`, sin crear otro proyecto vacío. I-Simpa conserva fuentes y receptores al reemplazar la escena; verificar luego posiciones y reasignar materiales a los grupos nuevos, porque cambió la subdivisión de caras. Volver a mallar y guardar.

## Dispersión: corrección de las instrucciones anteriores

La importación observada por el usuario cargó absorción pero dejó Diffusion=0. La validación anterior del TXT solo comprobaba sintaxis/rangos, no todos los campos dentro de la interfaz. No considerar cargada la dispersión por el hecho de que α=.44 aparezca en butacas.

En un material editable bajo Materials → User, abrir Spectrum, editar primero Diffusion con un valor mayor que cero y confirmar Enter. Solo después elegir Lambert en Diffusion law de esa banda. Con s=0, I-Simpa bloquea la ley en Specular por diseño. Repetir en las bandas usadas. Si el material está en Reference, copiarlo a User para editarlo.

Valores iniciales por octavas:

| Material / familia | 125 | 250 | 500 | 1000 | 2000 | 4000 Hz |
|---|---:|---:|---:|---:|---:|---:|
| Butacas equivalentes | .40 | .45 | .50 | .55 | .60 | .65 |
| Relieves omitidos y cortina plegada | .05 | .10 | .15 | .20 | .25 | .30 |
| Superficies extensas lisas | .05 | .05 | .05 | .05 | .05 | .05 |

Para tercios, usar inicialmente el valor de octava en sus tres tercios: 100/125/160; 200/250/315; 400/500/630; 800/1000/1250; 1600/2000/2500; 3150/4000/5000 Hz. Fuera de ese rango los valores son extrapolaciones. En particular, 8 kHz sigue sin datos específicos de los materiales del teatro.

Absorción inicial de cortina media plegada: .07/.31/.49/.75/.70/.60 entre 125 y 4000 Hz, tomada de la referencia de materiales anterior. La distancia a la puerta, pliegues y tejido son inciertos; comparar con una variante menos absorbente antes de calibrar. No utilizar α=1 por tratarse del límite del recinto.

Referencia de edición y bloqueo con s=0: https://i-simpa-wiki.readthedocs.io/fr/latest/project_database.html

La malla revisada se verifica con detección de intersecciones y mallado TetGen, además de roundtrip de PLY y 3DS. Los controles no prueban que la distribución aproximada de materiales esté ya calibrada acústicamente.
