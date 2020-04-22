Installation
------------
    git clone https://github.com/OpenChemistry/mongochemdeploy.git
    cd mongochemdeploy
    pip install -e .

This will install a command line utility called ```ocdeploy``` which is a simple
wrapper around ```docker-compose```, allowing various parts of the stack to be
developed/tested from the host machine. This is designed to be accessed using
the localhost address, any access from remote machines will require additional
configuration.

Bringing up the stack
---------------------

To bring up the stack run the following commands:

    ocdeploy pull
    docker pull openchemistry/jupyterlab:latest
    ocdeploy up

This will bring the complete platform up in a series of docker containers. The
following ports are exposed on the host machine to the loopback address:

- ```8080``` - The Girder server.
- ```8888``` - The single page app.

You will generally want to access ```localhost:8888``` in order to see the
locally deployed development version of the platform in your browser.

Bind mounting development repositories from host
------------------------------------------------

In order to update code that is running in the containers it is possible to bind
mount repositories that exist on the host machine. If any of the following
variables are set in ```<repo>/dev/dev.env``` the repository will be mounted in
the appropriate container.

- ```MONGOCHEMCLIENT``` - The single page app.
- ```MONGOCHEMSERVER``` - The server side Girder plugins.
- ```OPENCHEMISTRYPY``` - The OpenChemistry Python library.
- ```JUPTERLAB_APP_DIR``` - The JupyterLab application directory containing the JupyterLab extensions.

Once ```<repo>/dev/dev.env``` has been update you can bring the stack back up
using ```ocdeploy up```.

Developing MongoChemClient
--------------------------

In order to see updates to the client before publishing, some extra steps may be
needed.

As the [MongoChemClient README](https://github.com/OpenChemistry/mongochemclient/blob/master/README.md)
mentions, `npm` and `Node.js` are required. After obtaining them, install
additional packages using `npm install` in the root MongoChemClient directory as
the README mentions, but building with `npm run build` will not be required
here.

Next, nginx needs to be installed. After installing it, copy the
[sample client site file](nginx/oc_client) into `/etc/nginx/sites-available/`.
Then remove the default soft link in `/etc/nginx/sites-enabled/`, and run
`sudo ln -s /etc/nginx/sites-available/oc_client /etc/nginx/sites-enabled/` to
enable the client site. Restart nginx.

Now, when running `ocdeploy up`, run the command `npm run start` in the
MongoChemClient directory as well. If `localhost:9090` is used instead of
`localhost:8888`, the local MongoChemClient source code will be used instead of
what is in the Docker image. The client page will also update immediately upon
any changes to the source in MongoChemClient.

Bringing down the stack
-----------------------

```ocdeploy down```

Note: That if the ```-v``` option is used the volumes will also be deleted along
with your data.

Troubleshooting
---------------

### Cleaning up old JupyterLab containers

Currenting if the user doesn't successfully logout of the single page app any
containers associated with their notebooks can hang around, this can cause
problems when trying to create new notebook session. The following command can
be using to remove the containers.

     docker ps -a  | grep jupyterlab | awk '{print $1}' |xargs -n1  docker rm
