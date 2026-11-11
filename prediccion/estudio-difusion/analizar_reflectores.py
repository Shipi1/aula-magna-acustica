"""Comparación de reflectores: respuestas completas, sin fijar energía temprana."""
from pathlib import Path
import json,csv,argparse,xml.etree.ElementTree as ET,hashlib
import numpy as np
import matplotlib.pyplot as plt
import analizar_absorcion_posterior as old
O=Path(__file__).resolve().parent/'reflectores'
OUT=O/'resultados';OUT.mkdir(exist_ok=True)
CASES=['base','adelantado','intermedio','combinado','selectivo']
PRIMARY=[('F1','P8'),('F1','P9'),('F2','P8')]
def save(name,d):(OUT/name).write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding='utf8')
def csvsave(name,d):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as fp:
        w=csv.DictWriter(fp,fieldnames=list(d[0]));w.writeheader();w.writerows(d)
def main(n,alpha=.05,scatter=.05):
    old.core.O=O
    runs=[r for r in old.core.load() if r['N']==n and r['alpha']==alpha and r['dispersion']==scatter]
    nr=1 if n==150000 else 3
    cases=[c for c in CASES if any(r['variante']==c for r in runs)]
    assert 'base' in cases
    singles=[];means=[];by={}
    for case in cases:
        for src in ('F1','F2'):
            rr=sorted([r for r in runs if r['variante']==case and r['fuente']==src],key=lambda r:r['semilla'])
            assert len(rr)==nr,(case,src,len(rr),nr)
            for rec in rr[0]['curves']:
                mm=[]
                for r in rr:
                    m=old.parameters(r['curves'][rec],r['t0'][rec]);mm.append(m)
                    singles.append(dict(variante=case,fuente=src,receptor=rec,N=n,semilla=r['semilla'],**m))
                m=old.parameters(np.mean([r['curves'][rec] for r in rr],axis=0),rr[0]['t0'][rec]);by[(case,src,rec)]=m
                means.append(dict(variante=case,fuente=src,receptor=rec,N=n,semillas=nr,**m,
                    min_D50=min(x['D50_pct'] for x in mm),max_D50=max(x['D50_pct'] for x in mm),min_C80=min(x['C80'] for x in mm),max_C80=max(x['C80'] for x in mm)))
    diffs=[]
    for row in means:
        c,s,p=(row[k] for k in ('variante','fuente','receptor'))
        if c=='base':continue
        b=by[('base',s,p)];m=by[(c,s,p)]
        d=dict(variante=c,fuente=s,receptor=p,N=n,primario=(s,p) in PRIMARY,D50=m['D50_pct'],C80=m['C80'],cumple=bool(48<=m['D50_pct']<=52 and -2<=m['C80']<=2))
        for k in ('D50_pct','C80','T30','EDT'):
            d['base_'+k]=b[k];d['delta_'+k]=m[k]-b[k]
        for k in ('E0_20','E20_50','E50_80','E0_50','E0_80','E50_total','E80_300','E300_1000','total'):
            d['delta_'+k+'_dB']=old.core.db(m[k]/b[k])
        diffs.append(d)
    summary=[]
    for case in cases[1:]:
        for zone,names in old.ZONES.items():
            rr=[r for r in diffs if r['variante']==case and r['receptor'] in names]
            summary.append(dict(variante=case,zona=zone,N=n,n=len(rr),D50=float(np.mean([r['D50'] for r in rr])),C80=float(np.mean([r['C80'] for r in rr])),
                **{k:float(np.mean([r[k] for r in rr])) for k in ('delta_D50_pct','delta_C80','delta_T30','delta_EDT','delta_E0_50_dB','delta_E50_80_dB','delta_E80_300_dB','delta_total_dB')},
                max_abs_delta_D50=max(abs(r['delta_D50_pct']) for r in rr),min_delta_D50=min(r['delta_D50_pct'] for r in rr)))
    tag=f'N{n}-a{alpha:g}-s{scatter:g}'
    for name,rows in [('semillas',singles),('medias',means),('comparaciones',diffs),('zonas',summary)]:
        save(name+'-'+tag+'.json',rows);csvsave(name+'-'+tag+'.csv',rows)
    fig,axs=plt.subplots(1,2,figsize=(12,6),constrained_layout=True)
    pairs=PRIMARY+[('F2','P9')];x=np.arange(4)
    for case in cases:
        for ax,key in zip(axs,('D50_pct','C80')):
            rr=[next(r for r in means if r['variante']==case and (r['fuente'],r['receptor'])==pair) for pair in pairs]
            y=[r[key] for r in rr];line,=ax.plot(x,y,'o-',label=case)
            if nr>1:
                ax.vlines(x,[r['min_D50' if key=='D50_pct' else 'min_C80'] for r in rr],[r['max_D50' if key=='D50_pct' else 'max_C80'] for r in rr],alpha=.3,color=line.get_color())
    axs[0].axhspan(48,52,color='#40a080',alpha=.12);axs[1].axhspan(-2,2,color='#40a080',alpha=.12)
    for ax,key in zip(axs,('D50 (%)','C80 (dB)')):
        ax.set_xticks(x,['F1–P8','F1–P9','F2–P8','F2–P9\ncontrol']);ax.set_ylabel(key);ax.grid(alpha=.15);ax.legend()
    particles=f'{n:,}'.replace(',','.')
    fig.suptitle(f'Reflectores · 1.000 Hz · {particles} partículas × {nr} semilla(s)\nα = {alpha:g}; s = {scatter:g} · hipótesis de material · barras: rango entre semillas')
    fig.savefig(OUT/('indicadores-'+tag+'.png'),dpi=160);plt.close(fig)
    checks=[]
    for r in runs:
        p=next(p for p in (O/'calculos').glob('*/ejecucion.json') if json.loads(p.read_text())['variante']==r['variante'] and json.loads(p.read_text())['fuente']==r['fuente'] and json.loads(p.read_text())['N']==n and json.loads(p.read_text())['semilla']==r['semilla'] and json.loads(p.read_text())['alpha']==alpha and json.loads(p.read_text())['dispersion']==scatter)
        root=ET.parse(p.parent/'config.xml').getroot();sim=root.find('simulation')
        ref=ET.parse(old.O/'calculos'/f"base-{r['fuente']}-1000Hz-N600000-seed20261019"/'config.xml').getroot()
        assert ET.tostring(root.find('sources'))==ET.tostring(ref.find('sources'))
        assert ET.tostring(root.find('recepteursp'))==ET.tostring(ref.find('recepteursp'))
        assert [int(b.get('freq')) for b in sim.find('freq_enum') if b.get('docalc')=='1']==[1000]
        for mat in root.find('surface_absorption_enum'):
            if mat.get('id')!='301':
                original=next(m for m in ref.find('surface_absorption_enum') if m.get('id')==mat.get('id'))
                assert mat.attrib==original.attrib and [(x.tag,x.attrib) for x in mat]==[(x.tag,x.attrib) for x in original]
        for label,path in [('config',p.parent/'config.xml'),('malla',O/r['variante']/'mesh.cbin'),('tetra',O/r['variante']/'tetramesh.mbin')]:
            assert hashlib.sha256(path.read_bytes()).hexdigest()==r[label+'_sha256']
        checks.append(p.parent.name)
    save('verificacion-'+tag+'.json',dict(corridas=len(runs),receptores=21,max_fraccion_perdidas=max(r['fraccion_perdidas'] for r in runs),archivos=checks))
    for c in cases:
        print(c,[(r['fuente']+'-'+r['receptor'],round(r['D50_pct'],2),round(r['C80'],2)) for r in means if r['variante']==c and r['receptor'] in ('P8','P9')])
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--N',type=int,default=150000);p.add_argument('--alpha',type=float,default=.05);p.add_argument('--scatter',type=float,default=.05);a=p.parse_args();main(a.N,a.alpha,a.scatter)
