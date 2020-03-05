#!/usr/bin/env python3

"""
This script converts qcarchive json to cjson

It includes automatic bond detection, since qcarchive
json does not store bonds.
"""

import json

import click

from avogadro.core import Molecule
from avogadro.io import FileFormatManager
from openbabel import OBMol, OBConversion


# Copied from mongochemserver
def avo_convert_str(str_data, in_format, out_format):
    mol = Molecule()
    conv = FileFormatManager()
    conv.read_string(mol, str_data, in_format)

    return conv.write_string(mol, out_format)


# Copied from mongochemserver
def cjson_to_ob_molecule(cjson):
    cjson_str = json.dumps(cjson)
    sdf_str = avo_convert_str(cjson_str, 'cjson', 'sdf')
    conv = OBConversion()
    conv.SetInFormat('sdf')
    conv.SetOutFormat('sdf')
    mol = OBMol()
    conv.ReadString(mol, sdf_str)
    return mol


# Copied from mongochemserver
def autodetect_bonds(cjson):
    mol = cjson_to_ob_molecule(cjson)
    mol.ConnectTheDots()
    mol.PerceiveBondOrders()
    conv = OBConversion()
    conv.SetInFormat('sdf')
    conv.SetOutFormat('sdf')
    sdf_str = conv.WriteString(mol)
    cjson_str = avo_convert_str(sdf_str, 'sdf', 'cjson')
    return json.loads(cjson_str)


def convert_to_cjson(qcjson):
    cjson = {}
    cjson['chemicalJson'] = 1

    # The qcjson geometry is in atomic units. Convert to angstrom.
    for i in range(len(qcjson['geometry'])):
        qcjson['geometry'][i] *= 0.529177249

    cjson['atoms'] = {
        'coords': {
            '3d': qcjson['geometry']
        },
        'elements': {
            'number': qcjson['atomic_numbers']
        }
    }

    # Auto-detect bonds, since qcjson does not store them
    cjson = autodetect_bonds(cjson)

    return cjson


@click.command()
@click.argument('input_file', type=click.File('r'))
@click.argument('output_file', type=click.File('w'))
def main(input_file, output_file):
    qcjson = json.load(input_file)
    cjson = convert_to_cjson(qcjson)
    json.dump(cjson, output_file)


if __name__ == '__main__':
    main()
