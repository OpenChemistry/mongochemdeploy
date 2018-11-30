import sys
import json
from chemml.models.keras.trained import OrganicLorentzLorenz

from openbabel import OBMol, OBConversion

def ob_convert_str(str_data, in_format, out_format):
    mol = OBMol()
    conv = OBConversion()
    conv.SetInFormat(in_format)
    conv.SetOutFormat(out_format)
    conv.ReadString(mol, str_data)

    return (conv.WriteString(mol), conv.GetOutFormat().GetMIMEType())

from avogadro.core import Molecule
from avogadro.io import FileFormatManager

def avo_convert_str(str_data, in_format, out_format):
    mol = Molecule()
    conv = FileFormatManager()
    conv.readString(mol, str_data, in_format)
    return conv.writeString(mol, out_format)

def cjson_to_smiles(cjson):
    cml = avo_convert_str(json.dumps(cjson), 'cjson', 'cml')
    smiles, mime = ob_convert_str(cml, 'cml', 'smiles')
    return smiles

if len(sys.argv) == 1:
    raise Exception("Input File not provided")

input_file = sys.argv[1]

with open(input_file) as f:
    cjson = json.load(f)

smiles = cjson_to_smiles(cjson)

cls = OrganicLorentzLorenz()
cls.load(summary=True)
pred = cls.predict(smiles)

if input_file.lower().endswith('.in'):
    output_file = input_file[:-3] + '.out'
else:
    output_file = input_file + '.out'

with open(output_file, 'w') as f:
    json.dump(pred, f)
