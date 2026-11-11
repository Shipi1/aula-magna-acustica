"""Subdivide coplanarmente, delimita paños y genera una malla SPPS común."""
from pathlib import Path
import json,collections,subprocess,struct,itertools
import numpy as np
B=Path(__file__).resolve().parent
O=B/'localizado';O.mkdir(exist_ok=True)
NATIVE=Path('C:/Program Files/I-SIMPA/python.exe')
TETGEN=Path('C:/Program Files/I-SIMPA/meshing/tetgen/tetgen.exe')

def save(name,d): (O/name).write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding='utf8')
def clip(poly,axis,value,side):
    result=[]
    for p,q in zip(poly,poly[1:]+poly[:1]):
        a=side*(p[axis]-value);b=side*(q[axis]-value)
        if a>=-1e-9:result.append(p)
        if (a>1e-9 and b< -1e-9) or (a< -1e-9 and b>1e-9):
            r=p+(q-p)*((value-p[axis])/(q[axis]-p[axis]));r[axis]=value;result.append(r)
    clean=[]
    for p in result:
        if not clean or np.linalg.norm(p-clean[-1])>1e-8:clean.append(p)
    if len(clean)>1 and np.linalg.norm(clean[0]-clean[-1])<1e-8:clean.pop()
    return clean

