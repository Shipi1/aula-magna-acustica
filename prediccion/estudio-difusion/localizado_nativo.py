"""Exportación CBIN desde JSON usando la biblioteca instalada de I-Simpa."""
import sys,json
from pathlib import Path
sys.path.insert(0,r'C:/Program Files/I-SIMPA')
import libsimpa as L
d=json.loads(Path(sys.argv[1]).read_text(encoding='utf8'))
m=L.ioModel()
for p in d['vertices']:m.vertices.append(L.t_pos(*p))
for x in d['faces']:
    f=L.ioFace();f.a,f.b,f.c=x['v'];f.idMat=x['idMat'];f.idRs=x['idRs'];f.idEn=x['idEn'];m.faces.append(f)
assert L.CformatBIN().ExportBIN(sys.argv[2],m)
check=L.ioModel();assert L.CformatBIN().ImportBIN(check,sys.argv[2])
assert len(check.vertices)==len(m.vertices) and len(check.faces)==len(m.faces)
for a,b in zip(m.faces,check.faces):assert (a.a,a.b,a.c,a.idMat,a.idRs,a.idEn)==(b.a,b.b,b.c,b.idMat,b.idRs,b.idEn)
print('CBIN verificado',len(check.vertices),len(check.faces))
