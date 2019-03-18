import json
from chemml.models.keras.trained import OrganicLorentzLorenz

from openbabel import OBMol, OBConversion
from avogadro.core import Molecule
from avogadro.io import FileFormatManager

def ob_convert_str(str_data, in_format, out_format):
    mol = OBMol()
    conv = OBConversion()
    conv.SetInFormat(in_format)
    conv.SetOutFormat(out_format)
    conv.ReadString(mol, str_data)

    return (conv.WriteString(mol), conv.GetOutFormat().GetMIMEType())

def avo_convert_str(str_data, in_format, out_format):
    mol = Molecule()
    conv = FileFormatManager()
    conv.read_string(mol, str_data, in_format)
    return conv.write_string(mol, out_format)

def cjson_to_smiles(cjson):
    cml = avo_convert_str(json.dumps(cjson), 'cjson', 'cml')
    smiles, _mime = ob_convert_str(cml, 'cml', 'smiles')
    return smiles

def run_calculation(geometry_file, output_file):
    # In the future we can probably accept SMILES directly from the molecule
    # model. For now we need somewhere to put the output, so the CJSON makes
    # more sense.
    with open(geometry_file) as f:
        cjson = json.load(f)

    smiles = cjson_to_smiles(cjson)

    cls = OrganicLorentzLorenz()
    cls.load(summary=True)
    pred = cls.predict(smiles)

    properties = {
        "refractiveIndex": pred[0],
        "polarizability": pred[1],
        "density": pred[2]
    }

    cjson.setdefault('properties', {}).update(properties)

    with open(output_file, 'w') as f:
        json.dump(cjson, f)
