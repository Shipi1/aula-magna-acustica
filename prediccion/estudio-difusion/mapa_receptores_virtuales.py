"""Mapa de los doce receptores realmente usados y su superficie de apoyo."""
from pathlib import Path
import json,csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

B=Path(__file__).resolve().parent;OUT=B/'reflectores/resultados'
MODEL=json.loads((B/'malla-base.json').read_text());v=np.array(MODEL['vertices'])
tri=v[np.array([f['v'] for f in MODEL['faces']])];mats=np.array([f['idMat'] for f in MODEL['faces']])
virtual=json.loads((B/'absorcion-posterior/receptores-virtuales.json').read_text())
audit=json.loads((B/'reflectores/auditoria-posiciones.json').read_text())

def support(p):
    a=tri[:,0,:2];u=tri[:,1,:2]-a;w=tri[:,2,:2]-a;q=np.array([p['x'],p['y']])-a
    det=u[:,0]*w[:,1]-u[:,1]*w[:,0];valid=abs(det)>1e-9;safe=np.where(valid,det,1.)
    s=(q[:,0]*w[:,1]-q[:,1]*w[:,0])/safe;t=(u[:,0]*q[:,1]-u[:,1]*q[:,0])/safe
    z=tri[:,0,2]+s*(tri[:,1,2]-tri[:,0,2])+t*(tri[:,2,2]-tri[:,0,2])
    mask=valid&(s>=-1e-6)&(t>=-1e-6)&(s+t<=1+1e-6)&(abs(z-p['piso_z_m'])<1e-4)&np.isin(mats,[110,112,113])
    ids=sorted(set(map(int,mats[mask])));assert len(ids)==1,(p,ids)
    return ids[0]

rows=[]
for p in virtual:
    assert np.allclose([p[k] for k in ('x','y','z')],audit['receptores'][p['nombre']],atol=1e-7)
    assert abs(p['z']-p['piso_z_m']-2)<1e-6
    mat=support(p)
    rows.append(dict(punto=p['nombre'],X_m=p['x'],Y_m=p['y'],Z_global_m=p['z'],piso_Z_m=p['piso_z_m'],altura_sobre_piso_m=2.,id_material_apoyo=mat,
        superficie_modelada='Butacas' if mat==113 else 'Madera expuesta',medicion_real=False))
assert len(rows)==12 and sum(r['id_material_apoyo']==113 for r in rows)==8
(OUT/'ubicacion-receptores-virtuales.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf8')
with (OUT/'ubicacion-receptores-virtuales.csv').open('w',encoding='utf-8-sig',newline='') as fp:
    w=csv.DictWriter(fp,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

projected=np.abs(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0])[:,2])>1e-7
floors=np.flatnonzero(projected&np.isin(mats,[110,111,112,113]));floors=floors[np.argsort(tri[floors,:,2].mean(axis=1))]
def background(ax):
    colors=[]
    for i in floors:
        high=tri[i,:,2].mean()>3.5
        if mats[i]==111:c='#ecd7c3'
        elif not high:c='#ededed'
        elif mats[i]==113:c='#c6e5e9'
        elif mats[i]==112:c='#eee1ba'
        else:c='#d6d8dc'
        colors.append(c)
    ax.add_collection(PolyCollection(tri[floors,:,:2],facecolors=colors,edgecolors='none',alpha=1))
    ax.grid(alpha=.2,zorder=0);ax.set_aspect('equal');ax.set_xlabel('X del modelo (m) · del escenario hacia el fondo');ax.set_ylabel('Y del modelo (m)')

