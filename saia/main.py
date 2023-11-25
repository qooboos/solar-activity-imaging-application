import asyncio
import logging
import threading
from itertools import batched
from pathlib import Path
from time import sleep

import httpx

from .sdo import Channel, IMGInfo, SDOClient


async def download_to_file(client: SDOClient, img: IMGInfo):
    Path("images").mkdir(exist_ok=True)
    print("Downloading:", img.filename)
    await client.get_image(img)
    print("Download finished:", img.filename)


async def main_():
    logging.basicConfig(level=logging.INFO)
    async with httpx.AsyncClient(timeout=300) as http:
        client = SDOClient(http, Path("images"))

        loop = asyncio.new_event_loop()
        t = threading.Thread(target=loop.run_forever, daemon=True)
        t.start()

        async def dl_files(*args):
            file_names = await client.fetch_file_info(*args)
            for imgs in batched(file_names, 20):
                await asyncio.gather(*(download_to_file(client, img) for img in imgs))

        async def async_sleeper():
            while True:
                logging.info("Async sleeper")
                await asyncio.sleep(1)

        asyncio.run_coroutine_threadsafe(async_sleeper(), loop)
        asyncio.run_coroutine_threadsafe(dl_files("2023", "01", "01"), loop)
        asyncio.run_coroutine_threadsafe(dl_files("2023", "01", "02"), loop)
        asyncio.run_coroutine_threadsafe(dl_files("2023", "01", "03"), loop)
        while True:
            logging.info("Main thread heart beat")
            sleep(1)
        return
        years = await client.fetch_years()
        months = await client.fetch_months(years[2])
        days = await client.fetch_days(years[2], months[1])
        file_names = await client.fetch_file_info(years[2], months[1], days[12])
        file_names = [f for f in file_names if f.channel == Channel.AIA131 and f.resolution == 4096]
        for imgs in batched(file_names, 20):
            await asyncio.gather(*(download_to_file(client, img) for img in imgs))


def main():
    asyncio.run(main_())


if __name__ == "__main__":
    main()
