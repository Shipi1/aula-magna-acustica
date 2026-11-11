"""Partición común de pared posterior; no altera geometría ni estudios anteriores."""
from pathlib import Path
import json,subprocess
import numpy as np
import preparar_localizado as mesh
mesh.O=mesh.B/'absorcion-posterior';mesh.O.mkdir(exist_ok=True)
O=mesh.O

def main():
    mesh.prepare(rear_y_cuts=(-8.,-4.,0.,4.,8.))
    model=json.loads((O/'malla-subdividida.json').read_text());v=np.array(model['vertices']);tri=v[np.array([f['v'] for f in model['faces']])]
    area=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1)/2
    total=[i for i,f in enumerate(model['faces']) if f['idMat']==115 and np.all(abs(tri[i,:,0]-40.25)<1e-5)]
    patches={'total':total}
    for label,zlo,zhi in [('sup',10.6,11.8),('med',9.,10.2)]:
        for j,(ylo,yhi) in enumerate(zip((-8.,-4.,0.,4.),(-4.,0.,4.,8.)),1):
            ids=[i for i in total if tri[i,:,1].min()>=ylo-1e-6 and tri[i,:,1].max()<=yhi+1e-6 and tri[i,:,2].min()>=zlo-1e-6 and tri[i,:,2].max()<=zhi+1e-6]
            assert abs(area[ids].sum()-4.8)<1e-4,(label,j,area[ids].sum())
            patches[f'{label}_{j}']=ids
        patches[label+'_centro']=patches[label+'_2']+patches[label+'_3']
        patches[label+'_exterior']=patches[label+'_1']+patches[label+'_4']
        patches[label+'_completa']=sum((patches[f'{label}_{j}'] for j in range(1,5)),[])
    info={name:dict(faces=ids,area_m2=float(area[ids].sum()),min=tri[ids].reshape(-1,3).min(0).tolist(),max=tri[ids].reshape(-1,3).max(0).tolist()) for name,ids in patches.items()}
    mesh.save('panos-absorcion.json',info)
    for name,ids in patches.items():
        if name.startswith(('sup_','med_')) and name.rsplit('_',1)[-1].isdigit():continue
        changes=O/(name+'-caras.json');changes.write_text(json.dumps({str(i):201 for i in ids}),encoding='utf8')
        subprocess.run([str(mesh.NATIVE),str(mesh.B/'nativo.py'),'mesh',str(O/'base.cbin'),str(O/(name+'.cbin')),str(changes)],check=True)
    cases={'base':dict(malla='base.cbin',alpha_por_banda={},area_m2=0,hipotesis='Referencia sin tratamiento'),
           'total_a100':dict(malla='total.cbin',alpha_por_banda={'1000':1.0},area_m2=info['total']['area_m2'],hipotesis='Límite ideal, no producto físico'),
           'total_a080':dict(malla='total.cbin',alpha_por_banda={'1000':.8},area_m2=info['total']['area_m2'],hipotesis='Límite de cobertura para alfa .80 a 1000 Hz; no producto seleccionado')}
    for name in ('sup_centro','sup_exterior','med_centro','med_exterior','sup_completa','med_completa'):
        for alpha in (.4,.6,.8,.95):
            cases[f'{name}_a{round(alpha*100):03}']=dict(malla=name+'.cbin',alpha_por_banda={'1000':alpha},area_m2=info[name]['area_m2'],hipotesis='Sensibilidad; coeficiente final, no material seleccionado')
    mesh.save('escenarios.json',cases)
    print('Muro disponible:',info['total']['area_m2'],'m²; ocho módulos de 4,8 m² verificados.')

if __name__=='__main__':main()
