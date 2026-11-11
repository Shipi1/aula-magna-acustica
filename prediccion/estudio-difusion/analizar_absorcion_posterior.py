"""Etapa A: absorción total posterior, factibilidad y efectos por receptor."""
import analizar_d50_laterales as core
from preparar_localizado import B
import json,argparse
import numpy as np
import matplotlib.pyplot as plt
O=B/'absorcion-posterior';OUT=O/'resultados';OUT.mkdir(exist_ok=True)
core.O=O;core.OUT=OUT
ZONES={'P8_P9':['P8','P9'],'virtuales':[f'V{i:02}' for i in range(1,13)],'platea_baja':['P1','P2','P4','P7'],'bajo_balcon':['P3','P5','P6']}

def parameters(e,t0):
    m=core.params(e,t0)
    cumulative=np.cumsum(e[::-1])[::-1];curve=10*np.log10(np.maximum(cumulative/cumulative[0],1e-30));t=np.arange(len(e))*.001
    start=np.flatnonzero(e>0)[0]
    for name,hi,lo in [('EDT',0,-10),('T20',-5,-25),('T30',-5,-35)]:
        mask=(curve<=hi)&(curve>=lo)&(np.arange(len(e))>=start)
        if mask.sum()<6:
            m[name]=None;m[name+'_r2']=None;continue
        fit=np.polyfit(t[mask],curve[mask],1);residual=curve[mask]-np.polyval(fit,t[mask]);variance=np.sum((curve[mask]-curve[mask].mean())**2)
        m[name]=-60/float(fit[0]) if fit[0]<0 else None;m[name+'_r2']=float(1-np.sum(residual**2)/variance) if variance>0 else None
    return m

