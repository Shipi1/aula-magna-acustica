# Base teórica, configuración y supuestos de la predicción acústica

**Proyecto:** Teatro Aula Magna de la Universidad Técnica Federico Santa María.  
**Fecha de esta versión:** 20 de octubre de 2026.  
**Modelo de referencia:** `G_base_efectiva_espectral_Lw90.proj`.

Para abrirlo en I-Simpa, usar el [proyecto de referencia vigente](../prediccion/G_base_efectiva_espectral_Lw90.proj). Es el archivo compatible cuya apertura fue confirmada por el usuario; la copia con sufijo `_compatible` ya no es la referencia disponible.

## 1. Propósito y alcance

Este documento reúne la configuración de cálculo, el fundamento de los parámetros y las hipótesis utilizadas para aproximar las mediciones acústicas del recinto mediante I-Simpa/SPPS. Su propósito es permitir la reproducción del trabajo y servir como referencia metodológica para el informe.

El objetivo del modelo es obtener una base suficientemente representativa del estado actual para comparar posteriormente intervenciones acústicas. No se exige reproducir exactamente cada medición, pero sí distinguir los efectos de una intervención de la variación numérica y de la incertidumbre de las hipótesis.

**El modelo G es una base provisional con absorción efectiva. No constituye una identificación única de los materiales reales ni una validación global de la sala. Los ensayos documentados aquí todavía no demuestran la eficacia de un tratamiento de platea alta.**

Debe diferenciarse entre:

- **Convergencia numérica:** estabilidad del resultado al aumentar partículas y repetir el cálculo con distintas semillas.
- **Calibración:** ajuste de una representación del recinto para aproximar las mediciones.
- **Validación:** contraste del modelo con datos y condiciones que permitan evaluar su capacidad predictiva; una coincidencia en un parámetro o promedio no basta para declararla completa.
- **Evaluación de una intervención:** comparación entre los estados actual y tratado, conservando condiciones de cálculo equivalentes y documentando las incertidumbres.

## 2. Fundamento del cálculo y de los parámetros

### 2.1. Método SPPS

SPPS sigue partículas sonoras en una geometría tridimensional y representa el transporte y las pérdidas de energía mediante una aproximación geométrica, energética y probabilística. El número de partículas y la aleatoriedad influyen en el resultado; por ello se estudió su convergencia [1, 2].

Se emplea el método **Energetic**. Esta representación no calcula explícitamente la vibración de la tarima ni constituye una simulación ondulatoria completa. Una posible resonancia de un elemento constructivo debe incorporarse mediante una propiedad equivalente respaldada o estudiarse con un modelo físico específico.

### 2.2. Potencia sonora y presión sonora

La potencia sonora se expresa mediante:

\[
L_W=10\log_{10}\left(\frac{W}{W_0}\right),\qquad W_0=10^{-12}\ \mathrm{W}.
\]

La configuración de trabajo utiliza **Lw global = 90 dB re 1 pW**, equivalente a una potencia acústica total de 1 mW. No es potencia eléctrica ni significa que se reciban 90 dB SPL en las butacas.

El nivel global se obtiene por suma energética de las bandas:

\[
L_{W,\mathrm{global}}=10\log_{10}\left(\sum_b10^{L_{W,b}/10}\right).
\]

Se conserva el espectro existente de G, con 27 bandas de tercio de octava entre 50 Hz y 20 kHz. **No se asignan 90 dB a cada banda.**

En el modelo lineal, aumentar todas las bandas de la fuente en 10 dB multiplica por diez las energías recibidas, pero no modifica sus cocientes ni las pendientes de decaimiento normalizado. Por tanto, no corrige RT, EDT o C80. Una medición real sí puede beneficiarse de una mayor relación señal/ruido; ese efecto no equivale a modificar la acústica de la sala.

### 2.3. Reverberación: T20, T30 y EDT

Los tiempos se obtienen a partir de la integración inversa de la respuesta energética, o curva de Schroeder [3]:

\[
D(t)=10\log_{10}\left(\frac{\int_t^{t_f}e(\tau)\,d\tau}{\int_{t_0}^{t_f}e(\tau)\,d\tau}\right).
\]

Para una pendiente ajustada \(m\), en dB/s, la extrapolación a una caída de 60 dB es:

\[
T=-\frac{60}{m}.
\]

