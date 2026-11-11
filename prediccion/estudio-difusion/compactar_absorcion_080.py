"""Conserva sin pérdida las salidas nativas de la continuación alfa .80."""
from analizar_absorcion_080 import O,OUT,CASES
import json,zipfile,hashlib

keep={'config.xml','motor.log','resultados-lineales.json','ejecucion.json','salidas-nativas.zip'}
auditpath=OUT/'verificacion-compactacion.json'
audit=json.loads(auditpath.read_text(encoding='utf8')) if auditpath.exists() else []
for marker in sorted((O/'calculos').glob('*/ejecucion.json')):
    d=json.loads(marker.read_text())
    if d['variante'] not in CASES[1:] or d['N']!=600000:continue
    folder=marker.parent.resolve();assert folder.is_relative_to((O/'calculos').resolve())
    target=folder/'salidas-nativas.zip'
    candidates=[p for p in folder.rglob('*') if p.is_file() and p.name not in keep]
    if not candidates:
        assert target.exists();continue
    assert not target.exists()
    hashes={p.relative_to(folder).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in candidates}
    before=sum(p.stat().st_size for p in candidates)
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in candidates:z.write(p,p.relative_to(folder))
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None and set(z.namelist())==set(hashes)
        for name,h in hashes.items():assert hashlib.sha256(z.read(name)).hexdigest()==h
    for p in candidates:
        assert p.resolve().is_relative_to(folder)
        assert hashlib.sha256(p.read_bytes()).hexdigest()==hashes[p.relative_to(folder).as_posix()]
        p.unlink()
    for p in sorted(folder.rglob('*'),key=lambda p:len(p.parts),reverse=True):
        if p.is_dir() and not any(p.iterdir()):p.rmdir()
    audit.append(dict(carpeta=folder.name,archivos=len(candidates),bytes_originales=before,bytes_zip=target.stat().st_size,
                      sha256=hashlib.sha256(target.read_bytes()).hexdigest()))
    auditpath.write_text(json.dumps(audit,indent=2),encoding='utf8')
print('Corridas nuevas archivadas y verificadas:',len(audit))
