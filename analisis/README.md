# Análisis de las respuestas al impulso

Pipeline reproducible que va de `datos/` a los JSON que alimentan el informe.
Hasta ahora los números publicados en `index.html` estaban embebidos a mano y no
había forma de regenerarlos ni de aplicar el mismo tratamiento a datos nuevos.

## Requisitos

Python 3.9 o superior, con `numpy` y `soundfile`:

```bash
py -m pip install -r analisis/requisitos.txt
```

No usa scipy: los filtros de octava se aplican en el dominio de la frecuencia,
lo que da fase cero por construcción.

## Uso

```bash
py analizar.py --comparar
```

Desde `analisis/`. Analiza las dos fuentes, escribe `salida/*.json` e imprime la
tabla comparativa. Tarda alrededor de un minuto para las 36 mediciones.

```bash
py validar.py          # contrasta contra los valores ya publicados en index.html
py verificar.py todo   # duplicados, INR y calidad de los ajustes de REW
```

## Qué produce

Por cada fuente, en `salida/`:

| Archivo | Contenido |
|---|---|
| `ir_<fuente>.json` | Análisis propio de cada WAV, con el mismo esquema que la constante `IR` de `index.html` |
| `rew_<fuente>.json` | Exportes RT60 de REW en el formato compacto que consume `index.html` |
| `resumen_<fuente>.json` | Promedios espaciales por octava y por zona, y KPIs globales |

`salida/` no se versiona: se regenera desde `datos/`.

## Módulos

| Archivo | Rol |
|---|---|
| `irlib.py` | Filtros de octava de fase cero, Lundeby, Schroeder, ajuste de T |
| `parametros.py` | Parámetros acústicos de un IR (EDT, T20, T30, C50, C80, D50, Ts, INR, ETC, reflexiones, eco) |
| `rew.py` | Lector de los exportes RT60 en texto |
| `sala.py` | Coordenadas, zonas, condiciones y **tomas descartadas**. Es el archivo de configuración |
| `verificar.py` | Controles de integridad sobre los datos crudos |
| `analizar.py` | Punto de entrada |
| `validar.py` | Prueba de regresión contra `index.html` |

## Validación

`validar.py` reanaliza los WAV del parlante y compara con los valores ya
publicados. Estado actual:

```
Octava     T30 script   T30 html      dif
   125          1.587      1.584   +0.003
   250          1.549      1.551   -0.001
   500          1.582      1.587   -0.005
  1000          1.674      1.678   -0.004
  2000          1.742      1.743   -0.001
  4000          1.565      1.566   -0.001
```

Entre 125 Hz y 4 kHz el pipeline reproduce el análisis original dentro de
±0,005 s en T30 y ±0,018 s en EDT. Esas son las bandas sobre las que se juzga
la validación.

**63 Hz y 8 kHz quedan fuera del criterio** (desvíos de +0,013 y −0,025 s). En
los extremos el resultado depende del faldón exacto del filtro de octava y del
tratamiento del ruido, y el análisis original no está documentado a ese nivel de
detalle, así que no hay contra qué calibrarlos. Si alguna vez se recupera el
script original, conviene fijar ahí el criterio también.

## Decisiones que conviene conocer

**Compuertas de calidad.** Un ajuste de decaimiento solo se acepta si la banda
tiene INR suficiente (45 dB para T30, 35 dB para T20, según ISO 3382) y si la
regresión es limpia. Sin esto, una banda dominada por ruido no falla: devuelve
un número grande y plausible. Es exactamente lo que pasaba con el globo en
graves, donde sin compuerta salía un T30 de 15 s en 63 Hz.

EDT no lleva umbral de correlación: se ajusta sobre los primeros 10 dB, que es
justamente el tramo donde el decaimiento no es recto. Exigirle |r| alto
descartaba ajustes buenos y sesgaba la media espacial hacia arriba.

**Tomas descartadas.** `sala.DESCARTADAS` excluye de los promedios las tomas que
`verificar.py duplicados` identificó como repetidas. Hoy son dos pares del
globo: `F1-P2`/`F1-P3` y `F2-P4`/`F2-P6`, con audio idéntico dentro de cada par.
No se pudo determinar cuál de las dos etiquetas de cada par es la correcta, así
que se descarta la segunda de forma arbitraria. **Si las notas de campo lo
aclaran, hay que corregir esa lista**: hoy el globo aporta 16 mediciones, no 18.

**Detección de duplicados.** Compara el audio alineado en `t0`, no un hash del
archivo. Un hash no alcanza: los dos pares de arriba difieren en metadatos, en
el recorte inicial y en la recuantización, pero son la misma toma.

## Relación con index.html

El informe embebe dos cosas distintas y conviene no confundirlas:

- Las constantes `IR`, `REW`, `REFL`, `XY` y `PLAN_IMG` vienen del **análisis
  original**, hecho antes de que existiera este pipeline. Alimentan todo el
  cuerpo del informe y **no se tocan desde acá**.
- La constante `FUENTES`, que alimenta la sección *Parlante contra globo*, la
  genera `exportar_web.py` entre dos marcadores:

  ```
  /* === generado por analisis/exportar_web.py — no editar a mano === */
  /* === fin del bloque generado === */
  ```

```bash
py exportar_web.py --embeber
```

Reanaliza ambas campañas y reescribe ese bloque en su lugar (14 KB). La
comparación entre fuentes tiene que salir del mismo pipeline para las dos, o
estaría comparando métodos además de fuentes; por eso el bloque incluye también
al parlante aunque el resto de la página ya tenga sus datos.

La sección compara solo las **16 posiciones pareadas**, es decir, las que existen
en las dos campañas una vez descartadas las tomas repetidas. Por eso los
promedios del parlante ahí no coinciden exactamente con los KPI de la cabecera
del informe, que promedian las 18.

Para regenerar el informe entero desde cero haría falta además reconstruir el
modelo de fuentes imagen (ver abajo).

## Lo que falta

**Atribución de reflexiones a superficies.** `parametros.reflexiones` detecta las
reflexiones (tiempo, nivel y prominencia sobre la mediana local) pero no dice de
qué superficie viene cada una. La constante `REFL` de `index.html` sí trae esas
etiquetas, de un modelo de fuentes imagen que no está en el repositorio.

No se reconstruyó porque los planos que se deducen de la geometría publicada en
el informe no cierran con las coordenadas de `sala.XY`: con el proscenio y el
fondo de sala que describe la sección "Condiciones", P5 (X = 33,5 m) queda por
fuera del muro trasero. Inventar los planos daría etiquetas equivocadas, que es
peor que no tenerlas. Para habilitarlo hay que definir `sala.PLANOS` con la
geometría confirmada y escribir el modelo de primer orden.
