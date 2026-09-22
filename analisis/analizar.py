"""Pipeline principal: de datos/ a analisis/salida/*.json

Uso:
    py analizar.py                      analiza todas las fuentes
    py analizar.py --fuente Globo       solo una
    py analizar.py --comparar           tabla comparativa entre fuentes
    py analizar.py --salida otra/ruta   cambia el destino

Genera, por cada fuente:
    ir_<fuente>.json     análisis propio de los WAV (esquema de index.html)
    rew_<fuente>.json    exportes RT60 de REW en formato compacto
    resumen_<fuente>.json  promedios espaciales por octava y por zona
"""
import argparse
import glob
import json
import os
import re
import sys
import time

import rew
import consola
import sala
from irlib import OCTAVAS, leer
from parametros import analizar_ir

SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "salida")


def _ident(path):
    m = re.search(r"(F\d)\s*-?\s*(P\d)", os.path.basename(path))
    if not m:
        raise ValueError(f"identificador no deducible: {path!r}")
    return f"{m.group(1)}-{m.group(2)}"


def promedio(vals):
    vals = [v for v in vals if v is not None]
    return sum(vals) / len(vals) if vals else None


def desviacion(vals):
    vals = [v for v in vals if v is not None]
    if len(vals) < 2:
        return None
    m = sum(vals) / len(vals)
    return (sum((v - m) ** 2 for v in vals) / len(vals)) ** 0.5


def analizar_fuente(nombre, filtfilt=False, verbose=True):
    """Analiza los WAV de una fuente. Devuelve la lista de dicts por medición."""
    cfg = sala.FUENTES[nombre]
    rutas = sorted(glob.glob(os.path.join(cfg["carpeta_ir"], "*.wav")))
    if not rutas:
        raise SystemExit(f"no hay WAV en {cfg['carpeta_ir']}")
    fuera = set(sala.DESCARTADAS.get(nombre, []))
    out = []
    for i, p in enumerate(rutas, 1):
        ident = _ident(p)
        x, sr = leer(p)
        t = time.time()
        m = analizar_ir(x, sr, ident, filtfilt=filtfilt)
        m["fuente"] = nombre
        m["zona"] = sala.zona_de(ident)
        m["distancia"] = round(sala.distancia(ident), 2)
        m["descartada"] = ident in fuera
        out.append(m)
        if verbose:
            marca = "  (descartada)" if ident in fuera else ""
            print(f"  [{i:2d}/{len(rutas)}] {ident}  {time.time()-t:4.1f} s{marca}")
    return out


def resumen(irs, datos_rew, nombre):
    """Promedios espaciales por octava y por zona, con las descartadas fuera."""
    utiles = [m for m in irs if not m["descartada"]]
    por_id = {m["id"]: m for m in utiles}
    banda = lambda m, fc: next((b for b in m["bands"] if b["fc"] == fc), {})

    por_octava = {}
    for fc in OCTAVAS:
        fila = {}
        for k in ("t30", "edt", "c50", "c80", "d50", "ts", "inr"):
            vals = [banda(m, fc).get(k) for m in utiles]
            fila[k] = {"media": promedio(vals), "sd": desviacion(vals),
                       "n": sum(1 for v in vals if v is not None)}
        if datos_rew:
            vals = [rew.valor_octava(datos_rew, i, fc, "t30", sala.R_MINIMO)
                    for i in por_id]
            fila["t30_rew"] = {"media": promedio(vals),
                               "n": sum(1 for v in vals if v is not None)}
        por_octava[fc] = fila

    def mid(m, k):
        fs = [500, 1000, 2000] if k in ("c80", "c50") else [500, 1000]
        return promedio([banda(m, f).get(k) for f in fs])

    por_zona = {}
    for z, info in sala.ZONAS.items():
        ms = [m for m in utiles if m["zona"] == z]
        por_zona[z] = {
            "nombre": info["nombre"], "n": len(ms),
            "puntos": sorted({m["id"].split("-")[1] for m in ms}),
            **{k: promedio([mid(m, k) for m in ms])
               for k in ("t30", "edt", "c50", "c80", "d50", "ts")},
        }

    globales = {k: promedio([mid(m, k) for m in utiles])
                for k in ("t30", "edt", "c50", "c80", "d50", "ts")}
    t = lambda fc: promedio([banda(m, fc).get("t30") for m in utiles])
    if all(t(f) for f in (125, 250, 500, 1000)):
        globales["bass_ratio"] = (t(125) + t(250)) / (t(500) + t(1000))
    globales["sd_t30"] = desviacion([mid(m, "t30") for m in utiles])

    return {"fuente": nombre, "descripcion": sala.FUENTES[nombre]["descripcion"],
            "n_total": len(irs), "n_utiles": len(utiles),
            "descartadas": sala.DESCARTADAS.get(nombre, []),
            "globales": globales, "por_octava": por_octava, "por_zona": por_zona}


