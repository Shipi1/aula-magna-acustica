"""Configuración del recinto y de la campaña de medición.

Las coordenadas vienen de la constante XY de index.html, trazadas sobre el plano
ARQ-01. Formato: [X, Y, Z en metros, px, py en píxeles de la imagen del plano].
El origen y la orientación son los del plano, no los del escenario.
"""
import math
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(RAIZ, "datos")

FUENTES = {
    "Parlante": {
        "carpeta_ir": os.path.join(DATOS, "Sweep IR (WAV)"),
        "carpeta_rt60": os.path.join(DATOS, "Parlante (Sine sweep)"),
        "descripcion": "Barrido logarítmico de 256k, 1 pasada, 48 kHz. IR deconvolucionado en REW.",
    },
    "Globo": {
        "carpeta_ir": os.path.join(DATOS, "Globo IR (WAV)"),
        "carpeta_rt60": os.path.join(DATOS, "Globo (Explosion)"),
        "descripcion": "Explosión de globo, fuente cuasi-omnidireccional. Grabación directa.",
    },
}

# [X, Y, Z, px, py]
XY = {
    "F1": [5.36, 0.02, 1.50, 360, 694],
    "F2": [5.60, 4.72, 1.50, 373, 444],
    "P1": [18.16, 9.40, 1.63, 1041, 195],
    "P2": [15.73, 4.53, 1.54, 912, 454],
    "P3": [27.42, -4.55, 1.95, 1534, 937],
    "P4": [18.16, -9.72, 1.63, 1041, 1212],
    "P5": [33.50, 0.34, 2.00, 1857, 677],
    "P6": [30.96, 4.30, 2.00, 1722, 466],
    "P7": [19.57, -4.53, 1.68, 1116, 936],
    "P8": [26.66, -8.14, 6.50, 1493, 1128],
    "P9": [26.59, 8.01, 6.50, 1490, 269],
}

ZONAS = {
    "piso":   {"nombre": "Piso abierto",    "pts": ["P1", "P2", "P4", "P7"]},
    "balcon": {"nombre": "Bajo balcón",     "pts": ["P3", "P5", "P6"]},
    "grad":   {"nombre": "Gradería inferior", "pts": ["P8", "P9"]},
}

# Condiciones ambientales supuestas (ver sección "Condiciones" del informe)
TEMPERATURA_C = 18.0
HUMEDAD_REL = 57.0
VELOCIDAD_SONIDO = 342.0
VOLUMEN_M3 = 8000.0

# Umbral de calidad para aceptar un ajuste de decaimiento de REW.
R_MINIMO = 0.98

# INR mínimo que exige ISO 3382 para cada parámetro
INR_MINIMO = {"t30": 45.0, "t20": 35.0}

# --- Tomas descartadas --------------------------------------------------------
# Pares de archivos cuyo audio es la misma toma (ver `verificar.py duplicados`).
# No se sabe cuál etiqueta es la correcta, así que se excluye una de cada par de
# los promedios; cambiar esta lista si las notas de campo lo aclaran.
DESCARTADAS = {
    "Globo": ["F1-P3", "F2-P6"],
    "Parlante": [],
}

# --- Modelo geométrico para atribuir reflexiones a superficies ----------------
# SIN CONFIRMAR. Los planos deducidos de la geometría publicada en el informe no
# son consistentes con las coordenadas de XY (P5 en X=33,5 cae por fuera del muro
# trasero implícito), así que la atribución de superficies queda desactivada.
# Para habilitarla: definir aquí los planos como (nombre, normal, punto) en el
# mismo sistema que XY y escribir el modelo de fuentes imagen de primer orden.
PLANOS = None


def distancia(ident):
    """Distancia fuente-receptor en 3D, en metros. `ident` con formato 'F1-P5'."""
    s, r = ident.split("-")
    a, b = XY[s], XY[r]
    return math.dist(a[:3], b[:3])


def angulo_fuera_de_eje(ident):
    """Ángulo respecto del eje +X de la sala, visto desde la fuente, en grados.

    Es una aproximación: supone que ambas fuentes apuntan a lo largo del eje.
    """
    s, r = ident.split("-")
    a, b = XY[s][:3], XY[r][:3]
    v = [b[i] - a[i] for i in range(3)]
    norma = math.dist([0, 0, 0], v)
    return math.degrees(math.acos(v[0] / norma))


def zona_de(ident):
    """Clave de zona de un identificador 'F1-P5'."""
    p = ident.split("-")[1]
    for z, info in ZONAS.items():
        if p in info["pts"]:
            return z
    raise KeyError(f"{ident} no pertenece a ninguna zona")


def identificadores(fuente):
    """Identificadores utilizables de una fuente, ya sin las tomas descartadas."""
    todos = [f"{s}-P{p}" for s in ("F1", "F2") for p in range(1, 10)]
    fuera = set(DESCARTADAS.get(fuente, []))
    return [i for i in todos if i not in fuera]