def main(partial=False):
    runs=core.load()
    runs=[r for r in runs if r['N']==600000 and r['frecuencia']==1000 and r['variante'] in ('base','total_a100')]
    if not partial:assert len(runs)==12,len(runs)
    by={};single=[];means={};cases=[];paired=[]
    for r in runs:
        for rec,e in r['curves'].items():
            m=parameters(e,r['t0'][rec]);by[(r['variante'],r['fuente'],r['semilla'],rec)]=m
            single.append({**{k:r[k] for k in ('variante','fuente','N','semilla','frecuencia')},'receptor':rec,**m})
    core.tocsv('indicadores-por-semilla.csv',single)
    for src in ('F1','F2'):
        selected={case:sorted([r for r in runs if r['variante']==case and r['fuente']==src],key=lambda r:r['semilla']) for case in ('base','total_a100')}
        if not all(len(r)==3 for r in selected.values()):
            assert partial;continue
        for rec in selected['base'][0]['curves']:
            t0=selected['base'][0]['t0'][rec]
            for case,rr in selected.items():
                e=np.mean([r['curves'][rec] for r in rr],axis=0);m=parameters(e,t0);means[(case,src,rec)]=(e,m)
                row=dict(variante=case,fuente=src,receptor=rec,frecuencia=1000,N_por_semilla=600000,semillas=3,**m)
                for k in ('D50_pct','C80'):
                    vv=[by[(case,src,r['semilla'],rec)][k] for r in rr];row['min_semilla_'+k]=min(vv);row['max_semilla_'+k]=max(vv)
                cases.append(row)
            base=means[('base',src,rec)][1];treated=means[('total_a100',src,rec)][1]
            d=dict(fuente=src,receptor=rec,base_D50_pct=base['D50_pct'],ideal_D50_pct=treated['D50_pct'],base_C80=base['C80'],ideal_C80=treated['C80'],delta_D50_pp=treated['D50_pct']-base['D50_pct'],delta_C80=treated['C80']-base['C80'])
            for k in ('E0_20','E0_50','E50_total','E0_80','E80_300','E300_1000','total'):
                d['delta_'+k+'_dB']=core.db(treated[k]/base[k]) if base[k]>0 and treated[k]>0 else None
            for k in ('EDT','T20','T30'):
                d['base_'+k]=base[k];d['ideal_'+k]=treated[k];d['delta_'+k]=treated[k]-base[k] if treated[k] is not None and base[k] is not None else None
                d['delta_'+k+'_pct']=100*(treated[k]/base[k]-1) if treated[k] is not None and base[k] is not None else None
                d['base_'+k+'_r2']=base[k+'_r2'];d['ideal_'+k+'_r2']=treated[k+'_r2']
            import xml.etree.ElementTree as ET
            # Configuration is retrieved independently of any inferred reflection.
            cfg=next((O/'calculos').glob(f'base-{src}-1000Hz-N600000-seed*/config.xml'));root=ET.parse(cfg).getroot();source=root.find('sources')[0]
            receiver=next(x for x in root.find('recepteursp') if x.get('name')==rec)
            s=np.array([float(source.get(k)) for k in ('x','y','z')]);p=np.array([float(receiver.get(k)) for k in ('x','y','z')]);image=s.copy();image[0]=80.5-s[0]
            bound=(np.linalg.norm(image-p)-np.linalg.norm(s-p))/342*1000
            safe=bool(bound>.31/342*1000+51) # includes capture radius and 1 ms bin guard
            d['retardo_minimo_plano_posterior_ms']=float(bound);d['temprano50_invariante_demostrado']=safe
            if safe:
                controlled=100*base['E0_50']/(base['E0_50']+treated['E50_total']);d['ideal_D50_control_temprano_pct']=controlled
                early=[by[('base',src,r['semilla'],rec)]['E0_50'] for r in selected['base']]
                late=[by[('total_a100',src,r['semilla'],rec)]['E50_total'] for r in selected['total_a100']]
                d['D50_combinacion_extremos_favorables_pct']=100*max(early)/(max(early)+min(late))
                values=[100*by[('base',src,r['semilla'],rec)]['E0_50']/(by[('base',src,r['semilla'],rec)]['E0_50']+by[('total_a100',src,r['semilla'],rec)]['E50_total']) for r in selected['total_a100']]
                d['min_semilla_D50_control']=min(values);d['max_semilla_D50_control']=max(values)
            else:
                for key in ('ideal_D50_control_temprano_pct','D50_combinacion_extremos_favorables_pct','min_semilla_D50_control','max_semilla_D50_control'):d[key]=None
            paired.append(d)
    if not paired:return
    core.tocsv('respuestas-medias.csv',cases);core.save('respuestas-medias.json',cases)
    core.tocsv('comparacion-ideal.csv',paired);core.save('comparacion-ideal.json',paired)
    summaries=[]
    def avg(v):
        v=[x for x in v if x is not None];return float(np.mean(v)) if v else None
    for zone,names in ZONES.items():
        rr=[r for r in paired if r['receptor'] in names]
        if not rr:continue
        summaries.append(dict(zona=zone,n=len(rr),D50_base=avg([r['base_D50_pct'] for r in rr]),D50_ideal=avg([r['ideal_D50_pct'] for r in rr]),C80_base=avg([r['base_C80'] for r in rr]),C80_ideal=avg([r['ideal_C80'] for r in rr]),**{k:avg([r[k] for r in rr]) for k in rr[0] if k.startswith('delta_')},pares_D50_al_menos55=int(sum(r['ideal_D50_pct']>=55 for r in rr)),pares_ambas_metas=int(sum(r['ideal_D50_pct']>=55 and -2<=r['ideal_C80']<=2 for r in rr)),max_abs_cambio_D50_pp=max(abs(r['delta_D50_pp']) for r in rr)))
    core.save('resumen-ideal.json',summaries)
    if partial:return
    assert len(cases)==84 and len(paired)==42
    fig,axs=plt.subplots(1,2,figsize=(13,6),sharey=True,constrained_layout=True)
    for ax,names,title in zip(axs,[['P8','P9'],[f'V{i:02}' for i in range(1,13)]],['P8/P9','Receptores virtuales altos']):
        for case,color,label in [('base','#444444','Base'),('total_a100','#a54b6a','Fondo ideal α = 1')]:
            values=[np.mean([r['D50_pct'] for r in cases if r['variante']==case and r['receptor']==n]) for n in names];ax.plot(range(len(names)),values,marker='o',color=color,label=label)
        ax.axhline(55,color='#339966',ls=':',label='Meta 55 %');ax.set_xticks(range(len(names)),names,rotation=45 if len(names)>2 else 0);ax.set(title=title,ylabel='D50 (%) · media descriptiva F1/F2');ax.grid(alpha=.15)
    axs[0].legend();fig.suptitle('Absorción ideal posterior · 1.000 Hz · 600.000 partículas × 3 semillas')
    fig.savefig(OUT/'D50-limite-ideal.png',dpi=160);plt.close(fig)
    fig,axs=plt.subplots(1,2,figsize=(13,5),constrained_layout=True)
    for ax,k,label in zip(axs,('delta_D50_pp','delta_C80'),('Cambio D50 (puntos porcentuales)','Cambio C80 (dB)')):
        ax.bar(range(len(summaries)),[r[k] for r in summaries],color='#a54b6a');ax.axhline(0,color='#444',lw=.8);ax.set_xticks(range(len(summaries)),['P8/P9','Virtuales altos','Platea baja','Bajo balcón']);ax.set_ylabel(label);ax.grid(axis='y',alpha=.15)
    fig.suptitle('Efecto medio del límite ideal por zona; no equivale a ausencia de efectos individuales');fig.savefig(OUT/'efectos-por-zona.png',dpi=160);plt.close(fig)
    for r in summaries:print('ZONA',r)
    for r in paired:
        if r['receptor'] in ('P8','P9'):print('ALTO',r)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--partial',action='store_true');a=p.parse_args();main(a.partial)
