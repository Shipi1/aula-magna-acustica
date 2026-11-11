"""Predicción SPPS de paneles geométricos; fuente/receptores de referencia."""
from pathlib import Path
import argparse,json,subprocess,time,os,hashlib,copy,xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
import ejecutar_absorcion_posterior as previous
from ejecutar import ENGINE,native
B=Path(__file__).resolve().parent;O=B/'reflectores'

def config(out,case,src,freq,n,seed,alpha=.05,scatter=.05):
    assert freq==1000,'Esta primera etapa solo define material a 1.000 Hz'
    previous.config(out,'base',src,freq,n,seed)
    r=ET.parse(out/'config.xml').getroot();sim=r.find('simulation')
    sim.set('modelName',os.path.relpath(O/case/'mesh.cbin',out));sim.set('tetrameshFileName',os.path.relpath(O/case/'tetramesh.mbin',out))
    mats=r.find('surface_absorption_enum');m=copy.deepcopy(next(m for m in mats if m.get('id')=='115'));m.set('id','301')
    for bf in m:
        if int(bf.get('freq'))==freq:bf.set('absorb',str(alpha));bf.set('diffusion',str(scatter));bf.set('loi','2' if scatter>0 else '0')
    mats.append(m)
    assert len(r.find('recepteursp'))==21
    ET.indent(r);ET.ElementTree(r).write(out/'config.xml',encoding='utf8',xml_declaration=True)

def run(case,src,freq,n,seed,alpha=.05,scatter=.05):
    label=f'{case}-{src}-{freq}Hz-N{n}-seed{seed}-a{alpha:g}-s{scatter:g}'
    out=O/'calculos'/label;out.mkdir(parents=True,exist_ok=True)
    if (out/'ejecucion.json').exists():return
    config(out,case,src,freq,n,seed,alpha,scatter);start=time.time()
    with (out/'motor.log').open('w') as log:
        p=subprocess.run([str(ENGINE),str(out/'config.xml')],cwd=out,stdout=log,stderr=subprocess.STDOUT)
    assert p.returncode==0,(label,p.returncode)
    native('read',out);d=json.loads((out/'resultados-lineales.json').read_text());assert len(d['receptores'])==21
    stats=d['estadisticas'][1];lost=(stats[4]+stats[5])/stats[-1];assert lost<.005,(label,lost)
    def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
    meta=dict(variante=case,fuente=src,frecuencia=freq,N=n,semilla=seed,alpha=alpha,dispersion=scatter,fraccion_perdidas=lost,segundos=time.time()-start,
              config_sha256=sha(out/'config.xml'),malla_sha256=sha(O/case/'mesh.cbin'),tetra_sha256=sha(O/case/'tetramesh.mbin'))
    (out/'ejecucion.json').write_text(json.dumps(meta,indent=2),encoding='utf8');print(label,round(meta['segundos'],1),'s',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cases',nargs='+',default=['base','adelantado','intermedio','combinado']);p.add_argument('--sources',nargs='+',default=['F1','F2']);p.add_argument('--N',type=int,default=150000);p.add_argument('--seeds',type=int,nargs='+',default=[20261019]);p.add_argument('--jobs',type=int,default=3);p.add_argument('--alpha',type=float,default=.05);p.add_argument('--scatter',type=float,default=.05);a=p.parse_args()
    tasks=[(c,s,1000,a.N,seed,a.alpha,a.scatter) for c in a.cases for s in a.sources for seed in a.seeds]
    (O/f"matriz-N{a.N}-a{a.alpha:g}-s{a.scatter:g}-{'_'.join(a.cases)}.json").write_text(json.dumps(tasks,indent=2),encoding='utf8')
    with ThreadPoolExecutor(max_workers=a.jobs) as pool:
        futures=[pool.submit(run,*t) for t in tasks]
        for f in futures:f.result()
