"""Control separado: baja absorción hipotética, no caracterización de un QRD."""
from ejecutar import B,config,ENGINE,native,save
from analizar import metric,db
import subprocess,json,time
import xml.etree.ElementTree as ET
import numpy as np
rows=[]
for source in ['F1','F2']:
    out=B/'sensibilidad-absorcion'/source;out.mkdir(parents=True,exist_ok=True)
    if not (out/'resultados-lineales.json').exists():
        config(out,'fondo_alto',source,2000,150000,20261019,.6)
        root=ET.parse(out/'config.xml').getroot()
        mat=next(e for e in root.find('surface_absorption_enum') if e.get('id')=='201')
        for bf in mat:
            if bf.get('freq')=='2000':bf.set('absorb','0.05')
        ET.ElementTree(root).write(out/'config.xml',encoding='utf8',xml_declaration=True)
        with (out/'motor.log').open('w',encoding='utf8') as log:
            r=subprocess.run([str(ENGINE),str(out/'config.xml')],stdout=log,stderr=subprocess.STDOUT,cwd=out)
        assert r.returncode==0
        native('read',out)
    result=json.loads((out/'resultados-lineales.json').read_text())
    basepath=B/'calculos'/f'base-s0.6-{source}-2000Hz-N150000-seed20261019'
    reference=json.loads((basepath/'resultados-lineales.json').read_text())
    conf=ET.parse(out/'config.xml').getroot();src=list(conf.find('sources'))[0]
    s=np.array([float(src.get(k)) for k in ['x','y','z']])
    for receiver in conf.find('recepteursp'):
        name=receiver.get('name');p=np.array([float(receiver.get(k)) for k in ['x','y','z']]);t0=np.linalg.norm(p-s)/342
        a=metric(np.array(next(iter(result['receptores'][name].values()))),t0)
        b=metric(np.array(next(iter(reference['receptores'][name].values()))),t0)
        rows.append({'fuente':source,'receptor':name,'alpha_base':.17,'alpha_hipotetico':.05,'s':.6,'delta_C80':a['C80']-b['C80'],**{'delta_'+k+'_dB':db(a[k]/b[k]) for k in ['total','E0_80','E80_300','E300_1000']}})
    print(source,'done',flush=True)
save(B/'resultados/sensibilidad-absorcion.json',rows)
