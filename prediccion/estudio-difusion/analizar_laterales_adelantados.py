"""D50/C80 y redistribución por zonas, con repeticiones de todos los candidatos."""
import analizar_d50_laterales as core
from preparar_localizado import B
import argparse,json
import numpy as np
import matplotlib.pyplot as plt
core.O=B/'laterales-adelantados';core.OUT=core.O/'resultados';core.OUT.mkdir(exist_ok=True)
variants=('base','Lneg','Lpos','Laterales')
zones={'P8_P9':['P8','P9'],'virtuales':[f'V{i:02}' for i in range(1,13)],'platea_baja':['P1','P2','P4','P7'],'bajo_balcon':['P3','P5','P6']}
colors={'base':'#444444','Lneg':'#278b99','Lpos':'#c17b25','Laterales':'#8951b0'}

def mean_valid(values):
    values=[x for x in values if x is not None]
    return float(np.mean(values)) if values else None

def parameters(e,t0):
    m=core.params(e,t0)
    m['E0_1']=core.win(e,0,t0+.001)
    m['E1_50']=core.win(e,t0+.001,t0+.05)
    m['E1_80']=core.win(e,t0+.001,t0+.08)
    m['E1_total']=core.win(e,t0+.001,4)
    return m

def differences(a,b):
    d=core.differences(a,b)
    for k in ('E0_1','E1_50'):
        d['delta_'+k+'_dB']=core.db(a[k]/b[k]) if a[k]>0 and b[k]>0 else None
    return d

