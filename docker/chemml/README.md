Running the ChemML Docker Container
=================================

In order to run the ChemML docker container, first download the
docker image:

```
docker pull openchemistry/chemml
```

One input file is required: a geometry file (there are currently
no parameters to set for the ChemML image). The geometry file should
be in SMILES format (`.smi`).

The following options should be specified in the command line:

*After `docker run`:*
* `-v`: Mount the input directory into the docker container.

*After the image name:*
* `-g`: The location of the input geometry in the docker container.
* `-o`: The location and name of the output file in the docker container
        (it should be placed in the mounted directory).
* `-s`: The location of the scratch directory in the docker container.

A complete example can be seen below:

```
cd example/
docker run -v $(pwd):/data openchemistry/chemml:latest -g /data/ethane.smi -o /data/out.cjson -s /data/scratch
```

After the docker container finishes, the output file will be located in
the directory that was mounted. The output file is in `cjson` format,
and it should contain the predicted properties.

A json description of the image and some of the options may be obtained via:
```
docker run openchemistry/chemml -d
```
