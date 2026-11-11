"""Mallas sólidas, conservación de área y comparación de orientación."""
import json,itertools,hashlib
import numpy as np
import preparar_inclinaciones_reflectores as p
cases=json.loads((p.O/'variantes.json').read_text());original=p.h.g.MODEL;out=[]
for case,ps in cases.items():
    folder=p.O/case;m=json.loads((folder/'malla-subdividida.json').read_text());assert m['vertices'][:len(original['vertices'])]==original['vertices'] and m['faces'][:len(original['faces'])]==original['faces']
    assert sum(q['ancho']*q['alto'] for q in ps)==48 and not any(p.h.overlaps(a,b) for a,b in itertools.combinations(ps,2))
    nodes=np.loadtxt(folder/'scene.1.node',skiprows=1,comments='#');ele=np.loadtxt(folder/'scene.1.ele',skiprows=1,comments='#');centers=nodes[:,1:4][ele[:,1:5].astype(int)-1].mean(1)
    for i,q in enumerate(ps):
        assert not np.all(abs((centers-np.array(q['centro']))@p.h.axes(q).T)<p.h.half(q)-1e-6,axis=1).any()
        assert not any(p.h.blocks(q,s,r) for s in p.h.S.values() for r in p.h.R.values())
        assert np.allclose(p.h.axes(q)@p.h.axes(q).T,np.eye(3))
        if case!='segmentada':assert q['centro']==p.original[i]['centro'] and [q[k] for k in ('ancho','alto','espesor')]==[4,3,.02]
    t=json.loads((folder/'verificacion-tetra.json').read_text());assert abs(t['volumen_m3']-(9543.733970598856-.96))<.001
    out.append(dict(variante=case,sala_original_conservada=True,area_frontal_m2=48,centros_originales_conservados=case!='segmentada',segmentos_directos_preservados=42,tetraedros_en_solidos=0,volumen_m3=t['volumen_m3'],sha256={f:hashlib.sha256((folder/f).read_bytes()).hexdigest() for f in ('mesh.cbin','tetramesh.mbin')}))
(p.O/'resultados').mkdir(exist_ok=True);(p.O/'resultados/verificacion-mallas.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print('Cuatro mallas verificadas, 48 m² constantes, segmentos directos conservados y sólidos excluidos del aire.')