fig,axs=plt.subplots(1,2,figsize=(16,8),gridspec_kw={'width_ratios':[1.5,1]},constrained_layout=True)
for ax in axs:
    background(ax)
    for x in (26,31,36):ax.axvline(x,color='#97a2a9',lw=.8,ls=':',zorder=1)
    for r in rows:
        x,y=r['X_m'],r['Y_m'];symbol='o' if r['id_material_apoyo']==113 else 'D'
        ax.scatter(x,y,s=65,marker=symbol,color='#176b9a',edgecolor='white',linewidth=.9,zorder=5)
        dx,dy=(.35,.4)
        if ax is axs[0] and r['punto'] in ('V01','V04'):dx=-2.;dy=-.9 if y<0 else .6
        if ax is axs[1] and r['punto']=='V01':dy=-.9
        ax.annotate(r['punto'],(x,y),xytext=(x+dx,y+dy),fontsize=10,color='#104b70',fontweight='bold',zorder=6,
                    bbox=dict(facecolor='white',alpha=.65,edgecolor='none',pad=.5))
    for name in ('P8','P9'):
        p=audit['receptores'][name]
        ax.scatter(p[0],p[1],s=130,marker='*',color='#b84436',edgecolor='white',linewidth=.7,zorder=7)
        ax.annotate(name,(p[0],p[1]),xytext=(p[0]+1.,p[1]+(.45 if name=='P8' else -.8)),color='#9d3328',fontweight='bold',fontsize=10,zorder=8,
                    arrowprops=dict(arrowstyle='-',color='#b84436',lw=.7))
    ax.set_ylim(-12.4,12.4)
axs[0].set_xlim(-.5,41.3);axs[0].set_title('Sala completa · fuentes y puntos de control',fontsize=13)
for name,p in audit['fuentes'].items():
    axs[0].scatter(p[0],p[1],s=110,marker='^',color='#2c3035',edgecolor='white',zorder=7)
    axs[0].text(p[0]+.8,p[1]+.2,name,fontsize=11,fontweight='bold')
axs[0].text(4.3,-6.5,'ESCENARIO',fontsize=10,color='#805e40',ha='center')
axs[0].annotate('Hacia el fondo',(39.7,-11.7),(28,-11.7),arrowprops=dict(arrowstyle='->',color='#666'),va='center',fontsize=9,color='#555')
axs[1].set_xlim(23.8,40.8);axs[1].set_title('Detalle de la zona alta · misma orientación',fontsize=13)
for x,label in [(26,'Delantera'),(31,'Intermedia'),(36,'Posterior')]:
    axs[1].text(x,11.4,label,ha='center',fontsize=9,color='#444',bbox=dict(facecolor='white',edgecolor='none',alpha=.8))
legend=[Line2D([],[],marker='o',ls='',color='#176b9a',markersize=8,label='Virtual sobre bloque de butacas'),
        Line2D([],[],marker='D',ls='',color='#176b9a',markersize=7,label='Virtual sobre madera expuesta'),
        Line2D([],[],marker='*',ls='',color='#b84436',markersize=12,label='P8/P9: posiciones del estudio real'),
        Line2D([],[],marker='^',ls='',color='#2c3035',markersize=9,label='F1/F2: fuentes del estudio'),
        Patch(facecolor='#c6e5e9',label='Superficie de butacas altas del modelo'),
        Patch(facecolor='#d6d8dc',label='Madera expuesta alta del modelo'),
        Patch(facecolor='#eee1ba',label='Alfombra alta del modelo'),
        Patch(facecolor='#ededed',label='Pisos inferiores en proyección')]
axs[0].legend(handles=legend,loc='upper center',bbox_to_anchor=(.5,-.16),ncol=2,fontsize=9,frameon=False)
fig.suptitle('12 receptores virtuales × 2 fuentes independientes = 24 combinaciones\nVista en planta del modelo · todos los virtuales a 2 m sobre su piso local',fontsize=16)
fig.savefig(OUT/'mapa-receptores-virtuales.png',dpi=180,bbox_inches='tight')
fig.savefig(OUT/'mapa-receptores-virtuales.svg',bbox_inches='tight');plt.close(fig)

