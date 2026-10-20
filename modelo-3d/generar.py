"""Geometría revisada ARQ-01. Dependencias: numpy y manifold3d (ver LEEME)."""
from pathlib import Path
import math, json, csv, sys
import struct
import numpy as np
import manifold3d as md
from collections import Counter

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent / 'analisis'))
from sala import XY

# Metros. Origen nuevo: muro posterior del escenario, eje central, nivel +0.00.
# Cotas horizontales encadenadas sobre el eje. NO usa XY para definir muros.
W = 23.33
STAGE = 11.55
BALCONY = STAGE + 12.48
COLUMNS = BALCONY + 8.52
REAR_FLOOR = 35.80  # Cierre detrás de los pilares, lectura a escala en planta.
LOWER_END = BALCONY + 7.96
REAR = LOWER_END + 8.26
TOP = 13.32

MATERIALS = {
 'escenario': {'label':'Piso de escenario', 'color':'#ae8160'},
 'platea': {'label':'Platea / butacas equivalentes', 'color':'#5b8f9a'},
 'gradas': {'label':'Graderías / butacas equivalentes', 'color':'#568794'},
 'frente_balcon': {'label':'Frente y contrahuellas', 'color':'#c3ab8f'},
 'bajo_balcon': {'label':'Cielo bajo balcón', 'color':'#cdbda7'},
 'muros': {'label':'Muros generales', 'color':'#b0b6b5'},
 'cielo': {'label':'Cielo de caja escénica / frente', 'color':'#e1d6bf'},
 'circulacion_alta': {'label':'Circulaciones de platea alta (hipótesis)', 'color':'#ae9e8b'},
 'embocadura': {'label':'Embocadura / jambas', 'color':'#d4bd9a'},
 'antepecho': {'label':'Antepecho curvo del balcón', 'color':'#e5c39d'},
 'laterales_altos': {'label':'Muros laterales de platea alta', 'color':'#c8b699'},
 'fondo_alto': {'label':'Muro posterior alto', 'color':'#bdab94'},
 'pilares': {'label':'Cuatro pilares bajo balcón', 'color':'#d5cbb4'},
}
for i in range(5):
 MATERIALS[f'cielo_{i+1}']={'label':f'Cielo acústico · plano {i+1}', 'color':['#d8c9ad','#d3c1a1','#ccb995','#c5b08a','#bda780'][i]}
MATERIALS.update({
 'butacas_platea':{'label':'Butacas vacías · platea equivalente','color':'#4f91af'},
 'butacas_alta_frontal':{'label':'Butacas vacías · platea alta frontal','color':'#579dad'},
 'butacas_alta_posterior':{'label':'Butacas vacías · platea alta posterior','color':'#68a7b0'},
 'pasillos_alfombra':{'label':'Pasillos · alfombra aproximada','color':'#a35e6f'},
 'madera_expuesta':{'label':'Madera expuesta / circulaciones','color':'#ba9269'},
 'cortinas_fondo':{'label':'Cortinas sobre puertas · fondo bajo balcón','color':'#944d55'},
})
# Sección del aire: cada etiqueta corresponde al borde que sale del vértice.
profile=[]
def add(x,z,mat): profile.append([x,z,mat])
add(0,.50,'escenario'); add(6.35,.50,'escenario')
add(6.35,.14,'escenario'); add(STAGE,.14,'frente_balcon')
add(STAGE,-.60,'platea'); add(REAR_FLOOR,0,'muros')
add(REAR_FLOOR,3.30,'bajo_balcon'); add(BALCONY,3.30,'frente_balcon')
add(BALCONY,3.80,'gradas')
for i in range(13):
 x=BALCONY+(i+1)*(LOWER_END-1.50-BALCONY)/13
 z=3.80+i*(5.54-3.80)/13
 add(x,z,'frente_balcon'); add(x,3.80+(i+1)*(5.54-3.80)/13,'gradas')
