# Overview

In addition to creating calculations through a `Jupyterlab` notebook, calculation
files may also be uploaded directly. The following scripts demonstrate how to
convert raw output from `PSI4` or `NWChem` into the required `cjson` format.

# Prerequisite

The python dependencies can be install using the the `requirements.txt`:

```bash

pip install -r <path to mongochemdeploy repo>/ingest/calculations/requirements.txt

```

# Converting from raw output to cjson

```bash

python <postprocess script> -r <raw input> -p <parameters> <output file>
```

The expected parameters file is described in `parameters-description.json` and
examples can be found in the `psi4-example` and `nwchem-example` folders.

#  A complete example of conversion from PSI4 raw output to cjson can be found below:
```bash

cd <path to mongochemdeploy repo>/ingest/calculations
python postprocess.py \
  -r psi4-example/psi4_raw.out \
  -p psi4-example/psi4_parameters.json \
  psi4-example/psi4_result.cjson
```
This example can also be followed with the `NWChem` example folder.

```bash

cd <path to mongochemdeploy repo>/ingest/calculations
python postprocess.py \
  -r nwchem-example/nwchem_raw.json \
  -p nwchem-example/nwchem_parameters.json \
  nwchem-example/nwchem_result.cjson
```
