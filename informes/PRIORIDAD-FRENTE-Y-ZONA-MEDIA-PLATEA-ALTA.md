# Prioridad de estudio: frente y zona media de la platea alta

**Actualización:** 9 de noviembre de 2026. **Origen:** decisión del usuario de concentrar el objetivo en las filas delanteras y medias. Se reinterpretan resultados ya calculados; no se ejecutaron nuevas simulaciones ni se cambiaron posiciones o respuestas.

## 1. Alcance vigente

La optimización se concentra en **la zona delantera como prioridad y la zona media como parte del objetivo**, manteniendo D50 de 48–52 % y C80 máximo +2 dB a 1.000 Hz, con la referencia de balance −2 a +2 dB. Las posiciones posteriores dejan de exigir el cumplimiento de esos rangos para seleccionar una geometría. Se mantienen como controles separados, fuera de la función objetivo.

| Sector | Posiciones | Combinaciones con F1/F2 | Papel |
|---|---|---:|---|
| Delantero, X = 26 m | V01, V02, V03 y V04 | 8 | Prioridad principal de optimización |
| Medio sobre butacas, X = 31 m | V05 y V08 | 4 | Objetivo espacial, evaluado por separado del frente |
| Posterior sobre butacas, X = 36 m | V10 y V11 | 4 | Control, fuera del objetivo |
| Madera expuesta alta | V06, V07, V09 y V12 | 8 | Control, fuera del objetivo |

El nuevo conjunto virtual de optimización tiene **seis posiciones y doce combinaciones**. V09–V12 quedan fuera del objetivo: V09/V12 ya eran controles sobre madera y V10/V11 dejan de ser exigencias de cobertura. V06/V07 son controles sobre madera del tramo medio y no se incorporan como butacas.

Se conservan los pares de campo prioritarios F1–P8, F1–P9 y F2–P8, y F2–P9 como control secundario. P1–P7 siguen separando platea baja y bajo balcón. Los posteriores no penalizan el incumplimiento de D50/C80 en la selección; se muestran para registrar qué cambia en el resto de la sala.

## 2. Alcance y explicación física son decisiones distintas

Priorizar frente y media es una decisión de alcance. **La cercanía al muro posterior no garantiza que C80 siempre sea mayor:** una reflexión puede llegar antes o después de 80 ms respecto del directo, y el indicador depende de la energía de ambas ventanas y de los demás recorridos. No se presume una claridad posterior inevitablemente excesiva.

La referencia a 1.000 Hz presenta este patrón descriptivo:

| Sector de butacas virtuales | D50 medio | C80 medio | Rango de C80 |
|---|---:|---:|---:|
| Delantero | 43,95 % | 0,40 dB | -0,53 a 1,01 dB |
| Medio | 39,52 % | 0,80 dB | -0,05 a 1,17 dB |
| Posterior | 43,24 % | 1,00 dB | 0,63 a 1,48 dB |



En promedio el C80 posterior es mayor, pero todos los valores posteriores de referencia están entre +0,63 y +1,48 dB. Además, F1–V10 (posterior) tiene C80 de aproximadamente +0,63 dB, menor que F1–V08 (medio), aproximadamente +1,17 dB. El patrón medio no permite afirmar que cada punto trasero tenga más claridad que cualquier punto delantero.

## 3. Reevaluación de las geometrías ya calculadas

Los siguientes valores utilizan solo las doce combinaciones delanteras e intermedias. Se promedian parámetros individuales calculados sobre las respuestas energéticas medias de tres semillas. No se mezclan fuentes actuando simultáneamente. La media conjunta da a cada combinación el mismo peso, no a cada metro cuadrado de audiencia.

