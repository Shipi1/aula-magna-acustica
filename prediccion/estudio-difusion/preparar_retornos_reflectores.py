"""Variante adaptativa: retorno reflectante desplazado respecto del muro posterior."""
import json,itertools
import numpy as np
import preparar_cobertura_reflectores as p
def main():
    candidates=[];tested=0
    for x,y,z in itertools.product((32.,34.,36.,38.),(-9.,-7.,7.,9.),(8.6,9.2,10.)):
        q=np.array([x,y,z])
        if not p.g.inside(q):continue
        for target,source in itertools.product(['P8','P9']+p.SEATS,[p.S['F1'],p.S['F2'],(p.S['F1']+p.S['F2'])/2]):
            tested+=1;panel=p.g.panel(q,p.R[target],source)
            if abs(panel['normal'][0])<.65:continue
            routes=p.paths(panel)
            if not routes:continue
            cc=p.g.corners(panel)
            if not all(p.g.inside(c) for c in cc):continue
            if any(not p.g.visible(a,b) for a,b in itertools.combinations(cc,2)):continue
            if any(p.blocks(panel,s,r) for s in p.S.values() for r in p.R.values()):continue
            if any(np.linalg.norm(np.maximum(abs((r-q)@p.axes(panel).T)-p.half(panel),0))<.32 for r in p.R.values()):continue
            panel.update(candidato=f'R{len(candidates)+1:04}',objetivo_de_orientacion=target,fuente_de_orientacion=source.tolist(),rutas_utiles=routes)
            candidates.append(panel)
    assert candidates
    p.g.save('candidatos-retornos.json',dict(orientaciones_exploradas=tested,candidatos=candidates))
    for c in candidates:c['holgura_vertical_muestreada']=p.floor_gap(c)
    candidates=[c for c in candidates if c['holgura_vertical_muestreada']['minimo_m']>=2.31]
    assert candidates,'Sin panel posterior compatible con envolvente de receptores 2 m + radio .31 m'
    p.g.save('candidatos-retornos-con-holgura.json',dict(criterio_m=2.31,significado='Reserva geometrica de altura receptor 2 m mas radio .31 m; no es un criterio normativo',candidatos=candidates))
    selected=p.greedy(candidates,2,'equilibrio')
    cases=json.loads((p.O/'variantes.json').read_text());cases['retornos2']=selected;p.g.save('variantes.json',cases)
    p.g.export('retornos2',selected)
    print('Retornos: candidatos',len(candidates),'seleccionados',[(r['centro'],r['objetivo_de_orientacion']) for r in selected])
if __name__=='__main__':main()
