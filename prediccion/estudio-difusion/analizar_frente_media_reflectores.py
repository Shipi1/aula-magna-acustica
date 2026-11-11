"""Análisis espacial y temporal de variantes dirigidas a frente/media."""
from pathlib import Path
import json,csv,xml.etree.ElementTree as ET,hashlib,math
import numpy as np
import matplotlib.pyplot as plt
import analizar_absorcion_posterior as calc
B=Path(__file__).resolve().parent;O=B/'reflectores-frente-media';OUT=O/'resultados';OUT.mkdir(exist_ok=True)
OBJ=json.loads((O/'objetivo.json').read_text());PROFILES=json.loads((O/'perfiles.json').read_text())
CASES=['base','cobertura6','retornos2']+list(PROFILES)
NAMES={'base':'Referencia','cobertura6':'Seis redistribuidos','retornos2':'Dos posteriores','lateral9':'Laterales Y±9','lateral8':'Laterales Y±8','lateral8_adel':'Laterales + adelantados','lateral8_inter':'Laterales + intermedios','lateral8_equiv':'Y±8 · α del muro'}
REFERENCES=[(B/'reflectores',['base']),(B/'reflectores-cobertura',['cobertura6','retornos2'])]
ENERGY_REFERENCE='base';ENERGY_CASES=None
def save(name,d):(OUT/name).write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding='utf8')
def csvsave(name,rows):
    with (OUT/name).open('w',newline='',encoding='utf-8-sig') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def load(root,cases):
    result=[]
    for p in sorted((root/'calculos').glob('*/ejecucion.json')):
        d=json.loads(p.read_text())
        if d['N']!=600000 or d['variante'] not in cases:continue
        cfg=ET.parse(p.parent/'config.xml').getroot();s=cfg.find('sources')[0];source=np.array([float(s.get(k)) for k in ('x','y','z')])
        coords={r.get('name'):np.array([float(r.get(k)) for k in ('x','y','z')]) for r in cfg.find('recepteursp')}
        values=json.loads((p.parent/'resultados-lineales.json').read_text())
        curves={name:np.array(next(iter(columns.values())),float) for name,columns in values['receptores'].items()}
        assert len(curves)==21 and set(curves)==set(coords)
        assert all(len(e)==4000 and np.isfinite(e).all() and (e>=0).all() and e.sum()>0 for e in curves.values())
        d.update(folder=p.parent,root=root,cfg=cfg,curves=curves,coords=coords,t0={name:float(np.linalg.norm(q-source)/342) for name,q in coords.items()})
        result.append(d)
    return result
