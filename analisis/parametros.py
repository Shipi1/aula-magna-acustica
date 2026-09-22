"""Parámetros acústicos de sala a partir de una respuesta al impulso.

La salida replica el esquema que consume index.html, de modo que el JSON
generado aquí puede reemplazar directamente la constante IR embebida.
"""
import numpy as np

from irlib import (OCTAVAS, BANDA_ANCHA, filtro_octava, lundeby, schroeder,
                   ajustar_T, hallar_t0)

# Ventana del sonido directo, relativa a t0
DIRECTO_MS = (-0.5, 2.5)

# Compuertas de calidad. Un ajuste de decaimiento solo se acepta si la curva de
# Schroeder tiene rango dinámico suficiente para el tramo que se le pide y si la
# regresión es limpia. Sin esto, una banda dominada por ruido devuelve valores
# enormes y sin sentido en vez de declararse inválida.
# EDT se ajusta sobre los primeros 10 dB, que es justamente el tramo donde el
# decaimiento NO es recto: exigirle una correlación alta descartaría ajustes
# buenos y sesgaría la media espacial. Por eso no lleva umbral de |r|.
R_MINIMO = {"edt": None, "t20": 0.98, "t30": 0.98,
            "tEarly": None, "tLate": 0.95}
INR_MINIMO = {"edt": 20.0, "t20": 35.0, "t30": 45.0,
              "tEarly": 25.0, "tLate": 45.0}


def _aceptar(T, r, inr, clave):
    """Devuelve T solo si el ajuste es utilizable; si no, None."""
    if T is None or r is None:
        return None
    r_min = R_MINIMO.get(clave)
    if r_min is not None and abs(r) < r_min:
        return None
    inr_min = INR_MINIMO.get(clave)
    if inr_min is not None and (inr is None or inr < inr_min):
        return None
    return T


def _energia(x, sr, t0, filtfilt=False, fc=BANDA_ANCHA):
    xb = filtro_octava(x, sr, fc, filtfilt=filtfilt)
    return xb, xb[t0:] ** 2


def _claridad(seg, sr, ms):
    """C = 10 log10( E[0,ms] / E[ms,fin] ) sobre la energía ya tratada."""
    k = int(round(ms * 1e-3 * sr))
    if k >= len(seg):
        return None
    temprana, tardia = seg[:k].sum(), seg[k:].sum()
    if temprana <= 0 or tardia <= 0:
        return None
    return float(10 * np.log10(temprana / tardia))


def _definicion(seg, sr):
    k = int(round(0.05 * sr))
    total = seg.sum()
    if total <= 0 or k >= len(seg):
        return None
    return float(100 * seg[:k].sum() / total)


def _tiempo_central(seg, sr):
    total = seg.sum()
    if total <= 0:
        return None
    t = np.arange(len(seg)) / sr
    return float(1000 * (seg * t).sum() / total)


def _directo_total(xb, sr, t0):
    """Energía del sonido directo respecto del total del IR, en dB.

    Es la medida que separa la directividad de la fuente del resto: al estar
    normalizada dentro de cada IR, no la afecta que cada globo suene distinto.
    """
    a = t0 + int(DIRECTO_MS[0] * 1e-3 * sr)
    b = t0 + int(DIRECTO_MS[1] * 1e-3 * sr)
    directo = (xb[max(a, 0):b] ** 2).sum()
    total = (xb[t0:] ** 2).sum()
    if directo <= 0 or total <= 0:
        return None
    return float(10 * np.log10(directo / total))


def _inr(seg, sr, ruido):
    """Relación impulso/ruido: pico de la energía suavizada sobre el ruido."""
    w = max(1, int(0.005 * sr))
    nb = len(seg) // w
    if nb < 2:
        return None
    prom = seg[:nb * w].reshape(nb, w).mean(axis=1)
    return float(10 * np.log10(prom.max() / max(ruido, 1e-300)))


def banda(x, sr, t0, fc, filtfilt=False, puntos_curva=125, paso_curva=0.01):
    """Todos los parámetros de una banda. `fc=0` es banda ancha."""
    xb, e = _energia(x, sr, t0, filtfilt=filtfilt, fc=fc)
    db, ruido, cruce = schroeder(e, sr, truncar=True)
    seg = np.maximum(e[:cruce] - ruido, 0.0)

    inr = _inr(e, sr, ruido)
    edt, r_edt = ajustar_T(db, sr, 0, -10)
    t20, r_t20 = ajustar_T(db, sr, -5, -25)
    t30, r30 = ajustar_T(db, sr, -5, -35)
    t_temprano, r_temp = ajustar_T(db, sr, -5, -15)
    t_tardio, r_tard = ajustar_T(db, sr, -25, -35)

    edt = _aceptar(edt, r_edt, inr, "edt")
    t20 = _aceptar(t20, r_t20, inr, "t20")
    t30 = _aceptar(t30, r30, inr, "t30")
    t_temprano = _aceptar(t_temprano, r_temp, inr, "tEarly")
    t_tardio = _aceptar(t_tardio, r_tard, inr, "tLate")

    # Curva de Schroeder submuestreada para el gráfico
    idx = (np.arange(puntos_curva) * paso_curva * sr).astype(int)
    idx = idx[idx < len(db)]
    curva = [round(float(db[i]), 2) for i in idx]

    r = lambda v, d=3: None if v is None else round(float(v), d)
    return dict(
        fc=fc,
        edt=r(edt), t20=r(t20), t30=r(t30), r30=r(r30, 4),
        c50=r(_claridad(seg, sr, 50), 2), c80=r(_claridad(seg, sr, 80), 2),
        d50=r(_definicion(seg, sr), 1), ts=r(_tiempo_central(seg, sr), 1),
        inr=r(inr, 1), dTot=r(_directo_total(xb, sr, t0), 2),
        tEarly=r(t_temprano), tLate=r(t_tardio), tc=r(cruce / sr),
        curve=curva,
    )


