# Prueba de absorción efectiva de paredes

Esta entrega continúa las simulaciones anteriores: A y C se habían calculado con F1 a 1 kHz; B, con F1 y F2 por separado en cinco bandas. La revisión posterior de rugosidad había sido documental, sin modificar materiales ni ejecutar otra simulación.

Ahora se ejecutó una búsqueda de absorción en **05_muros, 10_laterales_altos y 11_fondo_alto**, partiendo de B. La geometría, la dispersión y los demás materiales se conservaron. El nuevo material se llama **AM_Muros_ajuste_efectivo_NO_MEDIDO**: su valor ajustado no representa una medición del concreto.

Abrir **D_muros_ajuste_1kHz.proj** en I-Simpa. En Results → SPPS se incluyen:

- Ajuste-1kHz-F1-1200k: confirmación del objetivo con 1.200.000 partículas.
- Validacion-F1-300k y Validacion-F2-300k: siete bandas, nueve receptores y 300.000 partículas por banda.

El objetivo se definió como T20 de P1–F1 a 1000 Hz = 1,70 s, con tolerancia ±0,05 s. No se ajustó el promedio de la sala ni se impuso 1,7 s a todo el espectro. T20 y T30 ya son estimaciones extrapoladas a una caída de 60 dB.

El mismo incremento de absorción se aplicó a la curva inicial completa antes de comprobar otras bandas; no se reajustó cada frecuencia. La configuración activa del proyecto permite repetir la validación con F1 y siete bandas a 300.000 partículas. Para repetir la confirmación, seleccionar solo 1000 Hz y 1.200.000 partículas. La semilla configurada es 20261019. F2 se calcula por separado.

Leer **INFORME-AJUSTE-MUROS.md**, **ajuste-seleccionado.json** y **comparacion-REW.json** para el resultado, el procedimiento y sus límites. La estructura del proyecto se comprueba por ZIP/XML y referencias; no se ha comprobado su apertura en la interfaz gráfica. Los resultados proceden del motor SPPS instalado, no de una predicción por Sabine.

Los proyectos anteriores se conservan. No se ha incorporado todavía tratamiento nuevo de platea alta ni se ha modelado la directividad del line array.
