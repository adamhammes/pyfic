import aiohttp
import asyncio


async def get(session, url):
    '''Coroutine for downloading a url'''
    
    async with session.get(url) as response:
        return await response.text()


def download_async(links):
    '''Returns the html for each link (runs asynchronously)'''
    
    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession(loop=loop) as session:
        tasks = (get(session, link) for link in links)
        return loop.run_until_complete(asyncio.gather(*tasks))
