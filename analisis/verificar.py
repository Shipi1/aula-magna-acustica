"""Controles de integridad y de calidad sobre los datos crudos.

Uso:
    py verificar.py duplicados     tomas repetidas entre archivos
    py verificar.py inr            relación impulso/ruido contra los mínimos ISO
    py verificar.py ajustes        ajustes de decaimiento fallidos en los exportes REW
    py verificar.py todo
"""
import glob
import os
import sys

import numpy as np

import rew
import consola
import sala
from irlib import OCTAVAS, filtro_octava, hallar_t0, leer, lundeby


def _ident_wav(path):
    import re
    m = re.search(r"(F\d)\s*-?\s*(P\d)", os.path.basename(path))
    return f"{m.group(1)}-{m.group(2)}"


def duplicados(dur_s=1.5, umbral_r=0.99):
    """Detecta tomas repetidas comparando el audio alineado en t0.

    Un hash del archivo NO alcanza: dos exportes de la misma toma pueden diferir
    en metadatos, en el recorte inicial o en la recuantización. Aquí se alinea
    por t0 y se correlaciona una ventana fija.
    """
    print("=" * 78)
    print("TOMAS DUPLICADAS")
    print("=" * 78)
    hallados = 0
    for nombre, cfg in sala.FUENTES.items():
        rutas = sorted(glob.glob(os.path.join(cfg["carpeta_ir"], "*.wav")))
        if not rutas:
            print(f"\n{nombre}: sin archivos en {cfg['carpeta_ir']}")
            continue
        ids, segs = [], []
        for p in rutas:
            x, sr = leer(p)
            _, t0 = hallar_t0(x)
            n = int(dur_s * sr)
            s = x[t0:t0 + n]
            if len(s) < n:
                s = np.pad(s, (0, n - len(s)))
            pico = np.abs(s).max() or 1.0
            ids.append(_ident_wav(p))
            segs.append(s / pico)

        print(f"\n{nombre}: {len(ids)} archivos")
        pares = []
        for a in range(len(ids)):
            for b in range(a + 1, len(ids)):
                r = float(np.corrcoef(segs[a], segs[b])[0, 1])
                if abs(r) >= umbral_r:
                    pares.append((ids[a], ids[b], r))
        if not pares:
            print("  sin duplicados")
        for a, b, r in pares:
            hallados += 1
            print(f"  {a} y {b} son la misma toma (r = {r:.6f})")
        otros = [abs(float(np.corrcoef(segs[a], segs[b])[0, 1]))
                 for a in range(len(ids)) for b in range(a + 1, len(ids))
                 if (ids[a], ids[b]) not in [(x[0], x[1]) for x in pares]]
        if otros:
            print(f"  r máximo entre tomas distintas: {max(otros):.3f}")
    if hallados:
        print(f"\n{hallados} par(es) duplicado(s). Revisar sala.DESCARTADAS.")
    return hallados


def inr():
    """Relación impulso/ruido por octava contra los mínimos de ISO 3382."""
    print("=" * 84)
    print("RELACIÓN IMPULSO/RUIDO POR OCTAVA")
    print(f"mínimos ISO 3382: T30 >= {sala.INR_MINIMO['t30']:.0f} dB, "
          f"T20 >= {sala.INR_MINIMO['t20']:.0f} dB")
    print("=" * 84)
    for nombre, cfg in sala.FUENTES.items():
        rutas = sorted(glob.glob(os.path.join(cfg["carpeta_ir"], "*.wav")))
        fuera = set(sala.DESCARTADAS.get(nombre, []))
        rutas = [p for p in rutas if _ident_wav(p) not in fuera]
        if not rutas:
            continue
        print(f"\n{nombre}  ({len(rutas)} tomas)")
        print(f"{'Octava':>8} {'mín':>8} {'mediana':>9} {'máx':>8}   {'sirve para':>12}")
        print("-" * 52)
        for fc in OCTAVAS:
            vals = []
            for p in rutas:
                x, sr = leer(p)
                _, t0 = hallar_t0(x)
                xb = filtro_octava(x, sr, fc)
                e = xb[t0:] ** 2
                _, ruido = lundeby(e, sr)
                w = max(1, int(0.005 * sr))
                nb = len(e) // w
                prom = e[:nb * w].reshape(nb, w).mean(axis=1)
                vals.append(10 * np.log10(prom.max() / max(ruido, 1e-300)))
            vals.sort()
            if vals[0] >= sala.INR_MINIMO["t30"]:
                veredicto = "T30"
            elif vals[0] >= sala.INR_MINIMO["t20"]:
                veredicto = "solo T20"
            else:
                veredicto = "ninguno"
            print(f"{fc:8d} {vals[0]:8.1f} {vals[len(vals)//2]:9.1f} {vals[-1]:8.1f}   "
                  f"{veredicto:>12}")


def ajustes():
    """Ajustes de decaimiento nulos o de baja calidad en los exportes de REW."""
    print("=" * 84)
    print(f"AJUSTES DE DECAIMIENTO EN LOS EXPORTES REW  (umbral |r| >= {sala.R_MINIMO})")
    print("=" * 84)
    print(f"{'Tercio':>8} |" + "".join(f"{n:>22}" for n in sala.FUENTES))
    print(f"{'':>8} |" + "".join(f"{'T30 ok':>11}{'T20 ok':>11}" for _ in sala.FUENTES))
    print("-" * 84)
    cache = {}
    for nombre, cfg in sala.FUENTES.items():
        if os.path.isdir(cfg["carpeta_rt60"]):
            cache[nombre] = rew.leer_carpeta(cfg["carpeta_rt60"])[0]
    totales = {n: [0, 0, 0] for n in cache}
    for f in rew.TERCIOS:
        fila = f"{f:8.0f} |"
        for nombre, datos in cache.items():
            ids = [i for i in sala.identificadores(nombre) if i in datos]
            n30 = sum(1 for i in ids
                      if rew.valor(datos, i, f, "t30", sala.R_MINIMO) is not None)
            n20 = sum(1 for i in ids
                      if rew.valor(datos, i, f, "t20", sala.R_MINIMO) is not None)
            totales[nombre][0] += n30
            totales[nombre][1] += n20
            totales[nombre][2] += len(ids)
            fila += f"{n30:>6}/{len(ids):<4}{n20:>6}/{len(ids):<4}"
        print(fila)
    print("-" * 84)
    fila = f"{'TOTAL':>8} |"
    for nombre, (a, b, c) in totales.items():
        fila += f"{a:>6}/{c:<4}{b:>6}/{c:<4}"
    print(fila)


def main():
    consola.preparar()
    orden = sys.argv[1] if len(sys.argv) > 1 else "todo"
    if orden in ("duplicados", "todo"):
        duplicados()
        print()
    if orden in ("ajustes", "todo"):
        ajustes()
        print()
    if orden in ("inr", "todo"):
        inr()
    if orden not in ("duplicados", "ajustes", "inr", "todo"):
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
