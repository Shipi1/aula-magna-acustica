"""Prueba con el TetGen instalado junto a I-Simpa; no modifica el proyecto."""
from pathlib import Path
import json,subprocess
B=Path(__file__).resolve().parent
out=B.parent/'prediccion'/'diagnostico';out.mkdir(exist_ok=True)
g=json.loads((B/'geometria.json').read_text(encoding='utf8'))
s=[f"{len(g['vertices'])} 3 0 0"]+[f"{i+1} "+' '.join(map(str,p)) for i,p in enumerate(g['vertices'])]
s+=[f"{len(g['faces'])} 1"]
for i,f in enumerate(g['faces']):s+=[f'1 0 {i+1}','3 '+' '.join(str(v+1) for v in f['v'])]
s+=['0','0'];poly=out/'corregido.poly';poly.write_text('\n'.join(s)+'\n')
exe=Path('C:/Program Files/I-SIMPA/meshing/tetgen/tetgen.exe')
for suffix,flags in [('intersecciones','-d'),('mallado','-pq5AnY')]:
 r=subprocess.run([str(exe),flags,str(poly)],capture_output=True,text=True,timeout=90)
 text=r.stdout+r.stderr;(out/f'tetgen-{suffix}.txt').write_text(text,encoding='utf8')
 print(suffix,'exit',r.returncode)
 print('\n'.join(line for line in text.splitlines() if any(t in line for t in ['intersect','stopped','tetrahedra','seconds','Mesh points','Mesh faces'])))
 if r.returncode: raise SystemExit(r.returncode)
 if suffix=='intersecciones': assert 'No faces are intersecting.' in text
 else: assert 'Mesh tetrahedra:' in text and 'Program stopped' not in text

# Repetir con coordenadas float32 y vértices por grupo tal como salen del 3DS.
from verificar_geometria import read3ds
v,f,_=read3ds(B/'aula-magna.3ds')
s=[f'{len(v)} 3 0 0']+[f'{i+1} '+' '.join(map(str,p)) for i,p in enumerate(v)]
s+=[f'{len(f)} 1']
for i,face in enumerate(f): s += [f'1 0 {i+1}','3 '+' '.join(str(int(k)+1) for k in face)]
s+=['0','0']
for repair in [False,True]:
 p=out/('exportacion3ds-reparada.poly' if repair else 'exportacion3ds.poly')
 p.write_text('\n'.join(s)+'\n')
 if repair:
  r=subprocess.run([str(exe.with_name('preprocess.exe')),str(p)],capture_output=True,text=True,timeout=90)
  (out/'preprocess-corregido.txt').write_text(r.stdout+r.stderr,encoding='utf8')
  assert r.returncode==0
 r=subprocess.run([str(exe),'-pq5AnY',str(p)],capture_output=True,text=True,timeout=90)
 t=r.stdout+r.stderr;(out/(p.stem+'.log')).write_text(t,encoding='utf8')
 assert r.returncode==0 and 'Mesh tetrahedra:' in t and 'Program stopped' not in t
 print('3DS con reparación' if repair else '3DS sin reparación','OK')