profile[-1][2]='circulacion_alta'
add(LOWER_END,5.54,'gradas')
for i in range(19):
 x=LOWER_END+(i+1)*(REAR-LOWER_END)/19
 z=5.54+i*(8.53-5.54)/19
 add(x,z,'frente_balcon'); add(x,5.54+(i+1)*(8.53-5.54)/19,'gradas')
profile[-1][2]='muros'
add(REAR,TOP,'cielo'); add(0,TOP,'muros')

# Flechas aproximadas a partir de la planta, no radios levantados en terreno.
def bow(x):
 knots=[(0,0),(6.35,0),(STAGE,.90),(BALCONY,3.15),
        (LOWER_END,1.75),(REAR_FLOOR,1.65),(REAR,0)]
 for (a,va),(b,vb) in zip(knots,knots[1:]):
  if a<=x<=b: return va+(vb-va)*(x-a)/(b-a)
 return 0
ys=[-W/2+W*j/24 for j in range(25)]
vertices=[[round(x-bow(x)*(y/(W/2))**2,6),round(y,6),round(z,6)]
          for y in ys for x,z,_ in profile]
N=len(profile)
faces=[]
def tri(a,b,c,mat): faces.append({'v':[a,b,c],'material':mat})
for j in range(len(ys)-1):
 for i,(_,_,mat) in enumerate(profile):
  k=(i+1)%N; a=j*N+i; b=j*N+k; c=(j+1)*N+k; d=(j+1)*N+i
  tri(a,b,c,mat); tri(a,c,d,mat)