root=B.parents[1]
text=['# Mapa de los receptores virtuales de la platea alta',
    '**Fecha:** 9 de noviembre de 2026. Las posiciones corresponden a las utilizadas en los cálculos existentes; no se cambiaron receptores ni se ejecutaron nuevas predicciones.',
    '## Cómo se obtienen las 24 combinaciones',
    'Son **12 posiciones virtuales, V01–V12, calculadas una vez con F1 y otra con F2**. Por ejemplo, F1–V02 y F2–V02 son dos respuestas del mismo punto con distinta fuente. Las fuentes se calculan por separado. No son 24 ubicaciones ni fuentes actuando simultáneamente.',
    'Los doce virtuales complementan P1–P9. Cada corrida contiene **21 receptores**; para el análisis espacial alto se usan P8/P9 y los doce virtuales. P8/P9 son posiciones del estudio real y no forman parte del conteo de doce virtuales.',
    '![Mapa de receptores](../prediccion/estudio-difusion/reflectores/resultados/mapa-receptores-virtuales.png)',
    'El fondo del mapa procede de las superficies del modelo nativo. Es una proyección en planta: las superficies superiores pueden ocultar en ella las inferiores. La vista de detalle conserva la orientación de la sala completa. El escenario está a la izquierda y el fondo a la derecha.',
    '## Distribución',
    'La cuadrícula tiene tres franjas longitudinales y cuatro posiciones transversales. X aumenta del escenario hacia el fondo; los valores son coordenadas del modelo, no distancias medidas desde el borde del escenario. Y negativo corresponde al lado de P8 y Y positivo al de P9.',
    '| Franja | Y = −9 m | Y = −3 m | Y = +3 m | Y = +9 m |',
    '|---|---|---|---|---|',
    '| Delantera: X = 26 m | V01 | V02 | V03 | V04 |',
    '| Intermedia: X = 31 m | V05 | V06 | V07 | V08 |',
    '| Posterior: X = 36 m | V09 | V10 | V11 | V12 |',
    '## Coordenadas y altura',
    'Todos los virtuales están a **2,00 m sobre el piso local**. Z es la cota global del receptor; varía porque el piso y las gradas tienen alturas diferentes.',
    '| Punto | X (m) | Y (m) | Z receptor (m) | Z piso (m) | Superficie bajo el punto en el modelo |',
    '|---|---:|---:|---:|---:|---|']
for r in rows:
    text.append('| '+r['punto']+' | '+' | '.join(f"{r[k]:.2f}".replace('.',',') for k in ('X_m','Y_m','Z_global_m','piso_Z_m'))+' | '+r['superficie_modelada']+' |')
text+=['', '## Qué representa cada punto',
    'Son puntos de evaluación añadidos al modelo, no nuevas mediciones ni un recuento de butacas. Al comprobar la superficie de apoyo, **ocho están sobre bloques de butacas** y **cuatro sobre madera expuesta: V06, V07, V09 y V12**. Estos últimos muestrean partes del suelo alto que el modelo no clasifica como butacas. La clasificación procede de los materiales nativos, no de identificar una silla concreta en el plano.',
    'Por ello, el resultado anterior de **5/24 combinaciones dentro de los objetivos** describe esta cuadrícula de control y ambas fuentes. No equivale a que el 5/24 del público cumpla. Para estudiar cobertura de audiencia se puede informar por separado butacas y otras superficies, manteniendo todos estos puntos como referencia y añadiendo muestreo en las áreas de interés.',
    '## Archivos y referencias',
    '- [Coordenadas y clasificación CSV](../prediccion/estudio-difusion/reflectores/resultados/ubicacion-receptores-virtuales.csv).',
    '- [Coordenadas y clasificación JSON](../prediccion/estudio-difusion/reflectores/resultados/ubicacion-receptores-virtuales.json).',
    '- [Mapa vectorial SVG](../prediccion/estudio-difusion/reflectores/resultados/mapa-receptores-virtuales.svg).',
    '- [Posiciones originales de los virtuales](../prediccion/estudio-difusion/absorcion-posterior/receptores-virtuales.json).',
    '- [Auditoría de fuentes y receptores del estudio de reflectores](../prediccion/estudio-difusion/reflectores/auditoria-posiciones.json).',
    '- [Avances y estado del estudio](AVANCES-Y-ESTADO-DEL-ESTUDIO-ACUSTICO.md).',
    '- [Resultados iniciales de reflectores](RESULTADOS-INICIALES-REFLECTORES-PLATEA-ALTA.md).']
(root/'informes/MAPA-DE-RECEPTORES-VIRTUALES-PLATEA-ALTA.md').write_text('\n\n'.join(text).replace('|\n\n|','|\n|')+'\n',encoding='utf8')
print('Mapa generado; 12 posiciones verificadas, 8 sobre butacas y 4 sobre madera expuesta.')
