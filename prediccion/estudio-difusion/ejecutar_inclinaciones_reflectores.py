"""Corridas de orientación/segmentación con material fijo."""
import json,argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import ejecutar_reflectores as r
r.O=Path(__file__).resolve().parent/'reflectores-inclinacion'
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cases',nargs='+');p.add_argument('--N',type=int,default=600000);p.add_argument('--seeds',nargs='+',type=int,default=[20261019,20261020,20261021]);p.add_argument('--jobs',type=int,default=3);a=p.parse_args()
    cases=a.cases or list(json.loads((r.O/'variantes.json').read_text()));tasks=[(c,s,1000,a.N,seed,.05,.05) for c in cases for s in ('F1','F2') for seed in a.seeds]
    (r.O/f"matriz-N{a.N}-{'_'.join(cases)}.json").write_text(json.dumps(tasks,indent=2),encoding='utf8')
    with ThreadPoolExecutor(max_workers=a.jobs) as pool:
        futures=[pool.submit(r.run,*t) for t in tasks]
        for f in futures:f.result()
