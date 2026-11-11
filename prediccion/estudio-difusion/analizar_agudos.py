"""Extensión independiente a 8/16 kHz; no sobrescribe resultados históricos."""
from analizar import B, load, metric, db, DT
import numpy as np
import json, csv
import matplotlib.pyplot as plt

OUT = B/'resultados/agudos-8-16kHz'
OUT.mkdir(parents=True, exist_ok=True)

def change(a,b):
    return db(a/b) if a>0 and b>0 else None

def main():
    runs = [r for r in load() if r['frecuencia'] in (8000,16000)]
    exploration=[]; confirmation=[]
    for freq in (8000,16000):
        for src in ('F1','F2'):
            for rec in [f'P{i}' for i in range(1,10)]:
                for n,variants,target in [(150000,('lateral_Yneg','lateral_Ypos','fondo_alto'),exploration),(600000,('fondo_alto',),confirmation)]:
                    bases=sorted([r for r in runs if r['frecuencia']==freq and r['fuente']==src and r['variante']=='base' and r['N']==n],key=lambda r:r['semilla'])
                    assert len(bases)==(1 if n==150000 else 3),(freq,src,n,len(bases))
                    for variant in variants:
                        treated=sorted([r for r in runs if r['frecuencia']==freq and r['fuente']==src and r['variante']==variant and r['N']==n],key=lambda r:r['semilla'])
                        assert [r['semilla'] for r in bases]==[r['semilla'] for r in treated]
                        t0=bases[0]['t0'][rec]
                        means={v:np.mean([r['curves'][rec] for r in rr],axis=0) for v,rr in [('base',bases),('tratado',treated)]}
                        m={v:metric(e,t0) for v,e in means.items()}
                        singles=[(metric(a['curves'][rec],t0),metric(b['curves'][rec],t0)) for a,b in zip(treated,bases)]
                        row=dict(frecuencia=freq,fuente=src,receptor=rec,variante=variant,N=n,semillas=len(bases))
                        for k in ('E0_80','E80_300','E300_1000','max10ms_80_300','total'):
                            row['delta_'+k+'_dB']=change(m['tratado'][k],m['base'][k])
                            vals=[change(a[k],b[k]) for a,b in singles]
                            valid=[x for x in vals if x is not None]
                            row['min_'+k+'_dB']=min(valid) if valid else None; row['max_'+k+'_dB']=max(valid) if valid else None
                            row['n_validas_'+k]=len(valid)
                        for k in ('C80','T30','concentracion10ms','fraccion_tardia'):
                            for v in m: row[v+'_'+k]=m[v][k]
                            row['delta_'+k]=m['tratado'][k]-m['base'][k]
                        target.append(row)
    for name,rows in [('exploracion',exploration),('repeticion',confirmation)]:
        (OUT/(name+'.json')).write_text(json.dumps(rows,indent=2),encoding='utf8')
        with (OUT/(name+'.csv')).open('w',newline='',encoding='utf-8-sig') as f:
            w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    summary=[]
    for freq in (8000,16000):
        for zone,names in [('alta',['P8','P9']),('piso',['P1','P2','P4','P7']),('bajo',['P3','P5','P6'])]:
            rows=[r for r in confirmation if r['frecuencia']==freq and r['receptor'] in names]
            values={k:[r[k] for r in rows if r[k] is not None] for k in rows[0] if k.startswith('delta_')}
            summary.append(dict(frecuencia=freq,zona=zone,**{k:float(np.mean(v)) if v else None for k,v in values.items()},n_validos={k:len(v) for k,v in values.items()}))
    (OUT/'resumen.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    for freq in (8000,16000):
        fig,axs=plt.subplots(2,2,figsize=(12,7),sharex=True,sharey=True,constrained_layout=True)
        for i,rec in enumerate(('P8','P9')):
            for j,src in enumerate(('F1','F2')):
                ax=axs[i,j];selected=[r for r in runs if r['frecuencia']==freq and r['fuente']==src and r['N']==600000]
                base=np.mean([r['curves'][rec] for r in selected if r['variante']=='base'],axis=0)
                norm=np.convolve(base,np.ones(10),'same').max()
                for variant,color,label in [('base','#444444','Base'),('fondo_alto','#8054ac','Fondo: dispersión equivalente')]:
                    rr=[r for r in selected if r['variante']==variant]
                    avg=np.mean([r['curves'][rec] for r in rr],axis=0)
                    def smooth(e):return 10*np.log10(np.maximum(np.convolve(e,np.ones(10),'same')/norm,1e-12))
                    lines=np.array([smooth(r['curves'][rec]) for r in rr]);t=((np.arange(4000)+.5)*DT-rr[0]['t0'][rec])*1000
                    ax.fill_between(t,lines.min(0),lines.max(0),color=color,alpha=.12)
                    ax.plot(t,smooth(avg),color=color,label=label)
                ax.set(xlim=(0,400),ylim=(-55,3),title=f'{src} · {rec}',xlabel='Retardo respecto del directo (ms)',ylabel='Energía en 10 ms / máximo base (dB)')
                ax.axvline(80,color='#999',ls=':');ax.grid(alpha=.2)
        axs[0,0].legend(fontsize=8);fig.suptitle(f'{freq/1000:g} kHz · 600.000 partículas × 3 semillas\nSombras: rango entre realizaciones, no intervalo de confianza')
        fig.savefig(OUT/f'ecogramas-{freq}Hz.png',dpi=160);plt.close(fig)
    print('CORRIDAS NUEVAS',len(runs))
    for row in summary: print(row)
    print('POR PAR SUPERIOR')
    for r in confirmation:
        if r['receptor'] in ('P8','P9'):
            print(r['frecuencia'],r['fuente'],r['receptor'],{k:round(r[k],3) if r[k] is not None else None for k in ['delta_E80_300_dB','min_E80_300_dB','max_E80_300_dB','delta_C80','delta_max10ms_80_300_dB','delta_concentracion10ms']})

if __name__=='__main__':main()
