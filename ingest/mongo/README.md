# Overview

Data from an OpenChemistry instance can be dump or restored using a pair of
python scripts. These scripts using the native MongoDB client command `mongo`,
`mongodump` and `mongorestore` to extract and restore the collections.

# Prerequisite

As these scripts use the native MongoDB client it must be installed on the
machine these scripts will be run on. On Ubuntu this requires the installation
of [`mongodb-org-shell`](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/#additional-information)
and [`mongodb-org-tools`](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/#additional-information).

The python dependencies can be install using the the `requirements.txt`:

```bash

pip install -r <path to mongochemdeploy repo>/ingest/mongo/requirements.txt

```

# Dumping all data associated with a particular user

```bash

python <path to mongochemdeploy repo>/ingest/mongo/dump.py -u monogdb://localhost:27020 -l <user login> -o <path to output archive>

```

For example to export all data created by the user `mongochem` to `/tmp/data.tgz`:

```bash

python <path to mongochemdeploy repo>/ingest/mongo/dump.py -u monogdb://localhost:27020 -l mongochem -o /tmp/data.tgz

```

Note that the user associated with the data is also dumped so the data can be restored
without being orphaned.

# Restoring a data dump

```bash

python <path to mongochemdeploy repo>/ingest/mongo/restore.py -u monogdb://localhost:27020 /tmp/data.tgz

```
