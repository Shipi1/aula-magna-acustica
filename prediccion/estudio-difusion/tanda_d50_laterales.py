"""Primera tanda: exploración de ubicación y repetición de referencia."""
import ejecutar_d50_laterales as study
from concurrent.futures import ThreadPoolExecutor
import json

if __name__=='__main__':
    r=study.runner;r.receivers()
    tasks=[(v,s,f,150000,20261019) for v in ('base','R','Lneg','Lpos') for s in ('F1','F2') for f in (500,1000)]
    tasks += [('base',s,f,600000,seed) for s in ('F1','F2') for f in (500,1000) for seed in (20261019,20261020,20261021)]
    (r.O/'matriz-tanda-inicial.json').write_text(json.dumps([dict(zip(('variante','fuente','frecuencia','N','semilla'),t)) for t in tasks],indent=2),encoding='utf8')
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures=[pool.submit(r.run,*task) for task in tasks]
        for future in futures:future.result()
