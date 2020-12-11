import openchemistry as oc
import json
import click

def read_raw(software, f):
    s = software.lower()
    if s == 'psi4':
        return oc.Psi4Reader(f).read()
    elif s == 'nwchem':
        return oc.NWChemJsonReader(f).read()
    else:
        raise Exception('Cannot convert calculation from ' + software + ' to cjson.')

def remember_software(params):
    software = params.get('software')
    version = params.get('version')

    if software is None:
        raise Exception('The parameters file must include the software used to run the calculation.')

    # These software and version do not need to be kept as input parameters
    del params['software']
    if version is not None:
        del params['version']

    return (software, version)

@click.command('convert')
@click.option('-r', '--raw', default=None,
              help='The raw calculation to process.', required=True)
@click.option('-p', '--parameters', default=None,
              help='The parameters file.', required=True)
@click.argument('dump_path', type=click.Path(), required=True)
def main(raw, parameters, dump_path):
    # Read the parameters
    with open(parameters) as f:
      params = json.loads(f.read())

    software, version = remember_software(params)

    # Convert the raw output file into cjson
    with open(raw) as f:
      cjson = read_raw(software, f)

    # Save the calculation parameters in the cjson output for future reference
    cjson['inputParameters'] = params
    cjson['image'] = { 'repository': 'openchemistry/' + software }
    cjson['code'] = { 'version': version }

    with open(dump_path, 'w') as f:
        json.dump(cjson, f)

if __name__ == '__main__':
    main()
