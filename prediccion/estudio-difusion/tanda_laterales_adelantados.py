"""Barrido y repeticiones predefinidas para evitar elegir solo cambios favorables."""
import ejecutar_localizado as runner
from preparar_localizado import B
from concurrent.futures import ThreadPoolExecutor
import json,argparse
runner.O=B/'laterales-adelantados'
runner.save=lambda name,d:(runner.O/name).write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--pilot',action='store_true');a=p.parse_args();runner.receivers()
    if a.pilot:runner.run('base','F1',1000,20000,20261019)
    else:
        variants=('base','Lneg','Lpos','Laterales');seeds=(20261019,20261020,20261021)
        tasks=[(v,s,f,150000,20261019) for v in variants for s in ('F1','F2') for f in (500,1000)]
        tasks += [(v,s,1000,600000,seed) for v in variants for s in ('F1','F2') for seed in seeds]
        tasks += [('base',s,500,600000,seed) for s in ('F1','F2') for seed in seeds]
        (runner.O/'matriz.json').write_text(json.dumps([dict(zip(('variante','fuente','frecuencia','N','semilla'),x)) for x in tasks],indent=2),encoding='utf8')
        with ThreadPoolExecutor(max_workers=3) as pool:
            futures=[pool.submit(runner.run,*task) for task in tasks]
            for future in futures:future.result()
