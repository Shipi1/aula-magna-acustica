"""Contrasta el análisis de este script contra los valores embebidos en index.html.

Es la prueba de regresión del pipeline: si el script reproduce los números que ya
están publicados, se puede confiar en él para datos nuevos.

Uso:
    py validar.py                 tabla de diferencias por octava
    py validar.py --detalle       además, diferencias medición por medición
    py validar.py --tol 0.02      falla si T30 se desvía más que esto (segundos)
"""
import argparse
import json
import os
import re
import sys

import consola
import sala
from analizar import analizar_fuente, promedio
from irlib import OCTAVAS

INDEX = os.path.join(sala.RAIZ, "index.html")

# Bandas sobre las que se juzga la validación. Se excluyen 63 Hz y 8 kHz: en los
# extremos el resultado depende del faldón exacto del filtro de octava y del
# tratamiento del ruido, y el análisis original no está documentado a ese nivel.
CENTRALES = [125, 250, 500, 1000, 2000, 4000]


def ir_de_index_html(path=INDEX):
    """Extrae la constante IR embebida en index.html."""
    texto = open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r"^const IR = (\[.*?\]);\s*$", texto, re.M | re.S)
    if not m:
        raise SystemExit("no se encontró 'const IR = [...]' en index.html")
    return {d["id"]: d for d in json.loads(m.group(1))}


def main():
    consola.preparar()
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--detalle", action="store_true")
    ap.add_argument("--tol", type=float, default=0.01,
                    help="tolerancia en T30 [s] sobre las bandas centrales (125-4k)")
    ap.add_argument("--filtfilt", action="store_true")
    args = ap.parse_args()

    ref = ir_de_index_html()
    print(f"index.html: {len(ref)} mediciones embebidas")
    print("Analizando los WAV de Parlante con este script...\n")
    mios = {m["id"]: m for m in analizar_fuente("Parlante", filtfilt=args.filtfilt)}

    faltan = set(ref) - set(mios)
    if faltan:
        print(f"aviso: en index.html pero no en datos/: {sorted(faltan)}")

    banda = lambda m, fc: next((b for b in m["bands"] if b["fc"] == fc), {})
    comunes = sorted(set(ref) & set(mios))

    print()
    print("=" * 86)
    print("PROMEDIO ESPACIAL POR OCTAVA:  este script  vs  index.html")
    print("=" * 86)
    print(f"{'Octava':>8} | {'T30 script':>11} {'T30 html':>10} {'dif':>8} | "
          f"{'EDT script':>11} {'EDT html':>10} {'dif':>8}")
    print("-" * 86)
    peor, peor_banda = 0.0, None
    for fc in OCTAVAS:
        a30 = promedio([banda(mios[i], fc).get("t30") for i in comunes])
        b30 = promedio([banda(ref[i], fc).get("t30") for i in comunes])
        ae = promedio([banda(mios[i], fc).get("edt") for i in comunes])
        be = promedio([banda(ref[i], fc).get("edt") for i in comunes])
        if a30 is None or b30 is None:
            continue
        d30 = a30 - b30
        # Las bandas extremas dependen mucho del faldón del filtro y no entran
        # en el criterio de aprobación; se muestran igual, marcadas.
        central = fc in CENTRALES
        if central and abs(d30) > peor:
            peor, peor_banda = abs(d30), fc
        de = "" if (ae is None or be is None) else f"{ae-be:+8.3f}"
        print(f"{fc:8d} | {a30:11.3f} {b30:10.3f} {d30:+8.3f} | "
              f"{(ae or 0):11.3f} {(be or 0):10.3f} {de:>8}"
              f"{'' if central else '   (fuera del criterio)'}")

    if args.detalle:
        print()
        print("=" * 86)
        print("POR MEDICIÓN (T30 a 500-1k Hz)")
        print("=" * 86)
        print(f"{'ID':>8} | {'script':>8} {'html':>8} {'dif':>8}")
        print("-" * 86)
        for i in comunes:
            a = promedio([banda(mios[i], f).get("t30") for f in (500, 1000)])
            b = promedio([banda(ref[i], f).get("t30") for f in (500, 1000)])
            if a is None or b is None:
                continue
            print(f"{i:>8} | {a:8.3f} {b:8.3f} {a-b:+8.3f}")

    print()
    print("-" * 86)
    ok = peor <= args.tol
    print(f"Desviación máxima de T30 en {CENTRALES[0]}-{CENTRALES[-1]} Hz: "
          f"{peor:.3f} s en la banda de {peor_banda} Hz  "
          f"(tolerancia {args.tol:.3f} s)  ->  {'OK' if ok else 'FALLA'}")
    if not ok:
        print("\nEl pipeline dejó de reproducir los valores publicados. Revisar\n"
              "irlib.filtro_octava y irlib.lundeby antes de confiar en la salida.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
