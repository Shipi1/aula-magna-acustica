"""Estudio independiente: cuatro reflectores inclinados y paños absorbentes."""
from pathlib import Path
import json,subprocess,shutil,hashlib,copy
import numpy as np
import preparar_reflectores as g
B=g.B;O=B/'reflectores-absorcion-localizada';O.mkdir(exist_ok=True)
def save(name,x):(O/name).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
def main():
    source=B/'absorcion-posterior';partition=json.loads((source/'malla-subdividida.json').read_text());patches=json.loads((source/'panos-absorcion.json').read_text())
    panels=json.loads((B/'reflectores-inclinacion/variantes.json').read_text())['combinada']
    g.O=O;g.MODEL=partition;g.export('referencia',panels)
    common=O/'referencia';mesh=json.loads((common/'malla-subdividida.json').read_text());tri=np.array(mesh['vertices'])[np.array([f['v'] for f in mesh['faces']])]
    area=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1)/2
    profiles={'referencia':dict(parche=None,alpha=None,area_m2=0),
        'superior_centro_a060':dict(parche='sup_centro',alpha=.6),
        'superior_completa_a060':dict(parche='sup_completa',alpha=.6),
        'superior_completa_a080':dict(parche='sup_completa',alpha=.8),
        'media_centro_a060':dict(parche='med_centro',alpha=.6)}
    for case,p in profiles.items():
        ids=patches[p['parche']]['faces'] if p['parche'] else []
        assert all(mesh['faces'][i]['idMat']==115 for i in ids)
        p['area_m2']=float(area[ids].sum());p['caras']=ids;p['min']=tri[ids].reshape(-1,3).min(0).tolist() if ids else None;p['max']=tri[ids].reshape(-1,3).max(0).tolist() if ids else None
        folder=O/case;folder.mkdir(exist_ok=True)
        if case!='referencia':
            changes=folder/'cambios-material.json';changes.write_text(json.dumps({str(i):201 for i in ids}),encoding='utf8')
            subprocess.run([str(g.native_mesh.NATIVE),str(B/'nativo.py'),'mesh',str(common/'mesh.cbin'),str(folder/'mesh.cbin'),str(changes)],check=True)
            shutil.copyfile(common/'tetramesh.mbin',folder/'tetramesh.mbin')
        assert hashlib.sha256((folder/'tetramesh.mbin').read_bytes()).hexdigest()==hashlib.sha256((common/'tetramesh.mbin').read_bytes()).hexdigest()
        variant=copy.deepcopy(mesh)
        for i in ids:variant['faces'][i]['idMat']=201
        (folder/'modelo-materiales.json').write_text(json.dumps(variant),encoding='utf8')
        with (folder/'modelo.obj').open('w') as fp:
            fp.write('mtllib modelo.mtl\n')
            for v in variant['vertices']:fp.write('v '+' '.join(map(str,v))+'\n')
            mat=None
            for f in variant['faces']:
                if mat!=f['idMat']:
                    mat=f['idMat'];fp.write(f'g material_{mat}\nusemtl '+('reflector' if mat==301 else 'absorbente' if mat==201 else 'sala')+'\n')
                fp.write('f '+' '.join(str(i+1) for i in f['v'])+'\n')
        (folder/'modelo.mtl').write_text('newmtl sala\nKd 0.72 0.74 0.76\nnewmtl reflector\nKd 0.86 0.57 0.15\nnewmtl absorbente\nKd 0.20 0.62 0.65\n')
    objective=json.loads((B/'reflectores-inclinacion/objetivo.json').read_text());objective.update(version='mixto_v1',fecha='2026-11-10',D50_objetivo_pct=[45,55],C80_balance_dB=[-2,2],rango_D50_pct=[45,55],rango_C80_dB=[-2,2],alcance='Estudio independiente de absorcion localizada sobre la referencia de cuatro reflectores inclinados; rangos exploratorios actualizados sin reescribir estudios anteriores.',F2_V08='Caso crítico conservado, no requisito único de selección. No se elimina de los conteos.')
    save('objetivo.json',objective);save('perfiles.json',profiles);save('paneles-fijos.json',panels)
    save('diseno-estudio.json',dict(referencia='Cuatro con giro combinado del estudio de inclinaciones, con subdivisión coplanar común del muro posterior.',
        frecuencia_Hz=1000,material_reflectores=dict(alpha=.05,dispersion=.05),
        material_absorbente='Coeficiente final efectivo de 0.60 o 0.80 a 1000Hz; sin producto físico ni extrapolación a otras bandas. Dispersión del muro invariable.',
        comparaciones=['Área: superior centro 9.6 frente a superior completa 19.2 m² a alpha .60','Absorción: superior completa alpha .60 frente a .80','Altura: centro superior frente a centro medio, ambos 9.6 m² y alpha .60'],
        control_malla='Se recalcula referencia con partición común; todas las variantes conservan vertices, caras y MBIN idénticos salvo etiquetas de material en CBIN.',
        ventana_tiempo='0-50, 50-80, >80ms relativos al directo; también EDT/T30, energía total y controles fuera de platea alta.',
        criterios='Demostración de mejora local/repartida/consistente sin exigir cobertura perfecta ni excluir silenciosamente F2-V08. No se recalibran los materiales de la sala.'))
    print('Cinco condiciones listas:',[(k,p['area_m2'],p['alpha']) for k,p in profiles.items()],flush=True)
if __name__=='__main__':main()