def area(poly): return sum(poly[i][0]*poly[(i+1)%len(poly)][1]-poly[(i+1)%len(poly)][0]*poly[i][1] for i in range(len(poly)))/2
def cross2(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def triangulate(poly):
 ids=list(range(len(poly))); out=[]; sign=1 if area(poly)>0 else -1
 while len(ids)>3:
  found=False
  for j,b in enumerate(ids):
   a=ids[j-1]; c=ids[(j+1)%len(ids)]
   if sign*cross2(poly[a],poly[b],poly[c])<=1e-10: continue
   def inside(p):
    return all(sign*cross2(u,v,p)>=-1e-10 for u,v in [(poly[a],poly[b]),(poly[b],poly[c]),(poly[c],poly[a])])
   if any(inside(poly[k]) for k in ids if k not in (a,b,c)): continue
   out.append((a,b,c)); ids.pop(j); found=True; break
  if not found: raise ValueError('No se pudo triangular la sección')
 out.append(tuple(ids)); return out
endpoly=[[v[0],v[2]] for v in vertices[:N]]
for a,b,c in triangulate(endpoly):
 tri(c,b,a,'muros'); tri((len(ys)-1)*N+a,(len(ys)-1)*N+b,(len(ys)-1)*N+c,'muros')

def cross(a,b): return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def sub(a,b): return [x-y for x,y in zip(a,b)]
def volume(): return sum(dot(vertices[f['v'][0]],cross(vertices[f['v'][1]],vertices[f['v'][2]]))/6 for f in faces)
# Normales hacia el aire interior, también en OBJ y DXF.
if volume()>0:
 for f in faces: f['v'].reverse()

# Operaciones sobre el volumen de aire: las sustracciones son obstáculos.
# La procedencia de cada cara se conserva con los IDs de Manifold.
provenance={}
ordered=[]; runs=[0]; ids=[]
for mat in MATERIALS:
 group=[f['v'][::-1] for f in faces if f['material']==mat]
 if not group: continue
 oid=md.Manifold.reserve_ids(1); provenance[oid]=mat; ids.append(oid)
 ordered.extend(group); runs.append(3*len(ordered))
air=md.Manifold(md.Mesh64(np.asarray(vertices,np.float64),np.asarray(ordered,np.uint64),
 run_index=np.asarray(runs,np.uint64),run_original_id=np.asarray(ids,np.uint32)))
assert air.status()==md.Error.NoError
def tagged(solid,mat):
 solid=solid.as_original(); provenance[solid.original_id()]=mat; return solid
def box(lo,hi,mat):
 # Evitar tapas booleanas casi coincidentes con el perímetro exterior.
 lo=list(lo);hi=list(hi)
 if abs(lo[1]+W/2)<1e-8: lo[1]-=.10
 if abs(hi[1]-W/2)<1e-8: hi[1]+=.10
 return tagged(md.Manifold.cube(tuple(b-a for a,b in zip(lo,hi))).translate(lo),mat)
def prism(poly,z0,z1,mat):
 if area(poly)<0: poly=list(reversed(poly))
 return tagged(md.Manifold.extrude(md.CrossSection([poly]),z1-z0).translate((0,0,z0)),mat)

# Segundo bloque de asientos: límite lateral trazado en planta (m).
# Sus circulaciones se representan a +5.54; el cerramiento exterior se conserva
# rectangular por no existir un corte transversal que defina estos recintos.
upper_edge=[(30.24,9.085),(32.60,9.085),(33.35,8.90),(33.80,8.40),
            (34.25,7.85),(34.90,7.45),(35.50,7.245),(40.25,7.245)]
for sign in [-1,1]:
 poly=[(x,sign*y) for x,y in upper_edge]+[(REAR,sign*(W/2+.10)),(30.24,sign*(W/2+.10))]
 air=air+prism(poly,5.54,TOP,'circulacion_alta')

# Embocadura: ancho libre 15.93, espesor 0.50 de planta.
# Dintel +7.40 es una estimación del corte/foto, no una cota explícita.
for sign in [-1,1]:
 y0,y1=sorted((sign*9.515,sign*W/2))
 air=air-box((0,y0,-1),(6.35,y1,TOP+1),'muros')
for sign in [-1,1]:
 y0,y1=sorted((sign*7.965,sign*W/2))
 air=air-box((6.35,y0,-1),(6.85,y1,TOP+1),'embocadura')
air=air-box((6.35,-W/2,7.40),(6.85,W/2,TOP+1),'embocadura')

# Limitar ancho del proscenio a 16.80, dejando piso lateral bajo.
for sign in [-1,1]:
 y0,y1=sorted((sign*8.40,sign*W/2))
 air=air+box((6.85,y0,-.60),(STAGE,y1,.14),'platea')

# Antepecho macizo curvo: 0.25 de espesor y coronación +4.45 estimados.
# Base bajo intradós para que quede integrado en la envolvente.
front=[(BALCONY-bow(BALCONY)*(y/(W/2))**2,y) for y in ys]
dx=(front[1][0]-front[0][0])/(front[1][1]-front[0][1])
front=[(front[0][0]-.10*dx,front[0][1]-.10)]+front+[(front[-1][0]-.10*dx,front[-1][1]+.10)]
poly=[(x-.12,y) for x,y in front]+[(x+.13,y) for x,y in reversed(front)]
air=air-prism(poly,3.20,4.45,'antepecho')

# Cierre acústico equivalente siguiendo los cinco niveles del corte.
# Los solapes/luz entre paneles no están definidos: NO son nubes verificadas.
ceiling=[(16.30,20.40,9.80),(20.40,25.20,10.40),(25.20,30.00,10.95),
         (30.00,34.80,11.55),(34.80,REAR,12.12)]
for i,(x0,x1,z) in enumerate(ceiling):
 air=air-box((x0,-W/2,z),(x1,W/2,TOP+1),f'cielo_{i+1}')
for y in [-6.0,-3.5,3.5,6.0]:
 x=COLUMNS-1.65*(y/(W/2))**2
 column=md.Manifold.cylinder(4.30,.30,.30,24).translate((x,y,-.70))
 air=air-tagged(column,'pilares')
envelope=md.Manifold.cube((REAR,W,TOP+2)).translate((0,-W/2,-1))
air=air^tagged(envelope,'muros')
assert air.status()==md.Error.NoError and not air.is_empty()
air=air.simplify(1e-6)
mesh=air.to_mesh64()
raw_vertices=mesh.vert_properties[:,:3].astype(float).tolist()
vertices=[]; unique={}; remap={}
for j,v in enumerate(raw_vertices):
 key=tuple(round(c,6) for c in v)
 if key not in unique: unique[key]=len(vertices); vertices.append(list(key))
 remap[j]=unique[key]
faces=[]
for j,oid in enumerate(mesh.run_original_id):
 for idx in range(mesh.run_index[j]//3,mesh.run_index[j+1]//3):
  vv=[remap[k] for k in mesh.tri_verts[idx].tolist()[::-1]]; mat=provenance[oid]
  if len(set(vv))<3: continue
  pts=np.array([vertices[k] for k in vv]); center=pts.mean(axis=0)
  if mat=='muros' and center[2]>5.54:
   if np.all(np.abs(pts[:,0]-REAR)<1e-4): mat='fondo_alto'
   elif np.all(np.abs(np.abs(pts[:,1])-W/2)<1e-4) and center[0]>20: mat='laterales_altos'
  faces.append({'v':vv,'material':mat})

# Subdivisión conforme por planos: separa asignaciones sin añadir obstáculos.
# Las franjas de pasillo son aproximaciones explícitas, no un levantamiento.
for axis,cut in [(1,y) for y in [-10.25,-6.65,-.65,.65,6.65,10.25]]+[(0,x) for x in [12.50,31.90,35.00]]:
 new=[]
 def vertex(p):
  key=tuple(round(float(c),6) for c in p)
  if key not in unique: unique[key]=len(vertices);vertices.append(list(key))
  return unique[key]
 for f in faces:
  poly=[np.array(vertices[k]) for k in f['v']]
  distances=[p[axis]-cut for p in poly]
  if min(distances)>=-1e-8 or max(distances)<=1e-8:
   new.append(f);continue
  for sign in [-1,1]:
   clipped=[]
   for a,b in zip(poly,poly[1:]+poly[:1]):
    da,db=sign*(a[axis]-cut),sign*(b[axis]-cut)
    if da>=-1e-8: clipped.append(a)
    if (da>1e-8 and db< -1e-8) or (da< -1e-8 and db>1e-8):
     p=a+(b-a)*(da/(da-db));p[axis]=cut;clipped.append(p)
   vv=[vertex(p) for p in clipped]
   vv=list(dict.fromkeys(vv))
   for k in range(1,len(vv)-1):
    new.append({'v':[vv[0],vv[k],vv[k+1]],'material':f['material']})
 faces=new
for f in faces:
 pts=np.array([vertices[k] for k in f['v']]);x,y,z=pts.mean(axis=0);mat=f['material']
 if mat in ('platea','gradas','circulacion_alta'):
  if mat=='platea':
   if 12.50<x<35 and .65<abs(y)<10.25: mat='butacas_platea'
   elif x>11.55 and (abs(y)<.65 or abs(y)>10.25): mat='pasillos_alfombra'
   else: mat='madera_expuesta'
  elif mat=='gradas':
   limit=10.25 if x<31.90 else 6.65
   if .65<abs(y)<limit: mat='butacas_alta_frontal' if x<31.90 else 'butacas_alta_posterior'
   else: mat='pasillos_alfombra'
  else: mat='madera_expuesta'
 if mat=='muros' and np.all(pts[:,2]>=-1e-5) and np.all(pts[:,2]<=3.30001):
  rear=REAR_FLOOR-1.65*(pts[:,1]/(W/2))**2
  if np.max(np.abs(pts[:,0]-rear))<.02: mat='cortinas_fondo'
 f['material']=mat
# Simplificar la subdivisión a 0.1 mm manteniendo los grupos de material.
# Evita triángulos microscópicos por cruces de las nuevas líneas con diagonales.
ordered=[];runs=[0];ids=[];new_provenance={}
for mat in MATERIALS:
 fs=[f['v'][::-1] for f in faces if f['material']==mat]
 if not fs:continue
 oid=md.Manifold.reserve_ids(1);new_provenance[oid]=mat;ids.append(oid)
 ordered.extend(fs);runs.append(3*len(ordered))
partition=md.Manifold(md.Mesh64(np.asarray(vertices,np.float64),np.asarray(ordered,np.uint64),
 run_index=np.asarray(runs,np.uint64),run_original_id=np.asarray(ids,np.uint32))).simplify(.0001)
assert partition.status()==md.Error.NoError
mesh=partition.to_mesh64();vertices=mesh.vert_properties[:,:3].astype(float).tolist();faces=[]
for j,oid in enumerate(mesh.run_original_id):
 for i in range(mesh.run_index[j]//3,mesh.run_index[j+1]//3):
  faces.append({'v':mesh.tri_verts[i].tolist()[::-1],'material':new_provenance[oid]})
# Descartar vértices sin uso heredados de las operaciones booleanas/subdivisión.
used=sorted({k for f in faces for k in f['v']});mapping={k:i for i,k in enumerate(used)}
vertices=[vertices[k] for k in used]
for f in faces:f['v']=[mapping[k] for k in f['v']]
edges=Counter(); directed=Counter(); areas=Counter()
for f in faces:
 a,b,c=[vertices[i] for i in f['v']]
 ar=math.sqrt(dot(cross(sub(b,a),sub(c,a)),cross(sub(b,a),sub(c,a))))/2
 assert ar>1e-9,(ar,f,a,b,c)
 areas[f['material']]+=ar
 for a,b in zip(f['v'],f['v'][1:]+f['v'][:1]):
  edges[tuple(sorted([a,b]))]+=1; directed[(a,b)]+=1
assert all(v==2 for v in edges.values()),'Aristas abiertas o no manifold'
assert all(directed[(b,a)]==1 for a,b in directed),'Normales inconsistentes'
# Los cuatro pilares conectan piso y cielo: cuatro asas topológicas.
assert len(vertices)-len(edges)+len(faces)==-6

checks={'vertices':len(vertices),'triangulos':len(faces),'aristas_abiertas':0,
 'aristas_no_manifold':0,'caras_degeneradas':0,'normales':'hacia el interior',
 'euler':-6,'pilares_conectados':4,'volumen_m3':round(abs(volume()),2),
 'superficies_m2':{k:round(v,2) for k,v in areas.items()},
 'motor_booleano':str(air.status()), 'revision':'v2.2_2026-10-19',
 'alcance':'Cierre y orientación verificados; requiere comprobación de importación/mallado en I-Simpa y calibración acústica.'}
points=[{'id':k,'xyz':v[:3],'provisional':True} for k,v in XY.items()]
data={'units':'m','status':'revision_plano_v2_no_calibrado','vertices':vertices,'faces':faces,
 'materials':MATERIALS,'points':points,'checks':checks,
 'dimensions':{'ancho':W,'escenario':STAGE,'balcon_inicio':BALCONY,'platea_fondo':REAR_FLOOR,'fondo':REAR,'cielo':TOP},
 'revision':{'ceiling':ceiling,'upper_edge':upper_edge,'embocadura_ancho':15.93,'proscenio_ancho':16.80,'bloque_posterior_ancho':14.49}}
(BASE/'geometria.json').write_text(json.dumps(data,separators=(',',':'),ensure_ascii=False),encoding='utf8')
(BASE/'validacion.json').write_text(json.dumps(checks,indent=2,ensure_ascii=False),encoding='utf8')
obj=['# Aula Magna UTFSM - geometria preliminar en metros, Z arriba',
     '# Normales orientadas al interior. Ver LEEME.md antes de simular.',
     'mtllib aula-magna.mtl']
obj += ['v '+' '.join(map(str,v)) for v in vertices]
for mat in MATERIALS:
 obj+=['g '+mat,'usemtl '+mat]
 obj+=['f '+' '.join(str(i+1) for i in f['v']) for f in faces if f['material']==mat]
(BASE/'aula-magna.obj').write_text('\n'.join(obj)+'\n',encoding='utf8')
mtl=[]
for k,m in MATERIALS.items():
 col=[int(m['color'][i:i+2],16)/255 for i in [1,3,5]]
 mtl+=['newmtl '+k,'Kd '+' '.join(f'{v:.4f}' for v in col),'d 1','illum 1','']
(BASE/'aula-magna.mtl').write_text('\n'.join(mtl),encoding='utf8')
dxf=['0','SECTION','2','HEADER','9','$ACADVER','1','AC1015','9','$INSUNITS','70','6','0','ENDSEC','0','SECTION','2','ENTITIES']
for f in faces:
 dxf+=['0','3DFACE','8',f['material']]
 for j,i in enumerate(f['v']+[f['v'][-1]]):
  for ax,v in enumerate(vertices[i]): dxf += [str(10+10*ax+j),str(v)]
dxf+=['0','ENDSEC','0','EOF']
(BASE/'aula-magna.dxf').write_text('\n'.join(dxf)+'\n',encoding='ascii')

# PLY geométrico estándar, y 3DS agrupado para I-Simpa.
ply=['ply','format ascii 1.0','comment Aula Magna UTFSM v2; metres; Z up',
 f'element vertex {len(vertices)}','property float x','property float y','property float z',
 f'element face {len(faces)}','property list uchar int vertex_indices','end_header']
ply+=[' '.join(map(str,v)) for v in vertices]
ply+=['3 '+' '.join(map(str,f['v'])) for f in faces]
(BASE/'aula-magna.ply').write_text('\n'.join(ply)+'\n',encoding='ascii')
def chunk(tag,payload): return struct.pack('<HI',tag,len(payload)+6)+payload
objects=[]; mapping=[];visual_materials=[]
for number,mat in enumerate(MATERIALS):
 fs=[f['v'] for f in faces if f['material']==mat]
 if not fs: continue
 used=sorted({i for f in fs for i in f}); remap={v:i for i,v in enumerate(used)}
 assert len(used)<65536 and len(fs)<65536
 name=f'{number:02d}_{mat}'[:40]
 rgb=bytes(int(MATERIALS[mat]['color'][i:i+2],16) for i in [1,3,5])
 visual_materials.append(chunk(0xAFFF,chunk(0xA000,name.encode('ascii')+b'\0')+chunk(0xA020,chunk(0x0011,rgb))))
 vp=struct.pack('<H',len(used))+b''.join(struct.pack('<fff',*vertices[i]) for i in used)
 fp=struct.pack('<H',len(fs))+b''.join(struct.pack('<HHHH',*(remap[i] for i in f),0) for f in fs)
 fp+=chunk(0x4130,name.encode('ascii')+b'\0'+struct.pack('<H',len(fs))+b''.join(struct.pack('<H',i) for i in range(len(fs))))
 objects.append(chunk(0x4000,name.encode('ascii')+b'\0'+chunk(0x4100,chunk(0x4110,vp)+chunk(0x4120,fp))))
 mapping.append({'objeto_3ds':name,'familia':mat,'descripcion':MATERIALS[mat]['label'],'triangulos':len(fs)})
(BASE/'aula-magna.3ds').write_bytes(chunk(0x4D4D,chunk(0x0002,struct.pack('<I',3))+chunk(0x3D3D,chunk(0x0100,struct.pack('<f',1.0))+b''.join(visual_materials)+b''.join(objects))))
(BASE/'grupos-isimpa.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2),encoding='utf8')
with (BASE/'mediciones-originales.csv').open('w',newline='',encoding='utf8') as fh:
 w=csv.writer(fh); w.writerow(['id','x_original_m','y_original_m','z_original_m','estado'])
 for p in points: w.writerow([p['id'],*p['xyz'],'SIN_REGISTRAR_CON_EL_MODELO'])
template=(BASE/'visor.template.html').read_text(encoding='utf8')
(BASE/'visor.html').write_text(template.replace('__GEOMETRIA__',json.dumps(data,separators=(',',':'),ensure_ascii=False)),encoding='utf8')
print(json.dumps(checks,indent=2,ensure_ascii=False))
