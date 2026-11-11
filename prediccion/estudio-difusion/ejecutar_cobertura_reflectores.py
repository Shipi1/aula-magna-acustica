"""Corridas de nuevas geometrías, sin alterar las referencias anteriores."""
from pathlib import Path
import json,argparse
from concurrent.futures import ThreadPoolExecutor
import ejecutar_reflectores as runner
O=Path(__file__).resolve().parent/'reflectores-cobertura';runner.O=O
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cases',nargs='+',default=['cobertura4','equilibrio4','cobertura6','central5']);p.add_argument('--sources',nargs='+',default=['F1','F2']);p.add_argument('--N',type=int,default=600000);p.add_argument('--seeds',nargs='+',type=int,default=[20261019,20261020,20261021]);p.add_argument('--jobs',type=int,default=3);a=p.parse_args()
    tasks=[(c,s,1000,a.N,seed,.05,.05) for c in a.cases for s in a.sources for seed in a.seeds]
    (O/f"matriz-N{a.N}-{'_'.join(a.cases)}.json").write_text(json.dumps(tasks,indent=2),encoding='utf8')
    with ThreadPoolExecutor(max_workers=a.jobs) as pool:
        futures=[pool.submit(runner.run,*task) for task in tasks]
        for f in futures:f.result()