| Geometría | D50 frente | D50 medio | D50 frente + media | C80 frente + media | Distancia media a D50 de 50 % | Cumplen ambos rangos |
|---|---:|---:|---:|---:|---:|---:|
| Referencia | 43,95 % | 39,52 % | 42,47 % | 0,53 dB | 7,53 puntos | 0/12 |
| Cuatro anteriores | 45,15 % | 39,76 % | 43,35 % | 0,84 dB | 6,65 puntos | 3/12 |
| Cobertura 4 | 47,65 % | 41,51 % | 45,60 % | 1,12 dB | 5,25 puntos | 1/12 |
| Equilibrio 4 | 46,73 % | 41,40 % | 44,96 % | 1,01 dB | 5,42 puntos | 1/12 |
| Cobertura 6 | 50,70 % | 41,65 % | 47,68 % | 1,40 dB | 4,55 puntos | 2/12 |
| Anterior + central 5 | 45,91 % | 40,00 % | 43,94 % | 1,07 dB | 6,16 puntos | 3/12 |
| Posteriores 4 × 3 m | 46,37 % | 45,13 % | 45,96 % | 1,38 dB | 4,36 puntos | 3/12 |
| Posteriores 6 × 2 m | 46,29 % | 43,91 % | 45,50 % | 1,15 dB | 4,78 puntos | 3/12 |
| Mixta 6 | 47,06 % | 43,40 % | 45,84 % | 1,31 dB | 5,12 puntos | 2/12 |



### Cómo cambia la comparación

- **Seis paneles redistribuidos:** el frente alcanza D50 medio de 50,70 % y C80 medio de +1,56 dB, pero la zona media queda en 41,65 % de D50. La media frontal no significa que sus ocho combinaciones cumplan: lo hacen dos de ocho.

- **Dos posteriores de 4 × 3 m:** proporcionan el menor error medio frente + media entre los casos ensayados, aproximadamente 4,36 puntos, y mejoran la zona media a 45,13 % de D50. La ubicación del tratamiento y la del público objetivo son cosas distintas: una superficie posterior puede enviar energía hacia el frente y el centro.

- **Dos posteriores de 6 × 2 m:** su resultado anterior de 5/16 en butacas pasa a 3/12 en el nuevo objetivo. Dos de aquellos cumplimientos pertenecían a V10/V11 con alguna fuente y ahora son controles.

- **F2–V08 permanece dentro del objetivo:** está en la franja media, X = 31 m, Y = +9 m. Su D50 de referencia es 27,98 % y el 21,73 % de su energía está entre 50 y 80 ms. El déficit principal no desaparece al sacar la franja posterior de la optimización.

Ninguna de las geometrías ya ensayadas cumple ambos rangos en las doce combinaciones nuevas a la vez. El cambio de alcance modifica la comparación y las prioridades; no transforma retrospectivamente los cálculos en cumplimiento de una meta distinta sin identificarlo.

## 4. Consecuencia para la próxima búsqueda

1. Puntuar cobertura útil hacia V01–V05 y V08, con los pares de campo prioritarios conservados; retirar V10/V11 del puntaje objetivo.

2. Comparar frente y media por separado, además de su resumen de doce combinaciones. Una mejora frontal no compensa automáticamente un déficit medio.

3. Mantener las posiciones posteriores en las salidas como control, sin exigir que alcancen el mismo D50/C80. Conservar los datos históricos y su antiguo denominador de dieciséis.

4. Examinar los recorridos que aportan 50–80 ms en la zona media, especialmente F2–V08, y probar cómo la geometría puede redistribuirlos junto con los aportes 0–50 ms.

5. Mantener las restricciones geométricas, el material de comparación y los controles de las zonas inferiores. La ubicación de un reflector podrá ser adelantada, intermedia o posterior si beneficia la zona objetivo.

## 5. Referencias y datos

- [Resumen frente/media/posterior CSV](../prediccion/estudio-difusion/reflectores-cobertura/resultados/resumen-frente-media.csv).

- [Resumen frente/media/posterior JSON](../prediccion/estudio-difusion/reflectores-cobertura/resultados/resumen-frente-media.json).

- [Definición del objetivo revisado](../prediccion/estudio-difusion/reflectores-cobertura/objetivo-frente-media.json).

- [Mapa y coordenadas de receptores](MAPA-DE-RECEPTORES-VIRTUALES-PLATEA-ALTA.md).

- [Comparación de siete geometrías, con alcance histórico de dieciséis combinaciones sobre butacas](RESULTADOS-GEOMETRIAS-COBERTURA-PLATEA-ALTA.md).

- [Plan de reflectores](PLAN-DE-ESTUDIO-DE-REFLECTORES-PLATEA-ALTA.md).

- [Documento central de avances](AVANCES-Y-ESTADO-DEL-ESTUDIO-ACUSTICO.md).
