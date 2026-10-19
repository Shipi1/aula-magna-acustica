"""Diagnóstico exploratorio reproducible; no es una simulación acústica calibrada.

Ejecutar desde la raíz: py -B analisis/diagnosticar_platea_alta.py
Requiere numpy, soundfile y matplotlib. No altera los datos ni el informe web.
"""
from pathlib import Path
import sys, re, json, csv, hashlib, itertools
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from irlib import leer, filtro_octava, hallar_t0, schroeder
from sala import XY, FUENTES, DESCARTADAS, zona_de, distancia

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'analisis' / 'diagnostico_platea_alta'
OUT.mkdir(exist_ok=True)
BANDS = [500, 1000, 2000, 4000, 8000]
ZONES = {'piso': 'Audiencia general', 'balcon': 'Bajo balcón', 'grad': 'Platea alta (P8–P9)'}
records, curves, peaksets, manifest = [], {}, {}, []
windows = [(0,2.5),(2.5,20),(20,80),(80,300),(300,1000),(1000,1500)]

def db(v): return float(10*np.log10(max(float(v),1e-300)))
def savecsv(name, rows):
    if not rows: return
    with (OUT/name).open('w', newline='', encoding='utf-8-sig') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

for src, cfg in FUENTES.items():
    for p in sorted(Path(cfg['carpeta_ir']).glob('*.wav')):
        ident = '-'.join(re.search(r'(F\d)\s*-?\s*(P\d)',p.name).groups())
        raw, sr = leer(p); peak, t0 = hallar_t0(raw)
        manifest.append({'path':str(p.relative_to(ROOT)), 'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
                         'source':src,'id':ident,'excluded':ident in DESCARTADAS[src],
                         'sr':sr,'frames':len(raw),'t0_sample':int(t0),'peak_sample':int(peak)})
        if ident in DESCARTADAS[src]: continue
        for fc in BANDS:
            x = filtro_octava(raw,sr,fc)
            _,noise,cross=schroeder(x[t0:]**2,sr,truncar=True)
            # Mismo horizonte en todas las mediciones; señal y energía en unidades digitales.
            a=max(0,t0-int(.0005*sr)); stop=min(t0+int(1.5*sr),t0+cross,len(x))
            e=np.maximum(x*x-noise,0)
            def energy(lo,hi):
                aa=max(a,t0+round(lo*sr/1000));bb=min(stop,t0+round(hi*sr/1000))
                return float(e[aa:bb].sum()) if bb>aa else 0.
            total=energy(0,1500); early=energy(0,80);late=energy(80,1500)
            row={'source':src,'id':ident,'zone':zona_de(ident),'hz':fc,
                 'distance_m':distancia(ident),'noise_power':float(noise),
                 'integration_end_s':(stop-t0)/sr,'C80_common_horizon_db':db(early/late),
                 'late80_1500_pct':100*late/(early+late),
                 'late80_300_over_20_80_db':db(energy(80,300)/energy(20,80)),
                 'late300_1000_over_80_300_db':db(energy(300,1000)/energy(80,300)),
                 'E_direct_digital_db':db(energy(-.5,2.5)),
                 'E_late_digital_db':db(energy(80,1000)),
                 'E_direct_distance_corrected_db':db(energy(-.5,2.5)*distancia(ident)**2),
                 'E_late_distance_corrected_db':db(energy(80,1000)*distancia(ident)**2)}
            for lo,hi in windows:row[f'pct_{lo:g}_{hi:g}ms']=100*energy(lo,hi)/total
            for hi in [1,3,5]:row[f'direct_to_late_{hi}ms_db']=db(energy(-.5,hi)/energy(80,1000))
            records.append(row)
            w=round(.0005*sr); bins=[]
            for i in range(2000):
                aa=t0+i*w;bb=min(aa+w,stop)
                bins.append(float(e[aa:bb].sum()) if aa<stop else 0.)
            b=np.array(bins)
            curves[(src,ident,fc)]=b/max(total,1e-300)
            if ident.endswith(('P8','P9')):
                # Picos sobre energía suavizada 1,5 ms; banda y fuente siempre explícitas.
                smooth=np.convolve(b,np.ones(3)/3,'same')
                direct=max(smooth[:5]); peaks=[]
                for i in range(10,599):
                    if smooth[i]>smooth[i-1] and smooth[i]>=smooth[i+1]:
                        bg=np.median(smooth[max(6,i-10):i+11]); prom=db(smooth[i]/max(bg,1e-300))
                        if prom>=2.5:
                            peaks.append({'time_ms':i*.5+.25,'relative_direct_db':db(smooth[i]/direct),
                                          'prominence_db':prom})
                peaksets[(src,ident,fc)]=peaks
        print(src,ident,flush=True)