- **T20:** ajuste entre −5 y −25 dB.
- **T30:** ajuste entre −5 y −35 dB.
- **EDT:** extrapolación del decaimiento inicial de 10 dB; en el procesamiento del modelo se inicia en la primera llegada no nula, excluyendo el silencio de propagación.

Los valores T20 y T30 exportados por REW **ya están extrapolados a 60 dB**. No se deben multiplicar nuevamente por tres o por dos. EDT caracteriza el decaimiento inicial y no debe interpretarse como idéntico al tiempo de reverberación del tramo tardío.

Las salidas lineales RECP procesadas en este trabajo ya representan energía: **no se vuelven a elevar al cuadrado**. En una respuesta al impulso de presión, en cambio, se utiliza la presión al cuadrado para obtener una magnitud energética.

### 2.4. Claridad musical C80

\[
C_{80}=10\log_{10}\left(\frac{\int_{t_0}^{t_0+0,080}e(t)\,dt}{\int_{t_0+0,080}^{t_f}e(t)\,dt}\right).
\]

El numerador incluye el sonido directo y las primeras reflexiones durante los primeros 80 ms; el denominador incluye la energía posterior. C80 no separa el sonido directo de las reflexiones tempranas [4].

En la predicción se referencia la llegada directa mediante:

\[
t_0=\frac{d_{\mathrm{fuente-receptor}}}{342\ \mathrm{m/s}}.
\]

Se utiliza la energía recibida hasta los 4 s de duración del cálculo. Para contrastar con mediciones hay que considerar las diferencias de tiempo cero, filtrado, ruido y longitud de registro.

Un C80 mayor no garantiza por sí solo una acústica mejor para uso orquestal. Tampoco demuestra la desaparición de ecos flotantes: estos requieren examinar además el ecograma, la repetición de picos y su persistencia.

### 2.5. Uso limitado de Sabine

La relación estadística:

\[
T\approx\frac{0,161V}{A},\qquad A=\sum_iS_i\alpha_i
\]

se utilizó como control de orden de magnitud y como aproximación inicial para ensayos de absorción equivalente. No sustituye el cálculo espacial ni predice por sí sola C80, reflexiones concretas o diferencias entre platea general, bajo balcón y platea alta.

La curva efectiva G no se obtuvo de una identificación exacta de un material resonante. Es una hipótesis de calibración equivalente contrastada mediante simulación.

## 3. Configuración exacta recomendada para continuar

Abrir [G_base_efectiva_espectral_Lw90.proj](../prediccion/G_base_efectiva_espectral_Lw90.proj) y conservar la geometría, la malla, las asignaciones y las posiciones existentes.

| Parámetro | Valor de trabajo |
|---|---|
| Código | SPPS |
| Calculation method | Energetic |
| Potencia de la fuente | Lw global = 90 dB, sin ponderación A |
| Espectro | Conservar el existente en G |
| Number of sound particles per source | 4.800.000 |
| Simulation length | 4 s |
| Time step | 0,001 s |
| Receiver radius | 0,31 m |
| Particle extinction: exponente | 5 |
| Partículas para visualización | 0 |
| Absorción atmosférica | Activada |
| Direct field only | Desactivado: incluir directo y reflexiones |
| Transmission | Desactivada |
| Echogram per source | Activado |
| Fuentes activas | Una por cálculo |
| Bandas activas | Una por cálculo |

El proyecto conserva activada la opción de difusión por objetos de amueblamiento; no se añadieron zonas volumétricas de amueblamiento para representar individualmente las butacas. Estas se modelan mediante superficies equivalentes.

La selección inicial guardada es **F1 activa, F2 desactivada y únicamente 1000 Hz**. La documentación de SPPS advierte que la selección simultánea de varias bandas puede impedir controlar la secuencia aleatoria mediante la semilla, debido al procesamiento multihilo [2]. Por ello, las repeticiones reproducibles se realizan con una banda por proceso.

### Secuencia de repeticiones

Para cada combinación de fuente y frecuencia:

1. Activar F1 y desactivar F2.
2. Seleccionar una sola banda; empezar por 1000 Hz.
3. Ejecutar tres cálculos de 4.800.000 partículas, conservando el resto de parámetros:

   | Ejecución | Random initialization number |
   |---|---:|
   | 1 | 20261019 |
   | 2 | 20261020 |
   | 3 | 20261021 |

