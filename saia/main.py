import asyncio
from itertools import batched
from pathlib import Path

import httpx

from .sdo import Channel, IMGInfo, SDOClient


async def download_to_file(client: SDOClient, img: IMGInfo):
    Path("images").mkdir(exist_ok=True)
    print("Downloading:", img.filename)
    await client.get_image(img)
    print("Download finished:", img.filename)


async def main_():
    async with httpx.AsyncClient() as http:
        http.timeout = 300
        client = SDOClient(http, Path("images"))
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