savecsv('energia_por_ventanas.csv',records)
(OUT/'inventario_wav.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
peakrows=[dict(source=s,id=i,hz=f,**p) for (s,i,f),ps in peaksets.items() for p in ps]
savecsv('picos_platea_alta.csv',peakrows)

# Contraste geométrico: planos nominales del modelo, con validación de visibilidad.
geom=json.loads((ROOT/'modelo-3d/geometria.json').read_text(encoding='utf8'))
verts=np.array(geom['vertices']);faces=np.array([f['v'] for f in geom['faces']])
tri=verts[faces];v0=tri[:,0];edge1=tri[:,1]-v0;edge2=tri[:,2]-v0
planes={'lateral_negativo':(1,-11.665),'lateral_positivo':(1,11.665),
        'fondo_escenario':(0,0.),'fondo_sala':(0,40.25),'cielo_modelo':(2,13.32)}

def hits(a,b):
    direction=b-a;h=np.cross(np.broadcast_to(direction,edge2.shape),edge2)
    det=np.einsum('ij,ij->i',edge1,h);valid=np.abs(det)>1e-9
    inv=np.zeros_like(det);inv[valid]=1/det[valid]
    s=a-v0;u=inv*np.einsum('ij,ij->i',s,h);q=np.cross(s,edge1)
    v=inv*np.einsum('j,ij->i',direction,q);t=inv*np.einsum('ij,ij->i',edge2,q)
    mask=valid&(u>=-1e-6)&(v>=-1e-6)&(u+v<=1+1e-6)&(t>=-1e-6)&(t<=1+1e-6)
    return t[mask]

def reflect(p,plane):
    q=p.copy();axis,value=plane;q[axis]=2*value-q[axis];return q

def path_for(s,r,seq,ps=planes):
    images=[s]
    for name in seq:images.append(reflect(images[-1],ps[name]))
    current=r.copy();back=[]
    for j in range(len(seq)-1,-1,-1):
        axis,value=ps[seq[j]];vec=images[j+1]-current
        if abs(vec[axis])<1e-9:return None,'sin_interseccion'
        t=(value-current[axis])/vec[axis]
        if not 0<t<1:return None,'orden_no_fisico'
        b=current+t*vec;back.append(b);current=b
    pts=[s]+list(reversed(back))+[r]
    for a,b in zip(pts,pts[1:]):
        ts=hits(a,b)
        if np.any((ts>1e-5)&(ts<1-1e-5)):return pts,'obstruido'
    # Cada rebote debe pertenecer a la frontera real, no a la extensión infinita del plano.
    for b in pts[1:-1]:
        eps=np.array([.013,.017,.019]);ts=hits(b-eps,b+eps)
        if not np.any(np.abs(ts-.5)<.002):return pts,'fuera_de_superficie'
    return pts,'visible'

paths=[]
for fid,rid in itertools.product(['F1','F2'],['P8','P9']):
    ident=f'{fid}-{rid}';s=np.array(XY[fid][:3]);r=np.array(XY[rid][:3]);direct=np.linalg.norm(r-s)
    assert not np.any((hits(s,r)>1e-5)&(hits(s,r)<1-1e-5)),f'Directo obstruido: {ident}'
    for n in [1,2]:
        for seq in itertools.product(planes,repeat=n):
            if n==2 and seq[0]==seq[1]:continue
            image=s.copy()
            for name in seq:image=reflect(image,planes[name])
            delay=(np.linalg.norm(image-r)-direct)/342*1000
            if delay<=0:continue
            pts,status=path_for(s,r,seq)
            row={'id':ident,'order':n,'surfaces':' > '.join(seq),'delay_ms':float(delay),'visibility':status,
                 'bounce_xyz':json.dumps([p.tolist() for p in pts[1:-1]]) if pts else '[]'}
            for src in ['Parlante','Globo']:
                ps=peaksets[(src,ident,2000)]
                near=min(ps,key=lambda p:abs(p['time_ms']-delay)) if ps else None
                row[f'{src}_nearest_peak_ms']=near['time_ms'] if near else None
                row[f'{src}_error_ms']=abs(near['time_ms']-delay) if near else None
                row[f'{src}_peak_level_db']=near['relative_direct_db'] if near else None
            paths.append(row)
savecsv('recorridos_geometricos.csv',paths)

# Sensibilidad de tiempos, no validación de visibilidad en las geometrías perturbadas.
rng=np.random.default_rng(20261019);sensitivity=[]
for row in paths:
    if row['visibility']!='visible':continue
    fid,rid=row['id'].split('-');seq=row['surfaces'].split(' > ');delays=[]
    for k in range(400):
        s=np.array(XY[fid][:3])+rng.uniform(-.3,.3,3)
        r=np.array(XY[rid][:3])+rng.uniform(-.3,.3,3);r[2]+=rng.uniform(-.4,.4)
        ps={name:(axis,value) for name,(axis,value) in planes.items()}
        for name in ['lateral_negativo','lateral_positivo']:ps[name]=(1,ps[name][1]+rng.uniform(-.3,.3))
        ps['fondo_sala']=(0,40.25+rng.uniform(-1,1));ps['fondo_escenario']=(0,rng.uniform(-.3,.3))
        ps['cielo_modelo']=(2,rng.uniform(9.5,13.32))
        image=s.copy()
        for name in seq:image=reflect(image,ps[name])
        delays.append((np.linalg.norm(image-r)-np.linalg.norm(s-r))/rng.uniform(340,345)*1000)
    sensitivity.append(dict(id=row['id'],surfaces=row['surfaces'],nominal_ms=row['delay_ms'],
                            p05_ms=float(np.quantile(delays,.05)),p95_ms=float(np.quantile(delays,.95))))
savecsv('sensibilidad_retardos.csv',sensitivity)

# Resúmenes: medias de proporciones por toma; no mezcla de energías de globos distintos.
summary=[]
for src,z,fc in itertools.product(FUENTES,ZONES,BANDS):
    rr=[r for r in records if r['source']==src and r['zone']==z and r['hz']==fc]
    keys=[k for k in rr[0] if isinstance(rr[0][k],(float,int)) and k not in ['hz']]
    summary.append(dict(source=src,zone=z,hz=fc,n=len(rr),**{k:float(np.mean([r[k] for r in rr])) for k in keys}))
savecsv('resumen_zonas.csv',summary)

plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
colors={'piso':'#237c9a','balcon':'#ce8c30','grad':'#a64b77'}
fig,axs=plt.subplots(2,2,figsize=(12,8),sharex=True,sharey=True)
for ax,(src,fc) in zip(axs.flat,itertools.product(FUENTES,[2000,4000])):
    for z in ZONES:
        cc=[c for (s,i,f),c in curves.items() if s==src and f==fc and zona_de(i)==z]
        # Integración inversa con horizonte común 1 s para comparación gráfica, no ajuste T30.
        c=np.mean(cc,axis=0);dec=np.cumsum(c[::-1])[::-1];dec=10*np.log10(np.maximum(dec/dec[0],1e-8))
        ax.plot(np.arange(len(c))*.5,dec,label=ZONES[z],color=colors[z])
    ax.set(title=f'{src} · {fc/1000:g} kHz',xlim=(0,800),ylim=(-35,0),xlabel='Tiempo desde llegada inicial [ms]',ylabel='Energía restante relativa [dB]')
    ax.axvline(80,color='gray',ls=':',lw=1);ax.grid(alpha=.2)
axs[0,0].legend(fontsize=8);fig.suptitle('Decaimiento normalizado por zona · integración hasta 1 s\nNo representa niveles absolutos ni atribuye superficies')
fig.tight_layout();fig.savefig(OUT/'decaimientos_zonas.png',dpi=180);plt.close(fig)

fig,axs=plt.subplots(2,2,figsize=(13,8),sharex=True,sharey=True)
for ax,ident in zip(axs.flat,['F1-P8','F1-P9','F2-P8','F2-P9']):
    for src,col in [('Parlante','#237c9a'),('Globo','#ce8c30')]:
        c=curves[(src,ident,2000)];c=np.convolve(c,np.ones(3)/3,'same')
        ax.plot(np.arange(len(c))*.5+.25,10*np.log10(np.maximum(c/max(c[:5]),1e-8)),lw=.8,color=col,label=src)
    pp=[p for p in paths if p['id']==ident and p['order']==1 and p['visibility']=='visible']
    for p in pp:
        ax.axvline(p['delay_ms'],color='gray',alpha=.5,lw=.8)
        ax.text(p['delay_ms'],3,p['surfaces'].replace('lateral_','lat. ').replace('fondo_','f. '),rotation=90,va='top',fontsize=6)
    ax.axvspan(80,150,color='#a64b77',alpha=.06);ax.set(title=ident,xlim=(0,150),ylim=(-35,5),xlabel='Retardo relativo [ms]',ylabel='Energía de ventana / llegada inicial [dB]');ax.grid(alpha=.2)
axs[0,0].legend();fig.suptitle('Platea alta · ETC suavizada 1,5 ms · octava de 2 kHz\nLíneas: primer orden visible en geometría nominal; coincidencia temporal no prueba causalidad')
fig.tight_layout();fig.savefig(OUT/'etc_geometria_2khz.png',dpi=180);plt.close(fig)

fig,axs=plt.subplots(1,2,figsize=(12,5),sharey=True)
for ax,src in zip(axs,FUENTES):
    bottom=np.zeros(3)
    for j,(lo,hi) in enumerate(windows):
        vals=[np.mean([r[f'pct_{lo:g}_{hi:g}ms'] for r in records if r['source']==src and r['zone']==z and r['hz'] in [1000,2000,4000]]) for z in ZONES]
        ax.bar(range(3),vals,bottom=bottom,label=f'{lo:g}–{hi:g} ms');bottom+=vals
    ax.set_xticks(range(3),['Audiencia\ngeneral','Bajo\nbalcón','Platea alta\nP8–P9']);ax.set(title=src,ylabel='Proporción de energía [%]',ylim=(0,100));ax.grid(axis='y',alpha=.2)
axs[1].legend(bbox_to_anchor=(1.02,1),loc='upper left',fontsize=8)
fig.suptitle('Distribución temporal · media de octavas 1, 2 y 4 kHz\nCada toma se normaliza por su propia energía; no compara nivel entre fuentes')
fig.tight_layout();fig.savefig(OUT/'energia_ventanas.png',dpi=180);plt.close(fig)

fig,axs=plt.subplots(1,2,figsize=(13,5))
for ax,projection in zip(axs,[(0,1),(0,2)]):
    a,b=projection
    for p in paths:
        if p['id']!='F2-P8' or p['visibility']!='visible' or p['order']!=1:continue
        pts=np.array([XY['F2'][:3]]+json.loads(p['bounce_xyz'])+[XY['P8'][:3]])
        ax.plot(pts[:,a],pts[:,b],marker='.',label=f"{p['surfaces']} · {p['delay_ms']:.1f} ms")
    ax.scatter([XY[k][a] for k in ['F2','P8']],[XY[k][b] for k in ['F2','P8']],c='black',zorder=5)
    for k in ['F2','P8']:ax.annotate(k,(XY[k][a],XY[k][b]),xytext=(4,4),textcoords='offset points')
    ax.set(xlabel='X [m]',ylabel=('Y [m]' if b==1 else 'Z [m]'));ax.grid(alpha=.2);ax.legend(fontsize=7)
axs[0].set_title('Planta · recorridos nominales de primer orden');axs[1].set_title('Proyección lateral · cielo horizontal simplificado')
fig.suptitle('Recorridos candidatos F2 → P8 · no se representan amplitudes acústicas')
fig.tight_layout();fig.savefig(OUT/'recorridos_f2_p8.png',dpi=180);plt.close(fig)

fig,axs=plt.subplots(1,2,figsize=(13,5))
latefamilies=['lateral_positivo > lateral_negativo','cielo_modelo > fondo_sala']
for ax,(a,b) in zip(axs,[(0,1),(0,2)]):
    for p in paths:
        if p['id']!='F1-P9' or p['surfaces'] not in latefamilies:continue
        pts=np.array([XY['F1'][:3]]+json.loads(p['bounce_xyz'])+[XY['P9'][:3]])
        ax.plot(pts[:,a],pts[:,b],marker='o',ms=3,label=f"{p['surfaces']} · {p['delay_ms']:.1f} ms")
    for k in ['F1','P9']:
        ax.scatter(XY[k][a],XY[k][b],c='black',s=20,zorder=5)
        ax.annotate(k,(XY[k][a],XY[k][b]),xytext=(4,4),textcoords='offset points')
    if b==1:
        ax.plot([0,40.25,40.25,0,0],[-11.665,-11.665,11.665,11.665,-11.665],color='gray',lw=.8)
    else:
        center=verts[np.isclose(verts[:,1],0)]
        ax.plot(center[:,0],center[:,2],color='gray',lw=.8,label='Sección nominal del volumen de aire')
        p=next(p for p in paths if p['id']=='F1-P9' and p['surfaces']=='fondo_sala')
        pts=np.array([XY['F1'][:3]]+json.loads(p['bounce_xyz'])+[XY['P9'][:3]])
        ax.plot(pts[:,a],pts[:,b],ls='--',color='#a44c4c',lw=1,label='Retorno posterior simple: obstruido')
    ax.set(xlabel='X [m]',ylabel=('Y [m]' if b==1 else 'Z [m]'));ax.grid(alpha=.2);ax.legend(fontsize=7,loc='upper left')
axs[0].set_title('Planta');axs[1].set_title('Proyección lateral')
fig.suptitle('Dos familias de recorridos tardíos posibles · F1 → P9\nGeometría nominal: no prueba identificación ni predice amplitud')
fig.tight_layout();fig.savefig(OUT/'recorridos_tardios.png',dpi=180);plt.close(fig)

# Comprobaciones de consistencia de las nuevas tablas.
assert len(manifest)==36 and len(records)==34*len(BANDS)
for row in records:
    assert abs(sum(row[f'pct_{lo:g}_{hi:g}ms'] for lo,hi in windows)-100)<1e-6
    assert abs(row['late80_1500_pct']-100/(1+10**(row['C80_common_horizon_db']/10)))<1e-6
    assert row['integration_end_s']>.3
for p in paths:
    if p['visibility']=='visible':
        assert json.loads(p['bounce_xyz'])
print('Controles: 36 WAV inventariados, 34 útiles, proporciones y C80 consistentes, directo visible en los cuatro pares altos.')

print('OUTPUT',OUT)
for src in FUENTES:
    print('\n',src)
    for z in ZONES:
        rr=[r for r in records if r['source']==src and r['zone']==z and r['hz'] in [1000,2000,4000]]
        print(z,{k:round(float(np.mean([r[k] for r in rr])),2) for k in ['late80_1500_pct','direct_to_late_3ms_db','late80_300_over_20_80_db','late300_1000_over_80_300_db']})
print('\nVISIBLE PATHS F2-P8')
for p in paths:
    if p['id']=='F2-P8' and p['visibility']=='visible':print(p['surfaces'],round(p['delay_ms'],2))
