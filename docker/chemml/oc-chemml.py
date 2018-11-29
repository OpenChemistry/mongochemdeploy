import sys
import json
from chemml.models.keras.trained import OrganicLorentzLorenz

if len(sys.argv) == 1:
    raise Exception("Input File not provided")

input_file = '/data/' + sys.argv[1]

with open(input_file) as f:
    smiles = f.read()

cls = OrganicLorentzLorenz()
cls.load(summary=True)
pred = cls.predict(smiles)

if input_file.endswith('.in'):
    output_file = input_file[:-3] + '.out'
else:
    output_file = input_file + '.out'

with open(output_file, 'w') as f:
    json.dump(pred, f)
