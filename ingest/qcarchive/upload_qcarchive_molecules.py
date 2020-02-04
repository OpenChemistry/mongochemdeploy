#!/usr/bin/env python3

import json

import girder_client

import qcfractal.interface as ptl

from convert_to_cjson import convert_to_cjson

# These can be listed using the client
# We might be able to come up with a method to generate these automatically
collection_type = 'OptimizationDataset'
collection_name = 'JGI Metabolite Set 1'
specification = 'default'

# Need to use a girder api key
girder_api_key = ''

gc = girder_client.GirderClient()
gc.authenticate(apiKey=girder_api_key)

client = ptl.FractalClient()

print('Downloading records from:', collection_type, collection_name)
ds = client.get_collection(collection_type, collection_name)
records = ds.status()
num_records = records.shape[0]

print('Number of records found:', num_records)
for i in range(num_records):

    name = records.iloc[i].name

    print('Downloading data for record:', name)

    try:
        record = ds.get_record(name, specification)

        if 'INCOMPLETE' in record.status:
            print(name, 'is incomplete. Skipping')
            continue

        final_molecule = record.get_final_molecule()
        qcjson = json.loads(final_molecule.json())
        id = qcjson['id']

        cjson = convert_to_cjson(qcjson)

        # The id can be used to find the molecule in qcarchive like so:
        # client.query_molecules(id=id)
        provenance = 'qcarchive molecule: ' + id
        params = {
            'cjson': json.dumps(cjson),
            'provenance': provenance
        }

        print('Uploading to girder...')
        gc.post('/molecules', json=params)

    except Exception as exc:
        print('Failed to get records for:', name)
        print('Exception was:', exc)
        continue
