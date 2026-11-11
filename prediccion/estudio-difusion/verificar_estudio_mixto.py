"""Subdivisión coplanar, paneles idénticos y materiales sin alterar geometría."""
import json,hashlib
import numpy as np
import preparar_cobertura_reflectores as h
B=h.B;O=B/'reflectores-absorcion-localizada';OUT=O/'resultados';OUT.mkdir(exist_ok=True)
reference=json.loads((O/'referencia/modelo-materiales.json').read_text());old=json.loads((B/'malla-base.json').read_text());original_panel=json.loads((B/'reflectores-inclinacion/combinada/malla-subdividida.json').read_text())
assert reference['vertices'][-32:]==original_panel['vertices'][-32:]
v=np.array(reference['vertices']);tri=v[np.array([f['v'] for f in reference['faces']])];oldtri=np.array(old['vertices'])[np.array([f['v'] for f in old['faces']])]
area=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1)/2;oldarea=np.linalg.norm(np.cross(oldtri[:,1]-oldtri[:,0],oldtri[:,2]-oldtri[:,0]),axis=1)/2
accum=np.zeros(len(oldarea));maxplane=0.
for i,f in enumerate(reference['faces'][:-48]):
    parent=f['parent'];a,b,c=oldtri[parent];n=np.cross(b-a,c-a);n/=np.linalg.norm(n)
    dist=max(abs((tri[i]-a)@n));assert dist<1e-5;maxplane=max(maxplane,float(dist));accum[parent]+=area[i]
    assert np.cross(tri[i,1]-tri[i,0],tri[i,2]-tri[i,0])@n>0
assert max(abs(accum-oldarea))<1e-4
nodes=np.loadtxt(O/'referencia/scene.1.node',skiprows=1,comments='#');ele=np.loadtxt(O/'referencia/scene.1.ele',skiprows=1,comments='#');centers=nodes[:,1:4][ele[:,1:5].astype(int)-1].mean(1)
panels=json.loads((O/'paneles-fijos.json').read_text())
for p in panels:assert not np.all(abs((centers-np.array(p['centro']))@h.axes(p).T)<h.half(p)-1e-6,axis=1).any()
profiles=json.loads((O/'perfiles.json').read_text());checks=[]
for case,p in profiles.items():
    m=json.loads((O/case/'modelo-materiales.json').read_text());assert m['vertices']==reference['vertices']
    actual=[]
    for i,(f,g) in enumerate(zip(m['faces'],reference['faces'])):
        if f!=g:
            assert f['idMat']==201 and g['idMat']==115 and {k:x for k,x in f.items() if k!='idMat'}=={k:x for k,x in g.items() if k!='idMat'};actual.append(i)
    assert set(actual)==set(p['caras']) and len(actual)==len(p['caras']);assert abs(area[actual].sum()-p['area_m2'])<1e-8
    checks.append(dict(variante=case,caras_material_modificado=len(actual),area_m2=p['area_m2'],vertices_y_geometria_identicos=True,sha256={f:hashlib.sha256((O/case/f).read_bytes()).hexdigest() for f in ('mesh.cbin','tetramesh.mbin')}))
assert len({c['sha256']['tetramesh.mbin'] for c in checks})==1
(OUT/'verificacion-geometria.json').write_text(json.dumps(dict(max_error_area_original_m2=float(max(abs(accum-oldarea))),max_desviacion_plano_m=maxplane,paneles_identicos=True,tetraedros_dentro_paneles=0,condiciones=checks),indent=2),encoding='utf8')
print('Sala conservada por subdivisión coplanar; paneles idénticos; cinco variantes con MBIN común y cambios solo de material.')
