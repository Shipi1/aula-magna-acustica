"""Resultados D50/C80 por fuente, banda, posición y resolución."""
from preparar_localizado import B
from analizar import win,metric,db
import json,csv,argparse,xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
O=B/'d50-laterales';OUT=O/'resultados';OUT.mkdir(exist_ok=True)
def save(name,d):(OUT/name).write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding='utf8')
def tocsv(name,rows):
    with (OUT/name).open('w',newline='',encoding='utf-8-sig') as fp:
        w=csv.DictWriter(fp,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
def params(e,t0):
    m=metric(e,t0);m['D50_pct']=100*win(e,0,t0+.05)/sum(e)
    m['E0_50']=win(e,0,t0+.05);m['E50_total']=win(e,t0+.05,4)
    for a,b in ((20,50),(50,80)):m[f'E{a}_{b}']=win(e,t0+a/1000,t0+b/1000)
    return m
def load():
    runs=[]
    for p in sorted((O/'calculos').glob('*/ejecucion.json')):
        d=json.loads(p.read_text())
        if d['N']<150000:continue
        root=ET.parse(p.parent/'config.xml').getroot();source=root.find('sources')[0];xyz=np.array([float(source.get(k)) for k in ('x','y','z')])
        result=json.loads((p.parent/'resultados-lineales.json').read_text())
        d['curves']={n:np.array(next(iter(cols.values())),float) for n,cols in result['receptores'].items()}
        assert len(d['curves'])==21
        assert all(len(e)==4000 and np.isfinite(e).all() and (e>=0).all() and sum(e)>0 for e in d['curves'].values())
        d['t0']={r.get('name'):float(np.linalg.norm(np.array([float(r.get(k)) for k in ('x','y','z')])-xyz)/342) for r in root.find('recepteursp')};runs.append(d)
    return runs
def differences(a,b):
    return {**{'delta_'+k: a[k]-b[k] for k in ('D50_pct','C80','T30','concentracion10ms')},**{'delta_'+k+'_dB':db(a[k]/b[k]) if a[k]>0 and b[k]>0 else None for k in ('E0_20','E0_50','E50_total','E0_80','E80_300','E300_1000','total')}}

def main(partial=False):
    runs=load();screen=[r for r in runs if r['N']==150000];assert len(screen)==16,len(screen)
    idx={(r['variante'],r['fuente'],r['frecuencia'],r['N'],r['semilla']):r for r in runs}
    rows=[];metrics={}
    for r in runs:
        for rec,e in r['curves'].items():
            key=(r['variante'],r['fuente'],r['frecuencia'],r['N'],r['semilla'],rec);m=params(e,r['t0'][rec]);metrics[key]=m
            rows.append({**{k:r[k] for k in ('variante','fuente','frecuencia','N','semilla')},'receptor':rec,**m})
    tocsv('indicadores.csv',rows)
    diff=[]
    for row in rows:
        if row['variante']=='base':continue
        ref=metrics[('base',row['fuente'],row['frecuencia'],row['N'],row['semilla'],row['receptor'])]
        diff.append({**{k:row[k] for k in ('variante','fuente','frecuencia','N','semilla','receptor')},**differences(row,ref)})
    tocsv('diferencias.csv',diff);save('diferencias.json',diff)
    zones={'P8_P9':['P8','P9'],'virtuales':[f'V{i:02}' for i in range(1,13)],'piso':['P1','P2','P4','P7'],'bajo':['P3','P5','P6']}
    summary=[]
    for variant in ('base','R','Lneg','Lpos'):
        for f in (500,1000):
            for zone,names in zones.items():
                selected=[r for r in rows if r['N']==150000 and r['variante']==variant and r['frecuencia']==f and r['receptor'] in names]
                dd=[r for r in diff if r['N']==150000 and r['variante']==variant and r['frecuencia']==f and r['receptor'] in names]
                summary.append(dict(variante=variant,frecuencia=f,zona=zone,n=len(selected),C80=float(np.mean([r['C80'] for r in selected])),D50_pct=float(np.mean([r['D50_pct'] for r in selected])),**{k:float(np.mean([r[k] for r in dd])) for k in dd[0] if k.startswith('delta_')} if dd else {}))
    save('resumen-exploracion.json',summary)
    base_rows=[]
    for source in ('F1','F2'):
        for f in (500,1000):
            rr=sorted([r for r in runs if r['N']==600000 and r['variante']=='base' and r['fuente']==source and r['frecuencia']==f],key=lambda r:r['semilla'])
            if partial and len(rr)!=3:continue
            assert len(rr)==3,(source,f,len(rr))
            for rec in rr[0]['curves']:
                avg=np.mean([r['curves'][rec] for r in rr],axis=0);m=params(avg,rr[0]['t0'][rec])
                singles=[metrics[('base',source,f,600000,r['semilla'],rec)] for r in rr]
                row=dict(fuente=source,frecuencia=f,receptor=rec,N_por_semilla=600000,semillas=3,**m)
                for k in ('D50_pct','C80','T30'):
                    row['min_semilla_'+k]=min(x[k] for x in singles);row['max_semilla_'+k]=max(x[k] for x in singles)
                base_rows.append(row)
    if base_rows:tocsv('referencia-tres-semillas.csv',base_rows);save('referencia-tres-semillas.json',base_rows)
    repeated=[]
    if not partial:
        for src in ('F1','F2'):
            chosen={variant:sorted([r for r in runs if r['N']==600000 and r['frecuencia']==1000 and r['fuente']==src and r['variante']==variant],key=lambda r:r['semilla']) for variant in ('base','R')}
            assert all(len(x)==3 for x in chosen.values()),('Falta repetición del fondo',src)
            for rec in chosen['base'][0]['curves']:
                m={variant:params(np.mean([r['curves'][rec] for r in selected],axis=0),selected[0]['t0'][rec]) for variant,selected in chosen.items()}
                dd=[differences(metrics[('R',src,1000,600000,r['semilla'],rec)],metrics[('base',src,1000,600000,r['semilla'],rec)]) for r in chosen['R']]
                row=dict(fuente=src,receptor=rec,frecuencia=1000,N_por_semilla=600000,semillas=3,base_D50_pct=m['base']['D50_pct'],R_D50_pct=m['R']['D50_pct'],base_C80=m['base']['C80'],R_C80=m['R']['C80'],**differences(m['R'],m['base']))
                # Secondary diagnostic only: geometry proves R cannot affect
                # pre-50 ms energy at P8/P9. Never replace the raw responses.
                if rec in ('P8','P9'):
                    invariant=100*m['base']['E0_50']/(m['base']['E0_50']+m['R']['E50_total'])
                    row['D50_R_control_temprano_invariante_pct']=invariant
                    row['delta_D50_control_invariante_pp']=invariant-m['base']['D50_pct']
                else:
                    row['D50_R_control_temprano_invariante_pct']=None;row['delta_D50_control_invariante_pp']=None
                for k in ('delta_D50_pct','delta_C80','delta_E0_50_dB','delta_E50_total_dB'):
                    row['min_semilla_'+k]=min(r[k] for r in dd);row['max_semilla_'+k]=max(r[k] for r in dd)
                repeated.append(row)
        tocsv('fondo-repetido-1000Hz.csv',repeated);save('fondo-repetido-1000Hz.json',repeated)
    # Each source and receiver stays separate; plot source-averaged descriptive
    # parameters with the target band shown only on D50 at 1 kHz.
    fig,axs=plt.subplots(1,2,figsize=(15,6),sharey=True,constrained_layout=True)
    names=['P8','P9']+[f'V{i:02}' for i in range(1,13)];styles={'base':('#444444','Base'),'R':('#8951b0','Fondo R'),'Lneg':('#278b99','Lateral Y−'),'Lpos':('#c17b25','Lateral Y+')}
    for ax,f in zip(axs,(500,1000)):
        for variant,(color,label) in styles.items():
            values=[np.mean([r['D50_pct'] for r in rows if r['N']==150000 and r['variante']==variant and r['frecuencia']==f and r['receptor']==rec]) for rec in names]
            ax.plot(values,np.arange(len(names)),marker='o',ms=4,color=color,label=label)
        if f==1000:ax.axvspan(55,60,color='#339966',alpha=.13,label='Meta de proyecto 55–60 %')
        ax.set_yticks(range(len(names)),names);ax.set(title=f'{f} Hz',xlabel='D50 (%) · media descriptiva de F1/F2');ax.grid(alpha=.15)
    axs[0].invert_yaxis()
    axs[0].legend(fontsize=8);fig.suptitle('Exploración de dispersión equivalente: 150.000 partículas, una semilla\nLos promedios no sustituyen la revisión individual')
    fig.savefig(OUT/'d50-por-posicion.png',dpi=160);plt.close(fig)
    if repeated:
        selected=[r for r in repeated if r['receptor'] in ('P8','P9')]
        fig,axs=plt.subplots(1,2,figsize=(12,5),constrained_layout=True)
        x=np.arange(len(selected))
        for variant,color in [('base','#444444'),('R','#8951b0')]:
            axs[0].plot(x,[r[variant+'_D50_pct'] for r in selected],marker='o',color=color,label='Base' if variant=='base' else 'Fondo R')
        axs[0].axhspan(55,60,color='#339966',alpha=.13,label='Meta de proyecto');axs[0].set_ylabel('D50 (%)');axs[0].legend(fontsize=8)
        axs[1].vlines(x,[r['min_semilla_delta_D50_pct'] for r in selected],[r['max_semilla_delta_D50_pct'] for r in selected],color='#999',lw=3,label='Rango entre semillas')
        axs[1].scatter(x,[r['delta_D50_pct'] for r in selected],color='#8951b0',s=40,label='Cambio sobre medias energéticas');axs[1].axhline(0,color='#444',lw=.8);axs[1].set_ylabel('Cambio de D50 (puntos porcentuales)');axs[1].legend(fontsize=8)
        for ax in axs:ax.set_xticks(x,[r['fuente']+'\n'+r['receptor'] for r in selected]);ax.grid(alpha=.15)
        fig.suptitle('Fondo alto R · 1.000 Hz · 600.000 partículas × 3 semillas\nRangos descriptivos, no intervalos de confianza')
        fig.savefig(OUT/'fondo-repetido-1000Hz.png',dpi=160);plt.close(fig)
    for r in summary:
        if r['zona']=='P8_P9':print(r)
    if not partial:
        print('REFERENCIA REPETIDA')
        for f in (500,1000):
            rr=[r for r in base_rows if r['frecuencia']==f and r['receptor'] in ('P8','P9')]
            print(f,'D50',np.mean([r['D50_pct'] for r in rr]),'C80',np.mean([r['C80'] for r in rr]))
    print('corridas',len(runs),'filas',len(rows),'diferencias',len(diff))
    if repeated:
        print('FONDO REPETIDO')
        for r in repeated:
            if r['receptor'] in ('P8','P9'):print(r)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--partial',action='store_true');a=p.parse_args();main(a.partial)
