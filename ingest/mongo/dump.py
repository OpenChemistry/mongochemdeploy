import subprocess
import json
import tempfile
from urllib.parse import urlparse

import click


def dump_cmd(mongo_uri, collection, output_path):
    return ['mongodump', '--uri', mongo_uri, '-o', output_path, '-c', collection]

def find_user_id(mongo_uri, login):
    find_by_login = 'JSON.stringify(db.user.findOne({login: "%s"}, {_id: 1}))' % login
    cmd  = ['mongo', mongo_uri, '--quiet', '--eval', find_by_login]

    result = subprocess.check_output(cmd)
    result = json.loads(result)

    if not result:
        raise Exception('Unable to find user: %s' % login)

    return result['_id']

def dump_collection(mongo_uri, name, query, dump_dir):
    cmd = dump_cmd(mongo_uri, name, dump_dir)
    cmd.append('-q')
    cmd.append(json.dumps(query))
    subprocess.check_call(cmd)


def dump_user(mongo_uri, user_id, dump_dir):
    user_query = {
        '_id': user_id
    }

    dump_collection(mongo_uri, 'user', user_query, dump_dir)

def dump_molecules(mongo_uri, user_id, dump_dir):
    molecules_query = {
        'creatorId': user_id
    }

    dump_collection(mongo_uri, 'molecules', molecules_query, dump_dir)

def dump_calculations(mongo_uri, user_id, dump_dir):
    calculations_query = {
        'creatorId': user_id
    }

    dump_collection(mongo_uri, 'calculations', calculations_query, dump_dir)

def create_archive(path, output_path):
    cmd = ['tar', '-C',  path, '-cf', output_path, '-z', 'girder']
    subprocess.check_call(cmd)

@click.command('dump')
@click.option('-l', '--login', default=None,
              help='the login of the girder user to extract data for.', required=True)
@click.option('-u', '--mongo-uri', default='mongodb://localhost:27020',
                help='The URI for the mongo instance.')
@click.argument('dump_path', type=click.Path(), required=True)
def main(login, mongo_uri, dump_path):
    # Default to girder for db name
    parsed = urlparse(mongo_uri)
    if len(parsed.path.strip()) == 0:
        mongo_uri = 'mongodb://%s/girder' % parsed.netloc

    with tempfile.TemporaryDirectory() as tmpdir:
        _id = find_user_id(mongo_uri, login)
        click.echo("Dumping data for user: '%s'" % login)
        dump_user(mongo_uri, _id, tmpdir)
        dump_molecules(mongo_uri, _id, tmpdir)
        dump_calculations(mongo_uri, _id, tmpdir)
        click.echo('Creating archive.')
        create_archive(tmpdir, dump_path)

if __name__ == '__main__':
    main()
