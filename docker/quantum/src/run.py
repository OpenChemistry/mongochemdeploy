import json

from qiskit import BasicAer
from qiskit.aqua import QuantumInstance
from qiskit.chemistry.algorithms.ground_state_solvers.minimum_eigensolver_factories import VQEUCCSDFactory
from qiskit.chemistry.drivers import PySCFDriver, UnitsType, Molecule
from qiskit.chemistry.transformations import FermionicTransformation, FermionicQubitMappingType
from qiskit.aqua.algorithms import NumPyMinimumEigensolver, VQE
from qiskit.chemistry.algorithms.ground_state_solvers import GroundStateEigensolver

def run_calculation(geometry_file, output_file, params, scratch_dir):
  # Read in the geometry from the geometry file
  # This container expects the geometry file to be in .xyz format
  with open(geometry_file) as f:
      # remove the first two lines in the xyz file
      # (i.e. number of atom and optional comment)
      xyz_structure = f.readlines()[2:]
      # restructure geometry as 2D array
      ## TODO: can use named tuple or data class?
      geom = []
      for line in xyz_structure:
        data = [i for i in line.split(' ') if i]
        name = data[0]
        vals = [float(v) for v in data[1:]]
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
    'geometry': geom,
    'total_energies': res.total_energies[0]
  }

  with open(output_file, 'w') as f:
    json.dump(cjson, f)
