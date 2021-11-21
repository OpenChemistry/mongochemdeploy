import os
import tarfile
from chemml.models import MLP
from chemml.chem import Molecule
from chemml import datasets
from chemml.preprocessing import ConstantColumns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from chemml.chem import RDKitFingerprint

def run_calculation(output_file, params, scratch_dir):
    nhidden = params.get('nhidden', 4)
    nneurons = params.get('nneurons', [256,128,64,32])
    activations = params.get('activations', ['relu','relu','relu','relu'])
    nepochs = params.get('nepochs', 100)
    batch_size = params.get('batch_size', 75)
    loss = params.get('loss', 'mean_absolute_error')
    regression = params.get('regression', True)


    mlp = MLP(nhidden=nhidden, nneurons=nneurons, activations=activations, nepochs=nepochs,
              batch_size=batch_size, loss=loss, regression=regression)

    smiles, targets, features = datasets.load_organic_density()
    molecules = [Molecule(smi, input_type='smiles') for smi in smiles['smiles']]

    rd = RDKitFingerprint(fingerprint_type='morgan',n_bits=1024)
    fingerprints = rd.represent(molecules)

    # Removing Constant Columns
    # print('... Removing Constant Columns ...')
    # print('Original dataset dimensions: ',fingerprints.shape)
    # cc = ConstantColumns()
    # fingerprints_reduced = cc.fit_transform(fingerprints)
    # print('Reduced dataset dimensions: ',fingerprints_reduced.shape)

    xscale = StandardScaler()
    yscale = StandardScaler()

    X_train, X_test, y_train, y_test = train_test_split(fingerprints, targets, test_size=0.25, random_state=42)
    y_train = yscale.fit_transform(y_train)

    mlp.fit(X = X_train, y = y_train)

    prefix = 'model'

    mlp.save(path=scratch_dir,filename=prefix)

    tmp_csv_filename = os.path.join(scratch_dir, '%s_chemml_model.csv' % prefix)
    csv_filename = os.path.join(scratch_dir, '%s.csv' % prefix)
    h5_filename = os.path.join(scratch_dir, '%s.h5' % prefix)

    # Use relative path to refer to h5 file inside the csv
    with open(tmp_csv_filename, 'r') as f:
        csv_content = f.read()

    csv_content = csv_content.replace(h5_filename, 'model.h5')

    with open(csv_filename, 'w') as f:
        f.write(csv_content)

    with tarfile.open(output_file, 'w') as tar:
        for filename in [csv_filename, h5_filename]:
            tar.add(filename, arcname=os.path.basename(filename))

    # tmp_dir = os.path.join(scratch_dir, 'tmp')
    # os.mkdir(tmp_dir)
    # with tarfile.open(output_file, 'r') as tar:
    #     tar.extractall(tmp_dir)

    # os.chdir(tmp_dir)

    # loaded_MLP = MLP()
    # loaded_MLP = loaded_MLP.load("model.csv")
    # mols = [Molecule("C1CSC(CS1)c1ncc(s1)CC1CCCC1", "smiles"), Molecule("C1CSC(CS1)c1ncc(s1)CC1CCCC1", "smiles")]
    # fingerprints = rd.represent(mols)

    # # cm = CoulombMatrix(cm_type='SC', n_jobs=-1)

    # # features = cm.represent(mols)
    # # # y_pred = loaded_MLP.predict(X_test)
    # y_pred = loaded_MLP.predict(fingerprints)
    # print(loaded_MLP, y_pred)
