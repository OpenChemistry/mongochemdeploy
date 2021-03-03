Running the Qiskit Docker Container
=================================

In order to run the Qiskit docker container, first build the
docker image:

```
docker build -t openchemistry/qiskit:1.0 .
```

Two input files are required: a geometry file and a parameters file.
The geometry file should be in `xyz` format. The parameters file should be in 
`json` format. Example input files are provided [here](example). Look in the 
example parameters file to see the different parameters that may be set.

The following options should be specified in the command line:

*After `docker run`:*
* `-v`: Mount the input directory into the docker container.

*After the image name:*
* `-g`: The location of the input geometry in the docker container.
* `-p`: The location of the parameters file in the docker container.
* `-o`: The location and name of the output file in the docker container
        (it should be placed in the mounted directory).
* `-s`: The location of the scratch directory in the docker container.

A complete example can be seen below:

```
cd example/
docker run -v $(pwd):/data openchemistry/qiskit:1.0 -g /data/geometry.xyz -p /data/parameters.json -o /data/out.cjson -s /data/scratch
```

Or to optimize the geometry with Psi4 before running the calculation:

```
docker run -v $(pwd):/data openchemistry/qiskit:1.0 -g /data/geometry.xyz -p /data/optimization_parameters.json -o /data/out.cjson -s /data/scratch
```

After the docker container finishes, the output file will be located in
the example directory. The output file is in `cjson` format.

A json description of the image and some of the options may be obtained via:
```
docker run openchemistry/qiskit:1.0 -d
```
