Running the CP2K Docker Container
=================================

In order to run the CP2K docker container, first download the
docker image:

```
docker pull openchemistry/cp2k
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
docker run -v $(pwd):/data openchemistry/cp2k:latest -g /data/geometry.xyz -p /data/parameters.json -o /data/out.cjson -s /data/scratch
```

After the docker container finishes, the output file will be located in
the directory that was mounted. The output file is in `cjson` format.

A json description of the image and some of the options may be obtained via:
```
docker run openchemistry/cp2k -d
```
