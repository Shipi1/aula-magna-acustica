"""Barrido de octavas de la sala base y la propuesta; entradas independientes."""
from pathlib import Path
import json,copy,shutil,hashlib,time,subprocess,os,argparse,xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from ejecutar import ENGINE,native
B=Path(__file__).resolve().parent;O=B/'comparacion-octavas';O.mkdir(exist_ok=True)
FREQS=[63,125,250,500,1000,2000,4000,8000];SEEDS=[20261019,20261020,20261021]
SOURCE='https://www.ecophon.com/globalassets/old-structure/01.ecophon-master/technical-documentation/absorption_iso/akusto-wall/akusto_wall_wall_panel_a_super_g_ods43_octave.pdf/'
REFERENCE={125:.15,250:.65,500:1.,1000:1.,2000:1.,4000:1.}
ABS={63:.09,125:.09,250:.39,500:.60,1000:.60,2000:.60,4000:.60,8000:.60}
MODEL_SOURCES={'sin_tratamiento':B/'reflectores/base','propuesta':B/'reflectores-absorcion-localizada/media_centro_a060'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
def prepare():
    for case,source in MODEL_SOURCES.items():
        folder=O/'modelos'/case;folder.mkdir(parents=True,exist_ok=True)
        for f in ('mesh.cbin','tetramesh.mbin'):
            if not (folder/f).exists():shutil.copyfile(source/f,folder/f)
            assert sha(folder/f)==sha(source/f)
    save(O/'espectros.json',dict(frecuencias_Hz=FREQS,absorcion_pano=ABS,absorcion_reflectores={f:.05 for f in FREQS},dispersion_reflectores={f:.05 for f in FREQS},
        fuente_curva=SOURCE,ensayo='CSTB AC14-26051052/7, 01/10/2014; Akusto Wall A/Super G 40mm, profundidad total 43mm; coeficientes prácticos de octava.',
        coeficientes_publicados=REFERENCE,transformacion='Hipotesis efectiva alpha_A1(f)=0.60*alpha_referencia(f)/alpha_referencia(1000). Conserva el valor anterior de .60 a 1000Hz. No es el espectro ensayado del producto.',
        extremos='63Hz mantiene el valor de 125Hz y 8000Hz el de 4000Hz; extrapolaciones exploratorias sin dato de ensayo.',
        reflector='Superficie rigida idealizada alpha .05 y dispersion .05 constantes. Se ignoran resonancias y difraccion detallada; cautela especial en bajas frecuencias.',
        base='Se conserva todo el espectro efectivo de la sala, sin recalibrarlo. A 250Hz la absorcion efectiva original del muro (.60) supera la hipotesis nueva (.39).'))
    manifest=[]
    for case,source in [('sin_tratamiento',B/'reflectores'),('propuesta',B/'reflectores-absorcion-localizada')]:
        variant='base' if case=='sin_tratamiento' else 'media_centro_a060'
        for p in sorted((source/'calculos').glob('*/ejecucion.json')):
            d=json.loads(p.read_text())
            if d.get('variante')==variant and d.get('N')==600000 and d.get('frecuencia')==1000 and d.get('semilla') in SEEDS:
                cfg=ET.parse(p.parent/'config.xml').getroot();assert [int(f.get('freq')) for f in cfg.find('simulation/freq_enum') if f.get('docalc')=='1']==[1000]
                for mat in cfg.find('surface_absorption_enum'):
                    if case=='propuesta' and mat.get('id') in ('201','301'):
                        bf=next(f for f in mat if f.get('freq')=='1000');assert float(bf.get('absorb'))==(.6 if mat.get('id')=='201' else .05)
                assert sha(MODEL_SOURCES[case]/'mesh.cbin')==d['malla_sha256']
                manifest.append(dict(estado=case,fuente=d['fuente'],frecuencia=1000,semilla=d['semilla'],carpeta=str(p.parent.resolve()),N=d['N']))
    assert len(manifest)==12;save(O/'reutilizadas-1000Hz.json',manifest)
def config(out,case,src,freq,N,seed):
    variant='base' if case=='sin_tratamiento' else 'media_centro_a060'
    parent=B/('reflectores' if case=='sin_tratamiento' else 'reflectores-absorcion-localizada')/'calculos'
    template=next(parent.glob(f'{variant}-{src}-1000Hz-N600000-seed20261019*/config.xml'))
    r=ET.parse(template).getroot();r.set('workingdirectory',str(out)+'\\');sim=r.find('simulation')
    sim.set('modelName',os.path.relpath(O/'modelos'/case/'mesh.cbin',out));sim.set('tetrameshFileName',os.path.relpath(O/'modelos'/case/'tetramesh.mbin',out))
    sim.set('nbparticules',str(N));sim.set('random_seed',str(seed))
    for f in sim.find('freq_enum'):f.set('docalc','1' if int(f.get('freq'))==freq else '0')
    if case=='propuesta':
        for mat in r.find('surface_absorption_enum'):
            if mat.get('id') not in ('201','301'):continue
            for f in mat:
                hz=int(f.get('freq'))
                if hz not in FREQS:continue
                f.set('absorb',str(ABS[hz] if mat.get('id')=='201' else .05))
                if mat.get('id')=='301':f.set('diffusion','.05');f.set('loi','2')
    ET.indent(r);ET.ElementTree(r).write(out/'config.xml',encoding='utf8',xml_declaration=True)
def run(case,src,freq,N,seed):
    label=f'{case}-{src}-{freq}Hz-N{N}-seed{seed}';out=O/'calculos'/label;out.mkdir(parents=True,exist_ok=True)
    if (out/'ejecucion.json').exists() and not json.loads((out/'ejecucion.json').read_text()).get('pendiente',False):return
    config(out,case,src,freq,N,seed);start=time.time()
    with (out/'motor.log').open('w') as log:p=subprocess.run([str(ENGINE),str(out/'config.xml')],cwd=out,stdout=log,stderr=subprocess.STDOUT)
    assert p.returncode==0,(label,p.returncode)
    native('read',out);data=json.loads((out/'resultados-lineales.json').read_text());assert len(data['receptores'])==21
    assert all(len(next(iter(cols.values())))==4000 for cols in data['receptores'].values())
    stats=data['estadisticas'][1];lost=(stats[4]+stats[5])/stats[-1];assert lost<.005,(label,lost)
    save(out/'ejecucion.json',dict(variante=case,fuente=src,frecuencia=freq,N=N,semilla=seed,segundos=time.time()-start,fraccion_perdidas=lost,
        alpha_pano=ABS[freq] if case=='propuesta' else None,config_sha256=sha(out/'config.xml'),malla_sha256=sha(O/'modelos'/case/'mesh.cbin'),tetra_sha256=sha(O/'modelos'/case/'tetramesh.mbin')))
    print(label,round(time.time()-start,1),'s',flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--prepare',action='store_true');p.add_argument('--N',type=int,default=600000);p.add_argument('--seeds',nargs='+',type=int,default=SEEDS);p.add_argument('--freqs',nargs='+',type=int,default=[f for f in FREQS if f!=1000]);p.add_argument('--jobs',type=int,default=3);a=p.parse_args()
    if a.prepare:prepare()
    assert all(f in FREQS for f in a.freqs)
    tasks=[(c,s,f,a.N,seed) for f in a.freqs for c in MODEL_SOURCES for s in ('F1','F2') for seed in a.seeds]
    save(O/f"matriz-N{a.N}-{'_'.join(map(str,a.freqs))}.json",tasks)
    with ThreadPoolExecutor(max_workers=a.jobs) as pool:
        futures=[pool.submit(run,*t) for t in tasks]
        for f in futures:f.result()