def main():
    runs=[r for root,cases in REFERENCES for r in load(root,cases)]+load(O,list(PROFILES))
    assert len(runs)==6*len(CASES),len(runs)
    primary=[tuple(p) for p in OBJ['pares_campo_prioritarios']]
    groups={
        'frente':[(s,p) for s in ('F1','F2') for p in OBJ['frente_butacas']],
        'media':[(s,p) for s in ('F1','F2') for p in OBJ['media_butacas']],
        'posterior_control':[(s,p) for s in ('F1','F2') for p in OBJ['posterior_butacas_control']],
        'madera_control':[(s,p) for s in ('F1','F2') for p in OBJ['madera_control']],
        'campo_prioritario':primary,'F2_P9':[('F2','P9')],
        'platea_baja':[(s,p) for s in ('F1','F2') for p in ['P1','P2','P4','P7']],
        'bajo_balcon':[(s,p) for s in ('F1','F2') for p in ['P3','P5','P6']]}
    groups['frente_media']=groups['frente']+groups['media']
    singles=[];means=[];curves={};by={};positions={}
    for c in CASES:
        for src in ('F1','F2'):
            rr=sorted([r for r in runs if r['variante']==c and r['fuente']==src],key=lambda r:r['semilla'])
            assert [r['semilla'] for r in rr]==[20261019,20261020,20261021]
            positions=rr[0]['coords']
            for p in positions:
                mm=[]
                for r in rr:
                    m=calc.parameters(r['curves'][p],r['t0'][p]);mm.append(m);singles.append(dict(variante=c,fuente=src,receptor=p,semilla=r['semilla'],**m))
                e=np.mean([r['curves'][p] for r in rr],axis=0);m=calc.parameters(e,rr[0]['t0'][p]);by[(c,src,p)]=m;curves[(c,src,p)]=(e,rr[0]['t0'][p])
                means.append(dict(variante=c,fuente=src,receptor=p,**m,
                    min_semilla_D50=min(x['D50_pct'] for x in mm),max_semilla_D50=max(x['D50_pct'] for x in mm),
                    min_semilla_C80=min(x['C80'] for x in mm),max_semilla_C80=max(x['C80'] for x in mm)))
    diffs=[]
    for r in means:
        c,s,p=(r[k] for k in ('variante','fuente','receptor'));m=by[(c,s,p)];b=by[('base',s,p)]
        d=dict(variante=c,fuente=s,receptor=p,D50=m['D50_pct'],C80=m['C80'],cumple=bool(48<=m['D50_pct']<=52 and -2<=m['C80']<=2))
        for k in ('D50_pct','C80','T30','EDT'):d['base_'+k]=b[k];d['delta_'+k]=m[k]-b[k]
        for k in ('E0_20','E20_50','E0_50','E50_80','E0_80','E50_total','E80_300','E300_1000','total'):d['delta_'+k+'_dB']=calc.core.db(m[k]/b[k])
        d['fraccion_50_80_pct']=100*m['E50_80']/m['total'];diffs.append(d)
    summary=[]
    for c in CASES:
        for grp,pairs in groups.items():
            rr=[r for r in diffs if r['variante']==c and (r['fuente'],r['receptor']) in pairs]
            summary.append(dict(variante=c,grupo=grp,n=len(rr),D50_medio=float(np.mean([r['D50'] for r in rr])),C80_medio=float(np.mean([r['C80'] for r in rr])),
                error_medio_a50=float(np.mean([abs(r['D50']-50) for r in rr])),cumplen=sum(r['cumple'] for r in rr),
                bajo48=int(sum(r['D50']<48 for r in rr)),sobre52=int(sum(r['D50']>52 for r in rr)),C80_sobre2=sum(r['C80']>2 for r in rr),
                D50_min=min(r['D50'] for r in rr),D50_max=max(r['D50'] for r in rr),C80_max=max(r['C80'] for r in rr),
                **{k:float(np.mean([r[k] for r in rr])) for k in ('delta_D50_pct','delta_C80','delta_T30','delta_EDT','delta_E0_50_dB','delta_E50_80_dB','delta_total_dB')},
                min_delta_D50=min(r['delta_D50_pct'] for r in rr)))
    assert len(means)==42*len(CASES) and len(singles)==126*len(CASES)
    for name,rows in [('medias',means),('semillas',singles),('comparaciones',diffs),('resumen-grupos',summary)]:save(name+'.json',rows);csvsave(name+'.csv',rows)
    checks=[]
    for r in runs:
        ctrl=next(x for x in runs if x['variante']=='base' and x['fuente']==r['fuente'] and x['semilla']==r['semilla']);cfg=r['cfg'];base=ctrl['cfg'];sim=cfg.find('simulation')
        assert ET.tostring(cfg.find('sources'))==ET.tostring(base.find('sources')) and ET.tostring(cfg.find('recepteursp'))==ET.tostring(base.find('recepteursp'))
        for k in sim.attrib:
            if k not in ('modelName','tetrameshFileName'):assert sim.get(k)==base.find('simulation').get(k),(r['folder'],k)
        assert [int(f.get('freq')) for f in sim.find('freq_enum') if f.get('docalc')=='1']==[1000]
        for m in cfg.find('surface_absorption_enum'):
            ref=next(b for b in base.find('surface_absorption_enum') if b.get('id')==m.get('id'))
            if m.get('id')!='301':assert m.attrib==ref.attrib and [(b.tag,b.attrib) for b in m]==[(b.tag,b.attrib) for b in ref]
            else:
                alpha=PROFILES[r['variante']]['alpha'] if r['root']==O else .05
                for bf in m:
                    if bf.get('freq')=='1000':assert float(bf.get('absorb'))==alpha and float(bf.get('diffusion'))==.05
        for key,p in [('config',r['folder']/'config.xml'),('malla',r['root']/r['variante']/'mesh.cbin'),('tetra',r['root']/r['variante']/'tetramesh.mbin')]:assert hashlib.sha256(p.read_bytes()).hexdigest()==r[key+'_sha256']
        checks.append(str(r['folder'].relative_to(B)))
    save('verificacion-calculos.json',dict(nuevas=6*len(PROFILES),reutilizadas=sum(6*len(cases) for _,cases in REFERENCES),N=600000,semillas=[20261019,20261020,20261021],receptores=21,frecuencia_Hz=1000,max_fraccion_perdidas=max(r['fraccion_perdidas'] for r in runs if r['root']==O),corridas=checks))
    for src in ('F1','F2'):
        fig,axes=plt.subplots(2,4,figsize=(15,9),sharex=True,sharey=True,constrained_layout=True)
        for ax,c in zip(axes.flat,CASES):
            target=OBJ['frente_butacas']+OBJ['media_butacas'];control=OBJ['madera_control']+OBJ['posterior_butacas_control']
            for p in control:ax.scatter(positions[p][0],positions[p][1],marker='x',color='#888888',s=30)
            rr=[r for r in means if r['variante']==c and r['fuente']==src and r['receptor'] in target]
            pts=ax.scatter([positions[r['receptor']][0] for r in rr],[positions[r['receptor']][1] for r in rr],c=[r['D50_pct'] for r in rr],vmin=25,vmax=65,cmap='viridis',s=520,edgecolors='white')
            for r in rr:
                x,y=positions[r['receptor']][:2];ax.annotate(r['receptor'],(x,y),xytext=(0,16),textcoords='offset points',ha='center',fontsize=8)
                ax.text(x,y,f"{r['D50_pct']:.1f}",ha='center',va='center',fontsize=8,color='white' if r['D50_pct']<47 else '#222')
            ax.set(title=NAMES[c],xlim=(24,39),ylim=(-11.5,12),xlabel='X (m)',ylabel='Y (m)');ax.grid(alpha=.15)
        for ax in list(axes.flat)[len(CASES):]:ax.axis('off')
        fig.colorbar(pts,ax=axes,label='D50 (%)',shrink=.8);fig.suptitle(src+' · Prioridad frente y media · 1.000 Hz\nCruces: controles posteriores y sobre madera, fuera de la optimización')
        fig.savefig(OUT/f'mapa-D50-{src}.png',dpi=170);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(14,5),constrained_layout=True)
    for ax,rec in zip(axes,('V04','V08')):
        reference,t0=curves[(ENERGY_REFERENCE,'F2',rec)];norm=reference.sum();time=(np.arange(4000)*.001-t0)*1000
        for c in (ENERGY_CASES or ('base',)+tuple(PROFILES)):
            e,_=curves[(c,'F2',rec)];smooth=np.convolve(e,np.ones(3)/3,mode='same')/norm*100
            ax.plot(time,smooth,label=NAMES[c],lw=1.1)
        ax.axvline(50,c='#444',ls=':');ax.axvline(80,c='#888',ls=':');ax.set(xlim=(0,100),xlabel='Tiempo desde directo (ms)',ylabel='Energía por bin / total de referencia (%)',title='F2–'+rec);ax.grid(alpha=.15);ax.legend(fontsize=7)
    fig.suptitle('Respuestas energéticas medias · suavizado de 3 ms solo para visualización')
    fig.savefig(OUT/'energia-V04-V08.png',dpi=170);plt.close(fig)
    for r in summary:
        if r['grupo'] in ('frente','media','frente_media'):print(r['variante'],r['grupo'],'D50',round(r['D50_medio'],2),'C80',round(r['C80_medio'],2),'cumplen',str(r['cumplen'])+'/'+str(r['n']),'error50',round(r['error_medio_a50'],2))
if __name__=='__main__':main()
