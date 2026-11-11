"""Corridas de absorción con dispersión invariable y condiciones comunes."""
from ejecutar import config as initial_config,ENGINE,native
import ejecutar_localizado as receiver_helper
from preparar_localizado import B
import json,xml.etree.ElementTree as ET,copy,subprocess,hashlib,time,os,argparse
from concurrent.futures import ThreadPoolExecutor
O=B/'absorcion-posterior'
receiver_helper.O=O
receiver_helper.save=lambda name,d:(O/name).write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')

def config(out,case,src,freq,n,seed):
    spec=json.loads((O/'escenarios.json').read_text())[case]
    initial_config(out,'base',src,freq,n,seed,.05)
    r=ET.parse(out/'config.xml').getroot();sim=r.find('simulation')
    sim.set('modelName',os.path.relpath(O/spec['malla'],out));sim.set('tetrameshFileName',os.path.relpath(O/'tetramesh.mbin',out))
    mats=r.find('surface_absorption_enum');original=next(m for m in mats if m.get('id')=='115');m=copy.deepcopy(original);m.set('id','201')
    if case!='base':
        assert str(freq) in spec['alpha_por_banda'],'No extrapolar coeficientes a bandas no definidas'
        for bf in m:
            if int(bf.get('freq'))==freq:bf.set('absorb',str(spec['alpha_por_banda'][str(freq)]))
    assert [(b.get('diffusion'),b.get('loi')) for b in original]==[(b.get('diffusion'),b.get('loi')) for b in m]
    mats.append(m)
    group=r.find('recepteursp');template=group[0]
    for i,rec in enumerate(json.loads((O/'receptores-virtuales.json').read_text())):
        e=copy.deepcopy(template);e.set('id',str(20001+i));e.set('name',rec['nombre']);e.set('lbl',rec['nombre'])
        for k in ('x','y','z'):e.set(k,str(rec[k]))
        group.append(e)
    assert len(group)==21
    ET.indent(r);ET.ElementTree(r).write(out/'config.xml',encoding='utf8',xml_declaration=True)
    return spec

def run(case,src,freq,n,seed):
    out=O/'calculos'/f'{case}-{src}-{freq}Hz-N{n}-seed{seed}';out.mkdir(parents=True,exist_ok=True)
    if (out/'ejecucion.json').exists():return
    spec=config(out,case,src,freq,n,seed);start=time.time()
    with (out/'motor.log').open('w') as log:p=subprocess.run([str(ENGINE),str(out/'config.xml')],cwd=out,stdout=log,stderr=subprocess.STDOUT)
    assert p.returncode==0,(out,p.returncode)
    native('read',out);data=json.loads((out/'resultados-lineales.json').read_text());assert len(data['receptores'])==21
    stats=data['estadisticas'][1];loss=(stats[4]+stats[5])/stats[-1];assert loss<.005,(out,loss)
    d=dict(variante=case,fuente=src,frecuencia=freq,N=n,semilla=seed,area_m2=spec['area_m2'],alpha_final=spec['alpha_por_banda'].get(str(freq)),segundos=time.time()-start,fraccion_perdidas=loss,config_sha256=hashlib.sha256((out/'config.xml').read_bytes()).hexdigest(),malla_sha256=hashlib.sha256((O/spec['malla']).read_bytes()).hexdigest(),tetra_sha256=hashlib.sha256((O/'tetramesh.mbin').read_bytes()).hexdigest())
    (out/'ejecucion.json').write_text(json.dumps(d,indent=2),encoding='utf8');print(out.name,round(d['segundos'],1),'s',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cases',nargs='+',default=['base','total_a100']);p.add_argument('--sources',nargs='+',default=['F1','F2']);p.add_argument('--freqs',nargs='+',type=int,default=[1000]);p.add_argument('--N',type=int,default=600000);p.add_argument('--seeds',nargs='+',type=int,default=[20261019,20261020,20261021]);p.add_argument('--jobs',type=int,default=3);a=p.parse_args()
    receiver_helper.receivers()
    tasks=[(c,s,f,a.N,seed) for c in a.cases for s in a.sources for f in a.freqs for seed in a.seeds]
    (O/f'matriz-N{a.N}.json').write_text(json.dumps([dict(zip(('caso','fuente','frecuencia','N','semilla'),t)) for t in tasks],indent=2),encoding='utf8')
    with ThreadPoolExecutor(max_workers=a.jobs) as pool:
        futures=[pool.submit(run,*task) for task in tasks]
        for future in futures:future.result()
