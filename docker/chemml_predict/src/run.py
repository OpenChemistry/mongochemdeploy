import os
import json
import tarfile

from chemml.models import MLP
from chemml.chem import Molecule
from chemml.chem import RDKitFingerprint

def run_calculation(geometry_file, output_file, model_file, params, scratch_dir):

    with open(geometry_file) as f:
        smiles = f.read()

    with tarfile.open(model_file, 'r') as tar:
        tar.extractall(scratch_dir)

    os.chdir(scratch_dir)

    loaded_MLP = MLP()
    loaded_MLP = loaded_MLP.load("model.csv")
    mols = [Molecule(smiles, "smiles")]

    rd = RDKitFingerprint(fingerprint_type='morgan',n_bits=1024)
    fingerprints = rd.represent(mols)

    y_pred = loaded_MLP.predict(fingerprints)

    properties = {
        "predictedValue": y_pred.item()
    }

    cjson = {
        'chemicalJson': 1,
        'smiles': smiles,
        'properties': properties
    }

    with open(output_file, 'w') as f:
        json.dump(cjson, f)
