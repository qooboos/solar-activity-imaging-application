from io import BufferedWriter, TextIOWrapper
import logging
import httpx
from bs4 import BeautifulSoup
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Self

URL = "https://sdo.gsfc.nasa.gov/assets/img/browse"


class Channel(Enum):
    AIA193 = "0193"
    AIA304 = "0304"
    AIA171 = "0171"
    AIA211 = "0211"
    AIA131 = "0131"
    AIA335 = "0335"
    AIA094 = "0094"
    AIA1600 = "1600"
    AIA1700 = "1700"
    AIA211193171 = "211193171"
    AIA304211171 = "304211171"
    AIA094335193 = "094335193"
    AIA171HMIB = "HMI171"
    HMI_Magnetogram = "HMIB"
    HMI_Colorized_Magnetogram = "HMIBC"
    HMI_Intensitygram_Colored = "HMIIC"
    HMI_Intensitygram_Flattened = "HMIIF"
    HMI_Intensitygram = "HMII"
    HMI_Dopplergram = "HMID"


@dataclass
class IMGInfo:
    # 20120213_235957_1024_0304.jpg
    filename: str
    datetime_: datetime
    resolution: int
    channel: Channel

    @classmethod
    def from_filename(cls, filename: str) -> Self | None:
        date, time, resolution, channel = filename.removesuffix(".jpg").split("_")
        try:
            return cls(
                filename,
                datetime(
                    year=int(date[:4]),
                    month=int(date[4:6]),
                    day=int(date[6:]),
                    hour=int(time[:2]),
                    minute=int(time[2:4]),
                    second=int(time[4:]),
                ),
                int(resolution),
                Channel(channel),
            )
        except ValueError:
            logging.warning(f"Invalid filename: {filename}")
            return None


class SDOClient:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def fetch_table(self, path: str, remove_suffix: str = ""):
        r = await self.client.get(URL + path)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        a_tags = soup.body.pre.find_all("a")[5:]  # type: ignore
        return map(lambda a: a.text.removesuffix(remove_suffix), a_tags)

    async def fetch_years(self):
        return list(await self.fetch_table("/", "/"))

    async def fetch_months(self, year: str):
        return list(await self.fetch_table(f"/{year}/", "/"))

    async def fetch_days(self, year: str, month: str):
        return list(await self.fetch_table(f"/{year}/{month}/", "/"))

    async def fetch_file_info(self, year: str, month: str, day: str) -> list[IMGInfo]:
        filenames = await self.fetch_table(f"/{year}/{month}/{day}/")
        return list(filter(None, map(IMGInfo.from_filename, filenames)))

    async def download_image(self, image_info: IMGInfo, f: BufferedWriter):
        dt = image_info.datetime_
        url = "/".join(
            [
                URL,
                str(dt.year),
                str(dt.month).zfill(2),
                str(dt.day).zfill(2),
                image_info.filename,
            ]
        )

        async with self.client.stream("GET", url) as r:
            r.raise_for_status()
            async for chunk in r.aiter_raw(4096):
                f.write(chunk)
