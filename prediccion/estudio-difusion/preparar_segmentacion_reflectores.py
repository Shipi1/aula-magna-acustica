"""Ocho módulos de igual área total, orientados desde la variante combinada."""
import json,copy,itertools
import numpy as np
import preparar_inclinaciones_reflectores as p
def main():
    cases=json.loads((p.O/'variantes.json').read_text());parent=cases['combinada'];seed=[]
    for i,panel in enumerate(parent):
        for sign in (-1,1):
            q=copy.deepcopy(panel);q['centro']=(np.array(panel['centro'])+sign*1.10*np.array(panel['u'])).tolist();q['ancho']=2.;q['panel_padre']=i+1;q['mitad']=sign
            q=p.turn(q,0,0);assert p.valid(q);seed.append(q)
    assert not any(p.h.overlaps(a,b) for a,b in itertools.combinations(seed,2))
    chosen=p.optimize(seed,list(itertools.product((-10,-5,0,5,10),(-10,-5,0,5,10))),'segmentada')
    assert sum(x['ancho']*x['alto'] for x in chosen)==48
    cases['segmentada']=chosen;p.save('variantes.json',cases)
    p.save('segmentacion.json',dict(area_total_m2=48,modulos=8,dimensiones_m=[2,3,.02],separacion_coplanar_m=.20,
        partida='Orientación combinada, división por eje u. Los dos centros se desplazan ±1,10m desde el centro del panel padre.',
        control='No es una comparación de orientación pura: cambian tamaño finito, separación, bordes y número de módulos. No se asume que conserve área de absorción equivalente exactamente.',
        giros='Adicionales respecto de la orientación combinada, alrededor del centro de cada módulo; rango ±10 grados cada eje, paso 5.',
        puntaje_geometrico_plano=p.score(seed),puntaje_geometrico_segmentado=p.score(chosen),modulos_planos=seed))
    p.h.g.export('segmentada',chosen)
    spatial=json.loads((p.O/'verificacion-espacial.json').read_text());spatial=[r for r in spatial if r['variante']!='segmentada']
    for i,q in enumerate(chosen):spatial.append(dict(variante='segmentada',panel=i+1,holgura_vertical=p.h.floor_gap(q),segmentos_directos_preservados=42))
    p.save('verificacion-espacial.json',spatial)
if __name__=='__main__':main()
