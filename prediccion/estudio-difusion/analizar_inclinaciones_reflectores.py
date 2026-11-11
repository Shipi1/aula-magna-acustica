"""Mismos indicadores e integraciones; comparador adicional a igual área."""
import json
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import analizar_frente_media_reflectores as a
B=a.B;a.O=B/'reflectores-inclinacion';a.OUT=a.O/'resultados';a.OUT.mkdir(exist_ok=True)
a.OBJ=json.loads((a.O/'objetivo.json').read_text());a.PROFILES={c:dict(alpha=.05) for c in json.loads((a.O/'variantes.json').read_text())}
a.REFERENCES=[(B/'reflectores',['base','combinado']),(B/'reflectores-cobertura',['cobertura6'])]
a.CASES=['base','combinado','cobertura6']+list(a.PROFILES)
a.ENERGY_REFERENCE='combinado';a.ENERGY_CASES=['combinado']+list(a.PROFILES)
a.NAMES={'base':'Sala sin paneles','combinado':'Cuatro originales · 48 m²','cobertura6':'Seis redistribuidos · 72 m²','vertical':'Giro vertical · 48 m²','horizontal':'Giro horizontal · 48 m²','combinada':'Giro en ambos ejes · 48 m²','segmentada':'Ocho módulos · 48 m²'}
def main():
    a.main();means=json.loads((a.OUT/'medias.json').read_text());rows=[]
    for r in means:
        b=next(x for x in means if x['variante']=='combinado' and x['fuente']==r['fuente'] and x['receptor']==r['receptor'])
        rows.append(dict(variante=r['variante'],fuente=r['fuente'],receptor=r['receptor'],**{'delta_'+k:r[k]-b[k] for k in ('D50_pct','C80','EDT','T30')},
            **{'delta_'+k+'_dB':a.calc.core.db(r[k]/b[k]) for k in ('E0_50','E50_80','E0_80','E50_total','total')}))
    a.save('cambios-respecto-cuatro-originales.json',rows);a.csvsave('cambios-respecto-cuatro-originales.csv',rows)
    original=json.loads((B/'reflectores/resultados/medias-N600000-a0.05-s0.05.json').read_text());coverage=json.loads((B/'reflectores-cobertura/resultados/medias.json').read_text());checks=[]
    for r in means:
        if r['variante'] not in ('base','combinado','cobertura6'):continue
        ref=next(x for x in (coverage if r['variante']=='cobertura6' else original) if all(x[k]==r[k] for k in ('variante','fuente','receptor')))
        errors={k:abs(r[k]-ref[k]) for k in ('D50_pct','C80','EDT','T30','total')}
        assert all(errors[k]<1e-10*max(1,abs(ref[k])) for k in errors),(r['variante'],r['fuente'],r['receptor'],errors)
        checks.append(dict(variante=r['variante'],fuente=r['fuente'],receptor=r['receptor'],errores=errors))
    assert len(checks)==126;a.save('verificacion-referencias.json',checks)
    fig,axes=plt.subplots(2,4,figsize=(15,8),sharex=True,sharey=True,constrained_layout=True)
    target=a.OBJ['frente_butacas']+a.OBJ['media_butacas']
    for ax,c in zip(axes.flat,a.CASES):
        ax.add_patch(Rectangle((48,-2),4,4,facecolor='#a6cfad',alpha=.35,edgecolor='#397a43'))
        for src,color in [('F1','#23789b'),('F2','#be702e')]:
            for p in target:
                r=next(x for x in means if x['variante']==c and x['fuente']==src and x['receptor']==p)
                ax.scatter(r['D50_pct'],r['C80'],c=color,marker='o' if p in a.OBJ['frente_butacas'] else '^',s=35)
                if src=='F2' and p in ('V04','V08'):ax.annotate(src+'–'+p,(r['D50_pct'],r['C80']),xytext=(3,7 if p=='V08' else -12),textcoords='offset points',fontsize=7)
        ax.axhline(2,c='#777',ls=':',lw=.7);ax.set(xlim=(20,65),ylim=(-2.5,3.5),xlabel='D50 (%)',ylabel='C80 (dB)',title=a.NAMES[c]);ax.grid(alpha=.15)
    for ax in list(axes.flat)[len(a.CASES):]:ax.axis('off')
    fig.suptitle('Cobertura de ambos indicadores · doce respuestas objetivo por condición\nAzul: F1 · ocre: F2 · círculos: frente · triángulos: media · verde: rango de trabajo')
    fig.savefig(a.OUT/'D50-C80-conjunto.png',dpi=170);plt.close(fig)
if __name__=='__main__':main()
