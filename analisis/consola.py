"""La consola de Windows no siempre viene en UTF-8 y se come los acentos.

Todos los puntos de entrada llaman a `preparar()` antes de imprimir.
"""
import sys


def preparar():
    for flujo in (sys.stdout, sys.stderr):
        enc = (getattr(flujo, "encoding", "") or "").lower().replace("-", "")
        if enc != "utf8":
            try:
                flujo.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass
