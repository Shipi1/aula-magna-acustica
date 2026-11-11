"""Archivo nativo íntegro de corridas terminadas, con registro acumulativo."""
from pathlib import Path
import json,hashlib,zipfile,argparse
parser=argparse.ArgumentParser();parser.add_argument('--estudio',choices=['reflectores','reflectores-cobertura','reflectores-frente-media','reflectores-inclinacion','reflectores-absorcion-localizada','comparacion-octavas'],default='reflectores');args=parser.parse_args()
O=Path(__file__).resolve().parent/args.estudio;OUT=O/'resultados';OUT.mkdir(exist_ok=True)
auditfile=OUT/'verificacion-compactacion.json'
audit=json.loads(auditfile.read_text()) if auditfile.exists() else []
keep={'config.xml','motor.log','resultados-lineales.json','ejecucion.json','salidas-nativas.zip'}
for marker in sorted((O/'calculos').glob('*/ejecucion.json')):
    if json.loads(marker.read_text()).get('pendiente',False):continue
    folder=marker.parent.resolve();assert folder.is_relative_to((O/'calculos').resolve())
    files=[p for p in folder.rglob('*') if p.is_file() and p.name not in keep]
    target=folder/'salidas-nativas.zip'
    if not files:assert target.exists();continue
    assert not target.exists()
    hashes={p.relative_to(folder).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    before=sum(p.stat().st_size for p in files)
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in files:z.write(p,p.relative_to(folder))
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None and set(z.namelist())==set(hashes)
        for name,h in hashes.items():assert hashlib.sha256(z.read(name)).hexdigest()==h
    for p in files:
        assert p.resolve().is_relative_to(folder) and hashlib.sha256(p.read_bytes()).hexdigest()==hashes[p.relative_to(folder).as_posix()]
        p.unlink()
    for p in sorted(folder.rglob('*'),key=lambda p:len(p.parts),reverse=True):
        if p.is_dir() and not any(p.iterdir()):p.rmdir()
    audit.append(dict(carpeta=folder.name,archivos=len(files),bytes_originales=before,bytes_zip=target.stat().st_size,sha256=hashlib.sha256(target.read_bytes()).hexdigest()))
    auditfile.write_text(json.dumps(audit,indent=2),encoding='utf8')
print('Corridas archivadas y verificadas:',len(audit))
