"""Variantes de cobertura: paneles rígidos completos con distintas orientaciones."""
from pathlib import Path
import json,itertools,math
import numpy as np
import preparar_reflectores as g
B=Path(__file__).resolve().parent;O=B/'reflectores-cobertura';O.mkdir(exist_ok=True)
old=B/'reflectores';g.O=O
audit=json.loads((old/'auditoria-posiciones.json').read_text())
S={k:np.array(v) for k,v in audit['fuentes'].items()};R={k:np.array(v) for k,v in audit['receptores'].items()}
SEATS=['V01','V02','V03','V04','V05','V08','V10','V11']
PRIMARY=[('F1','P8'),('F1','P9'),('F2','P8')]
PAIRS=PRIMARY+[(s,r) for s in S for r in SEATS]
index={p:i for i,p in enumerate(PAIRS)}
base=json.loads((old/'resultados/medias-N600000-a0.05-s0.05.json').read_text())
weights=[]
for pair in PAIRS:
    d=next(r['D50_pct'] for r in base if r['variante']=='base' and (r['fuente'],r['receptor'])==pair)
    w=.3 if d>=48 else min(3.,1+(48-d)/10)
    weights.append(w*(1.5 if pair in PRIMARY else 1.))
weights=np.array(weights)

def axes(p):return np.array([p['u'],p['v'],p['normal']])
def half(p):return np.array([p['ancho']/2,p['alto']/2,p['espesor']/2])
def floor_gap(p):
    """Vertical gap sampled over both faces; geometric study envelope, not a norm."""
    triangles=g.TRI;ids=np.array([f['idMat'] in (110,111,112,113) for f in g.MODEL['faces']])
    tt=triangles[ids];mats=np.array([f['idMat'] for f in g.MODEL['faces']])[ids]
    a=tt[:,0,:2];u=tt[:,1,:2]-a;v=tt[:,2,:2]-a;den=u[:,0]*v[:,1]-u[:,1]*v[:,0];valid=abs(den)>1e-9;den=np.where(valid,den,1)
    q=np.array(p['centro']);axes_=axes(p);h=half(p)
    points=np.array([q+aa*h[0]*axes_[0]+bb*h[1]*axes_[1]+cc*h[2]*axes_[2] for aa,bb,cc in itertools.product(np.linspace(-1,1,5),np.linspace(-1,1,5),(-1,1))])
    dx=points[:,None,0]-a[None,:,0];dy=points[:,None,1]-a[None,:,1]
    s=(dx*v[:,1]-dy*v[:,0])/den;t=(u[:,0]*dy-u[:,1]*dx)/den
    z=tt[None,:,0,2]+s*(tt[:,1,2]-tt[:,0,2])+t*(tt[:,2,2]-tt[:,0,2])
    mask=valid&(s>=-1e-6)&(t>=-1e-6)&(s+t<=1+1e-6)&(z<points[:,None,2]-1e-6)
    floor=np.where(mask,z,-np.inf);index_floor=floor.argmax(1);heights=floor.max(1);gaps=points[:,2]-heights
    i=int(gaps.argmin());assert np.isfinite(gaps[i])
    return dict(minimo_m=float(gaps[i]),punto_panel=points[i].tolist(),cota_piso_m=float(heights[i]),material_piso=int(mats[index_floor[i]]),muestras=50)
def blocks(p,a,b):
    ax=axes(p);start=(a-np.array(p['centro']))@ax.T;delta=(b-a)@ax.T;h=half(p)
    low=0.;high=1.
    for s,d,hh in zip(start,delta,h):
        if abs(d)<1e-10:
            if abs(s)>hh:return False
        else:
            aa,bb=sorted(((-hh-s)/d,(hh-s)/d));low=max(low,aa);high=min(high,bb)
            if high<low:return False
    return low<1-1e-5 and high>1e-5
def overlaps(a,b):
    aa=axes(a);bb=axes(b);delta=np.array(b['centro'])-a['centro']
    directions=list(aa)+list(bb)+[np.cross(x,y) for x in aa for y in bb]
    for n in directions:
        norm=np.linalg.norm(n)
        if norm<1e-9:continue
        n=n/norm
        extent=np.sum(abs(aa@n)*(half(a)+.04))+np.sum(abs(bb@n)*(half(b)+.04))
        if abs(delta@n)>extent:return False
    return True

def paths(p):
    result=[]
    for src,rec in PAIRS:
        route=g.specular(p,S[src],R[rec])
        if route and route['retardo_ms']<45 and route['corte_finito_estimado_Hz']<=1000:
            direct=np.linalg.norm(R[rec]-S[src]);gain=.95*.95*(direct/route['distancia_reflejada_m'])**2
            result.append(dict(fuente=src,receptor=rec,indice=index[(src,rec)],ganancia_geometrica=float(gain),**route))
    return result

