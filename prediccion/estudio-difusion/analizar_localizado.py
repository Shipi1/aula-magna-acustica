"""Comparación del primer barrido localizado; una semilla, no convergencia."""
from preparar_localizado import B,O,save
from analizar import metric,win,db,DT
import json,csv,xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt

OUT=O/'resultados';OUT.mkdir(exist_ok=True)
def store(name,data): (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
def csvout(name,rows):
    with (OUT/name).open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
def metrics(e,t0):
    d=metric(e,t0);d['E60_120']=win(e,t0+.06,t0+.12)
    d['max10ms_60_120']=max(win(e,t,t+.01) for t in np.arange(t0+.06,t0+.11+1e-9,.001))
    return d
def loadruns():
    runs=[]
    for meta in sorted((O/'calculos').glob('*/ejecucion.json')):
        d=json.loads(meta.read_text());
        if d['N']!=150000:continue
        result=json.loads((meta.parent/'resultados-lineales.json').read_text());root=ET.parse(meta.parent/'config.xml').getroot();source=root.find('sources')[0]
        xyz=np.array([float(source.get(k)) for k in ('x','y','z')])
        rr={r.get('name'):np.array([float(r.get(k)) for k in ('x','y','z')]) for r in root.find('recepteursp')}
        d['curves']={n:np.array(next(iter(cols.values())),float) for n,cols in result['receptores'].items()}
        assert all(len(e)==4000 and np.isfinite(e).all() and (e>=0).all() and sum(e)>0 for e in d['curves'].values())
        d['t0']={n:float(np.linalg.norm(p-xyz)/342) for n,p in rr.items()};d['path']=meta.parent
        runs.append(d)
    return runs

def main():
    runs=loadruns();assert len(runs)==40,len(runs)
    indexed={(d['variante'],d['fuente'],d['frecuencia']):d for d in runs};rows=[];diffs=[];reference=[]
    parameters={}
    for d in runs:
        for rec,e in d['curves'].items():
            k=(d['variante'],d['fuente'],d['frecuencia'],rec);parameters[k]=metrics(e,d['t0'][rec])
            rows.append({**{x:d[x] for x in ('variante','fuente','frecuencia','N','semilla')},'receptor':rec,**parameters[k]})
    csvout('indicadores.csv',rows)
    energy=['E0_20','E0_80','E80_300','E300_1000','max10ms_80_300','E60_120','max10ms_60_120','total']
    other=['C80','T30','concentracion10ms','fraccion_tardia']
    def difference(a,b):
        return {**{'delta_'+k+'_dB':db(a[k]/b[k]) if a[k]>0 and b[k]>0 else None for k in energy},**{'delta_'+k:a[k]-b[k] for k in other}}
    for row in rows:
        if row['variante']=='base':continue
        base=parameters[('base',row['fuente'],row['frecuencia'],row['receptor'])]
        diffs.append({**{k:row[k] for k in ('variante','fuente','frecuencia','receptor')},**difference(row,base)})
    csvout('diferencias.csv',diffs);store('diferencias.json',diffs)
    zones={'alta_medida':['P8','P9'],'alta_virtual':[f'V{i:02}' for i in range(1,13)],'piso':['P1','P2','P4','P7'],'bajo':['P3','P5','P6']}
    summary=[]
    for variant in ('R','C','RC','D'):
        for freq in (1000,2000,4000,8000):
            for zone,names in zones.items():
                rr=[r for r in diffs if r['variante']==variant and r['frecuencia']==freq and r['receptor'] in names]
                values={k:[r[k] for r in rr if r[k] is not None] for k in rr[0] if k.startswith('delta_')}
                summary.append(dict(variante=variant,frecuencia=freq,zona=zone,n=len(rr),**{k:float(np.mean(x)) if x else None for k,x in values.items()},min_delta_max10ms_dB=min(r['delta_max10ms_80_300_dB'] for r in rr),max_delta_max10ms_dB=max(r['delta_max10ms_80_300_dB'] for r in rr)))
    store('resumen.json',summary)
    # Quantify reference changes caused by remeshing/additional receivers.
    for freq in (1000,2000,4000,8000):
        for src in ('F1','F2'):
            old=B/'calculos'/f'base-s0.6-{src}-{freq}Hz-N150000-seed20261019'
            d=json.loads((old/'resultados-lineales.json').read_text())
            for rec,cols in d['receptores'].items():
                e=np.array(next(iter(cols.values())),float);t0=indexed[('base',src,freq)]['t0'][rec]
                oldm=metrics(e,t0);new=parameters[('base',src,freq,rec)]
                reference.append(dict(frecuencia=freq,fuente=src,receptor=rec,**difference(new,oldm)))
    csvout('control-cambio-referencia.csv',reference);store('control-cambio-referencia.json',reference)
    colors={'base':'#444444','R':'#8951b0','C':'#278b99','RC':'#ac4b5b','D':'#d69936'}
    for src in ('F1','F2'):
        fig,axs=plt.subplots(2,4,figsize=(17,7),sharex=True,sharey=True,constrained_layout=True)
        for i,rec in enumerate(('P8','P9')):
            for j,freq in enumerate((1000,2000,4000,8000)):
                ax=axs[i,j];base=indexed[('base',src,freq)];norm=np.convolve(base['curves'][rec],np.ones(10),'same').max()
                for variant in ('base','R','C','RC','D'):
                    d=indexed[(variant,src,freq)];curve=d['curves'][rec];t=((np.arange(4000)+.5)*DT-d['t0'][rec])*1000
                    ax.plot(t,10*np.log10(np.maximum(np.convolve(curve,np.ones(10),'same')/norm,1e-12)),color=colors[variant],label=variant,lw=1)
                ax.set(xlim=(0,400),ylim=(-45,3),title=f'{src} · {rec} · {freq//1000} kHz',xlabel='Retardo (ms)',ylabel='Energía 10 ms / máximo base (dB)');ax.axvline(80,color='#999',ls=':');ax.grid(alpha=.15)
        axs[0,0].legend(fontsize=8,ncol=2);fig.suptitle('Exploración localizada: 150.000 partículas, una semilla; no convergencia')
        fig.savefig(OUT/f'ecogramas-{src}.png',dpi=150);plt.close(fig)
    fig,axs=plt.subplots(1,4,figsize=(17,6),sharey=True,constrained_layout=True)
    names=['P8','P9']+[f'V{i:02}' for i in range(1,13)]
    for ax,freq in zip(axs,(1000,2000,4000,8000)):
        values=[]
        for rec in names:
            values.append([np.mean([r['delta_max10ms_80_300_dB'] for r in diffs if r['receptor']==rec and r['variante']==variant and r['frecuencia']==freq]) for variant in ('R','C','RC','D')])
        im=ax.imshow(values,cmap='RdBu_r',vmin=-2,vmax=2,aspect='auto');ax.set_xticks(range(4),['R','C','RC','D']);ax.set_yticks(range(len(names)),names);ax.set_title(f'{freq//1000} kHz');ax.set_xlabel('Condición')
    fig.colorbar(im,ax=axs,label='Cambio del máximo 10 ms (dB); media descriptiva F1/F2; negativo = menor');fig.suptitle('Distribución espacial de cambios; una semilla, escala visual ±2 dB')
    fig.savefig(OUT/'mapa-maximos.png',dpi=160);plt.close(fig)
    print('Exploración:',len(runs),'corridas;',len(rows),'indicadores;',len(diffs),'comparaciones')
    for s in summary:
        if s['zona'] in ('alta_medida','alta_virtual'):print(s['variante'],s['frecuencia'],s['zona'],'E80_300',round(s['delta_E80_300_dB'],3),'max10',round(s['delta_max10ms_80_300_dB'],3),'C80',round(s['delta_C80'],3))
    print('Control referencia: max abs cambios', {k:max(abs(r[k]) for r in reference if r[k] is not None) for k in ('delta_E0_20_dB','delta_E80_300_dB','delta_C80')})

if __name__=='__main__':main()
