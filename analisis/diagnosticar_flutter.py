"""Exploración de periodicidad en envolventes; no clasificador validado de flutter."""
from pathlib import Path
import re,csv,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sala import FUENTES,DESCARTADAS,zona_de
from irlib import leer,filtro_octava,hallar_t0

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analisis/diagnostico_platea_alta'
rows=[];curves={};signals={}
for src,cfg in FUENTES.items():
    for path in sorted(Path(cfg['carpeta_ir']).glob('*.wav')):
        ident='-'.join(re.search(r'(F\d)\s*-?\s*(P\d)',path.name).groups())
        if ident in DESCARTADAS[src]:continue
        raw,sr=leer(path);_,t0=hallar_t0(raw)
        for fc in [2000,4000,8000]:
            x=filtro_octava(raw,sr,fc)[t0:t0+int(.7*sr)]
            w=round(.001*sr);e=(x[:len(x)//w*w]**2).reshape(-1,w).mean(axis=1)
            # Normalización local elimina la pendiente de decaimiento sin alinear picos.
            pad=np.pad(e,(10,10),mode='edge');trend=np.convolve(pad,np.ones(21)/21,'valid')
            q=e/np.maximum(trend,1e-30)-1
            r=q[40:650];acs=[]
            for lag in range(20,181):
                a,b=r[:-lag],r[lag:];acs.append(float(np.corrcoef(a,b)[0,1]))
            ac=np.array(acs);curves[src,ident,fc]=ac
            if ident.endswith(('P8','P9')):signals[src,ident,fc]=10*np.log10(np.maximum(e/e[:3].max(),1e-12))
            order=np.argsort(ac)[::-1];selected=[]
            for j in order:
                lag=int(j+20)
                if all(abs(lag-t)>5 for t in selected):selected.append(lag)
                if len(selected)==3:break
            rows.append(dict(source=src,id=ident,zone=zona_de(ident),hz=fc,
                             best_lag_ms=selected[0],best_r=float(ac[selected[0]-20]),
                             second_lag_ms=selected[1],second_r=float(ac[selected[1]-20]),
                             r68=float(ac[68-20]),r136=float(ac[136-20])))
    print(src,'terminado',flush=True)
with (OUT/'periodicidad_flutter.csv').open('w',newline='',encoding='utf-8-sig') as f:
    wr=csv.DictWriter(f,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)
fig,axs=plt.subplots(2,3,figsize=(13,7),sharex=True,sharey=True)
colors={'piso':'#237c9a','balcon':'#ce8c30','grad':'#a64b77'}
for ax,(src,fc) in zip(axs.flat,[(s,f) for s in FUENTES for f in [2000,4000,8000]]):
    for z in colors:
        a=np.array([v for (s,i,f),v in curves.items() if s==src and f==fc and zona_de(i)==z])
        ax.plot(range(20,181),np.mean(a,axis=0),color=colors[z],label={'piso':'Piso','balcon':'Bajo balcón','grad':'P8–P9'}[z])
    ax.axvline(136.43,color='gray',ls=':',lw=1);ax.axvline(68.22,color='gray',ls=':',lw=1)
    ax.set(title=f'{src} · {fc//1000} kHz',xlabel='Separación entre repeticiones [ms]',ylabel='Correlación media',ylim=(-.2,.4));ax.grid(alpha=.2)
axs[0,0].legend(fontsize=8)
fig.suptitle('Búsqueda exploratoria de periodicidad · energía en ventanas de 1 ms\nCola 40–650 ms, normalización local de 21 ms; líneas: W/c y 2W/c con W=23,33 m')
fig.tight_layout();fig.savefig(OUT/'periodicidad_flutter.png',dpi=170);plt.close(fig)
fig,axs=plt.subplots(2,2,figsize=(12,7),sharex=True,sharey=True)
for ax,ident in zip(axs.flat,['F1-P8','F1-P9','F2-P8','F2-P9']):
    for src,col in [('Parlante','#237c9a'),('Globo','#ce8c30')]:
        a=np.mean([signals[src,ident,f] for f in [2000,4000,8000]],axis=0)
        ax.plot(np.arange(len(a))+.5,a,color=col,lw=.7,label=src)
    ax.set(title=ident,xlim=(0,650),ylim=(-50,5),xlabel='Tiempo desde llegada inicial [ms]',ylabel='Media de niveles relativos [dB]');ax.grid(alpha=.2)
axs[0,0].legend()
fig.suptitle('Colas en P8–P9 · media de niveles de octavas 2, 4 y 8 kHz\nReferencia independiente por toma y banda; no son niveles SPL')
fig.tight_layout();fig.savefig(OUT/'colas_agudos.png',dpi=170);plt.close(fig)
for src in FUENTES:
    for fc in [2000,4000,8000]:
        rr=[r for r in rows if r['source']==src and r['hz']==fc and r['zone']=='grad']
        a=np.mean([curves[src,r['id'],fc] for r in rr],axis=0);j=np.argmax(a)
        print(src,fc,'P8-P9 pico media',j+20,round(float(a[j]),3),'individuales',[(r['id'],r['best_lag_ms'],round(r['best_r'],2)) for r in rr])
assert len(rows)==34*3
