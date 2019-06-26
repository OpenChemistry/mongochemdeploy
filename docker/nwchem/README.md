Running the NWChem Docker Container
=================================

In order to run the NWChem docker container, first download the
docker image:

```
docker pull openchemistry/nwchem
```

Two input files are required: a geometry file and a parameters file.
The geometry file should be in `xyz` or `cjson` format. The
parameters file should be in `json` format. Example input files are provided
[here](example). Look in the example parameters file to see the different
parameters that may be set.

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
docker run -v $(pwd):/data openchemistry/nwchem:latest -g /data/geometry.xyz -p /data/parameters.json -o /data/out.cjson -s /data/scratch
```

After the docker container finishes, the output file will be located in
the directory that was mounted. The output file is in `cjson` format.