def main(partial=False):
    runs=core.load();screen=[r for r in runs if r['N']==150000];assert len(screen)==16,len(screen)
    index={};rows=[]
    for r in runs:
        for rec,e in r['curves'].items():
            m=parameters(e,r['t0'][rec]);key=(r['variante'],r['fuente'],r['frecuencia'],r['N'],r['semilla'],rec);index[key]=m
            rows.append({**{k:r[k] for k in ('variante','fuente','frecuencia','N','semilla')},'receptor':rec,**m})
    core.tocsv('indicadores.csv',rows)
    paired=[]
    for r in rows:
        if r['variante']=='base':continue
        key=('base',r['fuente'],r['frecuencia'],r['N'],r['semilla'],r['receptor'])
        if key not in index:
            assert partial;continue
        paired.append({**{k:r[k] for k in ('variante','fuente','frecuencia','N','semilla','receptor')},**differences(r,index[key])})
    core.tocsv('diferencias.csv',paired)
    screen_summary=[]
    for variant in variants:
        for f in (500,1000):
            for zone,names in zones.items():
                sel=[r for r in rows if r['N']==150000 and r['variante']==variant and r['frecuencia']==f and r['receptor'] in names]
                diff=[r for r in paired if r['N']==150000 and r['variante']==variant and r['frecuencia']==f and r['receptor'] in names]
                result=dict(variante=variant,frecuencia=f,zona=zone,n=len(sel),D50_pct=float(np.mean([r['D50_pct'] for r in sel])),C80=float(np.mean([r['C80'] for r in sel])))
                if diff:result.update({k:mean_valid([r[k] for r in diff]) for k in diff[0] if k.startswith('delta_')})
                screen_summary.append(result)
    core.save('resumen-exploracion.json',screen_summary)
    references=[];repeated=[];means={}
    for src in ('F1','F2'):
        for freq in (500,1000):
            sel=sorted([r for r in runs if r['variante']=='base' and r['N']==600000 and r['frecuencia']==freq and r['fuente']==src],key=lambda r:r['semilla'])
            if len(sel)!=3:
                assert partial,(src,freq,len(sel));continue
            for rec in sel[0]['curves']:
                m=parameters(np.mean([r['curves'][rec] for r in sel],axis=0),sel[0]['t0'][rec]);means[('base',src,freq,rec)]=m
                single=[index[('base',src,freq,600000,r['semilla'],rec)] for r in sel]
                row=dict(fuente=src,frecuencia=freq,receptor=rec,**m)
                for k in ('D50_pct','C80','T30'):
                    row['min_semilla_'+k]=min(r[k] for r in single);row['max_semilla_'+k]=max(r[k] for r in single)
                references.append(row)
        for variant in variants[1:]:
            sel=sorted([r for r in runs if r['N']==600000 and r['frecuencia']==1000 and r['fuente']==src and r['variante']==variant],key=lambda r:r['semilla'])
            if len(sel)!=3:
                assert partial,(variant,src,len(sel));continue
            for rec in sel[0]['curves']:
                key=('base',src,1000,rec)
                if key not in means:
                    assert partial;continue
                base=means[key];m=parameters(np.mean([r['curves'][rec] for r in sel],axis=0),sel[0]['t0'][rec]);means[(variant,src,1000,rec)]=m
                row=dict(variante=variant,fuente=src,frecuencia=1000,receptor=rec,base_D50_pct=base['D50_pct'],tratado_D50_pct=m['D50_pct'],base_C80=base['C80'],tratado_C80=m['C80'],**differences(m,base))
                # Secondary control: no treated lateral path can arrive before
                # the fixed 1 ms cutoff, including finite receiver radius.
                row['D50_control_primero1ms_pct']=100*(base['E0_1']+m['E1_50'])/(base['E0_1']+m['E1_total'])
                row['delta_D50_control_primero1ms_pp']=row['D50_control_primero1ms_pct']-base['D50_pct']
                row['C80_control_primero1ms']=core.db((base['E0_1']+m['E1_80'])/(m['total']-m['E0_80']))
                row['delta_C80_control_primero1ms']=row['C80_control_primero1ms']-base['C80']
                per_seed=[differences(index[(variant,src,1000,600000,r['semilla'],rec)],index[('base',src,1000,600000,r['semilla'],rec)]) for r in sel]
                for k in ('delta_D50_pct','delta_C80','delta_E0_50_dB','delta_E50_total_dB'):
                    row['min_semilla_'+k]=min(d[k] for d in per_seed);row['max_semilla_'+k]=max(d[k] for d in per_seed)
                repeated.append(row)
    if references:core.tocsv('referencia-tres-semillas.csv',references);core.save('referencia-tres-semillas.json',references)
    if repeated:core.tocsv('comparacion-tres-semillas.csv',repeated);core.save('comparacion-tres-semillas.json',repeated)
    summary=[]
    for variant in variants[1:]:
        for zone,names in zones.items():
            sel=[r for r in repeated if r['variante']==variant and r['receptor'] in names]
            if not sel:continue
            summary.append(dict(variante=variant,zona=zone,n=len(sel),D50_base=float(np.mean([r['base_D50_pct'] for r in sel])),D50_tratado=float(np.mean([r['tratado_D50_pct'] for r in sel])),C80_base=float(np.mean([r['base_C80'] for r in sel])),C80_tratado=float(np.mean([r['tratado_C80'] for r in sel])),**{k:mean_valid([r[k] for r in sel]) for k in sel[0] if k.startswith('delta_')},max_abs_cambio_D50_pp=max(abs(r['delta_D50_pct']) for r in sel),pares_D50_55_60=int(sum(55<=r['tratado_D50_pct']<=60 for r in sel)),pares_C80_menos2_mas2=int(sum(-2<=r['tratado_C80']<=2 for r in sel)),pares_ambas_metas=int(sum(55<=r['tratado_D50_pct']<=60 and -2<=r['tratado_C80']<=2 for r in sel))))
    core.save('resumen-repeticiones.json',summary)
    names=['P8','P9']+[f'V{i:02}' for i in range(1,13)]
    fig,axs=plt.subplots(1,2,figsize=(14,6),sharey=True,constrained_layout=True)
    for ax,f in zip(axs,(500,1000)):
        for variant in variants:
            values=[np.mean([r['D50_pct'] for r in rows if r['N']==150000 and r['variante']==variant and r['frecuencia']==f and r['receptor']==rec]) for rec in names]
            ax.plot(values,np.arange(len(names)),marker='o',ms=4,color=colors[variant],label=variant)
        if f==1000:ax.axvspan(55,60,color='#339966',alpha=.13,label='Meta de proyecto')
        ax.set_yticks(range(len(names)),names);ax.set(title=f'{f} Hz',xlabel='D50 (%) · media descriptiva F1/F2');ax.grid(alpha=.15)
    axs[0].invert_yaxis();axs[0].legend(fontsize=8);fig.suptitle('Exploración de laterales adelantados · 150.000 partículas, una semilla')
    fig.savefig(core.OUT/'exploracion-D50.png',dpi=160);plt.close(fig)
    if not partial:
        assert len(runs)==46 and len(repeated)==126 and len(references)==84
        fig,axs=plt.subplots(1,3,figsize=(16,5),sharey=True,constrained_layout=True)
        for ax,variant in zip(axs,variants[1:]):
            sel=[r for r in repeated if r['variante']==variant and r['receptor'] in ('P8','P9')];x=np.arange(len(sel))
            ax.vlines(x,[r['min_semilla_delta_D50_pct'] for r in sel],[r['max_semilla_delta_D50_pct'] for r in sel],color='#999',lw=3)
            ax.scatter(x,[r['delta_D50_pct'] for r in sel],color=colors[variant],s=40);ax.axhline(0,color='#444',lw=.8)
            ax.set_xticks(x,[r['fuente']+'\n'+r['receptor'] for r in sel]);ax.set(title=variant,ylabel='Cambio D50 (puntos porcentuales)');ax.grid(alpha=.15)
        fig.suptitle('1.000 Hz · 600.000 partículas × 3 semillas\nPuntos: cambios sobre medias energéticas. Rangos descriptivos, no intervalos de confianza.')
        fig.savefig(core.OUT/'repeticiones-P8-P9.png',dpi=160);plt.close(fig)
        fig,axs=plt.subplots(1,2,figsize=(13,5),constrained_layout=True)
        for ax,key,title in zip(axs,('delta_D50_pct','delta_C80'),('D50 (puntos porcentuales)','C80 (dB)')):
            for variant in variants[1:]:
                values=[next(r[key] for r in summary if r['variante']==variant and r['zona']==zone) for zone in zones]
                ax.plot(range(4),values,marker='o',color=colors[variant],label=variant)
            ax.set_xticks(range(4),['P8/P9','Virtuales altos','Platea baja','Bajo balcón']);ax.axhline(0,color='#444',lw=.8);ax.set_ylabel(title);ax.grid(alpha=.15)
        axs[0].legend();fig.suptitle('Cambios medios por zona a 1.000 Hz; revisar también cada posición')
        fig.savefig(core.OUT/'cambios-por-zona.png',dpi=160);plt.close(fig)
    print('Corridas',len(runs),'filas',len(rows),'pares',len(paired))
    for r in screen_summary:
        if r['zona']=='P8_P9':print('EXPLORACION',r)
    for r in summary:print('REPETICION',r)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--partial',action='store_true');a=p.parse_args();main(a.partial)
