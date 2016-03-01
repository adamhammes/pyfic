import aiohttp
import asyncio


async def get(session, url):
    """
    A wrapper for a coroutine to asynchronously download a web page
    :param session: The managing session
    :param url: The link to dowload
    :return: The html at the url given
    """
    async with session.get(url) as response:
        return await response.text()


def download_async(links):
    """
    Download the given links asynchronously
    :param links: An iterable containing the urls to download
    :return: The html for each given link
    """
    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession(loop=loop) as session:
        tasks = (get(session, link) for link in links)
        return loop.run_until_complete(asyncio.gather(*tasks))
