"""Matrices controladas D50/C80 en carpeta independiente de estudios previos."""
import ejecutar_localizado as runner
from preparar_localizado import B
import argparse
from concurrent.futures import ThreadPoolExecutor

runner.O=B/'d50-laterales'
# receivers() resolves save() in the original module; avoid writing to old study.
runner.save=lambda name,d: (runner.O/name).write_text(__import__('json').dumps(d,ensure_ascii=False,indent=2),encoding='utf8')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--variants',nargs='+',default=['base','R','Lneg','Lpos']);p.add_argument('--sources',nargs='+',default=['F1','F2']);p.add_argument('--freqs',nargs='+',type=int,default=[500,1000]);p.add_argument('--N',type=int,default=150000);p.add_argument('--seeds',nargs='+',type=int,default=[20261019]);p.add_argument('--jobs',type=int,default=3);a=p.parse_args()
    runner.receivers()
    with ThreadPoolExecutor(max_workers=a.jobs) as pool:
        futures=[pool.submit(runner.run,v,s,f,a.N,seed) for v in a.variants for s in a.sources for f in a.freqs for seed in a.seeds]
        for future in futures:future.result()
