import click
import sys
import json

import describe
import run

def describe_callback(ctx, param, value):
    if not value:
        return
    # Print the description object and stop execution of the container if --describe option is passed
    description = json.dumps(describe.get_description(), indent=2)
    click.echo(description, file=sys.stdout)
    ctx.exit()

@click.command()
@click.option('--describe', '-d',
              help='Return an object to std output that describes the expected input and output parameters of this container.',
              is_flag=True, is_eager=True, expose_value=False, callback=describe_callback)
@click.option('--geometry', '-g', 'geometry_file', multiple=True,
              type=click.Path(exists=True, dir_okay=False, resolve_path=True),
              required=True,
              help='The path to the file containing the input geometry')
@click.option('--parameters', '-p', 'parameters_file',
              type=click.Path(exists=True, dir_okay=False, resolve_path=True),
              required=True,
              help='The path to the JSON file containing the input input parameters.')
@click.option('--output', '-o', 'output_file', multiple=True,
              type=click.Path(exists=False, dir_okay=False, resolve_path=True),
              required=True,
              help='The path to the file that will contain the converted calculation output.')
@click.option('--scratch', '-s', 'scratch_dir',
              type=click.Path(exists=False, dir_okay=True, file_okay=False, resolve_path=True),
              required=True,
              help='The path to the directory that will be used as scratch space while running the calculation.')
def main(geometry_file, parameters_file, output_file, scratch_dir):
    with open(parameters_file) as f:
        params = json.load(f)

    for g, o in zip(geometry_file, output_file):
        run.run_calculation(g, o, params, scratch_dir)


if __name__ == '__main__':
    main()
