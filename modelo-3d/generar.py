"""Geometría acústica preliminar; Python estándar, sin dependencias externas."""
from pathlib import Path
import math, json, csv, sys
from collections import Counter

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent / 'analisis'))
from sala import XY

# Metros. Origen nuevo: muro posterior del escenario, eje central, nivel +0.00.
# Cotas horizontales encadenadas sobre el eje. NO usa XY para definir muros.
W = 23.33
STAGE = 11.55
BALCONY = STAGE + 12.48
REAR_FLOOR = BALCONY + 8.52
LOWER_END = BALCONY + 7.96
REAR = LOWER_END + 8.26
TOP = 13.32

MATERIALS = {
 'escenario': {'label':'Piso de escenario', 'color':'#ae8160'},
 'platea': {'label':'Platea / butacas equivalentes', 'color':'#5b8f9a'},
 'gradas': {'label':'Graderías / butacas equivalentes', 'color':'#568794'},
 'frente_balcon': {'label':'Frente y contrahuellas', 'color':'#c3ab8f'},
 'bajo_balcon': {'label':'Cielo bajo balcón', 'color':'#cdbda7'},
 'muros': {'label':'Muros simplificados', 'color':'#b0b6b5'},
 'cielo': {'label':'Cielo superior simplificado', 'color':'#e1d6bf'},
}
# Sección del aire: cada etiqueta corresponde al borde que sale del vértice.
profile=[]
def add(x,z,mat): profile.append([x,z,mat])
add(0,.50,'escenario'); add(6.35,.50,'escenario')
add(6.35,.14,'escenario'); add(STAGE,.14,'frente_balcon')
add(STAGE,-.80,'platea'); add(REAR_FLOOR,0,'muros')
add(REAR_FLOOR,3.30,'bajo_balcon'); add(BALCONY,3.30,'frente_balcon')
add(BALCONY,3.80,'gradas')
for i in range(13):
 x=BALCONY+(i+1)*(LOWER_END-BALCONY)/13
 z=3.80+i*(5.54-3.80)/13
 add(x,z,'frente_balcon'); add(x,3.80+(i+1)*(5.54-3.80)/13,'gradas')
for i in range(19):
 x=LOWER_END+(i+1)*(REAR-LOWER_END)/19
 z=5.54+i*(8.53-5.54)/19
 add(x,z,'frente_balcon'); add(x,5.54+(i+1)*(8.53-5.54)/19,'gradas')
profile[-1][2]='muros'
add(REAR,TOP,'cielo'); add(0,TOP,'muros')

# Flechas aproximadas a partir de la planta, no radios levantados en terreno.
def bow(x):
 knots=[(0,0),(6.35,0),(STAGE,.90),(BALCONY,2.80),
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
edges=Counter(); directed=Counter(); areas=Counter()
for f in faces:
 a,b,c=[vertices[i] for i in f['v']]
 ar=math.sqrt(dot(cross(sub(b,a),sub(c,a)),cross(sub(b,a),sub(c,a))))/2
 assert ar>1e-9
 areas[f['material']]+=ar
 for a,b in zip(f['v'],f['v'][1:]+f['v'][:1]):
  edges[tuple(sorted([a,b]))]+=1; directed[(a,b)]+=1
assert all(v==2 for v in edges.values()),'Aristas abiertas o no manifold'
assert all(directed[(b,a)]==1 for a,b in directed),'Normales inconsistentes'
assert len(vertices)-len(edges)+len(faces)==2

checks={'vertices':len(vertices),'triangulos':len(faces),'aristas_abiertas':0,
 'aristas_no_manifold':0,'caras_degeneradas':0,'normales':'hacia el interior',
 'euler':2,'volumen_m3':round(abs(volume()),2),
 'superficies_m2':{k:round(v,2) for k,v in areas.items()},
 'alcance':'Cierre topológico y orientación verificados; no certifica exactitud arquitectónica ni compatibilidad con un simulador.'}
points=[{'id':k,'xyz':v[:3],'provisional':True} for k,v in XY.items()]
data={'units':'m','status':'preliminar_no_calibrado','vertices':vertices,'faces':faces,
 'materials':MATERIALS,'points':points,'checks':checks,
 'dimensions':{'ancho':W,'escenario':STAGE,'balcon_inicio':BALCONY,'platea_fondo':REAR_FLOOR,'fondo':REAR,'cielo':TOP}}
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
with (BASE/'mediciones-originales.csv').open('w',newline='',encoding='utf8') as fh:
 w=csv.writer(fh); w.writerow(['id','x_original_m','y_original_m','z_original_m','estado'])
 for p in points: w.writerow([p['id'],*p['xyz'],'SIN_REGISTRAR_CON_EL_MODELO'])
template=(BASE/'visor.template.html').read_text(encoding='utf8')
(BASE/'visor.html').write_text(template.replace('__GEOMETRIA__',json.dumps(data,separators=(',',':'),ensure_ascii=False)),encoding='utf8')
print(json.dumps(checks,indent=2,ensure_ascii=False))
