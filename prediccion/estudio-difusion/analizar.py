"""Comparación energética reproducible; conserva curvas, semillas y receptores."""
from pathlib import Path
import json,csv,xml.etree.ElementTree as ET
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
B=Path(__file__).resolve().parent
OUT=B/'resultados';OUT.mkdir(exist_ok=True)
DT=.001

def win(e,a,b):
    t=np.arange(len(e))*DT
    weights=np.maximum(0,np.minimum(t+DT,b)-np.maximum(t,a))/DT
    return float(e@weights)

def db(x):return float(10*np.log10(max(x,1e-30)))

def metric(e,t0):
    total=float(e.sum()); early=win(e,0,t0+.08); late=win(e,t0+.08,4)
    w=win(e,t0+.08,t0+.3)
    ends=np.arange(t0+.08,t0+.29+1e-8,.001)
    sliding=np.array([win(e,a,a+.01) for a in ends])
    maximum=int(sliding.argmax())
    sch=10*np.log10(np.maximum(np.cumsum(e[::-1])[::-1]/total,1e-30)); t=np.arange(len(e))*DT
    fit=(sch<=-5)&(sch>=-35)
    rt=-60/np.polyfit(t[fit],sch[fit],1)[0] if fit.sum()>5 else float('nan')
    return {'total':total,'E0_20':win(e,0,t0+.02),'E20_80':win(e,t0+.02,t0+.08),'E0_80':early,'E80_300':w,'E300_1000':win(e,t0+.3,t0+1),'C80':db(early/late),'T30':float(rt),'fraccion_tardia':late/total,'max10ms_80_300':float(sliding.max()),'concentracion10ms':float(sliding.max()/w),'retardo_max10ms':float((ends[maximum]-t0)*1000)}

def load():
    runs=[]
    for meta in sorted((B/'calculos').glob('*/ejecucion.json')):
        d=json.loads(meta.read_text()); path=meta.parent
        result=json.loads((path/'resultados-lineales.json').read_text())
        conf=ET.parse(path/'config.xml').getroot(); src=list(conf.find('sources'))[0]
        xyz=np.array([float(src.get(k)) for k in ['x','y','z']])
        receivers={r.get('name'):np.array([float(r.get(k)) for k in ['x','y','z']]) for r in conf.find('recepteursp')}
        curves={name:np.array(next(iter(cols.values())),float) for name,cols in result['receptores'].items()}
        assert all(len(e)==4000 and (e>=0).all() and e.sum()>0 for e in curves.values())
        d.update(curves=curves,t0={n:float(np.linalg.norm(p-xyz)/342) for n,p in receivers.items()},path=path,stats=result['estadisticas'])
        runs.append(d)
    return runs

