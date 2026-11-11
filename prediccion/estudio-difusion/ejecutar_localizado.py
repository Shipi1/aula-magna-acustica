"""Exploración de paños R/C/RC/D con una misma malla y receptores."""
from ejecutar import config as original_config, ENGINE, NATIVE, native
from preparar_localizado import B,O,save
import numpy as np
import json,copy,subprocess,time,hashlib,os,argparse
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

def clearance(point,tri):
    a=tri[:,0];u=tri[:,1]-a;v=tri[:,2]-a;q=point-a
    uu=np.einsum('ij,ij->i',u,u);vv=np.einsum('ij,ij->i',v,v);uv=np.einsum('ij,ij->i',u,v)
    qu=np.einsum('ij,ij->i',q,u);qv=np.einsum('ij,ij->i',q,v);den=uu*vv-uv*uv
    s=(qu*vv-qv*uv)/den;t=(qv*uu-qu*uv)/den
    n=np.cross(u,v);d=abs(np.einsum('ij,ij->i',q,n))/np.linalg.norm(n,axis=1)
    d=np.where((s>=0)&(t>=0)&(s+t<=1),d,np.inf)
    for j,k in ((0,1),(1,2),(2,0)):
        e=tri[:,k]-tri[:,j];q=point-tri[:,j]
        z=np.clip(np.einsum('ij,ij->i',q,e)/np.einsum('ij,ij->i',e,e),0,1)
        d=np.minimum(d,np.linalg.norm(q-z[:,None]*e,axis=1))
    return float(d.min())

def receivers():
    m=json.loads((O/'malla-subdividida.json').read_text());v=np.array(m['vertices']);tri=v[np.array([f['v'] for f in m['faces']])]
    seats=np.array([p for f,p in zip(m['faces'],tri) if f['idMat'] in (110,112,113) and p[:,2].min()>3.5])
    result=[]
    for x in (26.,31.,36.):
        for y in (-9.,-3.,3.,9.):
            p=np.array([x,y]);a=seats[:,0,:2];u=seats[:,1,:2]-a;w=seats[:,2,:2]-a;q=p-a
            det=u[:,0]*w[:,1]-u[:,1]*w[:,0];valid=abs(det)>1e-9;safe=np.where(valid,det,1.)
            s=(q[:,0]*w[:,1]-q[:,1]*w[:,0])/safe;t=(u[:,0]*q[:,1]-u[:,1]*q[:,0])/safe
            mask=valid&(s>=-1e-6)&(t>=-1e-6)&(s+t<=1+1e-6)
            assert mask.any(),('Sin suelo de butacas altas',x,y)
            z=seats[:,0,2]+s*(seats[:,1,2]-seats[:,0,2])+t*(seats[:,2,2]-seats[:,0,2])
            floor=float(z[mask].max());point=np.array([x,y,floor+2]);dist=clearance(point,tri)
            assert dist>.31,('Esfera intersecta frontera',point,dist)
            result.append(dict(nombre=f'V{len(result)+1:02}',x=x,y=y,z=float(point[2]),piso_z_m=floor,altura_local_m=2.,distancia_minima_superficie_m=dist,medido=False))
    save('receptores-virtuales.json',result)
    return result

def config(out,variant,src,freq,n,seed):
    original_config(out,'base',src,freq,n,seed,.6)
    root=ET.parse(out/'config.xml').getroot();sim=root.find('simulation')
    sim.set('modelName',os.path.relpath(O/(variant+'.cbin'),out));sim.set('tetrameshFileName',os.path.relpath(O/'tetramesh.mbin',out))
    mats=root.find('surface_absorption_enum')
    for original,new in [('115','201'),('108','202')]:
        parent=next(m for m in mats if m.get('id')==original);clone=copy.deepcopy(parent);clone.set('id',new)
        for bf in clone:
            if int(bf.get('freq'))==freq:bf.set('diffusion','.6');bf.set('loi','2')
        assert [b.get('absorb') for b in clone]==[b.get('absorb') for b in parent]
        mats.append(clone)
    group=root.find('recepteursp');template=group[0]
    for i,rec in enumerate(json.loads((O/'receptores-virtuales.json').read_text())):
        element=copy.deepcopy(template);element.set('id',str(20001+i));element.set('name',rec['nombre']);element.set('lbl',rec['nombre'])
        for k in ('x','y','z'):element.set(k,str(rec[k]))
        group.append(element)
    assert len(group)==21
    ET.indent(root);ET.ElementTree(root).write(out/'config.xml',encoding='utf8',xml_declaration=True)

def run(variant,src,freq,n,seed):
    out=O/'calculos'/f'{variant}-{src}-{freq}Hz-N{n}-seed{seed}';out.mkdir(parents=True,exist_ok=True)
    if (out/'ejecucion.json').exists():return
    config(out,variant,src,freq,n,seed);start=time.time()
    with (out/'motor.log').open('w') as log:r=subprocess.run([str(ENGINE),str(out/'config.xml')],cwd=out,stdout=log,stderr=subprocess.STDOUT)
    assert r.returncode==0,(out,r.returncode)
    native('read',out)
    data=json.loads((out/'resultados-lineales.json').read_text());assert len(data['receptores'])==21
    stats=data['estadisticas'][1];loss=(stats[4]+stats[5])/stats[-1]
    assert loss<.005,('Pérdidas de malla excesivas',loss,out)
    meta=dict(variante=variant,fuente=src,frecuencia=freq,N=n,semilla=seed,segundos=time.time()-start,fraccion_perdidas=loss,config_sha256=hashlib.sha256((out/'config.xml').read_bytes()).hexdigest(),malla_sha256=hashlib.sha256((O/(variant+'.cbin')).read_bytes()).hexdigest(),tetra_sha256=hashlib.sha256((O/'tetramesh.mbin').read_bytes()).hexdigest())
    (out/'ejecucion.json').write_text(json.dumps(meta,indent=2),encoding='utf8');print(out.name,round(meta['segundos'],1),'s',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--variants',nargs='+',default=['base','R','C','RC','D']);parser.add_argument('--sources',nargs='+',default=['F1','F2']);parser.add_argument('--freqs',nargs='+',type=int,default=[1000,2000,4000,8000]);parser.add_argument('--N',type=int,default=150000);parser.add_argument('--jobs',type=int,default=3);parser.add_argument('--seeds',nargs='+',type=int,default=[20261019]);args=parser.parse_args()
    receivers()
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures=[pool.submit(run,v,s,f,args.N,seed) for v in args.variants for s in args.sources for f in args.freqs for seed in args.seeds]
        for future in futures:future.result()
