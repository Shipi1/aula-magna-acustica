"""Indicadores por octava, curvas comparativas y verificación de entradas."""
from pathlib import Path
import json,csv,hashlib,argparse,xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
import analizar_estudio_mixto as core
import ejecutar_octavas_propuesta as setup
from analizar import win,db
B=setup.B;O=setup.O;OUT=O/'resultados';OUT.mkdir(exist_ok=True)
FREQS=setup.FREQS;CASES=['sin_tratamiento','propuesta'];NAMES={'sin_tratamiento':'Sin tratamiento','propuesta':'Propuesta mixta'}
SEEDS=setup.SEEDS;TARGET=core.TARGET
GROUPS={'frente':[(s,p) for s in ('F1','F2') for p in core.OBJ['frente_butacas']], 'media':[(s,p) for s in ('F1','F2') for p in core.OBJ['media_butacas']],
 'frente_media':core.PAIRS,'prioritarios':[tuple(x) for x in core.OBJ['pares_campo_prioritarios']],
 'P8_P9':[(s,p) for s in ('F1','F2') for p in ('P8','P9')], 'platea_baja':[(s,p) for s in ('F1','F2') for p in ('P1','P2','P4','P7')],
 'bajo_balcon':[(s,p) for s in ('F1','F2') for p in ('P3','P5','P6')], 'posteriores':[(s,p) for s in ('F1','F2') for p in core.OBJ['posterior_butacas_control']]}
