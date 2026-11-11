"""Aísla la dispersión de una superficie en la propuesta mixta de I-Simpa."""
import argparse
import copy
import json
import os
import subprocess
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from itertools import product

import numpy as np

from ejecutar_octavas_propuesta import B, O as OCTAVAS, SEEDS, config, save, sha
from ejecutar import ENGINE, native


OUT = B / 'dispersion-agudos'
MODEL = OCTAVAS / 'modelos/propuesta'
CASES = ('control', 'R1', 'R2', 'R3', 'R4', 'fondo', 'lateral_neg', 'lateral_pos')
SCATTERING = 0.60


def prepare():
    OUT.mkdir(exist_ok=True)
    model = json.loads((B / 'reflectores-absorcion-localizada/media_centro_a060/modelo-materiales.json').read_text())
    vertices = np.array(model['vertices'])
    faces = model['faces']
    triangles = vertices[[face['v'] for face in faces]]
    reflectors = [i for i, face in enumerate(faces) if face['idMat'] == 301]
    assert len(reflectors) == 48
    groups = {f'R{i+1}': (301, reflectors[i*12:(i+1)*12]) for i in range(4)}
    wall = np.array([face['idMat'] == 115 for face in faces])
    x, y, z = triangles.transpose(2, 0, 1)
    groups['fondo'] = (115, np.flatnonzero(wall & np.isclose(x, 40.25).all(axis=1)).tolist())
    for side, sign in [('neg', -1), ('pos', 1)]:
        region = np.isclose(y, sign*11.665).all(axis=1) & (x.min(axis=1) >= 20.4-1e-5) & (z.min(axis=1) >= 4.2-1e-5)
        groups[f'lateral_{side}'] = (115, np.flatnonzero(wall & region).tolist())
    areas = np.linalg.norm(np.cross(triangles[:, 1]-triangles[:, 0], triangles[:, 2]-triangles[:, 0]), axis=1)/2
    surfaces = {}
    for case, (material, ids) in groups.items():
        assert ids
        directory = OUT / 'modelos' / case
        directory.mkdir(parents=True, exist_ok=True)
        changes = directory / 'caras.json'
        save(changes, {str(i): 401 for i in ids})
        mesh = directory / 'mesh.cbin'
        native('mesh', MODEL / 'mesh.cbin', mesh, changes)
        surfaces[case] = dict(material=material, area_m2=float(areas[ids].sum()), faces=ids,
                              centro=triangles[ids].reshape(-1, 3).mean(axis=0).tolist(), malla_sha256=sha(mesh))
    save(OUT / 'superficies.json', surfaces)


def run(case, source, freq, particles, seed):
    label = f'{case}-{source}-{freq}Hz-N{particles}-seed{seed}'
    directory = OUT / 'calculos' / label
    directory.mkdir(parents=True, exist_ok=True)
    meta = directory / 'ejecucion.json'
    results = directory / 'resultados-lineales.json'
    if meta.exists() and results.exists():
        return
    config(directory, 'propuesta', source, freq, particles, seed)
    path = directory / 'config.xml'
    mesh = MODEL / 'mesh.cbin'
    if case != 'control':
        surface = json.loads((OUT / 'superficies.json').read_text())[case]
        root = ET.parse(path).getroot()
        materials = root.find('surface_absorption_enum')
        original = next(m for m in materials if m.get('id') == str(surface['material']))
        material = copy.deepcopy(original)
        material.set('id', '401')
        if freq in (4000, 8000):
            band = next(f for f in material if f.get('freq') == str(freq))
            band.set('diffusion', str(SCATTERING))
            band.set('loi', '2')
        assert [f.get('absorb') for f in original] == [f.get('absorb') for f in material]
        materials.append(material)
        mesh = OUT / 'modelos' / case / 'mesh.cbin'
        assert sha(mesh) == surface['malla_sha256']
        root.find('simulation').set('modelName', os.path.relpath(mesh, directory))
        ET.indent(root)
        ET.ElementTree(root).write(path, encoding='utf-8', xml_declaration=True)
    start = time.monotonic()
    with (directory / 'motor.log').open('w') as log:
        subprocess.run([str(ENGINE), str(path)], cwd=directory, stdout=log, stderr=subprocess.STDOUT, check=True)
    native('read', directory)
    data = json.loads(results.read_text())
    assert len(data['receptores']) == 21 and all(len(next(iter(p.values()))) == 4000 for p in data['receptores'].values())
    stats = data['estadisticas'][1]
    lost = (stats[4]+stats[5])/stats[-1]
    assert lost < .005
    save(meta, dict(variante=case, fuente=source, frecuencia=freq, N=particles, semilla=seed,
                    dispersion=SCATTERING if case != 'control' and freq in (4000, 8000) else None,
                    segundos=time.monotonic()-start, fraccion_perdidas=lost, config_sha256=sha(path), malla_sha256=sha(mesh)))
    print(label, round(time.monotonic()-start, 1), 's', flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--cases', nargs='+', choices=CASES, default=CASES)
    parser.add_argument('--sources', nargs='+', choices=['F1', 'F2'], default=['F1', 'F2'])
    parser.add_argument('--freqs', nargs='+', type=int, choices=[1000, 4000, 8000], default=[4000, 8000])
    parser.add_argument('--seeds', nargs='+', type=int, default=SEEDS)
    parser.add_argument('--particles', type=int, default=600000)
    parser.add_argument('--jobs', type=int, default=3)
    args = parser.parse_args()
    if args.prepare:
        prepare()
    tasks = product(args.cases, args.sources, args.freqs, [args.particles], args.seeds)
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        list(pool.map(lambda task: run(*task), tasks))


if __name__ == '__main__':
    main()
