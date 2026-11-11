"""Ecogramas, concentración temporal y controles de la prueba de dispersión."""
import csv
import json
from collections import defaultdict
from pathlib import Path
import xml.etree.ElementTree as ET

import matplotlib.pyplot as plt
import numpy as np

from analizar_octavas_propuesta import GROUPS, parameters, read
from probar_dispersion_agudos import OCTAVAS, OUT, SEEDS


RESULTS = OUT / 'resultados'
FOCUS = ('F1', 'V04')
COLORS = {'sin_tratamiento': '#7a8792', 'propuesta': '#9b541c', 'R2': '#157b76', 'lateral_neg': '#6355a5'}


def db(energy):
    return 10 * np.log10(max(energy, 1e-30))


def maximum5(energy):
    return np.convolve(energy, np.ones(5), mode='valid').max()


def metrics(energy, t0):
    i = round(t0*1000)
    direct = energy[i-2:i+3].sum()
    window = energy[i+3:i+16]
    peak = maximum5(window)
    room = parameters(energy, t0)
    return dict(pico_3a16_rel_dB=db(peak/direct) if direct > 0 else None, pico_3a16_nivel_dB=db(peak),
                concentracion_3a16_pct=100*peak/window.sum() if window.sum() > 0 else None, nivel_3a16_dB=db(window.sum()),
                pico_3a80_nivel_dB=db(maximum5(energy[i+3:i+80])),
                nivel_3a80_dB=db(energy[i+3:i+80].sum()), nivel_tardio_dB=db(room['E80_total']),
                nivel_total_dB=db(room['total']), D50_pct=room['D50_pct'], C80=room['C80'], EDT=room['EDT'])


def runs():
    entries = defaultdict(list)
    for folder in (OCTAVAS/'calculos', OUT/'calculos'):
        for meta in sorted(folder.glob('*/ejecucion.json')):
            row = json.loads(meta.read_text())
            if row.get('pendiente') or row['frecuencia'] not in (1000, 4000, 8000):
                continue
            if folder.parent == OCTAVAS and row['N'] != 600000:
                continue
            key = (row['N'], row['frecuencia'], row['fuente'], row['variante'])
            entries[key].append(read(meta.parent, row['variante']))
    for row in json.loads((OCTAVAS/'reutilizadas-1000Hz.json').read_text()):
        key = (row['N'], 1000, row['fuente'], row['estado'])
        entries[key].append(read(Path(row['carpeta']), row['estado'], True))
    return entries


