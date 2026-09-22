"""Núcleo de proceso de señal: filtros de octava de fase cero, Lundeby y Schroeder.

Sin dependencias fuera de numpy. Los filtros se aplican en el dominio de la
frecuencia, lo que da fase cero por construcción y evita necesitar scipy.
"""
import numpy as np

# Octavas nominales. fc = 0 se usa como convención para "banda ancha".
OCTAVAS = [63, 125, 250, 500, 1000, 2000, 4000, 8000]
BANDA_ANCHA = 0


def leer(path):
    """Devuelve (muestras mono float64, sr). Requiere soundfile."""
    import soundfile as sf
    x, sr = sf.read(path, always_2d=False, dtype="float64")
    if x.ndim > 1:
        x = x[:, 0]
    return x, sr


def filtro_octava(x, sr, fc, orden=6, filtfilt=False):
    """Pasabanda Butterworth de octava aplicado en frecuencia (fase cero).

    fc = BANDA_ANCHA devuelve la señal sin filtrar.

    `orden` es el del prototipo pasabajos, igual que en scipy.signal.butter.
    `filtfilt=True` aplica |H|² en vez de |H|, replicando un filtrado
    ida y vuelta. El informe original usa fase cero de una pasada, que es
    el valor por defecto (ver README, sección "Validación").
    """
    if fc == BANDA_ANCHA:
        return x
    n = len(x)
    # Se rellena a la siguiente potencia de dos por encima del doble para que
    # la convolución circular no envuelva la cola sobre el comienzo.
    N = 1 << (int(np.ceil(np.log2(n))) + 1)
    X = np.fft.rfft(x, N)
    f = np.fft.rfftfreq(N, 1 / sr)

    f1, f2 = fc / np.sqrt(2), fc * np.sqrt(2)
    f0 = np.sqrt(f1 * f2)
    with np.errstate(divide="ignore", invalid="ignore"):
        # Transformación pasabajos -> pasabanda del prototipo Butterworth
        Om = (f ** 2 - f0 ** 2) / (f * (f2 - f1))
    Om[0] = 1e12                       # DC fuera de banda
    H2 = 1.0 / (1.0 + Om ** (2 * orden))
    mag = H2 if filtfilt else np.sqrt(H2)
    return np.fft.irfft(X * mag, N)[:n]


def lundeby(e, sr, max_iter=8):
    """Punto de cruce entre el decaimiento y el ruido de fondo.

    `e` es la energía instantánea (señal filtrada al cuadrado) a partir del
    sonido directo. Devuelve (muestra_de_cruce, potencia_de_ruido).

    Sigue Lundeby et al. (1995): estimación gruesa del ruido en la cola,
    primer ajuste de pendiente, y luego refinamiento iterativo del intervalo
    de promediado, del nivel de ruido y del cruce.
    """
    n = len(e)
    ruido = e[int(0.9 * n):].mean()

    # (1) Promediado grueso en ventanas de 20 ms
    w = max(1, int(0.02 * sr))
    nb = n // w
    if nb < 5:
        return n, ruido
    prom = e[:nb * w].reshape(nb, w).mean(axis=1)
    t = (np.arange(nb) + 0.5) * w / sr
    pdb = 10 * np.log10(np.maximum(prom, 1e-300))
    pico = int(np.argmax(pdb))
    ndb = 10 * np.log10(max(ruido, 1e-300))

    # (2) Primera regresión entre el pico y 10 dB por encima del ruido
    sobre = np.where(pdb[pico:] < ndb + 10)[0]
    fin = pico + (sobre[0] if len(sobre) else nb - 1)
    if fin <= pico + 2:
        fin = min(nb - 1, pico + 3)
    A, B = np.polyfit(t[pico:fin], pdb[pico:fin], 1)[::-1]
    if B >= 0:
        return n, ruido
    cruce = (ndb - A) / B

    # (3) Iteración
    for _ in range(max_iter):
        w = max(1, int(round(-10 / B * sr / 6)))      # ~6 ventanas por cada 10 dB
        nb2 = n // w
        if nb2 < 5:
            break
        prom = e[:nb2 * w].reshape(nb2, w).mean(axis=1)
        t2 = (np.arange(nb2) + 0.5) * w / sr
        pdb = 10 * np.log10(np.maximum(prom, 1e-300))

        # Ruido medido desde 10 dB (de caída) después del cruce
        s0 = int((cruce + (-10 / B)) * sr)
        s0 = max(min(s0, n - 1), int(0.05 * n))
        ruido = e[s0:].mean() if s0 < n - 1 else e[int(0.9 * n):].mean()
        ndb = 10 * np.log10(max(ruido, 1e-300))

        sel = np.where((pdb > ndb + 5) & (pdb < ndb + 20)
                       & (t2 > t2[int(np.argmax(pdb))]))[0]
        if len(sel) < 3:
            break
        A, B = np.polyfit(t2[sel], pdb[sel], 1)[::-1]
        if B >= 0:
            break
        nuevo = (ndb - A) / B
        if abs(nuevo - cruce) < 1e-4:
            cruce = nuevo
            break
        cruce = nuevo

    return int(np.clip(cruce * sr, 1, n)), ruido


def schroeder(e, sr, truncar=True):
    """Integral de Schroeder en dB, normalizada a 0 dB en el origen.

    Con `truncar`, corta en el cruce de Lundeby y resta el ruido (Chu), que es
    lo que exige ISO 3382 para que T30 no se aplane sobre el piso de ruido.
    Devuelve (curva_dB, potencia_ruido, muestra_de_cruce).
    """
    n = len(e)
    if truncar:
        c, ruido = lundeby(e, sr)
        c = int(np.clip(c, int(0.02 * sr), n))
        seg = np.maximum(e[:c] - ruido, 0.0)
    else:
        c, ruido = n, 0.0
        seg = e
    acum = np.cumsum(seg[::-1])[::-1]
    total = max(acum[0], 1e-300)
    with np.errstate(divide="ignore"):
        db = 10 * np.log10(np.maximum(acum / total, 1e-300))
    return db, ruido, c


def ajustar_T(db, sr, desde, hasta):
    """Tiempo de reverberación por mínimos cuadrados entre dos niveles en dB.

    Devuelve (T en segundos, coeficiente de correlación r). (None, None) si el
    tramo pedido no existe en la curva.
    """
    i0 = int(np.argmax(db <= desde))
    i1 = int(np.argmax(db <= hasta))
    if i1 <= i0 or i1 == 0:
        return None, None
    t = np.arange(i0, i1) / sr
    y = db[i0:i1]
    if len(t) < 4:
        return None, None
    A, B = np.polyfit(t, y, 1)[::-1]
    if B >= 0:
        return None, None
    return -60.0 / B, float(np.corrcoef(t, y)[0, 1])


def hallar_t0(x, frac=0.2):
    """Origen del IR según ISO 3382: primera muestra antes del pico que supera
    `frac` del pico. Devuelve (indice_pico, indice_t0).
    """
    p = int(np.argmax(np.abs(x)))
    umbral = frac * abs(x[p])
    i = p
    while i > 0 and abs(x[i - 1]) > umbral:
        i -= 1
    return p, i
