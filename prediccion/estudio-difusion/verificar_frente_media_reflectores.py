"""Conservación de la sala y exclusión de sólidos en las cinco mallas."""
import json,hashlib
import numpy as np
import preparar_frente_media_reflectores as p
cases=json.loads((p.O/'variantes.json').read_text());original=p.h.g.MODEL;results=[]
for case,panels in cases.items():
    folder=p.O/case;m=json.loads((folder/'malla-subdividida.json').read_text())
    assert m['vertices'][:len(original['vertices'])]==original['vertices']
    assert m['faces'][:len(original['faces'])]==original['faces']
    nodes=np.loadtxt(folder/'scene.1.node',skiprows=1,comments='#');coords=nodes[:,1:4]
    ele=np.loadtxt(folder/'scene.1.ele',skiprows=1,comments='#');indices=ele[:,1:5].astype(int)-1;centers=coords[indices].mean(1)
    counts=[]
    for panel in panels:
        relative=(centers-np.array(panel['centro']))@p.h.axes(panel).T
        inside=np.all(abs(relative)<p.h.half(panel)-1e-6,axis=1);assert not inside.any();counts.append(int(inside.sum()))
    geo=json.loads((folder/'verificacion-geometrica.json').read_text());tet=json.loads((folder/'verificacion-tetra.json').read_text())
    assert abs(tet['volumen_m3']-(9543.733970598856-sum(x['ancho']*x['alto']*x['espesor'] for x in panels)))<.001
    results.append(dict(variante=case,sala_original_conservada=True,tetraedros_en_solidos=counts,volumen_m3=tet['volumen_m3'],volumen_desplazado_m3=geo['volumen_desplazado_m3'],sha256={f:hashlib.sha256((folder/f).read_bytes()).hexdigest() for f in ('mesh.cbin','tetramesh.mbin')}))
for f in ('mesh.cbin','tetramesh.mbin'):assert results[1]['sha256'][f]==results[-1]['sha256'][f]
(p.O/'resultados/verificacion-mallas.json').write_text(json.dumps(results,indent=2),encoding='utf8')
print('Cinco mallas verificadas: sala original conservada y ningún centro tetraédrico dentro de los paneles.')