def comparar(resumenes):
    """Tabla comparativa entre fuentes sobre los parámetros mid."""
    nombres = list(resumenes)
    if len(nombres) < 2:
        print("hace falta más de una fuente para comparar")
        return
    a, b = nombres[0], nombres[1]
    print("=" * 78)
    print(f"COMPARACIÓN  {a}  vs  {b}")
    print("=" * 78)
    etiquetas = {"t30": "T30,mid [s]", "edt": "EDT,mid [s]", "c50": "C50 (500-2k) [dB]",
                 "c80": "C80 (500-2k) [dB]", "d50": "D50 (500-1k) [%]",
                 "ts": "Ts (500-1k) [ms]", "bass_ratio": "Bass ratio"}
    print(f"{'Parámetro':>20} | {a:>10} | {b:>10} | {'dif':>9}")
    print("-" * 78)
    for k, lab in etiquetas.items():
        va = resumenes[a]["globales"].get(k)
        vb = resumenes[b]["globales"].get(k)
        if va is None or vb is None:
            continue
        d = 1 if k in ("c50", "c80", "d50", "ts") else 2
        print(f"{lab:>20} | {va:10.{d}f} | {vb:10.{d}f} | {va-vb:+9.{d}f}")
    print()
    print(f"{'T30 por octava':>20} | {a:>10} | {b:>10} | {'dif':>9} | {'n':>7}")
    print("-" * 78)
    for fc in OCTAVAS:
        fa = resumenes[a]["por_octava"][fc]["t30"]
        fb = resumenes[b]["por_octava"][fc]["t30"]
        if fa["media"] is None or fb["media"] is None:
            continue
        print(f"{fc:>20} | {fa['media']:10.2f} | {fb['media']:10.2f} | "
              f"{fa['media']-fb['media']:+9.2f} | {fa['n']:3d}/{fb['n']:<3d}")


def main():
    consola.preparar()
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fuente", action="append", choices=list(sala.FUENTES),
                    help="analizar solo esta fuente (repetible)")
    ap.add_argument("--salida", default=SALIDA, help="carpeta de destino")
    ap.add_argument("--filtfilt", action="store_true",
                    help="aplicar |H|^2 en los filtros de octava (ida y vuelta)")
    ap.add_argument("--comparar", action="store_true",
                    help="imprimir la tabla comparativa entre fuentes")
    args = ap.parse_args()

    os.makedirs(args.salida, exist_ok=True)
    fuentes = args.fuente or list(sala.FUENTES)
    resumenes = {}

    for nombre in fuentes:
        cfg = sala.FUENTES[nombre]
        print(f"\n=== {nombre} ===")
        if not os.path.isdir(cfg["carpeta_ir"]):
            print(f"  sin carpeta {cfg['carpeta_ir']}, se omite")
            continue

        irs = analizar_fuente(nombre, filtfilt=args.filtfilt)
        destino = os.path.join(args.salida, f"ir_{nombre.lower()}.json")
        with open(destino, "w", encoding="utf-8") as fh:
            json.dump(irs, fh, ensure_ascii=False, separators=(",", ":"))
        print(f"  -> {os.path.relpath(destino)}  ({os.path.getsize(destino)//1024} KB)")

        datos_rew = {}
        if os.path.isdir(cfg["carpeta_rt60"]):
            datos_rew, _ = rew.leer_carpeta(cfg["carpeta_rt60"])
            destino = os.path.join(args.salida, f"rew_{nombre.lower()}.json")
            with open(destino, "w", encoding="utf-8") as fh:
                json.dump(rew.a_filas_compactas(datos_rew), fh,
                          ensure_ascii=False, separators=(",", ":"))
            print(f"  -> {os.path.relpath(destino)}  "
                  f"({os.path.getsize(destino)//1024} KB, {len(datos_rew)} mediciones)")

        res = resumen(irs, datos_rew, nombre)
        resumenes[nombre] = res
        destino = os.path.join(args.salida, f"resumen_{nombre.lower()}.json")
        with open(destino, "w", encoding="utf-8") as fh:
            json.dump(res, fh, ensure_ascii=False, indent=1)
        print(f"  -> {os.path.relpath(destino)}")
        g = res["globales"]
        print(f"  T30,mid {g['t30']:.2f} s   EDT,mid {g['edt']:.2f} s   "
              f"C80 {g['c80']:+.1f} dB   D50 {g['d50']:.0f} %   "
              f"({res['n_utiles']}/{res['n_total']} tomas)")

    if args.comparar and len(resumenes) > 1:
        print()
        comparar(resumenes)
    return 0


if __name__ == "__main__":
    sys.exit(main())