4. Guardar cada realización con un nombre que identifique fuente, banda, número de partículas y semilla.
5. Repetir con F2 activa y F1 desactivada.
6. Aplicar después el procedimiento a 2000 y 4000 Hz, prioritarias para la intervención en agudos. Continuar con 500 Hz y mantener 250 Hz como banda de diagnóstico por su discrepancia de claridad. Las bandas extremas necesitan comprobaciones propias si van a fundamentar conclusiones.

No activar ambas fuentes simultáneamente para reproducir las mediciones individuales F1 y F2.

## 4. Promedio correcto de las realizaciones

Se promedian las energías lineales por instante, conservando separados cada receptor, fuente y banda:

\[
\overline{E}(t)=\frac{E_{20261019}(t)+E_{20261020}(t)+E_{20261021}(t)}{3}.
\]

Sobre esta respuesta energética media se recalculan C80, EDT, T20 y T30. No se promedian directamente las curvas en decibeles ni los tiempos de reverberación para construir una respuesta media.

También se conservan los parámetros individuales de cada realización para describir la variación entre semillas. Promediar parámetros puede servir como estadística descriptiva, pero no equivale a recalcularlos sobre la energía media. No se mezclan las respuestas de F1 y F2 ni diferentes posiciones de audiencia.

Cambiar la semilla en I-Simpa no realiza automáticamente el promedio. La respuesta media calculada en esta investigación se entrega en `convergencia-base-D/respuesta-media-semillas.json`; los proyectos contienen las realizaciones nativas individuales.

## 5. Diferencia entre los cálculos realizados y la receta recomendada

| Etapa | Fuente y bandas | Partículas | Semillas | Lw global utilizado |
|---|---|---:|---|---:|
| Confirmación previa de D, reutilizada | F1, 1000 Hz | 1.200.000 | 20261019 | 80 dB |
| Escalado de convergencia | F1, 1000 Hz | 2.400.000 y 4.800.000 | 20261019 | 80 dB |
| Repetición al nivel mayor | F1, 1000 Hz | 4.800.000 por realización | 20261019, 20261020 y 20261021 | 80 dB |
| Ensayos espectrales de G | F1 y F2 por separado; 250, 500, 2000 y 4000 Hz, una banda por proceso | 600.000 | 20261019 | 80 dB |
| Configuración guardada y recomendada para continuar | Una fuente y una banda por cálculo | 4.800.000 | Repetir las tres indicadas | 90 dB |

Por tanto, **los resultados espectrales publicados de G no proceden de tres realizaciones de 4,8 millones de partículas**. Para reproducir exactamente esos ensayos se utiliza 600.000, semilla 20261019 y Lw global 80 dB. Al recalcular a 90 dB se conserva el comportamiento temporal normalizado del modelo lineal y aumenta el nivel recibido.

La prueba de convergencia a 1 kHz se realizó sobre D; G conserva su ajuste a esa frecuencia. No se traslada automáticamente esa estabilidad a F2 o al resto del espectro.

## 6. Supuestos utilizados

### 6.1. Geometría

La geometría se basa en los planos disponibles y en las revisiones previas del modelo. Se conserva un volumen aproximado de **9544 m³**. No es un levantamiento tridimensional completo del teatro.

La ornamentación, las butacas individuales y el interior de los palcos están simplificados. Los paños de cortina de los palcos se representan como superficies equivalentes sobre la envolvente, sin reconstruir un interior que no está suficientemente documentado.

### 6.2. Fuentes y posiciones

Se utilizan fuentes omnidireccionales idealizadas. **No se representa el line array del teatro ni la directividad real del parlante utilizado en los barridos.** La explosión del globo tampoco es una fuente omnidireccional perfecta. Esta simplificación afecta especialmente la comparación de energía temprana y C80.

Se conservan las siguientes coordenadas del modelo, en metros:

| Fuente | X | Y | Z |
|---|---:|---:|---:|
| F1 | 5,36 | 0,02 | 1,50 |
| F2 | 5,60 | 4,72 | 1,50 |

Las fuentes se consideran aproximadamente 1 m sobre el escenario y los nueve receptores aproximadamente 2 m sobre su piso local. Las coordenadas Z son cotas respecto del origen del modelo: no equivalen por sí solas a la altura sobre el piso local. P8 y P9 corresponden a platea alta. Las posiciones no se desplazaron para mejorar el ajuste acústico.

Lw = 90 dB es una referencia de trabajo, no una potencia acústica medida del parlante de la campaña.

### 6.3. Ocupación y butacas

