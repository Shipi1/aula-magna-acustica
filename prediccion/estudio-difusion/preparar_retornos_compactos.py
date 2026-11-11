"""Paneles posteriores más anchos y menos altos: misma área frontal por módulo."""
import json,itertools
import numpy as np
import preparar_cobertura_reflectores as p
def main():
    candidates=[];tested=0
    for x,y,z in itertools.product((34.,36.,38.),(-6.,0.,6.),(10.4,11.,11.2)):
        q=np.array([x,y,z])
        if not p.g.inside(q):continue
        for target,s in itertools.product(['P8','P9']+p.SEATS,[p.S['F1'],p.S['F2'],(p.S['F1']+p.S['F2'])/2]):
            tested+=1;panel=p.g.panel(q,p.R[target],s,6.,2.)
            n=np.array(panel['normal']);u=p.g.unit(np.cross([0.,0.,1.],n));v=np.cross(n,u)
            panel['u']=u.tolist();panel['v']=v.tolist()
            routes=p.paths(panel)
            if not routes:continue
            cc=p.g.corners(panel)
            if not all(p.g.inside(c) for c in cc):continue
            if any(not p.g.visible(a,b) for a,b in itertools.combinations(cc,2)):continue
            if any(p.blocks(panel,a,b) for a in p.S.values() for b in p.R.values()):continue
            if any(np.linalg.norm(np.maximum(abs((r-q)@p.axes(panel).T)-p.half(panel),0))<.32 for r in p.R.values()):continue
            gap=p.floor_gap(panel)
            if gap['minimo_m']<2.31:continue
            panel.update(candidato=f'A{len(candidates)+1:04}',objetivo_de_orientacion=target,fuente_de_orientacion=s.tolist(),rutas_utiles=routes,holgura_vertical_muestreada=gap)
            candidates.append(panel)
    assert candidates
    p.g.save('candidatos-retornos-compactos.json',dict(orientaciones_exploradas=tested,area_por_panel_m2=12,dimensiones='6x2 m; eje largo horizontal',criterio_holgura_m=2.31,candidatos=candidates))
    rear=max(candidates,key=lambda c:sum(r['ganancia_geometrica'] for r in c['rutas_utiles'] if r['receptor'] in ('V10','V11')))
    assert any(r['receptor'] in ('V10','V11') for r in rear['rutas_utiles'])
    selected=p.greedy(candidates,2,'equilibrio',[rear])
    cases=json.loads((p.O/'variantes.json').read_text());cases['retornos_compactos2']=selected;p.g.save('variantes.json',cases)
    p.g.export('retornos_compactos2',selected)
    print('Retornos 6x2: candidatos',len(candidates),'elegidos',[(r['centro'],r['objetivo_de_orientacion']) for r in selected])
if __name__=='__main__':main()
