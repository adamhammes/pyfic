import aiohttp
import asyncio


async def get(client, url):
    """
    A wrapper for a coroutine to asynchronously download a web page
    :param session: The managing session
    :param url: The link to dowload
    :return: The html at the url given
    """
    async with client.get(url) as response:
        return await response.text()


async def spawn_tasks(links):
    async with aiohttp.ClientSession() as client:
        tasks = [get(client, link) for link in links]
        combined = await asyncio.gather(*tasks)
        return combined


def download_async(links):
    """
    Download the given links asynchronously
    :param links: An iterable containing the urls to download
    :return: The html for each given link
    """

    loop = asyncio.get_event_loop()
    done = loop.run_until_complete(spawn_tasks(links))
    return done