Se modelan butacas vacías mediante superficies equivalentes. No se incorpora público. La curva adoptada para las butacas de cuero es una aproximación de referencia, no una medición de sus tapizados, resortes o estructura.

### 6.4. Materiales, cortinas y reflectores

Se adoptan representaciones de parquet sobre soporte rígido, piso de escenario de madera, alfombra, revestimientos minerales rígidos y cortinas. Sus propiedades son aproximaciones de referencia y no ensayos de laboratorio de los materiales específicos del teatro.

Las cortinas laterales de audiencia se limitan a la zona junto al escenario, según la aclaración del usuario. Se consideran asimismo los paños de fondo bajo balcón y los del escenario. La extensión y el montaje de los paños son estimaciones; no se conocen todos sus pliegues, separaciones y propiedades.

La base conserva seis paneles reflectantes escénicos equivalentes. Su presencia se apoya en fotografías, pero su número equivalente, dimensiones y ubicación en el modelo son estimados. No representan un tratamiento nuevo de platea alta.

### 6.5. Posible escenario hueco

El piso del escenario utiliza inicialmente una curva de madera con α = 0,11 a 250 Hz y α = 0,10 a 500 Hz. No se simula explícitamente como una estructura vibrante con tablas, apoyos, cámara y amortiguamiento conocidos.

Una cámara bajo la tarima puede participar en un comportamiento resonante, pero ser hueca no define por sí solo su absorción a 250 Hz. Los ensayos con α = 1 en el piso del escenario fueron controles ideales de sensibilidad, **no una propuesta de material ni una identificación de su construcción**.

### 6.6. Condiciones ambientales

| Magnitud | Valor supuesto |
|---|---:|
| Temperatura | 18 °C |
| Humedad relativa | 57 % |
| Presión atmosférica | 101.325 Pa |
| Velocidad utilizada para referenciar C80 | 342 m/s |

Estos valores no se presentan como condiciones ambientales medidas durante la campaña. Se activa el cálculo de absorción atmosférica.

### 6.7. Absorción efectiva ajustada de G

Solo se modifica la curva del material efectivo 115, aplicado a:

- `05_muros`;
- `10_laterales_altos`;
- `11_fondo_alto`.

| Centro de frecuencia | Absorción efectiva α de G |
|---|---:|
| 125 Hz | 0,23095 |
| 250 Hz | 0,60 |
| 500 Hz | 0,44 |
| 1000 Hz | 0,24795 |
| 2000 Hz | 0,17 |
| 4000 Hz | 0,11 |
| 8000 Hz | 0,26795 |

Se interpola entre estos valores respecto al logaritmo de frecuencia. Los otros materiales conservan sus curvas anteriores.

**Estos coeficientes no se identifican como absorción real del concreto rugoso.** Constituyen una representación equivalente que puede compensar pérdidas de construcciones no resueltas, incertidumbres de áreas u otras simplificaciones. La coincidencia de RT no demuestra que se haya identificado la causa física de esas pérdidas.

Si posteriormente se trata una de estas superficies, debe definirse qué sistema representa el coeficiente efectivo antes de reemplazarlo por la curva del nuevo montaje. No corresponde sumar indiscriminadamente la absorción nueva sobre la efectiva existente.

### 6.8. Dispersión y procesos omitidos

La dispersión no se reajustó en G. Los tres grupos de muro mencionados conservan coeficiente 0,05. Cielos y ornamentación mantienen hipótesis crecientes de 0,05 a 0,30; las butacas, de 0,40 a 0,65 según frecuencia. Son estimaciones de modelado, no medidas de las superficies. Se conserva la ley de dispersión de tipo Lambert configurada en los materiales correspondientes.

Se desactiva la transmisión a través de cerramientos. No se calcula explícitamente la vibración estructural de la tarima ni una respuesta ondulatoria completa. Las limitaciones del enfoque geométrico energético deben considerarse al interpretar resonancias o reflexiones muy específicas [1].

## 7. Referencia de mediciones y criterios de aceptación

Los contrastes utilizan las exportaciones originales de REW para globos y barridos, conservando separados los dos métodos de excitación y las fuentes F1/F2. Para los resúmenes de globo se excluyen F1-P3 y F2-P6 por duplicación conocida de WAV; las etiquetas correctas de los pares implicados siguen siendo inciertas.

En las comparaciones de T20 se exige valor positivo y |r|≥0,99 en la referencia. Ese criterio de regresión del RT no se utiliza como filtro automático de C80; valores negativos o cero de claridad son válidos.

