"""Comparación directa de energías existentes: sala base frente a propuesta mixta."""
from pathlib import Path
import json,csv,hashlib,xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import analizar_estudio_mixto as shared
B=shared.B;O=B/'comparacion-sala-propuesta';O.mkdir(exist_ok=True)
SPECS={'sin_tratamiento':(B/'reflectores','base'),'propuesta':(shared.O,'media_centro_a060')}
NAMES={'sin_tratamiento':'Sala sin tratamiento propuesto','propuesta':'Cuatro reflectores + absorción central de 9,6 m²'}
TARGET=shared.TARGET
def save(name,x):(O/name).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
def csvsave(name,rows):
    with (O/name).open('w',newline='',encoding='utf-8-sig') as fp:w=csv.DictWriter(fp,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def main():
    runs={c:shared.shared.load(root,[case]) for c,(root,case) in SPECS.items()};means=[];singles=[];curves={};by={};singleby={}
    for c,rr in runs.items():
        assert len(rr)==6
        for s in ('F1','F2'):
            items=sorted([r for r in rr if r['fuente']==s],key=lambda r:r['semilla']);assert [r['semilla'] for r in items]==[20261019,20261020,20261021];positions=items[0]['coords']
            for p in positions:
                mm=[]
                for r in items:
                    m=shared.params(r['curves'][p],r['t0'][p]);mm.append(m);singleby[c,s,p,r['semilla']]=m;singles.append(dict(estado=c,fuente=s,receptor=p,semilla=r['semilla'],**m))
                e=np.mean([r['curves'][p] for r in items],axis=0);m=shared.params(e,items[0]['t0'][p]);by[c,s,p]=m;curves[c,s,p]=(e,items[0]['t0'][p])
                means.append(dict(estado=c,fuente=s,receptor=p,**m,cumple=shared.good(m),cumple_tres_semillas=all(shared.good(x) for x in mm),
                    **{tag+'_'+k:float(fun(x[k] for x in mm)) for tag,fun in [('min',min),('max',max)] for k in ('D50_pct','C80','T30','EDT')}))
    diffs=[]
    for s in ('F1','F2'):
        for p in positions:
            a=by['sin_tratamiento',s,p];b=by['propuesta',s,p];ds=[singleby['propuesta',s,p,seed]['D50_pct']-singleby['sin_tratamiento',s,p,seed]['D50_pct'] for seed in (20261019,20261020,20261021)]
            diffs.append(dict(fuente=s,receptor=p,**{'delta_'+k:b[k]-a[k] for k in ('D50_pct','C80','T30','EDT')},delta_T30_pct=100*(b['T30']/a['T30']-1),
                **{'delta_'+k+'_dB':shared.shared.calc.core.db(b[k]/a[k]) for k in ('E0_50','E50_80','E80_total','total')},min_delta_semilla_D50=float(min(ds)),max_delta_semilla_D50=float(max(ds)),D50_aumenta_tres_semillas=all(x>0 for x in ds)))
    groups={'frente':[(s,p) for s in ('F1','F2') for p in shared.OBJ['frente_butacas']], 'media':[(s,p) for s in ('F1','F2') for p in shared.OBJ['media_butacas']],
        'frente_media':shared.PAIRS,'prioritarios':[tuple(x) for x in shared.OBJ['pares_campo_prioritarios']],
        'platea_baja':[(s,p) for s in ('F1','F2') for p in ['P1','P2','P4','P7']], 'bajo_balcon':[(s,p) for s in ('F1','F2') for p in ['P3','P5','P6']],
        'posteriores_control':[(s,p) for s in ('F1','F2') for p in shared.OBJ['posterior_butacas_control']]}
    summary=[]
    for c in SPECS:
        for g,pairs in groups.items():
            rr=[r for r in means if r['estado']==c and (r['fuente'],r['receptor']) in pairs];dd=[r for r in diffs if (r['fuente'],r['receptor']) in pairs]
            summary.append(dict(estado=c,grupo=g,n=len(rr),cumplen=sum(r['cumple'] for r in rr),cumplen_tres_semillas=sum(r['cumple_tres_semillas'] for r in rr),
                **{k+'_medio':float(np.mean([r[k] for r in rr])) for k in ('D50_pct','C80','T30','EDT')},
                **{k+'_medio':float(np.mean([r[k] for r in dd])) for k in ('delta_D50_pct','delta_C80','delta_T30','delta_EDT','delta_total_dB')},
                distancia_media_banda=float(np.mean([max(45-r['D50_pct'],0,r['D50_pct']-55) for r in rr]))))
    for name,rows in [('medias',means),('semillas',singles),('diferencias',diffs),('resumen-zonas',summary)]:save(name+'.json',rows);csvsave(name+'.csv',rows)
    assert len(means)==84 and len(singles)==252
    checks=[]
    for c,rr in runs.items():
        for r in rr:
            ref=next(x for x in runs['sin_tratamiento'] if x['fuente']==r['fuente'] and x['semilla']==r['semilla']);cfg=r['cfg'];base=ref['cfg']
            assert ET.tostring(cfg.find('sources'))==ET.tostring(base.find('sources')) and ET.tostring(cfg.find('recepteursp'))==ET.tostring(base.find('recepteursp'))
            for k,v in cfg.find('simulation').attrib.items():
                if k not in ('modelName','tetrameshFileName'):assert v==base.find('simulation').get(k)
            for m in cfg.find('surface_absorption_enum'):
                original=next(x for x in base.find('surface_absorption_enum') if x.get('id')==m.get('id'));assert original.attrib==m.attrib
                for band,orig in zip(m,original):
                    expected=dict(orig.attrib)
                    if c=='propuesta' and m.get('id')=='201' and band.get('freq')=='1000':expected['absorb']='0.6'
                    assert band.attrib==expected
            for key,path in [('config',r['folder']/'config.xml'),('malla',r['root']/r['variante']/'mesh.cbin'),('tetra',r['root']/r['variante']/'tetramesh.mbin')]:assert hashlib.sha256(path.read_bytes()).hexdigest()==r[key+'_sha256']
            checks.append(dict(estado=c,carpeta=str(r['folder'].relative_to(B)),N=r['N'],semilla=r['semilla'],fraccion_perdidas=r['fraccion_perdidas'],config_sha256=r['config_sha256'],malla_sha256=r['malla_sha256'],tetra_sha256=r['tetra_sha256']))
    save('verificacion.json',dict(corridas_reutilizadas=12,nuevas_simulaciones=0,receptores=21,frecuencia_Hz=1000,condiciones_iguales_salvo_modelo_y_absorcion_del_pano=True,corridas=checks))
    for src in ('F1','F2'):
        fig,axes=plt.subplots(1,2,figsize=(9,6),sharex=True,sharey=True,constrained_layout=True)
        for ax,c in zip(axes,SPECS):
            rr=[r for r in means if r['estado']==c and r['fuente']==src and r['receptor'] in TARGET]
            pts=ax.scatter([positions[r['receptor']][0] for r in rr],[positions[r['receptor']][1] for r in rr],c=[r['D50_pct'] for r in rr],vmin=25,vmax=60,cmap='viridis',s=650,edgecolor='white')
            for r in rr:
                x,y=positions[r['receptor']][:2];ax.annotate(r['receptor'],(x,y),xytext=(0,18),textcoords='offset points',ha='center');ax.text(x,y,f"{r['D50_pct']:.1f}",ha='center',va='center',color='white' if r['D50_pct']<46 else '#222')
            ax.set(xlim=(24,34),ylim=(-11.5,12),xlabel='X (m)',ylabel='Y (m)',title='Sin tratamiento' if c=='sin_tratamiento' else 'Propuesta mixta');ax.grid(alpha=.15)
        fig.colorbar(pts,ax=axes,label='D50 (%)');fig.suptitle(src+' · Frente y zona media · 1.000 Hz');fig.savefig(O/f'mapa-D50-{src}.png',dpi=180);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11,5),sharex=True,sharey=True,constrained_layout=True)
    for ax,c in zip(axes,SPECS):
        ax.add_patch(Rectangle((45,-2),10,4,facecolor='#acd2b0',alpha=.4,edgecolor='#417849'))
        for r in means:
            if r['estado']!=c or r['receptor'] not in TARGET:continue
            ax.scatter(r['D50_pct'],r['C80'],color='#23789b' if r['fuente']=='F1' else '#bd702d',marker='o' if r['receptor'] in shared.OBJ['frente_butacas'] else '^',s=45)
            if r['fuente']=='F2' and r['receptor'] in ('V04','V08'):ax.annotate('F2–'+r['receptor'],(r['D50_pct'],r['C80']),xytext=(3,6),textcoords='offset points',fontsize=8)
        ax.set(xlim=(20,60),ylim=(-2.5,3),xlabel='D50 (%)',ylabel='C80 (dB)',title='Sin tratamiento' if c=='sin_tratamiento' else 'Propuesta mixta');ax.grid(alpha=.15)
    fig.suptitle('Criterios conjuntos · verde: D50 45–55 % y C80 −2/+2 dB\nAzul F1 / ocre F2 · círculos frente / triángulos media');fig.savefig(O/'D50-C80.png',dpi=180);plt.close(fig)
    fig,axes=plt.subplots(1,3,figsize=(13,5),constrained_layout=True)
    for ax,(s,p) in zip(axes,[('F1','P8'),('F2','V04'),('F2','V08')]):
        bottom=np.zeros(2);ref=by['sin_tratamiento',s,p]['total']
        for k,label,color in [('E0_50','0–50 ms','#398b76'),('E50_80','50–80 ms','#d1a24b'),('E80_total','>80 ms','#7d8e9b')]:
            y=np.array([by[c,s,p][k]/ref*100 for c in SPECS]);ax.bar([0,1],y,bottom=bottom,color=color,label=label);bottom+=y
        ax.set(xticks=[0,1],xticklabels=['Sin tratamiento','Propuesta'],title=s+'–'+p,ylabel='Energía / total sin tratamiento (%)');ax.legend(fontsize=8);ax.grid(axis='y',alpha=.15)
    fig.suptitle('Balance energético por ventanas · normalización común por receptor');fig.savefig(O/'balance-ventanas.png',dpi=180);plt.close(fig)
    for r in summary:print(r['estado'],r['grupo'],'D50',round(r['D50_pct_medio'],2),'C80',round(r['C80_medio'],2),'T30',round(r['T30_medio'],3),'cumplen',r['cumplen'],'/',r['n'],'estables',r['cumplen_tres_semillas'])
if __name__=='__main__':main()
