import requests
import asyncio
import aiohttp
import time
from concurrent.futures import ThreadPoolExecutor






def get_url(url):
    res = requests.get(url)
    
    print(res.status_code, time.strftime('%a %H:%M:%S'), sep=' | ')
    return res

list_of_urls = []
for _ in range(2):
    for i in range(490):
        list_of_urls.append('https://www.ncpub.org/_web/search/commonsearch.aspx?mode=parid')
    with ThreadPoolExecutor(max_workers=50) as pool:
        print(list(pool.map(get_url,list_of_urls)))
    



# async def get(url):
#     try:
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url=url) as response:
#                 resp = await response.read()
#                 print("Successfully got url {} with response of length {}.".format(url, len(resp)))
#                 print()
#     except Exception as e:
#         print("Unable to get url {} due to {}.".format(url, e.__class__))


# async def main(urls, amount):
#     ret = await asyncio.gather(*[get(url) for url in urls])
#     print("Finalized all. ret is a list of len {} outputs.".format(len(ret)))



    