def echo_kraak(x, sr, t0, n, dtau_ms, fc, filtfilt=False, hasta_ms=500):
    """Criterio de eco de Dietsch–Kraak.

    ts(tau) = int t|p|^n / int |p|^n ; EK = max_tau [ts(tau+dt) - ts(tau)] / dt
    Umbrales de audibilidad para el 50 % de los oyentes: 1,0 (palabra) y 1,8 (música).
    """
    xb = filtro_octava(x, sr, fc, filtfilt=filtfilt)
    p = np.abs(xb[t0:t0 + int(hasta_ms * 1e-3 * sr)]) ** n
    if p.sum() <= 0:
        return None
    t = np.arange(len(p)) / sr
    num = np.cumsum(p * t)
    den = np.cumsum(p)
    with np.errstate(divide="ignore", invalid="ignore"):
        ts = np.where(den > 0, num / np.maximum(den, 1e-300), 0.0)
    k = int(round(dtau_ms * 1e-3 * sr))
    if k >= len(ts):
        return None
    ek = (ts[k:] - ts[:-k]) / (dtau_ms * 1e-3)
    return round(float(np.nanmax(ek)), 2)


def curva_etc(x, sr, t0, desde_ms=-5.0, paso_ms=0.5, puntos=610):
    """Curva energía-tiempo en dB relativa al pico, para el gráfico."""
    w = max(1, int(paso_ms * 1e-3 * sr))
    out = []
    for i in range(puntos):
        a = t0 + int((desde_ms + i * paso_ms) * 1e-3 * sr)
        if a < 0:
            out.append(None)
            continue
        out.append((x[a:a + w] ** 2).mean() if a < len(x) else 0.0)
    pico = max(v for v in out if v)
    return [None if v is None else round(float(10 * np.log10(max(v, 1e-300) / pico)), 1)
            for v in out]


def reflexiones(x, sr, t0, umbral_db=6.0, hasta_ms=300, paso_ms=0.25,
                ventana_mediana_ms=10.0):
    """Reflexiones que sobresalen `umbral_db` de la mediana local de la ETC.

    Devuelve una lista de [t_ms, nivel_dB_respecto_al_directo, prominencia_dB].
    La atribución a una superficie concreta NO se hace aquí: requiere un modelo
    geométrico de la sala que todavía no está confirmado (ver README).
    """
    w = max(1, int(paso_ms * 1e-3 * sr))
    nb = int(hasta_ms / paso_ms)
    e = np.array([(x[t0 + i * w: t0 + (i + 1) * w] ** 2).sum() for i in range(nb)])
    db = 10 * np.log10(np.maximum(e, 1e-300))
    directo = db[:int(2.5 / paso_ms)].max()
    db = db - directo

    half = max(1, int(ventana_mediana_ms / paso_ms) // 2)
    out = []
    for i in range(1, nb - 1):
        if db[i] <= db[i - 1] or db[i] < db[i + 1]:
            continue                                  # solo máximos locales
        lo, hi = max(0, i - half), min(nb, i + half + 1)
        vecinos = np.concatenate([db[lo:i], db[i + 1:hi]])
        if len(vecinos) == 0:
            continue
        prom = db[i] - float(np.median(vecinos))
        if prom >= umbral_db:
            out.append([round(i * paso_ms, 2), round(float(db[i]), 1), round(prom, 1)])
    return out


def analizar_ir(x, sr, ident, filtfilt=False, bandas=None):
    """Análisis completo de un IR. Devuelve el dict con el esquema de index.html."""
    bandas = bandas if bandas is not None else OCTAVAS + [BANDA_ANCHA]
    pico, t0 = hallar_t0(x)

    a = t0 + int(DIRECTO_MS[0] * 1e-3 * sr)
    b = t0 + int(DIRECTO_MS[1] * 1e-3 * sr)
    Ld = 10 * np.log10(max((x[max(a, 0):b] ** 2).sum(), 1e-300))

    pre = x[:max(t0 - int(0.005 * sr), 1)]
    cola = x[int(0.9 * len(x)):]
    pre_db = 10 * np.log10(max((pre ** 2).mean(), 1e-300)) if len(pre) > 100 else None
    cola_db = 10 * np.log10(max((cola ** 2).mean(), 1e-300))

    return dict(
        id=ident,
        peakIdx=int(pico), t0=int(t0), peak=round(float(abs(x[pico])), 8),
        Ld=round(float(Ld), 2),
        noisePreDb=None if pre_db is None else round(float(pre_db), 2),
        noiseTailDb=round(float(cola_db), 2),
        durTrasDirecto=round((len(x) - t0) / sr, 3),
        bands=[banda(x, sr, t0, fc, filtfilt=filtfilt) for fc in bandas],
        EKspeech=echo_kraak(x, sr, t0, n=2 / 3, dtau_ms=9, fc=1000, filtfilt=filtfilt),
        EKmusic=echo_kraak(x, sr, t0, n=1, dtau_ms=14, fc=BANDA_ANCHA, filtfilt=filtfilt),
        etc=curva_etc(x, sr, t0),
        refl=reflexiones(x, sr, t0),
    )
