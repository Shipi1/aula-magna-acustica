"""Lector de los exportes RT60 en texto de REW.

Ojo: los exportes de la sesión de parlante usan coma decimal en la cabecera
("Sweep level: -12,0 dBFS") y punto decimal en las filas de datos, mientras que
los del globo usan punto en ambas. El parser solo interpreta las filas.
"""
import glob
import os
import re

# Columnas después de (freq, BW), según la línea "Format is ..." de REW
COLUMNAS = ["edt", "r_edt", "t20", "r_t20", "t30", "r_t30", "topt", "r_topt",
            "toptStart", "toptEnd", "t60m", "filtro", "c50", "c80", "d50", "ts"]

TERCIOS = [50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000,
           1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000]

OCTAVA_DE_TERCIOS = {
    63: [50, 63, 80], 125: [100, 125, 160], 250: [200, 250, 315],
    500: [400, 500, 630], 1000: [800, 1000, 1250], 2000: [1600, 2000, 2500],
    4000: [3150, 4000, 5000], 8000: [6300, 8000, 10000],
}


def identificador(path):
    """'RT60_Parlatnte F1-P2 10_54_12.txt' -> 'F1-P2'. Tolera el typo 'Parlatnte'."""
    m = re.search(r"(F\d)\s*-?\s*(P\d)", os.path.basename(path))
    if not m:
        raise ValueError(f"no se pudo deducir el identificador de {path!r}")
    return f"{m.group(1)}-{m.group(2)}"


def leer_archivo(path):
    """Devuelve (cabecera dict, filas lista de dicts)."""
    texto = open(path, encoding="utf-8", errors="replace").read()
    cabecera, filas = {}, []
    for linea in texto.splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("Format is"):
            continue
        if not re.match(r"^\d", linea):
            m = re.match(r"^([A-Za-z ]+):\s*(.*)$", linea)
            if m:
                cabecera[m.group(1).strip()] = m.group(2).strip()
            continue
        partes = [p.strip() for p in linea.split(",")]
        fila = {"f": float(partes[0]), "bw": partes[1]}
        for i, nombre in enumerate(COLUMNAS):
            v = partes[2 + i]
            fila[nombre] = v if nombre == "filtro" else float(v)
        filas.append(fila)
    return cabecera, filas


def leer_carpeta(carpeta):
    """Devuelve (datos {id: {f: fila}}, cabeceras {id: dict})."""
    datos, cabeceras = {}, {}
    for p in sorted(glob.glob(os.path.join(carpeta, "*.txt"))):
        ident = identificador(p)
        cab, filas = leer_archivo(p)
        datos[ident] = {fila["f"]: fila for fila in filas}
        cabeceras[ident] = cab
    return datos, cabeceras


def valor(datos, ident, f, clave, r_min=None):
    """Valor de un tercio de octava, o None si el ajuste no es utilizable.

    REW escribe 0.000 cuando la regresión falla. `r_min` descarta además los
    ajustes cuyo |r| queda por debajo del umbral pedido.
    """
    fila = datos.get(ident, {}).get(f)
    if fila is None:
        return None
    v = fila[clave]
    if clave in ("edt", "t20", "t30", "topt"):
        if not v > 0:
            return None
        if r_min is not None and abs(fila["r_" + clave]) < r_min:
            return None
    return v * 1000 if clave == "ts" else v


def valor_octava(datos, ident, fc, clave, r_min=None):
    """Promedio de los tres tercios que componen la octava."""
    vs = [valor(datos, ident, f, clave, r_min) for f in OCTAVA_DE_TERCIOS[fc]]
    vs = [v for v in vs if v is not None]
    return sum(vs) / len(vs) if vs else None


def a_filas_compactas(datos):
    """Formato compacto que consume index.html: [f, edt, t20, t30, c50, c80, d50, ts]."""
    out = {}
    for ident, porfrec in datos.items():
        out[ident] = [[f, r["edt"], r["t20"], r["t30"], r["c50"], r["c80"],
                       r["d50"], r["ts"]]
                      for f, r in sorted(porfrec.items())]
    return out
