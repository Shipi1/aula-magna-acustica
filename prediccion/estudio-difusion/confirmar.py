"""Resumen sobre respuesta media lineal de tres semillas a 2 kHz, N=600.000."""
from analizar import B,OUT,load,metric,db,win,DT
import numpy as np,json,csv
import matplotlib.pyplot as plt

def main():
    runs=[r for r in load() if r['N']==600000 and r['frecuencia']==2000]
    rows=[];mean_curves={}
    for source in ['F1','F2']:
        for receiver in [f'P{i}' for i in range(1,10)]:
            selected={v:sorted([r for r in runs if r['variante']==v and r['fuente']==source],key=lambda r:r['semilla']) for v in ['base','fondo_alto']}
            assert all(len(rr)==3 for rr in selected.values()),'Esperar las tres semillas de cada condición'
            averages={v:np.mean([r['curves'][receiver] for r in rr],axis=0) for v,rr in selected.items()}
            t0=selected['base'][0]['t0'][receiver]; params={v:metric(e,t0) for v,e in averages.items()}
            mean_curves[(source,receiver)]={'t0':t0,**averages}
            row={'fuente':source,'receptor':receiver,'N_por_semilla':600000,'semillas':3}
            for k in ['total','E0_20','E0_80','E80_300','E300_1000','max10ms_80_300']:
                row['delta_'+k+'_dB']=db(params['fondo_alto'][k]/params['base'][k])
                ds=[db(metric(a['curves'][receiver],t0)[k]/metric(b['curves'][receiver],t0)[k]) for a,b in zip(selected['fondo_alto'],selected['base'])]
                row['min_semilla_'+k+'_dB']=min(ds);row['max_semilla_'+k+'_dB']=max(ds)
            for k in ['C80','T30','fraccion_tardia','concentracion10ms']:
                row['base_'+k]=params['base'][k];row['tratado_'+k]=params['fondo_alto'][k];row['delta_'+k]=params['fondo_alto'][k]-params['base'][k]
            rows.append(row)
    (OUT/'confirmacion-2kHz.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
    np.savez_compressed(OUT/'respuestas-medias-2kHz.npz',**{f'{src}_{rec}_{v}':d[v] for (src,rec),d in mean_curves.items() for v in ['base','fondo_alto']})
    fig,axs=plt.subplots(2,2,figsize=(12,7),sharex=True,sharey=True,constrained_layout=True)
    for row,receiver in enumerate(['P8','P9']):
        for col,source in enumerate(['F1','F2']):
            ax=axs[row,col];d=mean_curves[(source,receiver)]
            normal=np.convolve(d['base'],np.ones(10),'same').max()
            for variant,color,label in [('base','#444444','Base'),('fondo_alto','#8054ac','Fondo alto: s = 0,60')]:
                def smooth(e):return 10*np.log10(np.maximum(np.convolve(e,np.ones(10),'same')/normal,1e-12))
                curves=np.array([smooth(r['curves'][receiver]) for r in runs if r['fuente']==source and r['variante']==variant])
                t=((np.arange(4000)+.5)*DT-d['t0'])*1000
                ax.fill_between(t,curves.min(0),curves.max(0),color=color,alpha=.12)
                ax.plot(t,smooth(d[variant]),color=color,label=label,lw=1.2)
            ax.set_xlim(0,500);ax.set_ylim(-35,3);ax.axvline(80,color='#999',ls=':',lw=1);ax.set_title(f'{source} · {receiver} · 2 kHz');ax.grid(alpha=.15);ax.set_xlabel('Retardo respecto del directo (ms)');ax.set_ylabel('Energía en 10 ms / máximo base (dB)')
    axs[0,0].legend(fontsize=9);fig.suptitle('Media energética de 3 semillas × 600.000 partículas\nSombras: rango entre realizaciones; no intervalo de confianza',fontsize=11)
    fig.savefig(OUT/'confirmacion-ecogramas-2kHz.png',dpi=160);plt.close(fig)
    fig,axs=plt.subplots(1,3,figsize=(13,4),constrained_layout=True)
    names=[(s,p) for s in ['F1','F2'] for p in ['P8','P9']]
    for ax,k,title in zip(axs,['E0_80','E80_300','max10ms_80_300'],['Energía 0–80 ms','Energía 80–300 ms','Máxima energía en 10 ms (80–300 ms)']):
        data=[next(r for r in rows if (r['fuente'],r['receptor'])==name) for name in names]
        means=np.array([r['delta_'+k+'_dB'] for r in data]);lo=np.array([r['min_semilla_'+k+'_dB'] for r in data]);hi=np.array([r['max_semilla_'+k+'_dB'] for r in data])
        x=np.arange(4);ax.vlines(x,lo,hi,color='#777',lw=2,label='Rango entre semillas');ax.scatter(x,means,c='#8054ac',s=45,zorder=3,label='Cambio sobre media energética');ax.axhline(0,color='#777',lw=.8);ax.set_xticks(x,[f'{s}\n{p}' for s,p in names]);ax.set_title(title,fontsize=10);ax.set_ylabel('Tratamiento − base (dB)');ax.grid(axis='y',alpha=.2)
    axs[0].legend(fontsize=7);fig.savefig(OUT/'confirmacion-cambios-2kHz.png',dpi=160);plt.close(fig)
    for r in rows:
        if r['receptor'] in ['P8','P9']:print(r['fuente'],r['receptor'],'late',round(r['delta_E80_300_dB'],3),'range',round(r['min_semilla_E80_300_dB'],3),round(r['max_semilla_E80_300_dB'],3),'C80',round(r['delta_C80'],3),'max10',round(r['delta_max10ms_80_300_dB'],3))

if __name__=='__main__':main()
