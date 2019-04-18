### Building Orca docker image

In this file there are some instructions to build an ORCA docker image for
openchemistry.

1. Download an ORCA tarball from https://orcaforum.kofo.mpg.de/app.php/dlext/
2. Copy the tarball to /path/to/git/openchemistry/mongochemdeploy/docker/orca
3. Build the image using the command below:

docker build -t openchemistry/orca . --build-arg tarball=orca_4_1_2_linux_x86-64_openmpi313.tar.xz
