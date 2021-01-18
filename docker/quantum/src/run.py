import json
import psi4

from qiskit import BasicAer
from qiskit.aqua import QuantumInstance
from qiskit.chemistry.algorithms.ground_state_solvers.minimum_eigensolver_factories import VQEUCCSDFactory
from qiskit.chemistry.drivers import PySCFDriver, UnitsType, Molecule
from qiskit.chemistry.transformations import FermionicTransformation, FermionicQubitMappingType
from qiskit.aqua.algorithms import NumPyMinimumEigensolver, VQE
from qiskit.chemistry.algorithms.ground_state_solvers import GroundStateEigensolver


def optimize_geometry(geometry, params):
  opt = params.get('optimization', {})

  # Get parameters for optimization
  # Use qiskit parameters if no optimization values are provided
  theory = opt.get('theory', params.get('theory', 'hf'))
  basis = opt.get('basis', params.get('basis', 'cc-pvdz'))
  functional = opt.get('functional', params.get('functional', 'b3lyp'))
  charge = opt.get('charge', params.get('charge', 0))
  multiplicity = opt.get('multiplicity', params.get('multiplicty', 1))

  if theory.lower() == 'dft':
      _theory = functional
      reference = 'ks'
  else:
      _theory = 'scf'
      reference = 'hf'

  if multiplicity == 1:
      reference = 'r' + reference
  else:
      reference = 'u' + reference

  # Create molecule
  geometry.insert(0, f'{charge} {multiplicity}')
  mol = psi4.geometry(('\n').join(geometry))

  # Optimize geometry
  psi4.set_options({'reference': reference})
  psi4.core.be_quiet()
  energy = psi4.optimize(f'{_theory}/{basis}', molecule=mol)
  results = mol.to_dict()

  coords = results['geom']
  geom = []
  for elem, coord in zip(results['elem'], coords.reshape(-1, 3)):
    geom.append([elem, coord])

  return list(coords), geom, energy


def run_calculation(geometry_file, output_file, params, scratch_dir):
  # Read in the geometry from the geometry file
  # This container expects the geometry file to be in .xyz format
  with open(geometry_file) as f:
    atoms, comment, *xyz_structure = f.read().splitlines()

  # Warn the user that molecule should have 3 or fewer atoms
  # TODO: Add warning

  # Optimize geometry if input has been provided
  if params.get('optimization', {}):
    coords, geom, psi4_energy = optimize_geometry(xyz_structure, params)
  else:
    geom, coords = [], []
    for atom in xyz_structure:
      name, vals = atom.split(' ', 1)
      vals = [val for val in vals.split(' ') if val]
      coords.extend(vals)
      geom.append([name, vals])

  # Read the input parameters
  basis = params.get('basis', 'cc-pvdz')
  charge = params.get('charge', 0)
  multiplicity = params.get('multiplicity', 1)
  range_start, range_end = params.get('orbital_reduction', [4, 10])
  orbital_reduction = list(range(range_start, range_end))

  # Set up the molcule, here we can feed data from OpenChemistry
  molecule = Molecule(geometry=geom, charge=charge,
                      multiplicity=multiplicity)

  # Define the classical quantum chemistry driver to get the molecular integrals
  # Also gives us the Hartree-Fock energy and orbital energies if desired
  driver = PySCFDriver(molecule = molecule, unit=UnitsType.ANGSTROM, basis=basis)

  # Generating a small quantum calculation freezing core and throwing away virtuals, 
  # only keeping 2 electrons in 2 orbitals
  transformation = FermionicTransformation(qubit_mapping=FermionicQubitMappingType.JORDAN_WIGNER,
                                           freeze_core=True, orbital_reduction=orbital_reduction)

  # Quantum solver and wave function structure generator (UCCSD)
  vqe_solver = VQEUCCSDFactory(QuantumInstance(BasicAer.get_backend('qasm_simulator')), 
                               include_custom=True, method_doubles='succ_full')

  # Run the smallest quantum simulation
  calc = GroundStateEigensolver(transformation, vqe_solver)
  res = calc.solve(driver)

  cjson = {
    'chemicalJson': 1,
    'atoms': {
      'coords': {
        '3d': coords
      }
    },
    'properties': {
      'ground_state_energy': res.total_energies[0]
    }
  }

  if params.get('optimization', {}):
    cjson['properties']['optimization_energy'] = psi4_energy

  with open(output_file, 'w') as f:
    json.dump(cjson, f)