def prepare(include_laterals=False, lateral_bounds=(26.,34.,8.,10.4), rear_y_cuts=(-8.,8.)):
    original=json.loads((B/'malla-base.json').read_text());v=np.array(original['vertices'])
    verts=[];lookup={};faces=[];area_errors=[]
    def vertex(p):
        key=tuple(np.round(p,7))
        if key not in lookup:lookup[key]=len(verts);verts.append(p.tolist())
        return lookup[key]
    # Cut only posterior wall and last roof; propagate inserted edge points to
    # neighboring faces so the boundary remains conforming without global slivers.
    cuts=[(0,37.),(0,38.2)]+[(1,y) for y in rear_y_cuts]+[(2,9.),(2,10.2),(2,10.6),(2,11.8)]
    allpolys=[];newpoints=[]
    for parent,f in enumerate(original['faces']):
        p=v[f['v']];polys=[list(p)]
        rear=np.all(abs(p[:,0]-40.25)<1e-5) and f['idMat']==115
        roof=np.all(abs(p[:,2]-12.12)<1e-5) and f['idMat']==108
        selected=[c for c in cuts if (rear and c[0] in (1,2)) or (roof and c[0] in (0,1))]
        lateral=include_laterals and f['idMat']==115 and np.ptp(p[:,1])<1e-5 and abs(abs(p[0,1])-11.665)<1e-4
        if lateral:selected=[(0,lateral_bounds[0]),(0,lateral_bounds[1]),(2,lateral_bounds[2]),(2,lateral_bounds[3])]
        if include_laterals:
            selected=[(axis,float(v[np.argmin(abs(v[:,axis]-value)),axis]) if np.min(abs(v[:,axis]-value))<1e-5 else value) for axis,value in selected]
        for axis,value in selected:
            new=[]
            for poly in polys:
                arr=np.array(poly)
                if arr[:,axis].min()<value-1e-9 and arr[:,axis].max()>value+1e-9:
                    for side in (-1,1):
                        part=clip(poly,axis,value,side)
                        if len(part)>=3:new.append(part)
                else:new.append(poly)
            polys=new
        allpolys.append(polys)
        if selected:newpoints.extend(q for poly in polys for q in poly)
    candidates=np.unique(np.round(np.array(newpoints),10),axis=0)
    for parent,(f,polys) in enumerate(zip(original['faces'],allpolys)):
        p=v[f['v']]
        conforming=[]
        for poly in polys:
            boundary=[]
            for a,b in zip(poly,poly[1:]+poly[:1]):
                edge=b-a;length2=edge@edge;t=(candidates-a)@edge/length2
                distance=np.linalg.norm(candidates-(a+t[:,None]*edge),axis=1)
                mask=(t>1e-7)&(t<1-1e-7)&(distance<1e-8)
                additions=candidates[mask];order=np.argsort(t[mask]);boundary.append(a)
                boundary.extend(additions[order])
            conforming.append(boundary)
        polys=conforming
        oldnormal=np.cross(p[1]-p[0],p[2]-p[0]);area=0.
        for poly in polys:
            # Interior fan preserves all boundary segments, including collinear cuts.
            triangles=[poly] if len(poly)==3 else [[np.mean(poly,axis=0),a,b] for a,b in zip(poly,poly[1:]+poly[:1])]
            for center,a,b in triangles:
                normal=np.cross(a-center,b-center);ar=np.linalg.norm(normal)/2
                if ar<1e-10:continue
                assert normal@oldnormal>0
                ids=[vertex(center),vertex(a),vertex(b)]
                if len(set(ids))<3:continue
                faces.append({**f,'v':ids,'parent':parent});area+=ar
        area_errors.append(abs(area-np.linalg.norm(oldnormal)/2))
    vv=np.array(verts);tt=np.array([f['v'] for f in faces]);tri=vv[tt]
    edges=collections.Counter(tuple(sorted(e)) for a,b,c in tt for e in ((a,b),(b,c),(c,a)))
    if set(edges.values())!={2}:
        for edge,count in edges.items():
            if count!=2:print('ARISTA',count,vv[list(edge)].tolist(),[(f['parent'],f['v']) for f in faces if all(i in f['v'] for i in edge)])
    assert set(edges.values())=={2},collections.Counter(edges.values())
    assert max(area_errors)<1e-7
    areas=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1)/2
    patches={k:[] for k in (('R','C','D','Lneg','Lpos') if include_laterals else ('R','C','D'))}
    for i,(f,p) in enumerate(zip(faces,tri)):
        if include_laterals and f['idMat']==115 and np.ptp(p[:,1])<1e-5 and abs(abs(p[0,1])-11.665)<1e-4:
            if p[:,0].min()>=lateral_bounds[0]-1e-6 and p[:,0].max()<=lateral_bounds[1]+1e-6 and p[:,2].min()>=lateral_bounds[2]-1e-6 and p[:,2].max()<=lateral_bounds[3]+1e-6:
                patches['Lneg' if p[0,1]<0 else 'Lpos'].append(i)
        if p[:,1].min()<-8-1e-6 or p[:,1].max()>8+1e-6:continue
        if np.all(abs(p[:,0]-40.25)<1e-5) and f['idMat']==115:
            if p[:,2].min()>=10.6-1e-6 and p[:,2].max()<=11.8+1e-6:patches['R'].append(i)
            if p[:,2].min()>=9-1e-6 and p[:,2].max()<=10.2+1e-6:patches['D'].append(i)
        if f['idMat']==108 and np.all(abs(p[:,2]-12.12)<1e-5) and p[:,0].min()>=37-1e-6 and p[:,0].max()<=38.2+1e-6:patches['C'].append(i)
    info={k:dict(faces=ids,area_m2=float(areas[ids].sum()),min=tri[ids].reshape(-1,3).min(0).tolist(),max=tri[ids].reshape(-1,3).max(0).tolist()) for k,ids in patches.items()}
    assert all(abs(x['area_m2']-19.2)<1e-4 for k,x in info.items() if k in ('R','C','D')),info
    if include_laterals:
        assert abs(info['Lneg']['area_m2']-info['Lpos']['area_m2'])<1e-4
        assert info['Lneg']['area_m2']>0
    save('panos.json',info);save('malla-subdividida.json',dict(vertices=verts,faces=faces))
    volumes=lambda vertices,ff:float(np.einsum('ij,ij->i',vertices[ff[:,0]],np.cross(vertices[ff[:,1]],vertices[ff[:,2]])).sum()/6)
    oldvol=volumes(v,np.array([f['v'] for f in original['faces']]));newvol=volumes(vv,tt)
    assert abs(oldvol-newvol)<1e-4
    variants=[('base',[]),('R',patches['R']),('C',patches['C']),('RC',patches['R']+patches['C']),('D',patches['D'])]
    if include_laterals:variants.extend([(k,patches[k]) for k in ('Lneg','Lpos')]+[('Laterales',patches['Lneg']+patches['Lpos'])])
    for name,chosen in variants:
        chosen=set(chosen);data={'vertices':verts,'faces':[{**f,'idMat':(202 if f['idMat']==108 else 201) if i in chosen else f['idMat']} for i,f in enumerate(faces)]}
        save(name+'.json',data)
        subprocess.run([str(NATIVE),str(B/'localizado_nativo.py'),str(O/(name+'.json')),str(O/(name+'.cbin'))],check=True)
    with (O/'scene.poly').open('w') as fp:
        fp.write(f'{len(verts)} 3 0 0\n')
        for i,p in enumerate(verts):fp.write(f'{i+1} '+ ' '.join(f'{x:.12g}' for x in p)+'\n')
        fp.write(f'{len(faces)} 1\n')
        for i,f in enumerate(faces):fp.write(f'1 0 {i+1}\n3 '+' '.join(str(x+1) for x in f['v'])+'\n')
        fp.write('0\n0\n')
    with (O/'tetgen.log').open('w') as log:
        result=subprocess.run([str(TETGEN),'-pYa20T1e-10',str(O/'scene.poly')],stdout=log,stderr=subprocess.STDOUT)
    assert result.returncode==0,(O/'tetgen.log').read_text()
    convert_tetra()
    save('verificacion-geometrica.json',dict(vertices_originales=len(v),caras_originales=len(original['faces']),vertices_subdivididos=len(verts),caras_subdivididas=len(faces),aristas_todas_dos_caras=True,max_error_area_por_cara_m2=max(area_errors),volumen_firmado_original_m3=oldvol,volumen_firmado_nuevo_m3=newvol,area_total_m2=float(areas.sum()),panos=info))
    print('Preparación geométrica completa',len(verts),len(faces),{k:d['area_m2'] for k,d in info.items()})

