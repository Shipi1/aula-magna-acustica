"""Acceso a formatos nativos con el Python instalado de I-Simpa."""
from pathlib import Path
import sys, json
sys.path.insert(0, r'C:/Program Files/I-SIMPA')
import libsimpa as L

mode=sys.argv[1]
if mode=='dump':
    model=L.ioModel()
    assert L.CformatBIN().ImportBIN(model, sys.argv[2])
    data={'vertices':[[v[k] for k in range(3)] for v in model.vertices],
          'faces':[{'v':[f.a,f.b,f.c], 'idMat':f.idMat,'idRs':f.idRs,'idEn':f.idEn} for f in model.faces]}
    Path(sys.argv[3]).write_text(json.dumps(data),encoding='utf8')
    print('vertices',len(model.vertices),'faces',len(model.faces))
elif mode=='mesh':
    model=L.ioModel(); assert L.CformatBIN().ImportBIN(model,sys.argv[2])
    changes=json.loads(Path(sys.argv[4]).read_text(encoding='utf8'))
    original=[(f.a,f.b,f.c,f.idMat,f.idRs,f.idEn) for f in model.faces]
    for index,mat in changes.items():
        f=model.faces[int(index)]; f.idMat=int(mat); model.faces[int(index)]=f
    assert L.CformatBIN().ExportBIN(sys.argv[3], model)
    check=L.ioModel(); assert L.CformatBIN().ImportBIN(check,sys.argv[3])
    assert len(check.vertices)==len(model.vertices) and len(check.faces)==len(model.faces)
    for a,b in zip(model.vertices,check.vertices): assert all(a[k]==b[k] for k in range(3))
    for i,f in enumerate(check.faces):
        a,b,c,m,rs,en=original[i]
        assert (f.a,f.b,f.c,f.idRs,f.idEn)==(a,b,c,rs,en)
        assert f.idMat==int(changes.get(str(i),m))
    print('mesh verified',len(changes))
elif mode=='read':
    out=Path(sys.argv[2]); data={'receptores':{}}
    for folder in sorted((out/'Punctual receivers').iterdir()):
        if not folder.is_dir(): continue
        reader=L.Gabe_rw(); assert reader.Load(str(folder/'Sound level.recp'))
        cols=reader.ToList()
        data['receptores'][folder.name]={c[0]:c[1:] for c in cols[1:]}
    reader=L.Gabe_rw(); assert reader.Load(str(out/'SPPS particle statistics.gabe'))
    data['estadisticas']=reader.ToList()
    (out/'resultados-lineales.json').write_text(json.dumps(data),encoding='utf8')