Los exportes REW empleados indican filtrado Forward. El modelo entrega energía por banda sin reproducir el filtro temporal de la medición. También existen diferencias en el origen temporal y la longitud de registro. La auditoría auxiliar con un filtro común no elimina la diferencia entre globos y barridos; por ello no se fuerza una única curva objetivo mezclando ambas campañas.

Se propusieron como criterios de trabajo, no normativos:

- Convergencia entre niveles de partículas: cambio de C80 <0,5 dB y de T20/T30 <5 %.
- Repetición entre tres semillas: rango máximo−mínimo de C80 <0,5 dB y rango/media de T20/T30 <5 %.
- Aproximación inicial de la base: error del RT medio del orden de ±10–15 % y error medio absoluto de C80 del orden de 1–2 dB, revisando además los puntos y las zonas. Son objetivos de proyecto, no una garantía de precisión ni una tolerancia normativa.

En F1 a 1 kHz, las tres semillas de 4,8 millones obtuvieron un rango máximo de C80 de **0,437 dB**, cumpliendo el criterio en los nueve receptores. Para ambos parámetros de RT, siete de nueve puntos cumplieron el criterio entre semillas. Las excepciones fueron P6 en T30 (5,19 %) y P8 en T20 (5,07 %); no se relajó retrospectivamente el umbral.

G presenta la mejor coincidencia conjunta preliminar de RT y C80 en 2–4 kHz. A 250 Hz el RT se acerca, pero C80 empeora: **esa banda no se acepta como suficientemente calibrada para claridad**. Los ensayos espectrales de 600.000 partículas requieren su propia comprobación de convergencia antes de atribuir cambios pequeños a una intervención.

## 8. Aplicación en el informe y comparación de tratamientos

La descripción metodológica debe declarar la geometría aproximada, las fuentes idealizadas, las condiciones ambientales supuestas, el carácter equivalente de la absorción ajustada y la diferencia entre cálculos ejecutados y configuraciones recomendadas.

Para evaluar un tratamiento se deberán conservar condiciones equivalentes en los estados actual y tratado, repetir las semillas y examinar resultados por receptor, frecuencia y zona. La variación entre semillas no incluye la incertidumbre de materiales, geometría o directividad. Conviene comprobar también si la mejora persiste bajo varias bases físicamente plausibles.

No se debe presentar la coincidencia del RT medio como prueba suficiente de eliminación de ecos flotantes. Tampoco se atribuye eficacia a un tratamiento que todavía no se ha calculado. La documentación sirve como fundamento teórico y metodológico de la predicción; no sustituye la descripción completa de la campaña de medición ni certifica cumplimiento de una norma de ensayo.

## 9. Documentos asociados

- [Resultados y orientación de uso](../prediccion/convergencia-base-D/LEEME-RESULTADOS.md).
- [Informe de convergencia numérica](../prediccion/convergencia-base-D/INFORME-CONVERGENCIA.md).
- [Ensayos de absorción y contraste de la base G](../prediccion/convergencia-base-D/ENSAYOS-BASELINE.md).
- [Auditoría auxiliar del C80 medido](../prediccion/convergencia-base-D/AUDITORIA-MEDICIONES-C80.md).
- [Contraste previo de C80 con REW](../prediccion/ajuste-absorcion-muros/contraste-C80/INFORME-CONTRASTE-C80.md).

## 10. Referencias técnicas

1. Université Gustave Eiffel. [SPPS: principio, alcance y limitaciones del método](https://i-simpa.univ-gustave-eiffel.fr/presentation-1/embedded-codes/spps).
2. I-Simpa. [Using SPPS within I-Simpa: configuración, partículas, semillas y bandas](https://i-simpa-wiki.readthedocs.io/fr/latest/code_configuration_SPPS.html).
3. Room EQ Wizard. [RT60 Graph: integración de Schroeder, T20, T30 y EDT](https://www.roomeqwizard.com/help/help_en-GB/html/graph_rt60.html).
4. Room EQ Wizard. [Clarity Graph: C50, C80 y D50](https://www.roomeqwizard.com/help/help_en-GB/html/graph_clarity.html).
5. OSHA. [Technical Manual, Section III, Chapter 5, tabla V-2: referencias de absorción de materiales](https://www.osha.gov/otm/section-3-health-hazards/chapter-5). Las curvas de referencia no identifican por sí solas los materiales del teatro.