def lines(path):
    for line in path.read_text().splitlines():
        s=line.split('#')[0].strip()
        if s:yield s.split()

def convert_tetra():
    nodes=iter(lines(O/'scene.1.node'));header=next(nodes);points={int(x[0]):list(map(float,x[1:4])) for x in nodes}
    ids={x:i for i,x in enumerate(sorted(points))};v=[points[x] for x in sorted(points)]
    elements=iter(lines(O/'scene.1.ele'));next(elements);tets=[[ids[int(i)] for i in x[1:5]] for x in elements]
    boundary=iter(lines(O/'scene.1.face'));next(boundary)
    markers={tuple(sorted(ids[int(i)] for i in x[1:4])):int(x[4])-1 for x in boundary if int(x[4])>0}
    face_map={};tf=[]
    for ti,tet in enumerate(tets):
        ff=[]
        for a in ((1,2,3),(0,3,2),(0,1,3),(0,2,1)):
            face=[tet[i] for i in a]
            # Native MBIN uses normals pointing toward the opposite tetra vertex.
            pp=np.array([v[i] for i in face]);opposite=next(i for i in tet if i not in face)
            if np.cross(pp[1]-pp[0],pp[2]-pp[0])@(np.array(v[opposite])-pp[0])<0:face[1],face[2]=face[2],face[1]
            key=tuple(sorted(face));ff.append([face,markers.get(key,-1),-2]);face_map.setdefault(key,[]).append((ti,len(ff)-1))
        tf.append(ff)
    for key,adj in face_map.items():
        assert len(adj) in (1,2)
        if len(adj)==2:
            (a,af),(b,bf)=adj;tf[a][af][2]=b;tf[b][bf][2]=a
            assert key not in markers
        else:assert key in markers
    pts=np.array(v);ts=np.array(tets)
    volumes=np.abs(np.einsum('ij,ij->i',pts[ts[:,1]]-pts[ts[:,0]],np.cross(pts[ts[:,2]]-pts[ts[:,0]],pts[ts[:,3]]-pts[ts[:,0]])))/6
    model=json.loads((O/'malla-subdividida.json').read_text());mv=np.array(model['vertices']);mf=np.array([f['v'] for f in model['faces']])
    expected=abs(np.einsum('ij,ij->i',mv[mf[:,0]],np.cross(mv[mf[:,1]],mv[mf[:,2]])).sum()/6)
    assert abs(volumes.sum()-expected)<.01,(volumes.sum(),expected)
    assert min(volumes)>1e-10
    with (O/'tetramesh.mbin').open('wb') as fp:
        fp.write(struct.pack('<II',len(tets),len(v)))
        for p in v:fp.write(struct.pack('<3f',*p))
        for tet,faces in zip(tets,tf):
            fp.write(struct.pack('<5i',*tet,1))
            for face,marker,neighbor in faces:fp.write(struct.pack('<5i',*face,marker,neighbor))
    save('verificacion-tetra.json',dict(nodos=len(v),tetraedros=len(tets),volumen_m3=float(volumes.sum()),volumen_esperado_m3=expected,min_volumen_tetra_m3=float(min(volumes)),fronteras_con_marcador=True,vecinos_reciprocos=True))

if __name__=='__main__':prepare()
