"""Cobertura por butacas, suelo expuesto y puntos de campo, separadamente."""
from pathlib import Path
import json,csv,hashlib,math,xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
import analizar_absorcion_posterior as old
B=Path(__file__).resolve().parent;O=B/'reflectores-cobertura';PREV=B/'reflectores';OUT=O/'resultados';OUT.mkdir(exist_ok=True)
SEATS=['V01','V02','V03','V04','V05','V08','V10','V11'];WOOD=['V06','V07','V09','V12']
PRIMARY=[('F1','P8'),('F1','P9'),('F2','P8')]
NEWCASES=list(json.loads((O/'variantes.json').read_text()))
CASES=['base','combinado']+NEWCASES
NAMES={'base':'Referencia','combinado':'Cuatro anteriores','cobertura4':'Cobertura · 4','equilibrio4':'Equilibrio · 4','cobertura6':'Cobertura · 6','central5':'Anterior + central · 5','retornos2':'Retornos 4×3 · 2','retornos_compactos2':'Retornos 6×2 · 2','mixta6':'Frontal y posterior · 6'}
def save(name,x):(OUT/name).write_text(json.dumps(x,indent=2,ensure_ascii=False),encoding='utf8')
def csvsave(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as fp:
        w=csv.DictWriter(fp,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def group(row):
    p=(row['fuente'],row['receptor'])
    return 'prioritarios' if p in PRIMARY else 'butacas_virtuales' if p[1] in SEATS else 'madera_virtual' if p[1] in WOOD else 'F2_P9' if p==('F2','P9') else 'platea_baja' if p[1] in ['P1','P2','P4','P7'] else 'bajo_balcon'

def main():
    old.core.O=O;new=[r for r in old.core.load() if r['N']==600000]
    old.core.O=PREV;refs=[r for r in old.core.load() if r['N']==600000 and r['variante'] in ('base','combinado')]
    assert len(new)==6*len(NEWCASES) and len(refs)==12,(len(new),len(refs))
    runs=refs+new;means=[];singles=[];by={}
    for c in CASES:
        for src in ('F1','F2'):
            rr=sorted([r for r in runs if r['variante']==c and r['fuente']==src],key=lambda r:r['semilla'])
            assert [r['semilla'] for r in rr]==[20261019,20261020,20261021]
            for p in rr[0]['curves']:
                mm=[]
                for r in rr:
                    m=old.parameters(r['curves'][p],r['t0'][p]);mm.append(m)
                    singles.append(dict(variante=c,fuente=src,receptor=p,semilla=r['semilla'],grupo=group(dict(fuente=src,receptor=p)),**m))
                m=old.parameters(np.mean([r['curves'][p] for r in rr],axis=0),rr[0]['t0'][p]);by[(c,src,p)]=m
                means.append(dict(variante=c,fuente=src,receptor=p,grupo=group(dict(fuente=src,receptor=p)),**m,
                    min_semilla_D50=min(r['D50_pct'] for r in mm),max_semilla_D50=max(r['D50_pct'] for r in mm),
                    min_semilla_C80=min(r['C80'] for r in mm),max_semilla_C80=max(r['C80'] for r in mm)))
    diffs=[];summary=[]
    for r in means:
        c,s,p=(r[k] for k in ('variante','fuente','receptor'));base=by[('base',s,p)];m=by[(c,s,p)]
        d=dict(variante=c,fuente=s,receptor=p,grupo=r['grupo'],D50=m['D50_pct'],C80=m['C80'],
            cumple=bool(48<=m['D50_pct']<=52 and -2<=m['C80']<=2))
        for k in ('D50_pct','C80','T30','EDT'):d['base_'+k]=base[k];d['delta_'+k]=m[k]-base[k]
        for k in ('E0_20','E20_50','E0_50','E50_80','E0_80','E50_total','E80_300','E300_1000','total'):d['delta_'+k+'_dB']=old.core.db(m[k]/base[k])
        diffs.append(d)
    for c in CASES:
        for grp in ('prioritarios','butacas_virtuales','madera_virtual','F2_P9','platea_baja','bajo_balcon'):
            rr=[r for r in diffs if r['variante']==c and r['grupo']==grp]
            summary.append(dict(variante=c,grupo=grp,n=len(rr),D50_medio=float(np.mean([r['D50'] for r in rr])),C80_medio=float(np.mean([r['C80'] for r in rr])),
                cumplen=sum(r['cumple'] for r in rr),bajo48=int(sum(r['D50']<48 for r in rr)),sobre52=int(sum(r['D50']>52 for r in rr)),C80_sobre2=int(sum(r['C80']>2 for r in rr)),
                D50_min=min(r['D50'] for r in rr),D50_max=max(r['D50'] for r in rr),C80_max=max(r['C80'] for r in rr),
                error_medio_a50=float(np.mean([abs(r['D50']-50) for r in rr])),
                **{k:float(np.mean([r[k] for r in rr])) for k in ('delta_D50_pct','delta_C80','delta_E0_50_dB','delta_T30','delta_EDT','delta_total_dB')},
                min_delta_D50=min(r['delta_D50_pct'] for r in rr),max_delta_D50=max(r['delta_D50_pct'] for r in rr)))
    assert len(means)==42*len(CASES) and len(singles)==126*len(CASES) and len(diffs)==42*len(CASES)
    for name,rows in [('medias',means),('semillas',singles),('comparaciones',diffs),('resumen-grupos',summary)]:save(name+'.json',rows);csvsave(name+'.csv',rows)
    checks=[]
    for data in runs:
        rootdir=PREV if data['variante'] in ('base','combinado') else O
        folder=rootdir/'calculos'/f"{data['variante']}-{data['fuente']}-1000Hz-N600000-seed{data['semilla']}-a0.05-s0.05"
        r=ET.parse(folder/'config.xml').getroot();sim=r.find('simulation')
        control=ET.parse(PREV/'calculos'/f"base-{data['fuente']}-1000Hz-N600000-seed{data['semilla']}-a0.05-s0.05"/'config.xml').getroot()
        assert ET.tostring(r.find('sources'))==ET.tostring(control.find('sources'))
        assert ET.tostring(r.find('recepteursp'))==ET.tostring(control.find('recepteursp'))
        assert [int(f.get('freq')) for f in sim.find('freq_enum') if f.get('docalc')=='1']==[1000]
        for source in r.find('sources'):
            lw=10*math.log10(sum(10**(float(b.get('db'))/10) for b in source.findall('bfreq')));assert abs(lw-90)<1e-3
        for k in sim.attrib:
            if k not in ('modelName','tetrameshFileName'):assert sim.get(k)==control.find('simulation').get(k),(folder,k)
        for x,y in zip(r.find('surface_absorption_enum'),control.find('surface_absorption_enum')):
            assert x.attrib==y.attrib and [(b.tag,b.attrib) for b in x]==[(b.tag,b.attrib) for b in y]
        for label,p in [('config',folder/'config.xml'),('malla',rootdir/data['variante']/'mesh.cbin'),('tetra',rootdir/data['variante']/'tetramesh.mbin')]:assert hashlib.sha256(p.read_bytes()).hexdigest()==data[label+'_sha256']
        checks.append(folder.name)
    save('verificacion-calculos.json',dict(nuevas=len(new),reutilizadas=12,receptores=21,frecuencia=1000,N=600000,semillas=[20261019,20261020,20261021],max_fraccion_perdidas=max(r['fraccion_perdidas'] for r in new),corridas=checks))
    # Eight-seat maps preserve exact positions; the four wood controls are distinct.
    xy=json.loads((PREV/'auditoria-posiciones.json').read_text())['receptores']
    fig,axs=plt.subplots(2,len(CASES),figsize=(19,8),sharex=True,sharey=True,constrained_layout=True)
    for col,c in enumerate(CASES):
        for row,src in enumerate(('F1','F2')):
            ax=axs[row,col]
            for rec in WOOD:ax.scatter(xy[rec][0],xy[rec][1],marker='x',c='#888888',s=25)
            rr=[r for r in means if r['variante']==c and r['fuente']==src and r['receptor'] in SEATS]
            pts=ax.scatter([xy[r['receptor']][0] for r in rr],[xy[r['receptor']][1] for r in rr],c=[r['D50_pct'] for r in rr],vmin=25,vmax=65,cmap='viridis',s=190,edgecolors='white',linewidth=.8)
            for r in rr:
                x,y=xy[r['receptor']][:2];ax.annotate(r['receptor'],(x,y),xytext=(0,13),textcoords='offset points',ha='center',fontsize=7)
                ax.text(x,y,f"{r['D50_pct']:.0f}",ha='center',va='center',fontsize=8,color='white' if r['D50_pct']<47 else '#222222')
            ax.set(xlim=(24,39),ylim=(-11,11),xlabel='X (m)');ax.grid(alpha=.15)
            if col==0:ax.set_ylabel(src+' · Y (m)')
            if row==0:ax.set_title(NAMES[c],fontsize=10)
    fig.colorbar(pts,ax=axs,label='D50 (%)',shrink=.8)
    fig.suptitle('Cobertura de ocho posiciones virtuales sobre butacas · 1.000 Hz\nValores medios de tres semillas · cruces grises: controles sobre madera')
    fig.savefig(OUT/'mapa-D50-butacas.png',dpi=170);plt.close(fig)
    for src in ('F1','F2'):
        colsmap=3 if len(CASES)==9 else 4
        rowsmap=math.ceil(len(CASES)/colsmap)
        fig,axes=plt.subplots(rowsmap,colsmap,figsize=(12 if colsmap==3 else 14,4.3*rowsmap),sharex=True,sharey=True,constrained_layout=True)
        for ax,c in zip(axes.flat,CASES):
            for rec in WOOD:ax.scatter(xy[rec][0],xy[rec][1],marker='x',c='#888888',s=25)
            rr=[r for r in means if r['variante']==c and r['fuente']==src and r['receptor'] in SEATS]
            pts=ax.scatter([xy[r['receptor']][0] for r in rr],[xy[r['receptor']][1] for r in rr],c=[r['D50_pct'] for r in rr],vmin=25,vmax=65,cmap='viridis',s=520,edgecolors='white')
            for r in rr:
                x,y=xy[r['receptor']][:2];ax.annotate(r['receptor'],(x,y),xytext=(0,17),textcoords='offset points',ha='center',fontsize=8)
                ax.text(x,y,f"{r['D50_pct']:.1f}",ha='center',va='center',fontsize=8,color='white' if r['D50_pct']<47 else '#222222')
            ax.set(title=NAMES[c],xlim=(24,39),ylim=(-11,11),xlabel='X (m)',ylabel='Y (m)');ax.grid(alpha=.15)
        for ax in list(axes.flat)[len(CASES):]:ax.axis('off')
        fig.colorbar(pts,ax=axes,label='D50 (%)',shrink=.8)
        fig.suptitle(src+' · Cobertura en posiciones sobre butacas · 1.000 Hz\nMisma escala de color en todas las geometrías · cruces: controles sobre madera')
        fig.savefig(OUT/f'mapa-D50-butacas-{src}.png',dpi=180);plt.close(fig)
    fig,axs=plt.subplots(1,2,figsize=(13,5),constrained_layout=True)
    for c in CASES:
        for ax,k in zip(axs,('D50_pct','C80')):
            pp=PRIMARY+[('F2','P9')];rr=[next(r for r in means if r['variante']==c and (r['fuente'],r['receptor'])==p) for p in pp]
            line,=ax.plot(range(4),[r[k] for r in rr],'o-',label=NAMES[c])
            ax.vlines(range(4),[r['min_semilla_D50' if k=='D50_pct' else 'min_semilla_C80'] for r in rr],[r['max_semilla_D50' if k=='D50_pct' else 'max_semilla_C80'] for r in rr],color=line.get_color(),alpha=.25)
    axs[0].axhspan(48,52,color='#459f70',alpha=.13);axs[1].axhspan(-2,2,color='#459f70',alpha=.13)
    for ax,label in zip(axs,('D50 (%)','C80 (dB)')):ax.set_xticks(range(4),['F1–P8','F1–P9','F2–P8','F2–P9\ncontrol']);ax.set_ylabel(label);ax.grid(alpha=.15);ax.legend(fontsize=8)
    fig.suptitle('Geometrías de cobertura · 600.000 partículas × 3 semillas · 1.000 Hz\nBarras: rango observado, no intervalo de confianza')
    fig.savefig(OUT/'comparacion-prioritarios.png',dpi=170);plt.close(fig)
    for r in summary:
        if r['grupo'] in ('prioritarios','butacas_virtuales'):print(r['variante'],r['grupo'],'D50',round(r['D50_medio'],2),'cumplen',str(r['cumplen'])+'/'+str(r['n']),'error50',round(r['error_medio_a50'],2))

if __name__=='__main__':main()
