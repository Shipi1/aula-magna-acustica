"""Recorridos de primera reflexión candidatos; no etiquetan picos simulados."""
import json
import numpy as np
import preparar_cobertura_reflectores as h
O=h.B/'reflectores-absorcion-localizada';profiles=json.loads((O/'perfiles.json').read_text());panels=json.loads((O/'paneles-fijos.json').read_text());rows=[]
for c in ('superior_centro_a060','superior_completa_a060','media_centro_a060'):
    p=profiles[c];lo=np.array(p['min']);hi=np.array(p['max'])
    for src in ('F1','F2'):
        for rec in ('V04','V08','P8','P9'):
            s=h.S[src];r=h.R[rec]
            def length(q):return np.linalg.norm(s-q)+np.linalg.norm(r-q)
            image=s.copy();image[0]=80.5-s[0];t=(40.25-r[0])/(image[0]-r[0]);unconstrained=r+t*(image-r);candidates=[]
            if np.all(unconstrained>=lo-1e-6) and np.all(unconstrained<=hi+1e-6):candidates.append(unconstrained)
            for fixed,free in ((1,2),(2,1)):
                for value in (lo[fixed],hi[fixed]):
                    def point(x):
                        q=np.array([40.25,0.,0.]);q[fixed]=value;q[free]=x;return q
                    def derivative(x):
                        q=point(x);return (q[free]-s[free])/np.linalg.norm(q-s)+(q[free]-r[free])/np.linalg.norm(q-r)
                    left=lo[free];right=hi[free]
                    if derivative(left)>=0:minimum=left
                    elif derivative(right)<=0:minimum=right
                    else:
                        for _ in range(80):
                            mid=(left+right)/2
                            if derivative(mid)>0:right=mid
                            else:left=mid
                        minimum=(left+right)/2
                    candidates.append(point(minimum))
            q=min(candidates,key=length);clear=h.g.visible(s,q) and h.g.visible(q,r) and not any(h.blocks(panel,s,q) or h.blocks(panel,q,r) for panel in panels)
            rows.append(dict(variante=c,fuente=src,receptor=rec,punto_candidato=q.tolist(),retardo_ms=float((length(q)-np.linalg.norm(s-r))/342*1000),visible_con_paneles=bool(clear),
                alcance='Mínimo geométrico numérico de una primera reflexión en el rectángulo; si está obstruido no identifica la primera llegada visible. No prueba causalidad de un pico.'))
(O/'resultados/rutas-candidatas.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
for r in rows:
    if r['fuente']=='F2' and r['receptor'] in ('V04','V08'):print(r['variante'],r['fuente'],r['receptor'],round(r['retardo_ms'],2),'ms','visible',r['visible_con_paneles'])