def distribution(selected):
    values=np.zeros(len(PAIRS))
    for i,p in enumerate(selected):
        for route in p['rutas_utiles']:
            a=S[route['fuente']];b=R[route['receptor']];q=np.array(route['punto'])
            if any(blocks(other,a,q) or blocks(other,q,b) for j,other in enumerate(selected) if i!=j):continue
            values[route['indice']]+=route['ganancia_geometrica']
    return values

def score(selected,mode):
    d=distribution(selected)
    if mode=='cobertura':return float(weights@np.minimum(d,1.))
    # Diminishing returns plus reward for balanced depth groups; still geometric.
    totals=[]
    for names in (['V01','V02','V03','V04'],['V05','V08'],['V10','V11']):
        ids=[index[(s,r)] for s in S for r in names];totals.append(float(np.mean(d[ids])))
    return float(weights@np.log1p(d)+2*min(totals))

def pool():
    result=[];seen=set();tested=0
    targets=['P8','P9']+SEATS
    sources=[S['F1'],S['F2'],(S['F1']+S['F2'])/2]
    for x,y,z in itertools.product((12.,16.,20.,24.,28.),(-7.,0.,7.),(8.,9.,10.)):
        q=np.array([x,y,z])
        if not g.inside(q):continue
        for target,s in itertools.product(targets,sources):
            tested+=1;p=g.panel(q,R[target],s)
            key=tuple(q)+tuple(np.round(p['normal'],4))
            if key in seen:continue
            seen.add(key)
            routes=paths(p)
            if not routes:continue
            cc=g.corners(p)
            if not all(g.inside(c) for c in cc):continue
            if any(not g.visible(a,b) for a,b in itertools.combinations(cc,2)):continue
            if any(blocks(p,s,r) for s in S.values() for r in R.values()):continue
            # Finite receiver spheres must remain outside each rigid box.
            if any(np.linalg.norm(np.maximum(abs((r-q)@axes(p).T)-half(p),0))<.32 for r in R.values()):continue
            p.update(candidato=f'C{len(result)+1:04}',objetivo_de_orientacion=target,rutas_utiles=routes)
            result.append(p)
        print('Centro',q.tolist(),'candidatos acumulados',len(result),flush=True)
    assert result
    g.save('candidatos.json',dict(orientaciones_exploradas=tested,candidatos=result))
    return result

def greedy(candidates,n,mode,initial=None):
    selected=list(initial or [])
    while len(selected)<n:
        eligible=[p for p in candidates if not any(overlaps(p,q) for q in selected)]
        assert eligible
        p=max(eligible,key=lambda p:score(selected+[p],mode));selected.append(p)
    return selected

def main():
    candidates=pool()
    previous=json.loads((old/'paneles-elegidos.json').read_text())['combinado']
    for i,p in enumerate(previous):p['candidato']=f'Anterior{i+1}';p['rutas_utiles']=paths(p)
    four=greedy(candidates,4,'cobertura')
    balanced=greedy(candidates,4,'equilibrio')
    if {p['candidato'] for p in four}=={p['candidato'] for p in balanced}:
        rear=max(candidates,key=lambda p:sum(r['ganancia_geometrica'] for r in p['rutas_utiles'] if r['receptor'] in ('V10','V11')))
        balanced=greedy(candidates,4,'equilibrio',[rear])
    central=[]
    for p in candidates:
        if any(overlaps(p,q) for q in previous):continue
        central.append(p)
    assert central
    extra=max(central,key=lambda p:sum(distribution(previous+[p])[index[(s,r)]] for s in S for r in ('V02','V03')))
    cases=dict(cobertura4=four,equilibrio4=balanced,cobertura6=greedy(candidates,6,'equilibrio',four),central5=previous+[extra])
    assert len({tuple(sorted(p['candidato'] for p in ps)) for ps in cases.values()})==4
    g.save('variantes.json',cases)
    g.save('criterios-geometricos.json',dict(pares_ponderados=[dict(fuente=s,receptor=r,peso=float(weights[i])) for i,(s,r) in enumerate(PAIRS)],
        control_no_optimizado='F2-P9 y puntos sobre madera; se conservan todos los 21 receptores en SPPS',
        material='alpha .05, dispersion .05 a 1000 Hz; no cambia entre variantes',
        condiciones='Paneles 4x3 m, 20 mm. Dentro de envolvente, sin interseccion entre cajas, sin bloquear segmentos directos de F1/F2 a 21 receptores, corte conservador <=1000 Hz y retardo <45 ms para rutas puntuadas. El puntaje es geometrico; no predice D50/C80.'))
    for case,ps in cases.items():
        print(case,[p['candidato'] for p in ps],flush=True)
        g.export(case,ps)
    g.save('cobertura-geometrica.json',{case:[dict(fuente=s,receptor=r,aporte_geometrico=float(distribution(ps)[i])) for i,(s,r) in enumerate(PAIRS)] for case,ps in cases.items()})

if __name__=='__main__':main()
