"""Ensayos controlados de dispersión con SPPS instalado, sin alterar la base."""
from pathlib import Path
import json, copy, subprocess, time, hashlib, argparse, os
import xml.etree.ElementTree as ET
import numpy as np
from concurrent.futures import ThreadPoolExecutor

B=Path(__file__).resolve().parent
ROOT=B.parents[1]
ORIG=ROOT/'prediccion/convergencia-base-D/curva-espectral'
NATIVE=Path('C:/Program Files/I-SIMPA/python.exe')
ENGINE=Path('C:/Program Files/I-SIMPA/core/spps/spps.exe')

def save(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
def native(*args):
    r=subprocess.run([str(NATIVE),str(B/'nativo.py'),*map(str,args)],capture_output=True,text=True)
    if r.returncode: raise RuntimeError(r.stdout+r.stderr)

def prepare():
    m=json.loads((B/'malla-base.json').read_text());v=np.array(m['vertices'])
    patches={'lateral_Yneg':[], 'lateral_Ypos':[], 'fondo_alto':[]}
    # Geometry conditions, not centroid tests: every vertex stays in the upper region.
    for i,f in enumerate(m['faces']):
        if f['idMat']!=115: continue
        p=v[f['v']]
        if np.ptp(p[:,1])<1e-5 and abs(abs(p[0,1])-11.665)<1e-4 and p[:,0].min()>=20.4-1e-5 and p[:,2].min()>=4.2-1e-5:
            patches['lateral_Yneg' if p[0,1]<0 else 'lateral_Ypos'].append(i)
        if np.all(abs(p[:,0]-40.25)<1e-4): patches['fondo_alto'].append(i)
    info={}
    for name,ids in patches.items():
        p=v[np.array([m['faces'][i]['v'] for i in ids])]
        areas=np.linalg.norm(np.cross(p[:,1]-p[:,0],p[:,2]-p[:,0]),axis=1)/2
        info[name]={'faces':ids,'area_m2':float(areas.sum()),'min':p.reshape(-1,3).min(0).tolist(),'max':p.reshape(-1,3).max(0).tolist()}
    save(B/'panos.json',info)
    for name,ids in [('base',[])]+list(patches.items()):
        change=B/(name+'-caras.json');save(change,{str(i):201 for i in ids})
        native('mesh',ORIG/'mesh.cbin',B/(name+'.cbin'),change)
    return info

def config(out,variant,source,freq,n,seed,s):
    # Native historical config used 80 dB globally; shift all 27 source bands to 90 dB.
    r=ET.parse(ORIG/('G-'+source+'-2000Hz')/'config.xml').getroot()
    r.set('workingdirectory',str(out)+'\\')
    sim=r.find('simulation')
    sim.set('modelName',os.path.relpath(B/(variant+'.cbin'),out))
    sim.set('tetrameshFileName',os.path.relpath(ORIG/'tetramesh.mbin',out))
    sim.set('nbparticules',str(n));sim.set('nbparticules_rendu','0');sim.set('random_seed',str(seed))
    sim.set('pasdetemps','0.001');sim.set('duree_simulation','4')
    for bf in sim.find('freq_enum'):bf.set('docalc','1' if int(bf.get('freq'))==freq else '0')
    for src in r.find('sources'):
        for bf in src.findall('bfreq'):bf.set('db',str(float(bf.get('db'))+10))
        lw=10*np.log10(sum(10**(float(b.get('db'))/10) for b in src.findall('bfreq')))
        assert abs(lw-90)<1e-3,(lw,source)
    if variant!='base':
        mats=r.find('surface_absorption_enum')
        mat=copy.deepcopy(next(e for e in mats if e.get('id')=='115'));mat.set('id','201')
        for bf in mat.findall('bfreq'):
            if int(bf.get('freq'))==freq: bf.set('diffusion',str(s));bf.set('loi','2')
        mats.append(mat)
        orig=next(e for e in mats if e.get('id')=='115')
        assert [b.get('absorb') for b in mat]==[b.get('absorb') for b in orig]
    ET.indent(r);ET.ElementTree(r).write(out/'config.xml',encoding='utf-8',xml_declaration=True)

def run(variant,source,freq,n,seed,s):
    label=f'{variant}-s{s:g}-{source}-{freq}Hz-N{n}-seed{seed}'
    out=B/'calculos'/label;out.mkdir(parents=True,exist_ok=True)
    if (out/'ejecucion.json').exists() and (out/'resultados-lineales.json').exists():
        return
    config(out,variant,source,freq,n,seed,s)
    t=time.time()
    with (out/'motor.log').open('w',encoding='utf8') as log:
        proc=subprocess.run([str(ENGINE),str(out/'config.xml')],stdout=log,stderr=subprocess.STDOUT,cwd=out)
    assert proc.returncode==0, (label,proc.returncode)
    native('read',out)
    meta={'variante':variant,'fuente':source,'frecuencia':freq,'N':n,'semilla':seed,'dispersion':s if variant!='base' else .05,'segundos':time.time()-t,
          'config_sha256':hashlib.sha256((out/'config.xml').read_bytes()).hexdigest(),'mesh_sha256':hashlib.sha256((B/(variant+'.cbin')).read_bytes()).hexdigest()}
    save(out/'ejecucion.json',meta)
    print(label,'seconds',round(meta['segundos'],1),flush=True)

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--prepare',action='store_true');a.add_argument('--variants',nargs='+',default=['base','lateral_Yneg','lateral_Ypos','fondo_alto']);a.add_argument('--sources',nargs='+',default=['F1','F2']);a.add_argument('--freqs',type=int,nargs='+',default=[1000,2000,4000]);a.add_argument('--N',type=int,default=600000);a.add_argument('--seeds',type=int,nargs='+',default=[20261019]);a.add_argument('--s',type=float,default=.6);a.add_argument('--jobs',type=int,default=3)
    args=a.parse_args()
    if args.prepare: print(prepare(),flush=True)
    tasks=[(v,src,f,args.N,seed,args.s) for v in args.variants for src in args.sources for f in args.freqs for seed in args.seeds]
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures=[pool.submit(run,*task) for task in tasks]
        for future in futures:future.result()
