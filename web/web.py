import aiohttp
import asyncio


@asyncio.coroutine
def get(*args, **kwargs):
    response = yield from aiohttp.ClientSession().request('GET', *args, **kwargs)
    return (yield from response.read_and_close())


def download_async(links):
    fetchers = [get(link) for link in links]
    return [(yield from f) for f in asyncio.as_completed(fetchers)]
