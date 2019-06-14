import json

import torch
import torchani
import ase
import ase.data
import ase.optimize
import ase.vibrations

EV_TO_J_MOL = 96485.33290025658

def _get_ase_atoms(cjson_atoms):
    elements = cjson_atoms.get('elements', {})
    number = elements.get('number')
    if number is None:
        symbol = elements.get('symbol')
        if symbol is None:
            raise Exception('Atomic numbers are missing.')
        number = list(map(lambda sym : ase.data.atomic_numbers[sym], symbol))
    n_atoms = len(number)
    positions = cjson_atoms.get('coords', {}).get('3d', [])
    if len(positions) != 3 * n_atoms:
        raise Exception('Atomic positions are missing.')
    atoms = []
    for i in range(n_atoms):
        atoms.append(ase.Atom(number[i], positions[i * 3 : i * 3 + 3]))
    return atoms

def _get_cjson_atoms(ase_molecule):
    atoms = {
        'coords': {
            '3d': list(ase_molecule.get_positions().flatten())
        },
        'elements': {
            'number': [int(z) for z in ase_molecule.get_atomic_numbers()]
        }
    }
    return atoms

def _get_cjson_vibrations(ase_vibrations):
    n_frequencies = len(ase_vibrations.get_frequencies())
    vibrations = {
        'frequencies': [freq.real for freq in ase_vibrations.get_frequencies()],
        'intensities': [1 for i in range(n_frequencies)],
        'modes': list(range(n_frequencies)),
        'eigenVectors': [list(ase_vibrations.get_mode(i).flatten()) for i in range(n_frequencies)]
    }
    return vibrations

def run_calculation(geometry_file, output_file, params, scratch_dir):
    # In the future we can probably accept SMILES directly from the molecule
    # model. For now we need somewhere to put the output, so the CJSON makes
    # more sense.
    with open(geometry_file) as f:
        cjson = json.load(f)

    atoms = _get_ase_atoms(cjson.get('atoms', {}))

    # Read the input parameters
    theory = params.get('theory', 'ani-1ccx')
    task = params.get('task', 'energy')

    if theory.lower() == 'ani-1x':
        model = torchani.models.ANI1x()
    else:
        model = torchani.models.ANI1ccx()

    calculator = model.ase()
    calculator.device = torch.device('cpu')

    molecule = ase.Atoms(atoms, calculator=calculator)

    cjson_out = {"chemicalJson": 1}

    if task.lower() in ['optimize', 'frequencies']:
        ase.optimize.BFGS(molecule).run(fmax=0.0005)

    cjson_out['atoms'] = _get_cjson_atoms(molecule)
    # Preserve bonds
    if cjson.get('bonds') is not None:
        cjson_out['bonds'] = cjson.get('bonds')

    cjson_out['properties'] = {
        'totalEnergy': molecule.get_potential_energy() * EV_TO_J_MOL
    }

    if task.lower() == 'frequencies':
        vib = ase.vibrations.Vibrations(molecule)
        vib.run()
        cjson_out['vibrations'] = _get_cjson_vibrations(vib)
        vib.clean()

    with open(output_file, 'w') as f:
        json.dump(cjson_out, f)
