import os
import subprocess
import jinja2

def run_calculation(geometry_file, output_file, params):
    # Read in the geometry from the geometry file
    # This container expects the geometry file to be in .xyz format
    with open(geometry_file) as f:
        xyz_structure = f.read()
        # remove the first two lines in the xyz file
        # (i.e. number of atom and optional comment)
        xyz_structure = xyz_structure.split('\n')[2:]
        xyz_structure = '\n  '.join(xyz_structure)

    # Read the input parameters
    theory = params.get('theory', 'hf')
    task = params.get('task', 'energy')
    basis = params.get('basis', 'cc-pvdz')
    functional = params.get('functional', 'b3lyp')
    charge = params.get('charge', 0)
    multiplicity = params.get('multiplicity', 1)

    if theory.lower() == 'ks':
        _theory = functional
    else:
        _theory = 'scf'
    
    reference = theory.lower()

    if multiplicity == 1:
        reference = 'r' + reference
    else:
        reference = 'u' + reference

    optimization = params.get('optimization', None)
    vibrational = params.get('vibrational', None)
    charge = params.get('charge', 0)
    multiplicity = params.get('multiplicity', 1)
    theory = params.get('theory', 'scf')
    functional = params.get('functional', 'b3lyp')
    basis = params.get('basis', 'cc-pvdz')

    context = {
        'task': task,
        'theory': _theory,
        'reference': reference,
        'charge': charge,
        'multiplicity': multiplicity,
        'basis': basis
    }

    # Combine the input parameters and geometry into a concrete input file
    # that can be executed by the simulation code
    template_path = os.path.dirname(__file__)
    jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path),
                                    trim_blocks=True)

    input_file = os.path.join(os.path.dirname(geometry_file), 'psi4.in')
    output_file = os.path.join(os.path.dirname(geometry_file), 'psi4.out')
    with open(input_file, 'wb') as f:
        jinja2_env.get_template('psi4.in.j2').stream(**context, xyz_structure=xyz_structure).dump(f, encoding='utf8')

    # Execute the code and write to output
    subprocess.run(["/usr/local/bin/psi4", input_file, output_file])

    # Convert the raw output file generate by the code execution, into the
    # output format declared in the container description
