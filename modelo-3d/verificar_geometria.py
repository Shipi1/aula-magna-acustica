"""Verifica exportaciones mediante lectores independientes del generador."""
from pathlib import Path
import json, struct, hashlib, importlib.metadata
from collections import Counter
import numpy as np
import trimesh

B=Path(__file__).resolve().parent
g=json.loads((B/'geometria.json').read_text(encoding='utf8'))
V=np.array(g['vertices']); F=np.array([f['v'] for f in g['faces']])

def read3ds(path):
 data=path.read_bytes(); objects=[]
 def chunks(start,end):
  while start<end:
   tag,size=struct.unpack_from('<HI',data,start)
   assert size>=6 and start+size<=end
   yield tag,start+6,start+size
   start+=size
  assert start==end
 def readmesh(start,end,name):
  v=f=None
  for tag,a,b in chunks(start,end):
   if tag==0x4110:
    n=struct.unpack_from('<H',data,a)[0]
    v=np.array([struct.unpack_from('<fff',data,a+2+12*i) for i in range(n)])
   elif tag==0x4120:
    n=struct.unpack_from('<H',data,a)[0]
    f=np.array([struct.unpack_from('<HHHH',data,a+2+8*i)[:3] for i in range(n)])
  assert v is not None and f is not None
  objects.append((name,v,f))
 def walk(start,end):
  for tag,a,b in chunks(start,end):
   if tag in (0x4D4D,0x3D3D): walk(a,b)
   elif tag==0x4000:
    e=data.index(b'\0',a); name=data[a:e].decode('ascii')
    for t,c,d in chunks(e+1,b):
     if t==0x4100: readmesh(c,d,name)
 walk(0,len(data))
 vs=[];fs=[];offset=0
 for _,v,f in objects:
  vs.extend(v);fs.extend(f+offset);offset+=len(v)
 return np.array(vs),np.array(fs),[o[0] for o in objects]

def checks(v,f):
 # Los objetos 3DS comparten coordenadas en sus fronteras, no índices.
 unique={}; vv=[]; remap=[]
 for p in v:
  key=tuple(np.round(p,5))
  if key not in unique: unique[key]=len(vv);vv.append(p)
  remap.append(unique[key])
 ff=np.array(remap)[f]; vv=np.array(vv)
 mesh=trimesh.Trimesh(vv,ff,process=False)
 assert mesh.is_watertight and mesh.is_winding_consistent
 assert mesh.euler_number==-6
 assert np.min(mesh.area_faces)>1e-9
 assert mesh.volume<0 # normals into air
 assert abs(abs(mesh.volume)-g['checks']['volumen_m3'])<.02
 assert len(ff)==len(F)
 assert np.max(np.abs(mesh.bounds-np.array([V.min(0),V.max(0)])))<1e-4
 edges=Counter(tuple(sorted(e)) for f in ff for e in zip(f,np.roll(f,-1)))
 assert all(n==2 for n in edges.values())
 return {'vertices_unidos':len(vv),'caras':len(ff),'cerrada':True,'orientacion_consistente':True,
  'euler':int(mesh.euler_number),'volumen_m3':round(abs(float(mesh.volume)),3),
  'area_minima_m2':float(mesh.area_faces.min()),'bounds_m':mesh.bounds.tolist()}

ply=trimesh.load(B/'aula-magna.ply',process=False)
v3,f3,names=read3ds(B/'aula-magna.3ds')
result={'json':checks(V,F),'ply':checks(ply.vertices,ply.faces),'3ds':checks(v3,f3),'grupos_3ds':names}
# Ángulo sólido: evita depender de un índice espacial o de un rayo que toque aristas.
def inside(p):
 t=V[F]-p;a,b,c=t[:,0],t[:,1],t[:,2]
 la,lb,lc=np.linalg.norm(a,axis=1),np.linalg.norm(b,axis=1),np.linalg.norm(c,axis=1)
 num=np.einsum('ij,ij->i',a,np.cross(b,c))
 den=la*lb*lc+np.einsum('ij,ij->i',a,b)*lc+np.einsum('ij,ij->i',b,c)*la+np.einsum('ij,ij->i',c,a)*lb
 return bool(abs(np.sum(2*np.arctan2(num,den)))>2*np.pi)
result['puntos_heredados']={p['id']:{'dentro':inside(np.array(p['xyz'])),'coordenadas':p['xyz'],'registro':'provisional'} for p in g['points']}
assert result['puntos_heredados']['P5']['dentro']
result['versiones']={k:importlib.metadata.version(k) for k in ['numpy','manifold3d','trimesh','matplotlib','Pillow']}
result['sha256_fuentes']={str(p.relative_to(B.parent)):hashlib.sha256(p.read_bytes()).hexdigest()
 for p in sorted((B.parent/'datos').glob('*')) if p.suffix.lower() in ['.pdf','.jpeg']}
result['isimpa']='No se ha ejecutado importación ni mallado dentro de I-Simpa.'
(B/'revision'/'verificacion-exportaciones.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf8')
print(json.dumps({'checks':'OK','triangulos':len(F),'grupos':len(names),'puntos':result['puntos_heredados']},ensure_ascii=False))
