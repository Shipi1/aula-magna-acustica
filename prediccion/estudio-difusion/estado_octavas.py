"""Estado verificable del barrido; lectura acotada de registros en escritura."""
import json,re,argparse
from pathlib import Path
O=Path(__file__).resolve().parent/'comparacion-octavas'
FREQS=json.loads((O/'espectros.json').read_text())['frecuencias_Hz']
def snapshot():
    done=[];active=[]
    for folder in sorted((O/'calculos').glob('*')):
        if not folder.is_dir():continue
        marker=folder/'ejecucion.json'
        if marker.exists():
            try:d=json.loads(marker.read_text())
            except ValueError:continue
            if not d.get('pendiente',False):
                if d['N']==600000:done.append(d)
                continue
        if 'N600000' in folder.name and (folder/'config.xml').exists():
            p=folder/'motor.log';progress=None
            if p.exists():
                size=p.stat().st_size;start=max(0,size-2048)
                with p.open('rb') as fp:fp.seek(start);tail=fp.read(size-start).decode('utf8','replace')
                values=re.findall(r'#([0-9.]+)',tail);progress=float(values[-1]) if values else None
            active.append(dict(corrida=folder.name,porcentaje=progress))
    rows=[]
    for hz in FREQS:
        n=sum(d['frecuencia']==hz for d in done);reused=12 if hz==1000 else 0
        rows.append(dict(frecuencia_Hz=hz,nuevas_terminadas=n,reutilizadas=reused,total=n+reused,esperadas=12))
    d=dict(principales_nuevas_terminadas=len(done),principales_nuevas_esperadas=84,reutilizadas=12,bandas=rows,activas=active)
    (O/'avance.json').write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding='utf8')
    lines=['# Avance del barrido por octavas','',f"Corridas principales nuevas: {len(done)}/84. Se reutilizan doce a 1.000 Hz.",'','| Banda | Principales disponibles |','|---|---:|']+[f"| {r['frecuencia_Hz']} Hz | {r['total']}/12 |" for r in rows]
    (O/'AVANCE.md').write_text('\n'.join(lines)+'\n',encoding='utf8');return d
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--compacto',action='store_true');args=parser.parse_args();d=snapshot()
    if args.compacto:
        print(f"Nuevas {d['principales_nuevas_terminadas']}/84; reutilizadas 12. "+' | '.join(f"{r['frecuencia_Hz']}Hz {r['total']}/12" for r in d['bandas']))
        print('Activas: '+'; '.join(r['corrida'].replace('-N600000','')+f" {r['porcentaje']}%" for r in d['activas']))
    else:print(json.dumps(d,ensure_ascii=False))
