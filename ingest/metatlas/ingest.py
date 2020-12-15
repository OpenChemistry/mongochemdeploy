import json
import asyncio
import logging
import sys
from pathlib import Path
import signal

from tqdm import tqdm
import click
import aiohttp
import tenacity
import coloredlogs


class AsyncGirderClient(object):

    def __init__(self, session, api_url):
        self._ratelimit_semaphore = asyncio.Semaphore(15)
        self._api_url = api_url.rstrip('/')
        self._session = session

    async def authenticate(self, api_key):
        params = {'key': api_key}
        async with self._session.post('%s/api_key/token' % (self._api_url), params=params) as r:
            r.raise_for_status()
            auth = await r.json()
        self._headers = {
            'Girder-Token': auth['authToken']['token']
        }

    @tenacity.retry(retry=tenacity.retry_if_exception_type(aiohttp.client_exceptions.ServerConnectionError),
                    wait=tenacity.wait_exponential(max=10),
                    stop=tenacity.stop_after_attempt(10))
    async def post(self, path, headers=None, params=None, raise_for_status=True, **kwargs):
        if params is not None:
            params = {k:str(v) for (k,v) in params.items()}

        if headers is None:
            headers = self._headers
        else:
            headers.update(self._headers)

        async with self._ratelimit_semaphore:
            async with self._session.post('%s/%s' % (self._api_url, path),
                                        headers=headers, params=params,
                                        **kwargs) as r:
                if raise_for_status:
                    r.raise_for_status()
                return await r.json()

class BlockKeyboardInterrupt(object):
    def __enter__(self):
        self._signal = None
        self._orignal_handler = signal.signal(signal.SIGINT, self._handler)

    def _handler(self, sig, frame):
        self.signal = (sig, frame)

    def __exit__(self, type, value, traceback):
        signal.signal(signal.SIGINT, self._orignal_handler)
        if self._signal is not None:
            self._orignal_handler(*self._signal)

def _ingested_log_file():
    return Path.home() / '.oc-ingested-log'

ingested = []
def _save_ingested_log():
    with _ingested_log_file().open('w') as fp:
        json.dump(ingested, fp)


async def ingest_molecule(gc, data, index):
    if index not in ingested:
        r = await gc.post('molecules',  raise_for_status=False, json=data)
        ingested.append(index)

        with BlockKeyboardInterrupt():
            _save_ingested_log()

        return r

async def ingest(api_url, api_key, data_file, chunk_size):
    global ingested
    logger = logging.getLogger('ingest')

    if _ingested_log_file().exists():
        logger.info('Retrying, loading ingest state from log.')
        with _ingested_log_file().open() as fp:
            ingested = json.load(fp)

    async with aiohttp.ClientSession() as session:
        gc = AsyncGirderClient(session, api_url)
        await gc.authenticate(api_key)

        logger.info('Loading %s.' % data_file.name)
        documents = json.loads(data_file.read())
        logger.info('File contains %d molecules.' % len(documents))

        logger.info('Ingesting in batches of %d' % chunk_size)

        progress = tqdm(total=len(documents), unit=' structures')
        # Process in chunks so don't run out of memory
        count = 0
        for i in range(0, len(documents), chunk_size):
            chunk = documents[i:i+chunk_size]
            tasks = [ingest_molecule(gc, json.loads(data), i+j) for (j, data) in enumerate(chunk)]
            for f in asyncio.as_completed(tasks):
                await f
                count += 1
                progress.update()
        progress.close()

        logger.info('Ingest complete.')

        if _ingested_log_file().exists():
            _ingested_log_file().unlink()


@click.command('metatlas')
@click.option('-u', '--api-url', default='http://localhost:8080/api/v1', help='RESTful API URL '
                   '(e.g https://girder.example.com/api/v1)')
@click.option('-k', '--api-key', envvar='GIRDER_API_KEY', default=None,
              help='[default: GIRDER_API_KEY env. variable]', required=True)
@click.argument('data_file', type=click.File('r'), required=True)
@click.option('-c', '--chunk-size', default=1000, help='the batch size to ingest molecules in.')
def main(api_url, api_key, data_file, chunk_size):
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = coloredlogs.ColoredFormatter('%(asctime)s,%(msecs)03d - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
    asyncio.run(
        ingest(api_url, api_key, data_file, chunk_size)
    )

if __name__ == '__main__':
    main()