def csvsave(name, rows):
    with (RESULTS/name).open('w', newline='', encoding='utf-8-sig') as fp:
        writer = csv.DictWriter(fp, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def audit(entries):
    summary = {'corridas_nuevas': 0, 'max_fraccion_perdidas': 0.0}
    for (n, hz, source, case), group in entries.items():
        for run in group:
            if run['folder'].parent != OUT/'calculos':
                continue
            summary['corridas_nuevas'] += 1
            summary['max_fraccion_perdidas'] = max(summary['max_fraccion_perdidas'], run['fraccion_perdidas'])
            reference = next(r for r in entries[n, hz, source, 'propuesta' if n == 600000 else 'control']
                             if r['semilla'] == run['semilla'])
            cfg, ref = run['cfg'], reference['cfg']
            for tag in ('sources', 'recepteursp'):
                assert ET.tostring(cfg.find(tag)) == ET.tostring(ref.find(tag))
            for key, value in ref.find('simulation').attrib.items():
                if key not in ('modelName', 'tetrameshFileName'):
                    assert cfg.find('simulation').get(key) == value, (run['folder'], key)
            materials = {m.get('id'): m for m in cfg.find('surface_absorption_enum')}
            for original in ref.find('surface_absorption_enum'):
                actual = materials[original.get('id')]
                assert actual.attrib == original.attrib
                for a, b in zip(actual, original):
                    if hz != 1000 or int(a.get('freq')) == hz:
                        assert a.attrib.keys() == b.attrib.keys()
                        assert all(float(a.get(k)) == float(v) for k, v in b.attrib.items())
            if case != 'control':
                surfaces = json.loads((OUT/'superficies.json').read_text())
                original = materials[str(surfaces[case]['material'])]
                modified = materials['401']
                for a, b in zip(original, modified):
                    expected = dict(a.attrib)
                    if int(a.get('freq')) == hz and hz in (4000, 8000):
                        expected.update(diffusion=str(run['dispersion']), loi='2')
                    assert expected == b.attrib
            if hz == 1000:
                checks = [(r, metrics(run['curves'][r], t0), metrics(reference['curves'][r], t0)) for r, t0 in run['t0'].items()]
                summary['control_1000Hz'] = dict(caso=case, fuente=source, semilla=run['semilla'], receptores=len(checks),
                    max_abs_delta_D50_pp=max(abs(a['D50_pct']-b['D50_pct']) for _, a, b in checks),
                    max_abs_delta_C80_dB=max(abs(a['C80']-b['C80']) for _, a, b in checks))
    (RESULTS/'verificacion.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')


def analyze(entries):
    means, seed_rows = [], []
    curves = {}
    for (n, hz, source, case), group in sorted(entries.items()):
        seeds = sorted(r['semilla'] for r in group)
        if n == 600000 and seeds != SEEDS:
            continue
        reference_case = 'propuesta' if n == 600000 else 'control'
        ref = {r['semilla']: r for r in entries[n, hz, source, reference_case]}
        assert all(seed in ref for seed in seeds)
        group = sorted(group, key=lambda r: r['semilla'])
        for receptor, t0 in group[0]['t0'].items():
            energy = np.mean([r['curves'][receptor] for r in group], axis=0)
            baseline = np.mean([ref[s]['curves'][receptor] for s in seeds], axis=0)
            keys = dict(N=n, frecuencia=hz, fuente=source, caso=case, receptor=receptor)
            def comparison(e, b):
                values = metrics(e, t0)
                original = metrics(b, t0)
                return {**values, **{f'delta_{k}': v-original[k] if v is not None and original[k] is not None else None
                                     for k, v in values.items()}}
            means.append(dict(**keys, semillas=len(seeds), **comparison(energy, baseline)))
            for run in group:
                seed = run['semilla']
                seed_rows.append(dict(**keys, semilla=seed, **comparison(run['curves'][receptor], ref[seed]['curves'][receptor])))
            curves[n, hz, source, case, receptor] = (t0, energy)
    return means, seed_rows, curves


def plot_focus(curves):
    fig, axes = plt.subplots(2, 2, figsize=(12, 7), layout='constrained')
    for hz, row in zip((4000, 8000), axes):
        t0, reference = curves[600000, hz, FOCUS[0], 'propuesta', FOCUS[1]]
        i = round(t0*1000)
        direct = reference[i-2:i+3].sum()
        for case, color in COLORS.items():
            key = (600000, hz, FOCUS[0], case, FOCUS[1])
            if key not in curves:
                continue
            _, energy = curves[key]
            times = np.arange(-5, 151)
            y = np.convolve(energy, np.ones(5), mode='same')[i+times]
            y = 10*np.log10(np.maximum(y/direct, 1e-9))
            for ax in row:
                ax.plot(times, y, color=color, lw=1.5, label=case.replace('_', ' '))
        for ax, end in zip(row, (25, 145)):
            ax.axvspan(3, 16, alpha=.11, color='#c5a758')
            ax.axvline(0, color='#444', lw=.7, ls=':')
            ax.set(xlim=(-4, end), ylim=(-25, 5), title=f'{hz:,} Hz'.replace(',', '.'),
                   xlabel='Tiempo desde el directo (ms)', ylabel='Energía en 5 ms (dB relativos)')
            ax.grid(alpha=.16)
    axes[1, 1].legend(loc='lower left', ncol=2, fontsize=8)
    fig.suptitle('F1–V04 · comparación de ecogramas · referencia común: directo de la propuesta')
    fig.savefig(RESULTS/'ecogramas-F1-V04.png', dpi=170)
    plt.close(fig)


def plot_spatial(means):
    rows = [r for r in means if r['N'] == 600000 and r['frecuencia'] == 8000 and r['caso'] in ('R2', 'lateral_neg')]
    if not rows:
        return
    cases = [(r['caso'], r['fuente']) for r in rows]
    cases = list(dict.fromkeys(cases))
    receptors = list(dict.fromkeys(p for _, p in GROUPS['frente_media'])) + ['P8', 'P9']
    indices = {(r['caso'], r['fuente'], r['receptor']): r for r in rows}
    fig, axes = plt.subplots(1, 2, figsize=(12, max(3.2, len(cases)*.60)), layout='constrained')
    for ax, field, label in zip(axes, ('pico_3a80_nivel_dB', 'nivel_3a80_dB'), ('Pico de 5 ms', 'Energía integrada')):
        matrix = np.array([[indices[case, src, p]['delta_'+field] for p in receptors] for case, src in cases])
        limit = max(abs(matrix).max(), .1)
        image = ax.imshow(matrix, cmap='RdBu_r', vmin=-limit, vmax=limit, aspect='auto')
        for i, row in enumerate(matrix):
            for j, val in enumerate(row):
                ax.text(j, i, f'{val:+.1f}', ha='center', va='center', fontsize=8,
                        color='white' if abs(val) > .65*limit else '#20242a')
        ax.set(xticks=range(len(receptors)), xticklabels=receptors, yticks=range(len(cases)),
               yticklabels=[f'{case} · {src}' for case, src in cases], title=label)
        fig.colorbar(image, ax=ax, label='Cambio (dB)')
    fig.suptitle('8 kHz · 3–80 ms · cambio respecto a la propuesta mixta')
    fig.savefig(RESULTS/'cambios-por-butaca-8k.png', dpi=170)
    plt.close(fig)


def zones(means, seed_rows):
    seed_deltas = defaultdict(list)
    for row in seed_rows:
        if row['N'] == 600000:
            key = (row['frecuencia'], row['caso'], row['fuente'], row['receptor'])
            seed_deltas[key].append(row['delta_pico_3a80_nivel_dB'])
    groups = defaultdict(list)
    for row in means:
        if row['N'] != 600000 or row['caso'] not in ('R2', 'lateral_neg'):
            continue
        pair = (row['fuente'], row['receptor'])
        for name in ('frente_media', 'P8_P9', 'posteriores', 'platea_baja', 'bajo_balcon'):
            if pair in GROUPS[name]:
                groups[row['frecuencia'], row['caso'], row['fuente'], name].append(row)
    summary = []
    for (hz, case, source, zone), group in sorted(groups.items()):
        peaks = [r['delta_pico_3a80_nivel_dB'] for r in group]
        count = sum(all(v < 0 for v in seed_deltas[hz, case, source, r['receptor']]) for r in group)
        average = {f'media_delta_{key}': np.mean([r[f'delta_{key}'] for r in group])
                   for key in ('nivel_3a80_dB', 'nivel_tardio_dB', 'nivel_total_dB', 'C80', 'D50_pct', 'EDT')}
        summary.append(dict(frecuencia=hz, caso=case, fuente=source, zona=zone, receptores=len(group),
                            pico_baja_tres_semillas=count, media_delta_pico_3a80_dB=np.mean(peaks),
                            mayor_aumento_pico_3a80_dB=max(peaks), **average))
    return summary


if __name__ == '__main__':
    RESULTS.mkdir(exist_ok=True)
    entries = runs()
    audit(entries)
    means, seeds, curves = analyze(entries)
    csvsave('medias.csv', means)
    csvsave('por-semilla.csv', seeds)
    if summary := zones(means, seeds):
        csvsave('por-zona.csv', summary)
    plot_focus(curves)
    plot_spatial(means)
