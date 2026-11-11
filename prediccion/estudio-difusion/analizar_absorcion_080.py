"""Comparación posterior alfa .80: respuestas energéticas medias, sin interpolación."""
import json, csv, hashlib
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import analizar_absorcion_posterior as previous

O=previous.O
OUT=O/'resultados-a080'
OUT.mkdir(exist_ok=True)
CASES=['base','total_a080','sup_centro_a080','sup_exterior_a080','sup_completa_a080',
       'med_centro_a080','med_exterior_a080','med_completa_a080']
LABELS=['Base','Muro completo','Superior central','Superior exterior','Superior completa',
        'Media central','Media exterior','Media completa']
SEEDS=[20261019,20261020,20261021]

def save(name,data):
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')

def csvsave(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    runs=[r for r in previous.core.load() if r['N']==600000 and r['frecuencia']==1000 and r['variante'] in CASES]
    assert len(runs)==48,len(runs)
    specs=json.loads((O/'escenarios.json').read_text(encoding='utf8'))
    singles=[];means=[];curves={};separate={}
    for case in CASES:
        for src in ('F1','F2'):
            rr=sorted([r for r in runs if r['variante']==case and r['fuente']==src],key=lambda r:r['semilla'])
            assert [r['semilla'] for r in rr]==SEEDS
            for rec in rr[0]['curves']:
                ms=[]
                for r in rr:
                    m=previous.parameters(r['curves'][rec],r['t0'][rec]);ms.append(m)
                    singles.append(dict(variante=case,fuente=src,receptor=rec,semilla=r['semilla'],**m))
                e=np.mean([r['curves'][rec] for r in rr],axis=0)
                m=previous.parameters(e,rr[0]['t0'][rec]);curves[(case,src,rec)]=m;separate[(case,src,rec)]=ms
                means.append(dict(variante=case,fuente=src,receptor=rec,area_m2=specs[case]['area_m2'],**m,
                    min_semilla_D50=min(x['D50_pct'] for x in ms),max_semilla_D50=max(x['D50_pct'] for x in ms),
                    min_semilla_C80=min(x['C80'] for x in ms),max_semilla_C80=max(x['C80'] for x in ms)))
    comparison=[]
    safe=json.loads((O/'resultados/comparacion-ideal.json').read_text(encoding='utf8'))
    safe={(r['fuente'],r['receptor']):r['temprano50_invariante_demostrado'] for r in safe}
    for row in means:
        case,src,rec=(row[k] for k in ('variante','fuente','receptor'))
        if case=='base':continue
        base=curves[('base',src,rec)];m=curves[(case,src,rec)]
        d=dict(variante=case,fuente=src,receptor=rec,area_m2=row['area_m2'],
               base_D50=base['D50_pct'],D50=m['D50_pct'],delta_D50_pp=m['D50_pct']-base['D50_pct'],
               base_C80=base['C80'],C80=m['C80'],delta_C80=m['C80']-base['C80'],
               cumple_D50=bool(48<=m['D50_pct']<=52),cumple_C80=bool(m['C80']<=2),
               cumple_conjunto=bool(48<=m['D50_pct']<=52 and -2<=m['C80']<=2),
               min_semilla_D50=row['min_semilla_D50'],max_semilla_D50=row['max_semilla_D50'],
               min_semilla_C80=row['min_semilla_C80'],max_semilla_C80=row['max_semilla_C80'])
        for k in ('EDT','T20','T30'):
            d['base_'+k]=base[k];d[k]=m[k];d['delta_'+k]=m[k]-base[k]
        for k in ('E0_50','E50_80','E0_80','E50_total','E80_300','E300_1000','total'):
            d['delta_'+k+'_dB']=previous.core.db(m[k]/base[k])
        d['D50_control_temprano']=100*base['E0_50']/(base['E0_50']+m['E50_total']) if safe[(src,rec)] else None
        late80=m['total']-m['E0_80']
        d['C80_control_temprano']=previous.core.db((base['E0_50']+m['E50_80'])/late80) if safe[(src,rec)] else None
        control=[100*separate[('base',src,rec)][i]['E0_50']/(separate[('base',src,rec)][i]['E0_50']+separate[(case,src,rec)][i]['E50_total']) for i in range(3)] if safe[(src,rec)] else []
        d['min_semilla_control']=min(control) if control else None;d['max_semilla_control']=max(control) if control else None
        comparison.append(d)
    summaries=[]
    for case in CASES[1:]:
        for zone,names in previous.ZONES.items():
            rr=[r for r in comparison if r['variante']==case and r['receptor'] in names]
            summaries.append(dict(variante=case,zona=zone,n=len(rr),area_m2=specs[case]['area_m2'],
                D50=float(np.mean([r['D50'] for r in rr])),C80=float(np.mean([r['C80'] for r in rr])),
                min_D50=min(r['D50'] for r in rr),max_D50=max(r['D50'] for r in rr),
                max_C80=max(r['C80'] for r in rr),cumplen_conjunto=sum(r['cumple_conjunto'] for r in rr),
                **{k:float(np.mean([r[k] for r in rr])) for k in ('delta_D50_pp','delta_C80','delta_T30','delta_EDT','delta_total_dB')},
                max_abs_delta_D50=max(abs(r['delta_D50_pp']) for r in rr)))
    assert (len(singles),len(means),len(comparison),len(summaries))==(1008,336,294,28)
    for name,rows in [('indicadores-por-semilla',singles),('respuestas-medias',means),('comparaciones',comparison),('resumen-zonas',summaries)]:
        save(name+'.json',rows);csvsave(name+'.csv',rows)
    fig,axs=plt.subplots(2,2,figsize=(14,9),sharex=True,constrained_layout=True)
    colors=['#176b83','#b45b26'];x=np.arange(len(CASES))
    for col,rec in enumerate(('P8','P9')):
        for src,color in zip(('F1','F2'),colors):
            for ax,key in ((axs[0,col],'D50_pct'),(axs[1,col],'C80')):
                y=[curves[(case,src,rec)][key] for case in CASES]
                low=[min(m[key] for m in separate[(case,src,rec)]) for case in CASES]
                high=[max(m[key] for m in separate[(case,src,rec)]) for case in CASES]
                ax.vlines(x,low,high,color=color,alpha=.5)
                ax.plot(x,y,'o-',color=color,label=src)
        axs[0,col].axhspan(48,52,color='#61a45e',alpha=.15);axs[0,col].set(title=rec,ylabel='D50 (%)')
        axs[1,col].axhspan(-2,2,color='#61a45e',alpha=.15);axs[1,col].axhline(2,color='#61a45e',ls=':');axs[1,col].set(ylabel='C80 (dB)')
        for ax in axs[:,col]:ax.grid(alpha=.15);ax.legend();ax.set_xticks(x,LABELS,rotation=40,ha='right')
    for row in axs:
        lo=min(ax.get_ylim()[0] for ax in row);hi=max(ax.get_ylim()[1] for ax in row)
        for ax in row:ax.set_ylim(lo,hi)
    fig.suptitle('Absorción posterior α = 0,80 · 1.000 Hz\n600.000 partículas × 3 semillas · barras: rango observado, no intervalo de confianza')
    fig.savefig(OUT/'D50-C80-por-posicion.png',dpi=160);plt.close(fig)
    checks=dict(corridas_nuevas=42,referencias_reutilizadas=6,receptores=21,N=600000,semillas=SEEDS,frecuencia_Hz=1000,
        max_fraccion_perdidas=max(r['fraccion_perdidas'] for r in runs),verificaciones=[])
    import xml.etree.ElementTree as ET
    for p in (O/'calculos').glob('*/ejecucion.json'):
        r=json.loads(p.read_text())
        if r['variante'] not in CASES or r['N']!=600000 or r['frecuencia']!=1000:continue
        root=ET.parse(p.parent/'config.xml').getroot();mats=root.find('surface_absorption_enum')
        sim=root.find('simulation')
        assert int(sim.get('nbparticules'))==600000
        assert [int(b.get('freq')) for b in sim.find('freq_enum') if b.get('docalc')=='1']==[1000]
        for src in root.find('sources'):
            lw=10*np.log10(sum(10**(float(b.get('db'))/10) for b in src.findall('bfreq')))
            assert abs(lw-90)<1e-3
        baseline=ET.parse(O/'calculos'/f"base-{r['fuente']}-1000Hz-N600000-seed{r['semilla']}"/'config.xml').getroot()
        assert ET.tostring(root.find('sources'))==ET.tostring(baseline.find('sources'))
        assert ET.tostring(root.find('recepteursp'))==ET.tostring(baseline.find('recepteursp'))
        for key in sim.attrib:
            if key!='modelName':assert sim.get(key)==baseline.find('simulation').get(key),(p,key)
        for b,t in zip(baseline.find('surface_absorption_enum'),mats):
            if b.get('id')!='201':assert ET.tostring(b)==ET.tostring(t)
        base=next(m for m in mats if m.get('id')=='115');panel=next(m for m in mats if m.get('id')=='201')
        for b,t in zip(base,panel):
            assert b.get('diffusion')==t.get('diffusion') and b.get('loi')==t.get('loi')
            if r['variante']!='base' and b.get('freq')=='1000':assert float(t.get('absorb'))==.8
            else:assert b.get('absorb')==t.get('absorb')
        assert hashlib.sha256((p.parent/'config.xml').read_bytes()).hexdigest()==r['config_sha256']
        assert hashlib.sha256((O/specs[r['variante']]['malla']).read_bytes()).hexdigest()==r['malla_sha256']
        assert hashlib.sha256((O/'tetramesh.mbin').read_bytes()).hexdigest()==r['tetra_sha256']
        checks['verificaciones'].append(str(p.parent.name))
    assert len(checks['verificaciones'])==48
    save('verificacion.json',checks)
    print(json.dumps([r for r in summaries if r['zona']=='P8_P9'],ensure_ascii=False,indent=2))

if __name__=='__main__':main()
