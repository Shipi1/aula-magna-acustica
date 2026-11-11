"""Fuentes imagen hasta tercer orden en planos de la malla SPPS vigente.

Solo geometría y visibilidad: no calcula amplitudes ni confirma causalidad de picos.
"""
from pathlib import Path
import json,csv,itertools
import xml.etree.ElementTree as ET
import numpy as np
B=Path(__file__).resolve().parent
m=json.loads((B/'malla-base.json').read_text());v=np.array(m['vertices']);tri=v[np.array([f['v'] for f in m['faces']])]
v0=tri[:,0];e1=tri[:,1]-v0;e2=tri[:,2]-v0
patches=json.loads((B/'panos.json').read_text())

def hits(a,b):
    direction=b-a;h=np.cross(direction,e2);det=np.einsum('ij,ij->i',e1,h);valid=abs(det)>1e-9
    inv=np.zeros(len(det));inv[valid]=1/det[valid]
    s=a-v0;u=inv*np.einsum('ij,ij->i',s,h);q=np.cross(s,e1)
    w=inv*np.einsum('j,ij->i',direction,q);t=inv*np.einsum('ij,ij->i',e2,q)
    mask=valid&(u>=-1e-6)&(w>=-1e-6)&(u+w<=1+1e-6)&(t>=0)&(t<=1)
    return t[mask]

def on_faces(p,ids):
    a=v0[ids];u=e1[ids];w=e2[ids];q=p-a
    uu=np.einsum('ij,ij->i',u,u);ww=np.einsum('ij,ij->i',w,w);uw=np.einsum('ij,ij->i',u,w)
    qu=np.einsum('ij,ij->i',q,u);qw=np.einsum('ij,ij->i',q,w);den=uu*ww-uw*uw
    valid=den>1e-10; den=np.where(valid,den,1)
    s=(ww*qu-uw*qw)/den;t=(uu*qw-uw*qu)/den
    normals=np.cross(u,w);distance=abs(np.einsum('ij,ij->i',q,normals))/np.maximum(np.linalg.norm(normals,axis=1),1e-20)
    return np.array(ids)[valid&(s>=-1e-5)&(t>=-1e-5)&(s+t<=1+1e-5)&(distance<1e-4)].tolist()

planes={}
for name,axis,coord in [('lateral_Yneg',1,-11.665),('lateral_Ypos',1,11.665),('fondo_alto',0,40.25)]:
    ids=[i for i,p in enumerate(tri) if np.all(abs(p[:,axis]-coord)<1e-4)]
    n=np.eye(3)[axis];planes[name]=(n,coord,ids)
roof={}
for i,f in enumerate(m['faces']):
    if f['idMat']!=108 or tri[i,:,2].min()<9.7:continue
    n=np.cross(e1[i],e2[i]);n/=np.linalg.norm(n)
    if n[np.argmax(abs(n))]<0:n=-n
    d=float(n@tri[i,0]);key=tuple(np.round(n,4))+tuple([round(d,3)])
    if key not in roof:roof[key]=[n,d,[]]
    roof[key][2].append(i)
for j,value in enumerate(roof.values()):planes[f'cielo_{j+1}']=value

def reflect(p,plane):
    n,d,_=plane;return p-2*(p@n-d)*n

def path(source,receiver,seq):
    images=[source]
    for name in seq:images.append(reflect(images[-1],planes[name]))
    current=receiver.copy();back=[];facehits=[]
    for j in range(len(seq)-1,-1,-1):
        n,d,ids=planes[seq[j]];direction=images[j+1]-current;den=direction@n
        if abs(den)<1e-9:return None
        t=(d-current@n)/den
        if not 0<t<1:return None
        p=current+t*direction;fs=on_faces(p,ids)
        if not fs:return None
        back.append(p);facehits.append(fs);current=p
    pts=[source]+back[::-1]+[receiver]
    for a,b in zip(pts,pts[1:]):
        ts=hits(a,b)
        if np.any((ts>1e-5)&(ts<1-1e-5)):return None
    return pts,facehits[::-1]

rows=[]
for src in ['F1','F2']:
    r=ET.parse(B.parent/'convergencia-base-D/curva-espectral'/f'G-{src}-2000Hz/config.xml').getroot()
    source=np.array([float(list(r.find('sources'))[0].get(k)) for k in ['x','y','z']])
    for receiver in r.find('recepteursp'):
        if receiver.get('name') not in ['P8','P9']:continue
        point=np.array([float(receiver.get(k)) for k in ['x','y','z']]);direct=np.linalg.norm(point-source)
        assert not np.any((hits(source,point)>1e-5)&(hits(source,point)<1-1e-5))
        for order in [1,2,3]:
            for seq in itertools.product(planes,repeat=order):
                if any(a==b for a,b in zip(seq,seq[1:])):continue
                result=path(source,point,seq)
                if result is None:continue
                pts,fs=result;length=sum(np.linalg.norm(b-a) for a,b in zip(pts,pts[1:]))
                hit=[name for name,d in patches.items() if any(set(x)&set(d['faces']) for x in fs)]
                rows.append({'fuente':src,'receptor':receiver.get('name'),'orden':order,'superficies':' > '.join(seq),'retardo_ms':(length-direct)/342*1000,'panos_interceptados':';'.join(hit),'rebotes_xyz':json.dumps([p.tolist() for p in pts[1:-1]])})
        print(src,receiver.get('name'),'done',flush=True)
out=B/'resultados';out.mkdir(exist_ok=True)
with (out/'recorridos-candidatos-malla-vigente.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(out/'planos-recorridos.json').write_text(json.dumps({k:{'normal':n.tolist(),'d':d,'faces':ids} for k,(n,d,ids) in planes.items()},indent=2),encoding='utf8')
print('visible paths',len(rows),'planes',len(planes))
