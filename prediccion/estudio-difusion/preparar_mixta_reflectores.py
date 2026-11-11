"""Comparación a igual área: cuatro anteriores más dos posteriores 6x2 m."""
import json,itertools
import preparar_cobertura_reflectores as p
def main():
    cases=json.loads((p.O/'variantes.json').read_text())
    panels=cases['central5'][:4]+cases['retornos_compactos2']
    assert not any(p.overlaps(a,b) for a,b in itertools.combinations(panels,2))
    assert not any(p.blocks(d,s,r) for d in panels for s in p.S.values() for r in p.R.values())
    cases['mixta6']=panels;p.g.save('variantes.json',cases);p.g.export('mixta6',panels)
if __name__=='__main__':main()
