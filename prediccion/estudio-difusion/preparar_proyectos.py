"""Copias ligeras para I-Simpa con grupos de paños y dispersión equivalente.

Mantiene sceneMesh.bin y reasigna grupos por sus referencias nativas .finfo.
No altera ni sobreescribe el proyecto principal.
"""
from pathlib import Path
import zipfile,xml.etree.ElementTree as ET,json,copy,struct,hashlib
B=Path(__file__).resolve().parent
source=B.parent/'G_base_efectiva_espectral_Lw90.proj'
patches=json.loads((B/'panos.json').read_text())
with zipfile.ZipFile(source) as z:original={n:z.read(n) for n in z.namelist() if n.count('/')==1 and not n.endswith('/')}
base=ET.fromstring(original['instance1/projet_config.xml'])
groups=[e for e in base.iter('gr') if e.get('facesFile')]
offset=0;mapping={}
for group in groups:
    b=original['instance1/'+group.get('facesFile')];ints=struct.unpack('<'+'i'*(len(b)//4),b);assert len(ints)==1+2*ints[0]
    for j in range(ints[0]):mapping[offset+j]=(ints[1+2*j],ints[2+2*j])
    offset+=ints[0]
assert offset==len(json.loads((B/'malla-base.json').read_text())['faces'])
out=B/'proyectos';out.mkdir(exist_ok=True)
audit={}
for name,patch in patches.items():
    root=copy.deepcopy(base); parents={c:p for p in root.iter() for c in p}
    counter=max(int(e.get('wxid','0')) for e in root.iter())+100
    def fresh(element):
        global counter
        for e in element.iter():
            if 'wxid' in e.attrib: e.set('wxid',str(counter));counter+=1
    payload=dict(original)
    selected={mapping[i] for i in patch['faces']}
    nselected=0
    existinggroups=[e for e in root.iter('gr') if e.get('facesFile')]
    for group in existinggroups:
        key='instance1/'+group.get('facesFile');ints=struct.unpack('<'+'i'*(len(payload[key])//4),payload[key])
        old=[(ints[1+2*j],ints[2+2*j]) for j in range(ints[0])]
        keep=[p for p in old if p not in selected];nselected+=len(old)-len(keep)
        data=[len(keep)]+[n for pair in keep for n in pair];payload[key]=struct.pack('<'+'i'*len(data),*data)
        # Recompute area from original native face indices for all preserved group faces.
        area_prop=next((e for e in group if e.get('name')=='aire'),None)
        if area_prop is not None:
            import numpy as np
            mesh=json.loads((B/'malla-base.json').read_text());vertices=np.array(mesh['vertices']);reverse={p:i for i,p in mapping.items()}
            area=0.
            for pair in keep:
                p=vertices[mesh['faces'][reverse[pair]]['v']];area+=np.linalg.norm(np.cross(p[1]-p[0],p[2]-p[0]))/2
            area_prop.set('value',str(area))
        if not keep:parents[group].remove(group)
    assert nselected==len(selected)
    newgroup=copy.deepcopy(existinggroups[0]);newgroup.set('name','D_'+name+'_s060_HIPOTESIS');fresh(newgroup)
    fileid=str(counter);counter+=1;newgroup.set('facesFile',fileid+'.finfo')
    for e in newgroup:
        if e.get('name')=='idmat':e.set('value','201')
        if e.get('name')=='aire':e.set('value',str(patch['area_m2']))
    parents[existinggroups[0]].append(newgroup)
    data=[len(selected)]+[n for pair in sorted(selected) for n in pair]
    payload['instance1/'+fileid+'.finfo']=struct.pack('<'+'i'*len(data),*data)
    material=next(e for e in root.iter('materiau') if e.get('idmateriau')=='115')
    usermat=parents[material];newmat=copy.deepcopy(usermat);newmat.set('name','Dispersor_equivalente_s060_NO_QRD_VALIDADO');fresh(newmat)
    spectrum=next(newmat.iter('materiau'));spectrum.set('idmateriau','201')
    for band in spectrum:
        if band.get('name') not in ['1000','2000','4000']:continue
        for prop in band:
            if prop.get('name')=='diffusion':prop.set('value','0.6')
            if prop.get('name')=='loi':prop.set('choice','2')
    parents[usermat].append(newmat)
    report=root.find('Report')
    for child in list(report):report.remove(child)
    ET.indent(root);payload['instance1/projet_config.xml']=ET.tostring(root,encoding='utf-8',xml_declaration=True)
    target=out/(name+'_dispersion-equivalente-s060.proj')
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
        for folder in ['instance1/','instance1/report/','instance1/temp/']:z.writestr(folder,b'')
        for key,data in sorted(payload.items()):z.writestr(key,data)
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        assert z.read('instance1/sceneMesh.bin')==original['instance1/sceneMesh.bin']
        check=ET.fromstring(z.read('instance1/projet_config.xml'))
        pairs=[]
        for g in check.iter('gr'):
            if not g.get('facesFile'):continue
            b=z.read('instance1/'+g.get('facesFile'));ints=struct.unpack('<'+'i'*(len(b)//4),b)
            pairs.extend((ints[1+2*j],ints[2+2*j]) for j in range(ints[0]))
        assert len(pairs)==offset and len(set(pairs))==offset and set(pairs)==set(mapping.values())
    audit[name]={'archivo':target.name,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'caras':nselected,'area_m2':patch['area_m2'],'caras_totales_sin_duplicados':offset,'sceneMesh_identica':True,'GUI_verificada':False}
    print(target.name)
(out/'verificacion.json').write_text(json.dumps(audit,indent=2),encoding='utf8')
