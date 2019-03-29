import json
from chemml.models.keras.trained import OrganicLorentzLorenz

def run_calculation(geometry_file, output_file):

    with open(geometry_file) as f:
        smiles = f.read()

    cls = OrganicLorentzLorenz()
    cls.load(summary=True)
    pred = cls.predict(smiles)

    properties = {
        "refractiveIndex": pred[0],
        "polarizability": pred[1],
        "density": pred[2]
    }

    # We will only output the properties
    cjson = {
        'properties': properties
    }

    with open(output_file, 'w') as f:
        json.dump(cjson, f)
