import click
import os
import six
import subprocess

@click.group(help='ocdeploy.',
             context_settings=dict(help_option_names=['-h', '--help']))
def main():
  pass

REPO_DIR = os.path.dirname(__file__)

# These need to be set in the environment so they can be used in the docker-compose
# files.
DOCKER_BASE_DIRS = {
    'JUPYTERHUB_DOCKER_DIR': os.path.join(REPO_DIR, 'docker', 'jupyterhub'),
    'DEV_DOCKER_DIR': os.path.join(REPO_DIR, 'docker', 'dev'),
    'GIRDER_DOCKER_DIR': os.path.join(REPO_DIR, 'docker', 'girder')
}

def _load_dev_env():
    env_path = os.path.join(REPO_DIR, 'dev', 'dev.env')
    vars = {}
    with open(env_path) as f:
        for l in  f:
            l = l.rstrip('\n')
            if len(l) == 0 or l.startswith('#'):
                continue
            (name, value) = l.split('=')
            vars[name.strip()] = value.strip();

    return vars

BASE_COMPOSE_FILES = [
    'docker-compose.yml',
    '../girder/docker-compose.yml',
    '../jupyterhub/docker-compose.yml'
]

def _override_files(vars):
    files = []
    for n in vars:
        file = 'docker-compose.%s.yml' % n.lower()
        if os.path.exists(os.path.join(REPO_DIR, 'docker', 'dev', file)):
            files.append(file)

    return files

def _generate_file_switches():
    vars = _load_dev_env()
    overrides = _override_files(vars)
    files = BASE_COMPOSE_FILES + overrides
    switches = []
    for f in files:
        switches.append('-f')
        switches.append(f)

    return switches

def _generate_command(subcommand):
    cmd = _generate_file_switches()
    cmd.insert(0, 'docker-compose')
    cmd.append(subcommand)

    return cmd

def _execute_command(subcommand, args):
    env = _load_dev_env()
    env.update(DOCKER_BASE_DIRS)
    cwd = os.path.join(REPO_DIR, 'docker', 'dev')
    cmd = _generate_command(subcommand)
    cmd += args
    subprocess.call(cmd, cwd=cwd, env=env)

@main.command('up', short_help='Bring up stack.', help='Bring up stack.',
              context_settings=dict(allow_extra_args=True, ignore_unknown_options=True))
@click.pass_context
def up(ctx):
    _execute_command('up', ctx.args)

@main.command('down', short_help='Bring down stack.', help='Bring down stack.',
              context_settings=dict(allow_extra_args=True, ignore_unknown_options=True))
@click.pass_context
def down(ctx):
   _execute_command('down', ctx.args)

@main.command('pull', short_help='Pull images for stack.', help='Pull images for stack.',
              context_settings=dict(allow_extra_args=True, ignore_unknown_options=True))
@click.pass_context
def pull(ctx):
   _execute_command('pull', ctx.args)

@main.command('build', short_help='Build images for stack.', help='Build images for stack.',
              context_settings=dict(allow_extra_args=True, ignore_unknown_options=True))
@click.pass_context
def build(ctx):
   _execute_command('build', ctx.args)

