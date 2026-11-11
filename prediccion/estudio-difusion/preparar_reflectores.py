"""Búsqueda especular, paneles sólidos finitos y mallas de aire con huecos."""
from pathlib import Path
import json,subprocess,collections,itertools,xml.etree.ElementTree as ET
import numpy as np
import preparar_localizado as native_mesh
B=Path(__file__).resolve().parent
O=B/'reflectores';O.mkdir(exist_ok=True)
BASE=B/'absorcion-posterior'
MODEL=json.loads((B/'malla-base.json').read_text())
VERT=np.array(MODEL['vertices']);TRI=VERT[np.array([f['v'] for f in MODEL['faces']])]
A=TRI[:,0];E1=TRI[:,1]-A;E2=TRI[:,2]-A

def save(name,obj): (O/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False),encoding='utf8')
def unit(x):return np.array(x)/np.linalg.norm(x)
def intersections(a,b):
    direction=b-a;h=np.cross(direction,E2);det=np.einsum('ij,ij->i',E1,h)
    valid=abs(det)>1e-10;inv=np.divide(1.,det,out=np.zeros_like(det),where=valid)
    s=a-A;u=inv*np.einsum('ij,ij->i',s,h);q=np.cross(s,E1)
    w=inv*np.einsum('j,ij->i',direction,q);t=inv*np.einsum('ij,ij->i',E2,q)
    return t[valid&(u>=-1e-7)&(w>=-1e-7)&(u+w<=1+1e-7)&(t>=0)&(t<=1)]
def visible(a,b):
    ts=intersections(a,b)
    return not np.any((ts>1e-5)&(ts<1-1e-5))
def inside(p):
    hits=intersections(p,p+np.array([800.,137.,219.]));hits=hits[hits>1e-8]
    return len(np.unique(np.round(hits,7)))%2==1
def reference():
    sources={};recs={};audits=[]
    for src in ('F1','F2'):
        root=ET.parse(BASE/'calculos'/f'base-{src}-1000Hz-N600000-seed20261019'/'config.xml').getroot()
        sources[src]=np.array([float(root.find('sources')[0].get(k)) for k in ('x','y','z')])
        for r in root.find('recepteursp'):
            recs[r.get('name')]=np.array([float(r.get(k)) for k in ('x','y','z')])
        for name,p in recs.items():
            audits.append(dict(fuente=src,receptor=name,distancia_m=float(np.linalg.norm(p-sources[src])),directo_visible=visible(sources[src],p)))
    save('auditoria-posiciones.json',dict(fuentes={k:v.tolist() for k,v in sources.items()},receptores={k:v.tolist() for k,v in recs.items()},distancias=audits,
        cotejo='XY coherentes con analisis/sala.py, mediciones-originales.csv y marcas del plano-referencia.png; Z predictivas conservadas, registro de campo no certificado. F2/P9 al mismo lado, sin evidencia documental para intercambiarlos.'))
    return sources,recs

def panel(q,target,source,width=4.,height=3.):
    n=unit(unit(source-q)+unit(target-q))
    u=unit(np.array([0.,1.,0.])-n[1]*n);v=np.cross(n,u)
    return dict(centro=q.tolist(),normal=n.tolist(),u=u.tolist(),v=v.tolist(),ancho=width,alto=height,espesor=.02)
def corners(p):
    q=np.array(p['centro']);n=np.array(p['normal']);u=np.array(p['u']);v=np.array(p['v'])
    return [q+a*p['ancho']/2*u+b*p['alto']/2*v+c*p['espesor']/2*n for c in (-1,1) for a,b in ((-1,-1),(1,-1),(1,1),(-1,1))]
def specular(p,s,r):
    q=np.array(p['centro']);n=np.array(p['normal']);u=np.array(p['u']);v=np.array(p['v'])
    # Front face points toward both source and receiver, including 20 mm thickness.
    q=q+n*p['espesor']/2
    if (s-q)@n<=0 or (r-q)@n<=0:return None
    image=s-2*((s-q)@n)*n;direction=image-r;den=direction@n
    if abs(den)<1e-10:return None
    t=((q-r)@n)/den
    if not 0<t<1:return None
    hit=r+t*direction
    if abs((hit-q)@u)>p['ancho']/2 or abs((hit-q)@v)>p['alto']/2:return None
    if not visible(s,hit) or not visible(hit,r):return None
    d1=np.linalg.norm(s-hit);d2=np.linalg.norm(r-hit);direct=np.linalg.norm(r-s)
    cosinc=abs(unit(s-hit)@n);dstar=d1*d2/(d1+d2)
    # Conservative use of total incidence cosine in both dimensional cutoffs.
    cutoff=342*dstar/(2*(min(p['ancho'],p['alto'])*cosinc)**2)
    return dict(punto=hit.tolist(),retardo_ms=float((d1+d2-direct)/342*1000),distancia_reflejada_m=float(d1+d2),cos_incidencia=float(cosinc),corte_finito_estimado_Hz=float(cutoff))