def save(name,x):(OUT/name).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
def csvsave(name,rows):
    with (OUT/name).open('w',newline='',encoding='utf-8-sig') as fp:w=csv.DictWriter(fp,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def average(values):
    vv=[float(x) for x in values if x is not None and np.isfinite(x)];return float(np.mean(vv)) if vv else None
def read(folder,case,reused=False):
    d=json.loads((folder/'ejecucion.json').read_text());r=ET.parse(folder/'config.xml').getroot();src=r.find('sources')[0];xyz=np.array([float(src.get(k)) for k in ('x','y','z')])
    coords={p.get('name'):np.array([float(p.get(k)) for k in ('x','y','z')]) for p in r.find('recepteursp')};values=json.loads((folder/'resultados-lineales.json').read_text())
    curves={p:np.array(next(iter(cols.values())),float) for p,cols in values['receptores'].items()}
    assert len(curves)==21 and set(curves)==set(coords) and all(len(e)==4000 and np.isfinite(e).all() and (e>=0).all() and e.sum()>0 for e in curves.values())
    assert [int(f.get('freq')) for f in r.find('simulation/freq_enum') if f.get('docalc')=='1']==[d['frecuencia']]
    d.update(estado=case,folder=folder,cfg=r,curves=curves,t0={p:float(np.linalg.norm(q-xyz)/342) for p,q in coords.items()},reutilizada=reused);return d
def load(partial=False):
    runs=[]
    for p in sorted((O/'calculos').glob('*/ejecucion.json')):
        d=json.loads(p.read_text())
        if d['N']==600000 and not d.get('pendiente',False):runs.append(read(p.parent,d['variante']))
    for m in json.loads((O/'reutilizadas-1000Hz.json').read_text()):runs.append(read(Path(m['carpeta']),m['estado'],True))
    if not partial:assert len(runs)==96,len(runs)
    return runs
def parameters(e,t0):
    total=float(e.sum());early80=win(e,0,t0+.08);late80=win(e,t0+.08,4)
    m={'total':total,'E0_20':win(e,0,t0+.02),'E20_50':win(e,t0+.02,t0+.05),'E0_50':win(e,0,t0+.05),'E50_80':win(e,t0+.05,t0+.08),
       'E0_80':early80,'E80_total':total-early80,'E50_total':win(e,t0+.05,4),'E80_300':win(e,t0+.08,t0+.3),'E300_1000':win(e,t0+.3,t0+1),'C80':db(early80/late80),'fraccion_tardia':late80/total}
    m['D50_pct']=100*m['E0_50']/sum(e)
    cumulative=np.cumsum(e[::-1])[::-1];curve=10*np.log10(np.maximum(cumulative/cumulative[0],1e-30));t=np.arange(len(e))*.001;start=np.flatnonzero(e>0)[0]
    for name,hi,lo in [('EDT',0,-10),('T20',-5,-25),('T30',-5,-35)]:
        fitmask=(curve<=hi)&(curve>=lo)&(np.arange(len(e))>=start)
        if fitmask.sum()<6:m[name]=None;m[name+'_r2']=None;continue
        fit=np.polyfit(t[fitmask],curve[fitmask],1);residual=curve[fitmask]-np.polyval(fit,t[fitmask]);variance=np.sum((curve[fitmask]-curve[fitmask].mean())**2)
        m[name]=-60/float(fit[0]) if fit[0]<0 else None;m[name+'_r2']=float(1-np.sum(residual**2)/variance) if variance>0 else None
    mask=(curve<=-5)&(curve>=-35)
    m['T30_fin_ajuste_s']=float(np.flatnonzero(mask)[-1]*.001) if mask.any() else None
    m['energia_ultimos100ms_fraccion']=float(e[-100:].sum()/e.sum())
    m['T30_revision']=bool(m['T30'] is None or m['T30_r2'] is None or m['T30_r2']<.95 or (m['T30_fin_ajuste_s'] or 0)>3.8)
    return m
def main(partial=False):
    global FREQS
    runs=load(partial)
    if partial:
        FREQS=[hz for hz in FREQS if sum(r['frecuencia']==hz for r in runs)==12];runs=[r for r in runs if r['frecuencia'] in FREQS]
    assert FREQS
    means=[];singles=[];by={};singleby={};curves={}
    for hz in FREQS:
        for case in CASES:
            for src in ('F1','F2'):
                rr=sorted([r for r in runs if r['frecuencia']==hz and r['estado']==case and r['fuente']==src],key=lambda r:r['semilla']);assert [r['semilla'] for r in rr]==SEEDS
                for p in rr[0]['curves']:
                    mm=[]
                    for r in rr:
                        m=parameters(r['curves'][p],r['t0'][p]);mm.append(m);singleby[case,hz,src,p,r['semilla']]=m;singles.append(dict(estado=case,frecuencia=hz,fuente=src,receptor=p,semilla=r['semilla'],**m))
                    e=np.mean([r['curves'][p] for r in rr],axis=0);m=parameters(e,rr[0]['t0'][p]);by[case,hz,src,p]=m;curves[case,hz,src,p]=e
                    bounds={tag+'_'+k:(float(fun(x[k] for x in mm)) if all(x[k] is not None for x in mm) else None) for tag,fun in [('min',min),('max',max)] for k in ('D50_pct','C80','EDT','T30')}
                    means.append(dict(estado=case,frecuencia=hz,fuente=src,receptor=p,**m,**bounds))
    diffs=[]
    for hz in FREQS:
        for src in ('F1','F2'):
            for p in rr[0]['curves']:
                a=by['sin_tratamiento',hz,src,p];b=by['propuesta',hz,src,p]
                ds=[singleby['propuesta',hz,src,p,seed]['D50_pct']-singleby['sin_tratamiento',hz,src,p,seed]['D50_pct'] for seed in SEEDS]
                diffs.append(dict(frecuencia=hz,fuente=src,receptor=p,**{'delta_'+k:(b[k]-a[k] if a[k] is not None and b[k] is not None else None) for k in ('D50_pct','C80','EDT','T30')},
                    **{'delta_'+k+'_dB':core.shared.calc.core.db(b[k]/a[k]) for k in ('E0_50','E50_80','E80_total','total')},min_delta_semilla_D50=float(min(ds)),max_delta_semilla_D50=float(max(ds)),D50_aumenta_tres_semillas=all(x>0 for x in ds)))
    summary=[]
    for hz in FREQS:
        for case in CASES:
            for group,pairs in GROUPS.items():
                rows=[r for r in means if r['estado']==case and r['frecuencia']==hz and (r['fuente'],r['receptor']) in pairs]
                sm={k:average(r[k] for r in rows) for k in ('D50_pct','C80','EDT','T30')}
                bounds={}
                for k in sm:
                    seedmean=[average(singleby[case,hz,s,p,seed][k] for s,p in pairs) for seed in SEEDS];valid=[v for v in seedmean if v is not None]
                    bounds['min_media_semilla_'+k]=min(valid) if valid else None;bounds['max_media_semilla_'+k]=max(valid) if valid else None
                summary.append(dict(estado=case,frecuencia=hz,grupo=group,n=len(rows),**sm,**bounds,T30_revisar=sum(r['T30_revision'] for r in rows)))
    assert len(means)==84*len(FREQS) and len(singles)==252*len(FREQS) and len(diffs)==42*len(FREQS)
    for name,rows in [('medias',means),('semillas',singles),('diferencias',diffs),('resumen-zonas',summary)]:save(name+'.json',rows);csvsave(name+'.csv',rows)
    audits=[]
    for r in runs:
        base=next(x for x in runs if x['estado']=='sin_tratamiento' and x['frecuencia']==r['frecuencia'] and x['fuente']==r['fuente'] and x['semilla']==r['semilla']);cfg=r['cfg'];ref=base['cfg']
        assert ET.tostring(cfg.find('sources'))==ET.tostring(ref.find('sources')) and ET.tostring(cfg.find('recepteursp'))==ET.tostring(ref.find('recepteursp'))
        for k,v in cfg.find('simulation').attrib.items():
            if k not in ('modelName','tetrameshFileName'):assert v==ref.find('simulation').get(k),(r['folder'],k)
        for mat in cfg.find('surface_absorption_enum'):
            original=next(m for m in ref.find('surface_absorption_enum') if m.get('id')==mat.get('id'));assert mat.attrib==original.attrib
            for band,orig in zip(mat,original):
                if r['estado']=='propuesta' and mat.get('id') in ('201','301'):
                    if int(band.get('freq'))==r['frecuencia']:
                        assert float(band.get('absorb'))==(setup.ABS[r['frecuencia']] if mat.get('id')=='201' else .05)
                        if mat.get('id')=='301':assert float(band.get('diffusion'))==.05
                        else:assert band.get('diffusion')==orig.get('diffusion') and band.get('loi')==orig.get('loi')
                    continue
                assert band.attrib==orig.attrib
        for key,path in [('config',r['folder']/'config.xml'),('malla',O/'modelos'/r['estado']/'mesh.cbin'),('tetra',O/'modelos'/r['estado']/'tetramesh.mbin')]:assert hashlib.sha256(path.read_bytes()).hexdigest()==r[key+'_sha256']
        assert len(cfg.find('sources'))==1
        source=cfg.find('sources')[0];lw=float(10*np.log10(sum(10**(float(b.get('db'))/10) for b in source.findall('bfreq'))));assert abs(lw-90)<.001
        band_lw=float(next(b for b in source.findall('bfreq') if int(b.get('freq'))==r['frecuencia']).get('db'))
        audits.append(dict(estado=r['estado'],frecuencia=r['frecuencia'],fuente=r['fuente'],semilla=r['semilla'],carpeta=str(r['folder']),reutilizada=r['reutilizada'],perdidas=r['fraccion_perdidas'],Lw_global_dB=lw,Lw_frecuencia_activa_dB=band_lw))
    old=json.loads((B/'comparacion-sala-propuesta/medias.json').read_text());errors=[]
    for r in means:
        if r['frecuencia']!=1000:continue
        ref=next(x for x in old if all(x[k]==r[k] for k in ('estado','fuente','receptor')))
        for k in ('D50_pct','C80','EDT','T30'):assert abs(r[k]-ref[k])<1e-10;errors.append(abs(r[k]-ref[k]))
    save('verificacion.json',dict(parcial=partial,nuevas=sum(not r['reutilizada'] for r in runs),reutilizadas=sum(r['reutilizada'] for r in runs),pilotos_excluidos=28,N=600000,semillas=SEEDS,frecuencias_Hz=FREQS,respuestas_medias=len(means),respuestas_individuales=len(singles),max_error_reproduccion_1000Hz=max(errors),max_fraccion_perdidas=max(r['fraccion_perdidas'] for r in runs),T30_revisar=sum(r['T30_revision'] for r in means),corridas=audits))
    csvsave('corridas-verificadas.csv',audits)
    labels={'frente':'Frente de platea alta','media':'Zona media de platea alta','prioritarios':'P8/P9 prioritarios','platea_baja':'Platea baja abierta','bajo_balcon':'Bajo balcón','posteriores':'Posteriores · control'}
    x=np.arange(len(FREQS))
    for metric,title,unit in [('D50_pct','D50','%'),('C80','C80','dB'),('T30','T30','s'),('EDT','EDT','s')]:
        fig,axes=plt.subplots(2,3,figsize=(15,8),constrained_layout=True)
        for ax,(g,label) in zip(axes.flat,labels.items()):
            for case,color in [('sin_tratamiento','#617b90'),('propuesta','#23877d')]:
                rows=[next(r for r in summary if r['estado']==case and r['frecuencia']==hz and r['grupo']==g) for hz in FREQS]
                y=[r[metric] for r in rows];lo=[r['min_media_semilla_'+metric] for r in rows];hi=[r['max_media_semilla_'+metric] for r in rows]
                ax.plot(x,y,'o-',c=color,label=NAMES[case],ms=4);ax.fill_between(x,lo,hi,color=color,alpha=.12)
            ax.set(xticks=x,xticklabels=[str(f) for f in FREQS],xlabel='Banda de octava (Hz)',ylabel=title+' ('+unit+')',title=label);ax.grid(alpha=.18);ax.legend(fontsize=8)
        fig.suptitle(title+' por bandas · medias espaciales\nSombreado: mínimo/máximo de las tres medias por semilla; no intervalo de confianza')
        fig.savefig(OUT/(title+'-por-zona.png'),dpi=180);plt.close(fig)
    pairs=core.PAIRS
    for metric,title,unit in [('delta_D50_pct','Cambio de D50','puntos porcentuales'),('delta_C80','Cambio de C80','dB')]:
        matrix=np.array([[next(r[metric] for r in diffs if r['frecuencia']==hz and (r['fuente'],r['receptor'])==pair) for hz in FREQS] for pair in pairs]);fig,ax=plt.subplots(figsize=(12,7),constrained_layout=True)
        im=ax.imshow(abs(matrix),cmap='Purples',vmin=0,vmax=max(abs(matrix).max(),.1),aspect='auto')
        for i in range(len(pairs)):
            for j in range(len(FREQS)):ax.text(j,i,f'{matrix[i,j]:+.1f}',ha='center',va='center',fontsize=9,color='white' if abs(matrix[i,j])>abs(matrix).max()*.6 else '#222')
        ax.set(xticks=x,xticklabels=FREQS,yticks=np.arange(len(pairs)),yticklabels=[s+'–'+p for s,p in pairs],xlabel='Banda de octava (Hz)',title=title+' · propuesta menos sala sin tratamiento\nColor: magnitud absoluta · número: diferencia con signo')
        fig.colorbar(im,ax=ax,label='Magnitud ('+unit+')');fig.savefig(OUT/(metric+'.png'),dpi=180);plt.close(fig)
    fig,axes=plt.subplots(2,3,figsize=(15,8),constrained_layout=True)
    for col,(src,p) in enumerate([('F1','P8'),('F1','P9'),('F2','P8')]):
        for row,(metric,unit) in enumerate([('D50_pct','%'),('C80','dB')]):
            ax=axes[row,col]
            for case,color in [('sin_tratamiento','#617b90'),('propuesta','#23877d')]:
                rows=[next(r for r in means if r['estado']==case and r['frecuencia']==hz and r['fuente']==src and r['receptor']==p) for hz in FREQS]
                ax.plot(x,[r[metric] for r in rows],'o-',color=color,label=NAMES[case]);ax.fill_between(x,[r['min_'+metric] for r in rows],[r['max_'+metric] for r in rows],color=color,alpha=.12)
            ax.set(xticks=x,xticklabels=FREQS,xlabel='Banda de octava (Hz)',ylabel=metric.replace('_pct','')+' ('+unit+')',title=src+'–'+p);ax.grid(alpha=.18);ax.legend(fontsize=8)
    fig.suptitle('Pares prioritarios · líneas: indicadores de respuesta media · sombra: rango entre semillas');fig.savefig(OUT/'P8-P9-por-octava.png',dpi=180);plt.close(fig)
    fig,axes=plt.subplots(2,2,figsize=(13,8),constrained_layout=True)
    for ax,(src,p) in zip(axes.flat,[('F1','P8'),('F1','P9'),('F2','V04'),('F2','V08')]):
        for k,label,color in [('delta_E0_50_dB','0–50 ms','#398b76'),('delta_E50_80_dB','50–80 ms','#d1a24b'),('delta_E80_total_dB','>80 ms','#7d8e9b')]:
            ax.plot(x,[next(r[k] for r in diffs if r['frecuencia']==hz and r['fuente']==src and r['receptor']==p) for hz in FREQS],'o-',label=label,color=color)
        ax.axhline(0,c='#777',lw=.7);ax.set(xticks=x,xticklabels=FREQS,xlabel='Banda de octava (Hz)',ylabel='Cambio de energía (dB)',title=src+'–'+p);ax.grid(alpha=.18);ax.legend(fontsize=8)
    fig.suptitle('Energía por ventanas · propuesta / sala sin tratamiento');fig.savefig(OUT/'energias-por-octava.png',dpi=180);plt.close(fig)
    for hz in FREQS:
        rows=[r for r in summary if r['frecuencia']==hz and r['grupo']=='frente_media'];print(hz,[(r['estado'],round(r['D50_pct'],2),round(r['C80'],2),round(r['T30'],3) if r['T30'] is not None else None) for r in rows])
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--parcial',action='store_true');args=p.parse_args()
    if args.parcial:OUT=O/'resultados-parciales';OUT.mkdir(exist_ok=True)
    main(args.parcial)