def main():
    runs=load();rows=[]
    for d in runs:
        for receiver,e in d['curves'].items():
            r={k:d[k] for k in ['variante','fuente','frecuencia','N','semilla','dispersion']}
            r['receptor']=receiver;r.update(metric(e,d['t0'][receiver]));rows.append(r)
    if not rows:return
    with (OUT/'indicadores.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    diffs=[]
    for row in rows:
        if row['variante']=='base':continue
        base=next((r for r in rows if r['variante']=='base' and all(r[k]==row[k] for k in ['fuente','frecuencia','N','semilla','receptor'])),None)
        if base is None:continue
        d={k:row[k] for k in ['variante','fuente','frecuencia','N','semilla','dispersion','receptor']}
        for k in ['total','E0_20','E20_80','E0_80','E80_300','E300_1000','max10ms_80_300']:
            d['delta_'+k+'_dB']=db(row[k]/base[k])
        for k in ['C80','T30','concentracion10ms','fraccion_tardia']:d['delta_'+k]=row[k]-base[k]
        diffs.append(d)
    if diffs:
        with (OUT/'diferencias.csv').open('w',newline='',encoding='utf-8-sig') as f:
            w=csv.DictWriter(f,fieldnames=list(diffs[0]));w.writeheader();w.writerows(diffs)
    summary=[]
    for variant in sorted(set(d['variante'] for d in diffs)):
        for n in sorted(set(d['N'] for d in diffs)):
            for s in sorted(set(d['dispersion'] for d in diffs if d['variante']==variant and d['N']==n)):
                for freq in [1000,2000,4000]:
                    for zone,names in [('alta',['P8','P9']),('piso',['P1','P2','P4','P7']),('bajo',['P3','P5','P6'])]:
                        sel=[d for d in diffs if d['variante']==variant and d['N']==n and d['dispersion']==s and d['frecuencia']==freq and d['receptor'] in names]
                        if not sel:continue
                        summary.append({'variante':variant,'N':n,'s':s,'frecuencia':freq,'zona':zone,'n':len(sel),**{k:float(np.mean([d[k] for d in sel])) for k in sel[0] if k.startswith('delta_')}})
    (OUT/'resumen.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    plot_patches()
    plot_screen(runs,diffs)
    print('runs',len(runs),'rows',len(rows),'paired',len(diffs))
    for d in summary:
        if d['zona']=='alta':print(d['variante'],d['N'],d['s'],d['frecuencia'],'late',round(d['delta_E80_300_dB'],2),'early',round(d['delta_E0_80_dB'],2),'C80',round(d['delta_C80'],2))

def plot_patches():
    m=json.loads((B/'malla-base.json').read_text());v=np.array(m['vertices']); patches=json.loads((B/'panos.json').read_text())
    fig,axs=plt.subplots(1,3,figsize=(14,4),constrained_layout=True)
    for ax,(name,d) in zip(axs,patches.items()):
        axes=[0,2] if name!='fondo_alto' else [1,2]
        faces=[v[m['faces'][i]['v']][:,axes] for i in d['faces']]
        ax.add_collection(PolyCollection(faces,facecolor='#248d9c',edgecolor='white',linewidth=.4,alpha=.8));ax.autoscale();ax.set_aspect('equal');ax.set_title(f'{name}\n{d["area_m2"]:.1f} m²');ax.set_xlabel('X (m)' if axes[0]==0 else 'Y (m)');ax.set_ylabel('Z (m)')
    fig.savefig(OUT/'panos.png',dpi=160);plt.close(fig)

def plot_screen(runs,diffs):
    colors={'base':'#333333','lateral_Yneg':'#237a9b','lateral_Ypos':'#b56b22','fondo_alto':'#7d4ca0'}
    for src in ['F1','F2']:
        fig,axs=plt.subplots(2,3,figsize=(15,7),sharex=True,sharey=True,constrained_layout=True)
        for ri,receiver in enumerate(['P8','P9']):
            for ci,freq in enumerate([1000,2000,4000]):
                ax=axs[ri,ci]; selected=[d for d in runs if d['N']==150000 and d['fuente']==src and d['frecuencia']==freq and (d['variante']=='base' or d['dispersion']==.6)]
                base=next((d for d in selected if d['variante']=='base'),None)
                if base is None:continue
                norm=np.convolve(base['curves'][receiver],np.ones(5),'same').max()
                for d in selected:
                    e=np.convolve(d['curves'][receiver],np.ones(5),'same')
                    t=(np.arange(len(e))+.5)*DT-d['t0'][receiver]
                    ax.plot(t*1000,10*np.log10(np.maximum(e/norm,1e-12)),color=colors[d['variante']],label=d['variante'],lw=.9,alpha=.85)
                ax.axvspan(80,300,color='#ccc',alpha=.15);ax.set_xlim(0,600);ax.set_ylim(-45,3);ax.set_title(f'{src} · {receiver} · {freq} Hz');ax.grid(alpha=.15);ax.set_xlabel('Retardo respecto del directo (ms)');ax.set_ylabel('Energía 5 ms / máximo base (dB)')
        axs[0,0].legend(fontsize=8);fig.savefig(OUT/f'ecogramas-exploracion-{src}.png',dpi=160);plt.close(fig)

if __name__=='__main__':main()