def choose():
    sources,recs=reference();s=np.mean(list(sources.values()),axis=0);candidates=[]
    for family,xs in [('adelantado',(12.,16.)),('intermedio',(20.,22.))]:
        for side in (-1,1):
            # Target both outer and inner virtual seats in the early upper rows.
            target=np.mean([recs['P8' if side<0 else 'P9'],recs['V05' if side<0 else 'V08'],recs['V02' if side<0 else 'V03']],axis=0)
            for x,y,z in itertools.product(xs,(side*4.,side*7.),(8.2,9.2)):
                q=np.array([x,y,z]);p=panel(q,target,s)
                cc=corners(p)
                if not all(inside(c) for c in cc):continue
                if any(not visible(a,b) for a,b in itertools.combinations(cc,2)):continue
                paths=[]
                for src,ss in sources.items():
                    for name,r in recs.items():
                        result=specular(p,ss,r)
                        if result:paths.append(dict(fuente=src,receptor=name,**result))
                useful=[r for r in paths if r['retardo_ms']<45 and r['corte_finito_estimado_Hz']<=1000]
                prim=sum((r['fuente'],r['receptor']) in [('F1','P8'),('F2','P8'),('F1','P9')] for r in useful)
                virt=sum(r['receptor'].startswith('V') for r in useful)
                p.update(familia=family,lado=side,rutas=paths,pares_primarios_tempranos=prim,virtuales_tempranos=virt)
                candidates.append(p)
    save('candidatos.json',candidates)
    chosen={}
    for family in ('adelantado','intermedio'):
        selected=[]
        for side in (-1,1):
            group=[p for p in candidates if p['familia']==family and p['lado']==side]
            assert group,(family,side)
            best=max(group,key=lambda p:(p['pares_primarios_tempranos'],p['virtuales_tempranos'],-max([r['corte_finito_estimado_Hz'] for r in p['rutas']] or [1e9])))
            assert best['pares_primarios_tempranos']>0,(family,side)
            selected.append(best)
        chosen[family]=selected
    chosen['combinado']=chosen['adelantado']+chosen['intermedio']
    chosen['selectivo']=[chosen['adelantado'][0]]+chosen['intermedio']
    save('paneles-elegidos.json',chosen)
    print('Candidatos',len(candidates),'seleccionados',[(k,[(p['centro'],p['pares_primarios_tempranos'],p['virtuales_tempranos']) for p in v]) for k,v in chosen.items()],flush=True)
    return chosen

def export(case,panels):
    folder=O/case;folder.mkdir(exist_ok=True)
    m=json.loads(json.dumps(MODEL));holes=[];details=[]
    for i,p in enumerate(panels):
        cc=np.array(corners(p)).astype(np.float32).astype(float);offset=len(m['vertices']);m['vertices'].extend(cc.tolist());holes.append(np.mean(cc,axis=0))
        cube_faces=[(0,1,2,3),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
        for a,b,c,d in cube_faces:
            for ids in ((a,b,c),(a,c,d)):
                ids=list(ids);tri=cc[ids];n=np.cross(tri[1]-tri[0],tri[2]-tri[0]);center=np.mean(tri,axis=0)
                if n@(center-holes[-1])<0:ids[1],ids[2]=ids[2],ids[1]
                f={**MODEL['faces'][0],'v':[offset+j for j in ids],'idMat':301,'idRs':-1,'idEn':-1};m['faces'].append(f)
        details.append(dict(id=i+1,**p))
    vertices=np.array(m['vertices']);ff=np.array([f['v'] for f in m['faces']])
    edges=collections.Counter(tuple(sorted(e)) for a,b,c in ff for e in ((a,b),(b,c),(c,a)))
    assert set(edges.values())=={2}
    volume=abs(np.einsum('ij,ij->i',vertices[ff[:,0]],np.cross(vertices[ff[:,1]],vertices[ff[:,2]])).sum()/6)
    expected=9543.733970598856-sum(p['ancho']*p['alto']*p['espesor'] for p in panels)
    assert abs(volume-expected)<.001,(case,volume,expected)
    (folder/'malla-subdividida.json').write_text(json.dumps(m),encoding='utf8')
    subprocess.run([str(native_mesh.NATIVE),str(B/'localizado_nativo.py'),str(folder/'malla-subdividida.json'),str(folder/'mesh.cbin')],check=True)
    with (folder/'scene.poly').open('w') as fp:
        fp.write(f'{len(vertices)} 3 0 0\n')
        for i,p in enumerate(vertices):fp.write(f'{i+1} '+' '.join(f'{x:.12g}' for x in p)+'\n')
        fp.write(f'{len(ff)} 1\n')
        for i,f in enumerate(ff):fp.write(f'1 0 {i+1}\n3 '+' '.join(str(x+1) for x in f)+'\n')
        fp.write(f'{len(holes)}\n')
        for i,p in enumerate(holes):fp.write(f'{i+1} '+' '.join(f'{x:.12g}' for x in p)+'\n')
        fp.write('0\n')
    with (folder/'tetgen.log').open('w') as log:
        proc=subprocess.run([str(native_mesh.TETGEN),'-pYa20T1e-10',str(folder/'scene.poly')],stdout=log,stderr=subprocess.STDOUT)
    assert proc.returncode==0,(case,(folder/'tetgen.log').read_text()[-2000:])
    native_mesh.O=folder;native_mesh.convert_tetra()
    (folder/'paneles.json').write_text(json.dumps(details,indent=2),encoding='utf8')
    (folder/'verificacion-geometrica.json').write_text(json.dumps(dict(caso=case,paneles=len(panels),area_frontal_m2=sum(p['ancho']*p['alto'] for p in panels),volumen_aire_m3=volume,volumen_desplazado_m3=9543.733970598856-volume,aristas_dos_caras=True),indent=2),encoding='utf8')
    # Generic OBJ usable in external viewers; distinct material IDs separate panels.
    with (folder/'modelo.obj').open('w') as fp:
        for p in vertices:fp.write('v '+' '.join(map(str,p))+'\n')
        last=None
        for f in m['faces']:
            if last!=f['idMat']:fp.write(f"g material_{f['idMat']}\n");last=f['idMat']
            fp.write('f '+' '.join(str(x+1) for x in f['v'])+'\n')
    print(case,'aire',round(volume,3),'m3',flush=True)

if __name__=='__main__':
    chosen=choose()
    export('base',[])
    for case,panels in chosen.items():export(case,panels)
