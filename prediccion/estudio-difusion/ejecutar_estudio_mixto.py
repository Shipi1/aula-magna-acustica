"""Mismo motor y condiciones; solo cambia absorción de los paños elegidos."""
from pathlib import Path
import json,argparse,xml.etree.ElementTree as ET,hashlib
from concurrent.futures import ThreadPoolExecutor
import ejecutar_reflectores as r
O=Path(__file__).resolve().parent/'reflectores-absorcion-localizada';r.O=O
original_config=r.config
def config(out,case,src,freq,n,seed,alpha=.05,scatter=.05):
    original_config(out,case,src,freq,n,seed,alpha,scatter)
    p=json.loads((O/'perfiles.json').read_text())[case];root=ET.parse(out/'config.xml').getroot()
    if p['alpha'] is not None:
        mat=next(m for m in root.find('surface_absorption_enum') if m.get('id')=='201')
        band=next(b for b in mat if b.get('freq')=='1000');band.set('absorb',str(p['alpha']))
    ET.indent(root);ET.ElementTree(root).write(out/'config.xml',encoding='utf8',xml_declaration=True)
r.config=config
def run(case,src,N,seed):
    r.run(case,src,1000,N,seed,.05,.05)
    folder=O/'calculos'/f'{case}-{src}-1000Hz-N{N}-seed{seed}-a0.05-s0.05';meta=folder/'ejecucion.json';d=json.loads(meta.read_text());p=json.loads((O/'perfiles.json').read_text())[case]
    d.update(alpha_absorbente=p['alpha'],area_absorbente_m2=p['area_m2'],referencia_estudio='Cuatro reflectores con giro combinado; particion comun')
    meta.write_text(json.dumps(d,indent=2),encoding='utf8')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cases',nargs='+');p.add_argument('--N',type=int,default=600000);p.add_argument('--seeds',nargs='+',type=int,default=[20261019,20261020,20261021]);p.add_argument('--jobs',type=int,default=3);a=p.parse_args()
    cases=a.cases or list(json.loads((O/'perfiles.json').read_text()));tasks=[(c,s,a.N,seed) for c in cases for s in ('F1','F2') for seed in a.seeds]
    (O/f"matriz-N{a.N}-{'_'.join(cases)}.json").write_text(json.dumps(tasks,indent=2),encoding='utf8')
    with ThreadPoolExecutor(max_workers=a.jobs) as pool:
        futures=[pool.submit(run,*task) for task in tasks]
        for f in futures:f.result()
