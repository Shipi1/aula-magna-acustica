"""Archiva sin pérdida las salidas nativas generadas por este estudio.

Verifica cada archivo antes de quitar su copia suelta. No toca datos anteriores.
"""
from pathlib import Path
import zipfile,hashlib,json
B=Path(__file__).resolve().parent
keep={'config.xml','motor.log','resultados-lineales.json','ejecucion.json','salidas-nativas.zip'}
audit=[]
folders=[p.parent for p in (B/'calculos').glob('*/ejecucion.json')]
folders += [p.parent for p in (B/'sensibilidad-absorcion').glob('*/resultados-lineales.json')]
for folder in folders:
    folder=folder.resolve();assert folder.is_relative_to(B.resolve()) and folder!=B.resolve()
    candidates=[p for p in folder.rglob('*') if p.is_file() and p.name not in keep]
    if not candidates:continue
    target=folder/'salidas-nativas.zip';assert not target.exists()
    hashes={str(p.relative_to(folder)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in candidates}
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in candidates:z.write(p,p.relative_to(folder))
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        assert set(z.namelist())==set(hashes)
        for name,h in hashes.items():assert hashlib.sha256(z.read(name)).hexdigest()==h
    before=sum(p.stat().st_size for p in candidates)
    for p in candidates:
        assert p.resolve().is_relative_to(folder)
        assert hashlib.sha256(p.read_bytes()).hexdigest()==hashes[str(p.relative_to(folder)).replace('\\','/')]
        p.unlink()
    for p in sorted(folder.rglob('*'),key=lambda p:len(p.parts),reverse=True):
        if p.is_dir() and not any(p.iterdir()):p.rmdir()
    audit.append({'carpeta':str(folder.relative_to(B)),'archivos':len(candidates),'bytes_originales':before,'bytes_zip':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
(B/'resultados/verificacion-compactacion.json').write_text(json.dumps(audit,indent=2),encoding='utf8')
print('Carpetas archivadas:',len(audit),'MiB antes',round(sum(a['bytes_originales'] for a in audit)/2**20,1),'despues',round(sum(a['bytes_zip'] for a in audit)/2**20,1))
