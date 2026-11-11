"""Comparación independiente por ventanas, zonas y semillas."""
from pathlib import Path
import json,csv,hashlib,xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import analizar_frente_media_reflectores as shared
B=Path(__file__).resolve().parent;O=B/'reflectores-absorcion-localizada';OUT=O/'resultados';OUT.mkdir(exist_ok=True)
PROFILES=json.loads((O/'perfiles.json').read_text());OBJ=json.loads((O/'objetivo.json').read_text());CASES=list(PROFILES)
NAMES={'referencia':'Cuatro inclinados · referencia','superior_centro_a060':'Superior centro · 9,6 m² · α0,60','superior_completa_a060':'Superior extendido · 19,2 m² · α0,60','superior_completa_a080':'Superior extendido · 19,2 m² · α0,80','media_centro_a060':'Medio centro · 9,6 m² · α0,60'}
TARGET=OBJ['frente_butacas']+OBJ['media_butacas'];PAIRS=[(s,r) for s in ('F1','F2') for r in TARGET]
def save(name,x):(OUT/name).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
def csvsave(name,rows):
    with (OUT/name).open('w',newline='',encoding='utf-8-sig') as fp:w=csv.DictWriter(fp,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def good(m):return bool(45<=m['D50_pct']<=55 and -2<=m['C80']<=2)
def params(e,t0):
    m=shared.calc.parameters(e,t0);m['E80_total']=m['total']-m['E0_80'];return m
def main():
    runs=shared.load(O,CASES);assert len(runs)==30,len(runs);means=[];singles=[];by={};singleby={};curves={}
    for c in CASES:
        for s in ('F1','F2'):
            rr=sorted([r for r in runs if r['variante']==c and r['fuente']==s],key=lambda r:r['semilla']);assert [r['semilla'] for r in rr]==[20261019,20261020,20261021]
            positions=rr[0]['coords']
            for p in positions:
                mm=[]
                for r in rr:
                    m=params(r['curves'][p],r['t0'][p]);mm.append(m);singleby[(c,s,p,r['semilla'])]=m
                    singles.append(dict(variante=c,fuente=s,receptor=p,semilla=r['semilla'],**m))
                e=np.mean([r['curves'][p] for r in rr],axis=0);m=params(e,rr[0]['t0'][p]);by[(c,s,p)]=m;curves[(c,s,p)]=(e,rr[0]['t0'][p])
                means.append(dict(variante=c,fuente=s,receptor=p,**m,cumple=good(m),cumple_tres_semillas=all(good(x) for x in mm),
                    min_semilla_D50=min(x['D50_pct'] for x in mm),max_semilla_D50=max(x['D50_pct'] for x in mm),min_semilla_C80=min(x['C80'] for x in mm),max_semilla_C80=max(x['C80'] for x in mm)))
    diffs=[];seedchanges=[]
    for r in means:
        c,s,p=(r[k] for k in ('variante','fuente','receptor'));base=by[('referencia',s,p)];m=by[(c,s,p)]
        cfg=next(x['cfg'] for x in runs if x['variante']=='referencia' and x['fuente']==s);src=cfg.find('sources')[0];source=np.array([float(src.get(k)) for k in ('x','y','z')]);image=source.copy();image[0]=80.5-source[0]
        bound=float((np.linalg.norm(image-positions[p])-np.linalg.norm(source-positions[p]))/342*1000);safe=bound>50+1000*.31/342+1
        d=dict(variante=c,fuente=s,receptor=p,D50=m['D50_pct'],C80=m['C80'],cumple=good(m),cumple_tres_semillas=r['cumple_tres_semillas'],
            **{'delta_'+k:m[k]-base[k] for k in ('D50_pct','C80','EDT','T30')},
            **{'delta_'+k+'_dB':shared.calc.core.db(m[k]/base[k]) for k in ('E0_50','E50_80','E80_total','E50_total','total')},
            fraccion_0_50_pct=100*m['E0_50']/m['total'],fraccion_50_80_pct=100*m['E50_80']/m['total'],fraccion_80_mas_pct=100*m['E80_total']/m['total'])
        d.update(retardo_minimo_plano_posterior_ms=bound,temprano50_invariante_por_geometria=safe,
            D50_control_temprano=100*base['E0_50']/(base['E0_50']+m['E50_total']) if safe else None,
            C80_control_temprano=shared.calc.core.db((base['E0_50']+m['E50_80'])/m['E80_total']) if safe else None)
        sd=[]
        for seed in (20261019,20261020,20261021):
            mm=singleby[(c,s,p,seed)];bb=singleby[('referencia',s,p,seed)];change=mm['D50_pct']-bb['D50_pct'];sd.append(change)
            seedchanges.append(dict(variante=c,fuente=s,receptor=p,semilla=seed,delta_D50_pp=change,delta_C80=mm['C80']-bb['C80']))
        d.update(min_delta_semilla_D50=min(sd),max_delta_semilla_D50=max(sd),D50_aumenta_tres_semillas=all(v>0 for v in sd));diffs.append(d)
    groups={'frente':[(s,p) for s in ('F1','F2') for p in OBJ['frente_butacas']],
        'media':[(s,p) for s in ('F1','F2') for p in OBJ['media_butacas']], 'frente_media':PAIRS,
        'prioritarios':[tuple(p) for p in OBJ['pares_campo_prioritarios']], 'F2_V08':[('F2','V08')], 'F2_P9':[('F2','P9')],
        'platea_baja':[(s,p) for s in ('F1','F2') for p in ('P1','P2','P4','P7')], 'bajo_balcon':[(s,p) for s in ('F1','F2') for p in ('P3','P5','P6')],
        'posteriores':[(s,p) for s in ('F1','F2') for p in OBJ['posterior_butacas_control']], 'madera':[(s,p) for s in ('F1','F2') for p in OBJ['madera_control']]}
    summary=[]
    for c in CASES:
        for g,pairs in groups.items():
            rr=[r for r in diffs if r['variante']==c and (r['fuente'],r['receptor']) in pairs]
            summary.append(dict(variante=c,grupo=g,n=len(rr),D50_medio=float(np.mean([r['D50'] for r in rr])),C80_medio=float(np.mean([r['C80'] for r in rr])),
                distancia_media_banda=float(np.mean([max(45-r['D50'],0,r['D50']-55) for r in rr])),error_medio_a50=float(np.mean([abs(r['D50']-50) for r in rr])),
                cumplen=sum(r['cumple'] for r in rr),cumplen_tres_semillas=sum(r['cumple_tres_semillas'] for r in rr),C80_sobre2=sum(r['C80']>2 for r in rr),
                D50_min=min(r['D50'] for r in rr),D50_max=max(r['D50'] for r in rr),C80_max=max(r['C80'] for r in rr),
                D50_aumenta_tres_semillas=sum(r['D50_aumenta_tres_semillas'] for r in rr),
                **{k:float(np.mean([r[k] for r in rr])) for k in ('delta_D50_pct','delta_C80','delta_EDT','delta_T30','delta_E0_50_dB','delta_E50_80_dB','delta_E80_total_dB','delta_total_dB')}))
    for name,rows in [('medias',means),('semillas',singles),('comparaciones',diffs),('cambios-por-semilla',seedchanges),('resumen-zonas',summary)]:save(name+'.json',rows);csvsave(name+'.csv',rows)
    assert len(means)==210 and len(singles)==630
    old=shared.load(B/'reflectores-inclinacion',['combinada']);triang=[]
    for s in ('F1','F2'):
        rr=[r for r in old if r['fuente']==s];assert len(rr)==3
        for p in positions:
            m=params(np.mean([r['curves'][p] for r in rr],axis=0),rr[0]['t0'][p]);n=by[('referencia',s,p)]
            triang.append(dict(fuente=s,receptor=p,D50_anterior=m['D50_pct'],D50_nueva_referencia=n['D50_pct'],delta_D50_pp=n['D50_pct']-m['D50_pct'],delta_C80=n['C80']-m['C80']))
    save('control-subdivision.json',triang);csvsave('control-subdivision.csv',triang)
    checks=[];tetrahash=hashlib.sha256((O/'referencia/tetramesh.mbin').read_bytes()).hexdigest()
    for r in runs:
        ref=next(x for x in runs if x['variante']=='referencia' and x['fuente']==r['fuente'] and x['semilla']==r['semilla']);cfg=r['cfg'];base=ref['cfg']
        assert ET.tostring(cfg.find('sources'))==ET.tostring(base.find('sources')) and ET.tostring(cfg.find('recepteursp'))==ET.tostring(base.find('recepteursp'))
        for k,v in cfg.find('simulation').attrib.items():
            if k not in ('modelName','tetrameshFileName'):assert v==base.find('simulation').get(k)
        assert [int(b.get('freq')) for b in cfg.find('simulation/freq_enum') if b.get('docalc')=='1']==[1000]
        for m in cfg.find('surface_absorption_enum'):
            refmat=next(x for x in base.find('surface_absorption_enum') if x.get('id')==m.get('id'));assert m.attrib==refmat.attrib
            for band,refband in zip(m,refmat):
                expected=dict(refband.attrib)
                if m.get('id')=='201' and band.get('freq')=='1000' and PROFILES[r['variante']]['alpha'] is not None:expected['absorb']=str(PROFILES[r['variante']]['alpha'])
                assert band.attrib==expected
        for key,path in [('config',r['folder']/'config.xml'),('malla',O/r['variante']/'mesh.cbin'),('tetra',O/r['variante']/'tetramesh.mbin')]:assert hashlib.sha256(path.read_bytes()).hexdigest()==r[key+'_sha256']
        assert r['tetra_sha256']==tetrahash;checks.append(str(r['folder'].relative_to(B)))
    save('verificacion-calculos.json',dict(principales=30,pilotos=10,respuestas_medias=210,respuestas_individuales=630,max_fraccion_perdidas=max(r['fraccion_perdidas'] for r in runs),corridas=checks,MBIN_identico=True,solo_alpha_201_activo_cambia=True))
    for src in ('F1','F2'):
        fig,axes=plt.subplots(1,5,figsize=(18,6),sharex=True,sharey=True,constrained_layout=True)
        for ax,c in zip(axes,CASES):
            rr=[r for r in means if r['variante']==c and r['fuente']==src and r['receptor'] in TARGET]
            pts=ax.scatter([positions[r['receptor']][0] for r in rr],[positions[r['receptor']][1] for r in rr],c=[r['D50_pct'] for r in rr],cmap='viridis',vmin=25,vmax=65,s=480,edgecolor='white')
            for r in rr:
                x,y=positions[r['receptor']][:2];ax.annotate(r['receptor'],(x,y),xytext=(0,15),textcoords='offset points',ha='center',fontsize=8);ax.text(x,y,f"{r['D50_pct']:.1f}",ha='center',va='center',fontsize=8,color='white' if r['D50_pct']<47 else '#222')
            ax.set(xlim=(24,39),ylim=(-11.5,12),xlabel='X (m)',ylabel='Y (m)',title=NAMES[c].replace(' · ','\n'));ax.grid(alpha=.15)
        fig.colorbar(pts,ax=axes,label='D50 (%)',shrink=.8);fig.suptitle(src+' · Estudio mixto · 1.000 Hz · frente y zona media');fig.savefig(OUT/f'mapa-D50-{src}.png',dpi=170);plt.close(fig)
    fig,axes=plt.subplots(1,5,figsize=(18,5),sharex=True,sharey=True,constrained_layout=True)
    for ax,c in zip(axes,CASES):
        ax.add_patch(Rectangle((45,-2),10,4,facecolor='#a6cfad',alpha=.35,edgecolor='#397a43'))
        for r in means:
            if r['variante']!=c or r['receptor'] not in TARGET:continue
            ax.scatter(r['D50_pct'],r['C80'],color='#23789b' if r['fuente']=='F1' else '#be702e',marker='o' if r['receptor'] in OBJ['frente_butacas'] else '^',s=35)
            if r['fuente']=='F2' and r['receptor'] in ('V04','V08'):ax.annotate('F2–'+r['receptor'],(r['D50_pct'],r['C80']),xytext=(3,6),textcoords='offset points',fontsize=7)
        ax.set(xlim=(20,70),ylim=(-2.5,4.5),xlabel='D50 (%)',ylabel='C80 (dB)',title=NAMES[c].replace(' · ','\n'));ax.grid(alpha=.15)
    fig.suptitle('D50 y C80 · doce combinaciones por condición\nVerde: rango del estudio · azul F1 / ocre F2 · círculos frente / triángulos media');fig.savefig(OUT/'D50-C80-conjunto.png',dpi=170);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(13,5),constrained_layout=True)
    for ax,p in zip(axes,('V04','V08')):
        e0,t0=curves[('referencia','F2',p)];time=(np.arange(4000)*.001-t0)*1000
        for c in CASES:
            e,_=curves[(c,'F2',p)];ax.plot(time,np.convolve(e,np.ones(3)/3,mode='same')/e0.sum()*100,label=NAMES[c],lw=1)
        for t in (50,80):ax.axvline(t,c='#888',ls=':')
        ax.set(xlim=(0,180),xlabel='Tiempo desde directo (ms)',ylabel='Energía / total de referencia (%)',title='F2–'+p);ax.grid(alpha=.15);ax.legend(fontsize=7)
    fig.suptitle('Respuestas energéticas · suavizado de 3 ms solo para visualización');fig.savefig(OUT/'energia-V04-V08.png',dpi=170);plt.close(fig)
    fig,axes=plt.subplots(1,3,figsize=(14,5),constrained_layout=True)
    for ax,(s,p) in zip(axes,[('F2','V04'),('F2','V08'),('F1','P9')]):
        bottom=np.zeros(len(CASES));ref=by[('referencia',s,p)]['total']
        for key,label,color in [('E0_50','0–50 ms','#398b76'),('E50_80','50–80 ms','#d1a24b'),('E80_total','>80 ms','#7d8e9b')]:
            y=np.array([by[(c,s,p)][key]/ref*100 for c in CASES]);ax.bar(np.arange(len(CASES)),y,bottom=bottom,label=label,color=color);bottom+=y
        ax.set(xticks=np.arange(len(CASES)),xticklabels=['Ref.','Sup.9,6\nα0,6','Sup.19,2\nα0,6','Sup.19,2\nα0,8','Med.9,6\nα0,6'],ylabel='Energía / total de referencia (%)',title=s+'–'+p);ax.grid(axis='y',alpha=.15);ax.legend(fontsize=8)
    fig.suptitle('Energía por ventanas: normalización común al total de la referencia\nLa altura total puede cambiar; los colores no se renormalizan a 100 % por variante')
    fig.savefig(OUT/'balance-ventanas.png',dpi=170);plt.close(fig)
    for r in summary:
        if r['grupo'] in ('frente_media','frente','media','prioritarios'):print(r['variante'],r['grupo'],'D50',round(r['D50_medio'],2),'C80',round(r['C80_medio'],2),'cumplen',str(r['cumplen'])+'/'+str(r['n']),'distancia banda',round(r['distancia_media_banda'],2))
if __name__=='__main__':main()
