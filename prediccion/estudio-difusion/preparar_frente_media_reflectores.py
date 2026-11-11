"""Ensayo dirigido: adelantar el retorno lateral de 50–80 hacia 0–50 ms."""
from pathlib import Path
import json,itertools,copy,xml.etree.ElementTree as ET,hashlib
import numpy as np
import preparar_cobertura_reflectores as h
B=Path(__file__).resolve().parent;O=B/'reflectores-frente-media';O.mkdir(exist_ok=True);h.g.O=O
objective=json.loads((B/'reflectores-cobertura/objetivo-frente-media.json').read_text())
TARGET=objective['frente_butacas']+objective['media_butacas']
PAIRS=[tuple(x) for x in objective['pares_campo_prioritarios']]+[(s,r) for s in h.S for r in TARGET]
assert not any(r in ('V09','V10','V11','V12') for s,r in PAIRS)
def save(name,x):(O/name).write_text(json.dumps(x,indent=2,ensure_ascii=False),encoding='utf8')
def side(y):
    n=np.array([0.,-np.sign(y),0.]);u=np.array([1.,0.,0.]);v=np.cross(n,u)
    return dict(centro=[15.5,float(y),4.4],normal=n.tolist(),u=u.tolist(),v=v.tolist(),ancho=6.,alto=3.,espesor=.02,funcion='Retorno lateral hacia frente y media')
def records(p):
    routes=[]
    for s in h.S:
        for r in h.R:
            path=h.g.specular(p,h.S[s],h.R[r])
            if path:routes.append(dict(fuente=s,receptor=r,objetivo=(s,r) in PAIRS,**path))
    return routes
def wall_path(s,r,y):
    image=s.copy();image[1]=2*y-s[1];t=(y-r[1])/(image[1]-r[1]);q=r+t*(image-r)
    tri=h.g.TRI;a=tri[:,0];u=tri[:,1]-a;v=tri[:,2]-a;w=q-a
    uu=np.einsum('ij,ij->i',u,u);vv=np.einsum('ij,ij->i',v,v);uv=np.einsum('ij,ij->i',u,v);wu=np.einsum('ij,ij->i',w,u);wv=np.einsum('ij,ij->i',w,v);den=uu*vv-uv*uv
    ss=(wu*vv-wv*uv)/den;tt=(wv*uu-wu*uv)/den;n=np.cross(u,v);dist=abs(np.einsum('ij,ij->i',w,n))/np.linalg.norm(n,axis=1)
    mask=(ss>=-1e-5)&(tt>=-1e-5)&(ss+tt<=1+1e-5)&(dist<1e-4)
    mats=sorted({f['idMat'] for f,keep in zip(h.g.MODEL['faces'],mask) if keep})
    delay=(np.linalg.norm(s-q)+np.linalg.norm(q-r)-np.linalg.norm(r-s))/342*1000
    return dict(punto=q.tolist(),retardo_ms=float(delay),sobre_superficie=bool(mask.any()),materiales=mats,visible=bool(mask.any()) and h.g.visible(s,q) and h.g.visible(q,r))
def main():
    old=json.loads((B/'reflectores/paneles-elegidos.json').read_text())
    pair9=[side(-9.),side(9.)];pair8=[side(-8.),side(8.)]
    geometries=dict(lateral9=pair9,lateral8=pair8,lateral8_adel=pair8+old['adelantado'],lateral8_inter=pair8+old['intermedio'])
    root=ET.parse(B/'reflectores/calculos/base-F1-1000Hz-N600000-seed20261019-a0.05-s0.05/config.xml').getroot()
    wall=next(m for m in root.find('surface_absorption_enum') if m.get('id')=='115');alpha=float(next(b for b in wall if b.get('freq')=='1000').get('absorb'))
    geometries['lateral8_equiv']=copy.deepcopy(pair8)
    profiles={c:dict(alpha=alpha if c=='lateral8_equiv' else .05,dispersion=.05,area_m2=sum(p['ancho']*p['alto'] for p in ps),paneles=len(ps),tipo='control de absorcion igual a muro efectivo' if c=='lateral8_equiv' else 'reflector nominal') for c,ps in geometries.items()}
    checks=[]
    for c,ps in geometries.items():
        assert not any(h.overlaps(a,b) for a,b in itertools.combinations(ps,2))
        assert not any(h.blocks(p,s,r) for p in ps for s in h.S.values() for r in h.R.values())
        for i,p in enumerate(ps,1):
            corners=h.g.corners(p);assert all(h.g.inside(q) for q in corners)
            assert all(h.g.visible(a,b) for a,b in itertools.combinations(corners,2))
            assert all(np.linalg.norm(np.maximum(abs((r-np.array(p['centro']))@h.axes(p).T)-h.half(p),0))>.32 for r in h.R.values())
            p['rutas_actuales']=records(p);gap=h.floor_gap(p);assert gap['minimo_m']>=2.31
            checks.append(dict(variante=c,panel=i,holgura_vertical=gap,segmentos_directos_preservados=42))
        h.g.export(c,ps)
    save('variantes.json',geometries);save('perfiles.json',profiles);save('objetivo.json',objective);save('verificacion-espacial.json',checks)
    for fn in ('mesh.cbin','tetramesh.mbin'):
        assert hashlib.sha256((O/'lateral8'/fn).read_bytes()).hexdigest()==hashlib.sha256((O/'lateral8_equiv'/fn).read_bytes()).hexdigest(),fn
    diagnostic=[]
    for s in h.S:
        for r in TARGET:
            for y in (-11.665,11.665):
                route=wall_path(h.S[s],h.R[r],y)
                alternatives={}
                for label,ps in [('lateral9',pair9),('lateral8',pair8)]:
                    p=ps[0 if y<0 else 1];alternatives[label]=h.g.specular(p,h.S[s],h.R[r])
                diagnostic.append(dict(fuente=s,receptor=r,muro_y_m=y,muro_actual=route,paneles=alternatives))
    critical=next(r for r in diagnostic if r['fuente']=='F2' and r['receptor']=='V08' and r['muro_y_m']<0)
    assert critical['muro_actual']['visible'] and critical['paneles']['lateral8']
    assert 50<critical['muro_actual']['retardo_ms']<80 and critical['paneles']['lateral8']['retardo_ms']<50
    save('hipotesis-retorno-lateral.json',diagnostic)
    print('F2-V08: muro',critical['muro_actual']['retardo_ms'],'ms; panel Y=-8',critical['paneles']['lateral8']['retardo_ms'],'ms',flush=True)
if __name__=='__main__':main()
