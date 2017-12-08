import aiohttp
import asyncio
from os.path import basename
from ...report.generator import generate
from ...report.merger import merge


class Http(object):
    def __init__(self, hosts, jsons):
        self.hosts = hosts
        self.jsons = jsons
        self.report_resp = []

    async def _post(self, session, url, jsons, params, report):
        async with session.post('http://' + url, json=jsons, params=params) as response:
            if report and response.status != 404:
                self.report_resp.append(await response.text())
            else:
                await response.text()

    async def _bound_post(self, sem, session, path, workers, rate, skip, report):
        if workers is not None and rate is not None:
            params = {'workers': workers, 'rate': rate}
        else:
            params = None
        async with sem:
            for i in range(len(self.hosts)):
                await self._post(session, self.hosts[i] + path,
                                 self.jsons[i * skip:(i + 1) * skip], params, report)

    async def _post_requests(self, path, workers=None, rate=None, report=False):
        skip = round(len(self.jsons) / len(self.hosts))
        sem = asyncio.Semaphore(50)
        async with aiohttp.ClientSession() as session:
            task = asyncio.ensure_future(self._bound_post(
                sem, session, path, workers, rate, skip, report))
            responses = asyncio.gather(task)
            await responses

    @property
    def report(self):
        return self.report_resp

    def load(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        future = asyncio.ensure_future(self._post_requests('/http/load'))
        loop.run_until_complete(future)
        loop.close()

    def fire(self, workers, rate):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        future = asyncio.ensure_future(
            self._post_requests('/http/fire', workers, rate, report=True))
        loop.run_until_complete(future)
        loop.close()


def execute(pegasus_hosts, test_data, env, workers, rate, file_name, step_name):
    test = Http(pegasus_hosts, test_data)
    test.load()
    test.fire(workers, rate)
    generate(merge(test.report), basename(file_name), step_name, env)
