# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub
import os
import six
import warnings


c = get_config()

# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
# Spawn containers from this image
c.DockerSpawner.container_image = os.environ['DOCKER_NOTEBOOK_IMAGE']
# JupyterHub requires a single-user instance of the Notebook server, so we
# default to using the `start-singleuser.sh` script included in the
# jupyter/docker-stacks *-notebook images as the Docker run command when
# spawning containers.  Optionally, you can override the Docker run command
# using the DOCKER_SPAWN_CMD environment variable.
# Connect containers to this Docker network
network_name = os.environ['DOCKER_NETWORK_NAME']
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name
c.DockerSpawner.extra_host_config = { 'network_mode': network_name }
c.DockerSpawner.remove = True
girder_api_url = os.environ.get('OC_INTERNAL_API_URL', 'http://localhost:8080/api/v1')

c.DockerSpawner.volumes = {}

# This is for dev deployment
if 'OPENCHEMISTRYPY' in os.environ and os.environ['OPENCHEMISTRYPY'] != '':
    c.DockerSpawner.volumes[os.environ['OPENCHEMISTRYPY']] = '/home/jovyan/openchemistrypy'

if 'JUPYTERLAB_CJSON' in os.environ and os.environ['JUPTERLAB_CJSON'] != '':
    c.DockerSpawner.volumes[os.environ['JUPTERLAB_CJSON']] = '/home/jovyan/jupyterlab_cjson'

if 'JUPTERLAB_APP_DIR' in os.environ and os.environ['JUPTERLAB_APP_DIR'] != '':
    c.DockerSpawner.volumes[os.environ['JUPTERLAB_APP_DIR']] = '/opt/conda/share/jupyter/lab'

spawn_cmd = os.environ.get('DOCKER_SPAWN_CMD', "start-singleuser.sh")
spawn_cmd += ' --NotebookApp.allow_origin=%s' % os.environ['OC_ORIGIN']
spawn_cmd += " --SingleUserNotebookApp.default_url=/lab"
spawn_cmd += " --NotebookApp.contents_manager_class='girder_jupyter.contents.manager.GirderContentsManager'"
spawn_cmd += " --GirderContentsManager.api_url=%s" % girder_api_url
spawn_cmd += " --GirderContentsManager.root=user/{login}/Private/oc/notebooks"

# Set environment variables needs by the openchemistry package
env_vars_keys = [
    'OC_SITE',
    'OC_ORIGIN',
    'OC_API_URL',
    'OC_INTERNAL_API_URL',
    'OC_APP_URL',
    'OC_JUPYTERHUB_URL'
]

env_vars = { k: os.environ.get(k) for k in env_vars_keys }
c.DockerSpawner.environment.update(env_vars)

c.DockerSpawner.extra_create_kwargs.update({ 'command': spawn_cmd })

# Connect containers to this Docker network
c.DockerSpawner.use_internal_ip = True
# Pass the network name as argument to spawned containers
# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_port = 8080
c.JupyterHub.base_url = '/jupyterhub'
c.JupyterHub.hub_connect_ip = 'jupyterhub'

# TLS config
#c.JupyterHub.port = 443
#c.JupyterHub.ssl_key = os.environ['SSL_KEY']
#c.JupyterHub.ssl_cert = os.environ['SSL_CERT']

# Authenticate users with Girder
c.JupyterHub.authenticator_class = 'girder_jupyterhub.auth.GirderAuthenticator'

c.GirderAuthenticator.api_url = girder_api_url
c.GirderAuthenticator.enable_auth_state = True
if 'JUPYTERHUB_CRYPT_KEY' not in os.environ:
    warnings.warn(
        "Need JUPYTERHUB_CRYPT_KEY env for persistent auth_state.\n"
        "    export JUPYTERHUB_CRYPT_KEY=$(openssl rand -hex 32)"
    )
    c.CryptKeeper.keys = [ os.urandom(32) ]

# Persist hub data on volume mounted inside container
data_dir = os.environ.get('DATA_VOLUME_CONTAINER', '/data')

c.JupyterHub.cookie_secret_file = os.path.join(data_dir,
    'jupyterhub_cookie_secret')

c.JupyterHub.db_url = 'postgresql://postgres:{password}@{host}/{db}'.format(
    host=os.environ['POSTGRES_HOST'],
    password=os.environ['POSTGRES_PASSWORD'],
    db=os.environ['POSTGRES_DB'],
)

# Whitlelist users and admins
#c.Authenticator.whitelist = whitelist = set()
#c.Authenticator.admin_users = admin = set()
#c.JupyterHub.admin_access = True
#pwd = os.path.dirname(__file__)
#with open(os.path.join(pwd, 'userlist')) as f:
#    for line in f:
#        if not line:
#            continue
#        parts = line.split()
#        name = parts[0]
#        whitelist.add(name)
#        if len(parts) > 1 and parts[1] == 'admin':
#            admin.add(name)
