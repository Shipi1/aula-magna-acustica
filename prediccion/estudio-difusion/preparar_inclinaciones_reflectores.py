"""Orientaciones controladas a igual área y segmentación posterior."""
import json,copy,itertools,math
import numpy as np
import preparar_cobertura_reflectores as h
B=h.B;O=B/'reflectores-inclinacion';O.mkdir(exist_ok=True);h.g.O=O
OBJ=json.loads((B/'reflectores-frente-media/objetivo.json').read_text())
TARGET=OBJ['frente_butacas']+OBJ['media_butacas'];PAIRS=h.PRIMARY+[(s,r) for s in h.S for r in TARGET]
original=json.loads((B/'reflectores/paneles-elegidos.json').read_text())['combinado']
baseline=json.loads((B/'reflectores/resultados/medias-N600000-a0.05-s0.05.json').read_text())
weights=np.array([max(.3,min(3.,1+(48-next(r['D50_pct'] for r in baseline if r['variante']=='combinado' and (r['fuente'],r['receptor'])==pair))/10)) for pair in PAIRS])
def save(name,x):(O/name).write_text(json.dumps(x,indent=2,ensure_ascii=False),encoding='utf8')
def rotate(v,axis,angle):
    axis=np.array(axis,float);axis/=np.linalg.norm(axis);t=np.deg2rad(angle);v=np.array(v,float)
    return v*np.cos(t)+np.cross(axis,v)*np.sin(t)+axis*(axis@v)*(1-np.cos(t))
def turn(p,pitch,yaw):
    q=copy.deepcopy(p);u=rotate(p['u'],[0,0,1],yaw)
    for k in ('u','v','normal'):q[k]=rotate(rotate(p[k],[0,0,1],yaw),u,pitch).tolist()
    q['giro_vertical_grados']=float(pitch);q['giro_horizontal_grados']=float(yaw)
    for k in ('rutas','rutas_utiles','rutas_actuales'):q.pop(k,None)
    q['rutas_utiles']=paths(q);return q
def paths(p):
    result=[]
    for i,(src,rec) in enumerate(PAIRS):
        route=h.g.specular(p,h.S[src],h.R[rec])
        if route and route['retardo_ms']<45 and route['corte_finito_estimado_Hz']<=1000:
            direct=np.linalg.norm(h.R[rec]-h.S[src]);gain=.95**2*(direct/route['distancia_reflejada_m'])**2
            result.append(dict(fuente=src,receptor=rec,indice=i,ganancia_geometrica=float(gain),**route))
    return result
def valid(p):
    cc=h.g.corners(p)
    if not all(h.g.inside(c) for c in cc):return False
    if not all(h.g.visible(a,b) for a,b in itertools.combinations(cc,2)):return False
    if any(h.blocks(p,s,r) for s in h.S.values() for r in h.R.values()):return False
    q=np.array(p['centro'])
    if any(np.linalg.norm(np.maximum(abs((r-q)@h.axes(p).T)-h.half(p),0))<.32 for r in h.R.values()):return False
    return h.floor_gap(p)['minimo_m']>=2.31
def distribution(ps):
    values=np.zeros(len(PAIRS))
    for i,p in enumerate(ps):
        for route in p['rutas_utiles']:
            q=np.array(route['punto']);s=h.S[route['fuente']];r=h.R[route['receptor']]
            if any(h.blocks(other,s,q) or h.blocks(other,q,r) for j,other in enumerate(ps) if j!=i):continue
            values[route['indice']]+=route['ganancia_geometrica']
    return values
def score(ps):
    values=distribution(ps);front=[i for i,(_,r) in enumerate(PAIRS) if r in OBJ['frente_butacas']];mid=[i for i,(_,r) in enumerate(PAIRS) if r in OBJ['media_butacas']]
    return float(weights@np.log1p(values)+3*min(np.mean(values[front]),np.mean(values[mid])))
def optimize(seed,angles,label):
    pools=[]
    for i,p in enumerate(seed):
        pool=[]
        for pitch,yaw in angles:
            q=turn(p,pitch,yaw)
            if valid(q):pool.append(q)
        assert pool,(label,i)
        pools.append(pool);print(label,'panel',i+1,'candidatos',len(pool),flush=True)
    current=[turn(p,0,0) for p in seed];trace=[]
    for cycle in range(3):
        before=score(current)
        for i,pool in enumerate(pools):
            eligible=[q for q in pool if not any(h.overlaps(q,r) for j,r in enumerate(current) if i!=j)]
            assert eligible
            current[i]=max(eligible,key=lambda q:score(current[:i]+[q]+current[i+1:]))
        trace.append(dict(ciclo=cycle+1,puntaje=score(current)))
        if abs(score(current)-before)<1e-9:break
    save('busqueda-'+label+'.json',dict(candidatos_por_panel=[len(p) for p in pools],traza=trace,paneles=current))
    print(label,'puntaje',score(current),'giros',[(p['giro_vertical_grados'],p['giro_horizontal_grados']) for p in current],flush=True)
    return current
def main():
    cases={}
    cases['vertical']=optimize(original,list(itertools.product(range(-20,21,5),(0,))),'vertical')
    cases['horizontal']=optimize(original,list(itertools.product((0,),range(-20,21,5))),'horizontal')
    cases['combinada']=optimize(original,list(itertools.product(range(-20,21,5),range(-20,21,5))),'combinada')
    for case,ps in cases.items():h.g.export(case,ps)
    save('variantes.json',cases);save('objetivo.json',OBJ)
    save('criterios.json',dict(area_frontal_m2=48,alpha_1000=.05,dispersion=.05,espesor_m=.02,centros_conservados=True,
        referencia='combinado del primer ciclo: cuatro paneles de 4x3m',
        rotaciones='Yaw alrededor de Z global; después pitch alrededor del eje u girado. Se rotan los tres ejes del panel.',
        seleccion='Ascenso por coordenadas, hasta tres ciclos; malla de -20 a +20 grados en pasos de 5; óptimo local geométrico, no predicción de indicadores.',
        pares=[dict(fuente=s,receptor=r,peso=float(weights[i])) for i,(s,r) in enumerate(PAIRS)],
        criterio='Ganancia de primera reflexión visible antes de 45ms, corte finito estimado <=1000Hz; utilidad logarítmica ponderada y equilibrio frente/media. Las rutas se vuelven a comprobar con los demás paneles presentes.'))
    spatial=[]
    for case,ps in cases.items():
        assert not any(h.overlaps(a,b) for a,b in itertools.combinations(ps,2))
        assert abs(sum(p['ancho']*p['alto'] for p in ps)-48)<1e-8
        for i,p in enumerate(ps):
            assert p['centro']==original[i]['centro']
            spatial.append(dict(variante=case,panel=i+1,holgura_vertical=h.floor_gap(p),segmentos_directos_preservados=42))
    save('verificacion-espacial.json',spatial)
if __name__=='__main__':main()
