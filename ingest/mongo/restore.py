import tempfile
import subprocess
from urllib.parse import urlparse
from pathlib import Path

import click



def extract(dump_archive_path, output_path):
    cmd = ['tar', '-xvf', dump_archive_path, '-C', output_path]
    subprocess.check_call(cmd)

def restore(mongo_uri, dump_path, db_name):
    sub_dirs = [x for x in Path(dump_path).iterdir() if x.is_dir()]
    # If we have a sub directory, then point restore at that, so we can override
    # the db name if necessary.
    if len(sub_dirs) == 1:
        dump_path = str(sub_dirs[0])

    cmd = ['mongorestore', '--uri', mongo_uri, '--db', db_name, '--noIndexRestore', dump_path]
    subprocess.check_call(cmd)

@click.command('restore')
@click.option('-u', '--mongo-uri', default='mongodb://localhost:27020',
                help='The URI for the mongo instance.')
@click.argument('dump_path', type=click.Path(), required=True)
def main(mongo_uri, dump_path):
    db_name = 'girder'
    # Default to girder for db name
    parsed = urlparse(mongo_uri)
    if len(parsed.path.strip()) == 0:
        mongo_uri = 'mongodb://%s/%s' % (parsed.netloc, db_name)
    else:
        db_name = parsed.path.lstrip('/').strip()

    with tempfile.TemporaryDirectory() as tmpdir:
        click.echo('Extracting data.')
        extract(dump_path, tmpdir)
        click.echo('Restoring data.')
        restore(mongo_uri, tmpdir, db_name)

if __name__ == '__main__':
    main()