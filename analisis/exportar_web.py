"""Genera la constante compacta que index.html embebe para la sección de fuentes.

La comparación entre fuentes tiene que salir del MISMO pipeline para las dos, o
estaría comparando métodos además de fuentes. Por eso este exportador reanaliza
ambas campañas y emite un solo bloque.

Las constantes IR/REW originales de index.html NO se tocan: siguen alimentando el
resto del informe. Ver README, "Relación con index.html".

Uso:
    py exportar_web.py                 escribe salida/fuentes.js
    py exportar_web.py --embeber       además lo inyecta en index.html
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

SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "salida")
INDEX = os.path.join(sala.RAIZ, "index.html")

# Marcadores que delimitan el bloque generado dentro de index.html
INICIO = "/* === generado por analisis/exportar_web.py — no editar a mano === */"
FIN = "/* === fin del bloque generado === */"

# Parámetros por banda que viajan al navegador
CLAVES = ["t30", "edt", "c50", "c80", "d50", "ts", "inr", "dTot"]


def compactar(nombre):
    """{id: {fc: [t30, edt, c50, c80, d50, ts, inr, dTot]}} más metadatos."""
    irs = analizar_fuente(nombre, verbose=True)
    med = {}
    for m in irs:
        if m["descartada"]:
            continue
        porbanda = {}
        for b in m["bands"]:
            if b["fc"] == 0:
                continue
            porbanda[b["fc"]] = [b.get(k) for k in CLAVES]
        med[m["id"]] = porbanda
    return {
        "nombre": nombre,
        "descripcion": sala.FUENTES[nombre]["descripcion"],
        "n": len(med),
        "nTotal": len(irs),
        "descartadas": sala.DESCARTADAS.get(nombre, []),
        "med": med,
    }


def main():
    consola.preparar()
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--embeber", action="store_true",
                    help="inyectar el bloque en index.html entre los marcadores")
    args = ap.parse_args()

    os.makedirs(SALIDA, exist_ok=True)
    fuentes = {}
    for nombre in sala.FUENTES:
        if not os.path.isdir(sala.FUENTES[nombre]["carpeta_ir"]):
            print(f"{nombre}: sin carpeta de IR, se omite")
            continue
        print(f"\n=== {nombre} ===")
        fuentes[nombre] = compactar(nombre)

    payload = {"claves": CLAVES, "octavas": OCTAVAS, "fuentes": fuentes,
               "zonas": {z: i["nombre"] for z, i in sala.ZONAS.items()},
               "puntosZona": {z: i["pts"] for z, i in sala.ZONAS.items()}}
    js = "const FUENTES = " + json.dumps(payload, ensure_ascii=False,
                                         separators=(",", ":")) + ";"

    destino = os.path.join(SALIDA, "fuentes.js")
    with open(destino, "w", encoding="utf-8") as fh:
        fh.write(js)
    print(f"\n-> {os.path.relpath(destino)}  ({len(js)//1024} KB)")
    for n, f in fuentes.items():
        print(f"   {n}: {f['n']}/{f['nTotal']} mediciones")

    if args.embeber:
        texto = open(INDEX, encoding="utf-8").read()
        bloque = f"{INICIO}\n{js}\n{FIN}"
        if INICIO in texto:
            texto = re.sub(re.escape(INICIO) + r".*?" + re.escape(FIN),
                           lambda _: bloque, texto, flags=re.S)
            accion = "reemplazado"
        else:
            print("\nNo se encontraron los marcadores en index.html.")
            print("Insertar manualmente una vez:\n")
            print(f"  {INICIO}\n  {FIN}\n")
            return 1
        with open(INDEX, "w", encoding="utf-8") as fh:
            fh.write(texto)
        print(f"   bloque {accion} en {os.path.relpath(INDEX)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
