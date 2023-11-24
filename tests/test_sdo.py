from datetime import datetime as dt
from pathlib import Path
from unittest.mock import AsyncMock

import httpx
import pytest
import pytest_asyncio

from saia.sdo import Channel, IMGInfo, SDOClient


def render_html_with_table(elements: list[str]) -> str:
    def render_a_tag(text: str) -> str:
        return " " * 12 + f'<a href="{text}">{text}</a>'

    joined_tags = "\n".join(render_a_tag(e) for e in elements)
    return f"""
<html>
    <head>
        <title>Index of /assets/img/browse</title>
    </head>
    <body>
        <pre>
            <h1>Index of /assets/img/browse</h1>
            <a href="?C=N;O=D">Name</a>
            <a href="?C=M;O=A">Last modified</a>
            <a href="?C=S;O=A">Size</a>
            <a href="?C=D;O=A">Description</a><hr><img src="/icons/back.gif">
            <a href="/assets/img/">Parent Directory</a>
{joined_tags}
        </pre>
    </body>
</html>
        """


def mock_response(status_code: int, **kwargs):
    def side_effect(url):
        return httpx.Response(status_code, request=httpx.Request("GET", url), **kwargs)

    return AsyncMock(side_effect=side_effect)


@pytest_asyncio.fixture
async def client(tmpdir: Path):
    async with httpx.AsyncClient() as http_client:
        yield SDOClient(http_client, tmpdir)


@pytest.mark.asyncio
async def test_get_years(client: SDOClient):
    # given
    client.client.get = mock_response(
        200, text=render_html_with_table(["2018/", "2019/", "2020/", "2021/", "2022/"])
    )

    # when
    years = await client.fetch_years()

    # then
    assert years == ["2018", "2019", "2020", "2021", "2022"]


@pytest.mark.asyncio
async def test_get_months(client: SDOClient):
    # given
    client.client.get = mock_response(
        200, text=render_html_with_table(["01/", "02/", "03/", "03/", "04/"])
    )

    # when
    months = await client.fetch_months("2020")

    # then
    assert months == ["01", "02", "03", "03", "04"]


@pytest.mark.asyncio
async def test_get_days(client: SDOClient):
    # given
    client.client.get = mock_response(
        200, text=render_html_with_table(["01/", "02/", "03/", "03/", "04/"])
    )

    # when
    days = await client.fetch_days("2020", "01")

    # then
    assert days == ["01", "02", "03", "03", "04"]


@pytest.mark.asyncio
async def test_get_file_info(client: SDOClient):
    # given
    client.client.get = mock_response(
        200,
        text=render_html_with_table(
            [
                "20231020_000000_1024_HMIB.jpg",
                "20231020_000000_2048_HMIIF.jpg",
            ]
        ),
    )

    # when
    files = await client.fetch_file_info("2023", "10", "20")

    # then
    assert files == [
        IMGInfo(
            "20231020_000000_1024_HMIB.jpg",
            dt(2023, 10, 20, 0, 0, 0, 0),
            1024,
            Channel.HMI_Magnetogram,
        ),
        IMGInfo(
            "20231020_000000_2048_HMIIF.jpg",
            dt(2023, 10, 20, 0, 0, 0, 0),
            2048,
            Channel.HMI_Intensitygram_Flattened,
        ),
    ]
