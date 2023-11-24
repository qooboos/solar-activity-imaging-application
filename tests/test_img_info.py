from datetime import datetime as dt

import pytest

from saia.sdo import Channel, IMGInfo


@pytest.mark.parametrize(
    ["file_name", "img_info"],
    [
        [
            "20231020_205317_1024_1700.jpg",
            IMGInfo(
                filename="20231020_205317_1024_1700.jpg",
                datetime_=dt(2023, 10, 20, 20, 53, 17),
                resolution=1024,
                channel=Channel.AIA1700,
            ),
        ],
        [
            "20231020_005238_1024_HMII.jpg",
            IMGInfo(
                filename="20231020_005238_1024_HMII.jpg",
                datetime_=dt(2023, 10, 20, 0, 52, 38),
                resolution=1024,
                channel=Channel.HMI_Intensitygram,
            ),
        ],
        [
            "20231020_201229_512_1700.jpg",
            IMGInfo(
                filename="20231020_201229_512_1700.jpg",
                datetime_=dt(2023, 10, 20, 20, 12, 29),
                resolution=512,
                channel=Channel.AIA1700,
            ),
        ],
        [
            "20231020_061705_512_0193.jpg",
            IMGInfo(
                filename="20231020_061705_512_0193.jpg",
                datetime_=dt(2023, 10, 20, 6, 17, 5),
                resolution=512,
                channel=Channel.AIA193,
            ),
        ],
        [
            "20231020_150050_4096_0335.jpg",
            IMGInfo(
                filename="20231020_150050_4096_0335.jpg",
                datetime_=dt(2023, 10, 20, 15, 0, 50),
                resolution=4096,
                channel=Channel.AIA335,
            ),
        ],
        [
            "20231020_170511_512_094335193.jpg",
            IMGInfo(
                filename="20231020_170511_512_094335193.jpg",
                datetime_=dt(2023, 10, 20, 17, 5, 11),
                resolution=512,
                channel=Channel.AIA094335193,
            ),
        ],
        [
            "20231020_103039_512_1600.jpg",
            IMGInfo(
                filename="20231020_103039_512_1600.jpg",
                datetime_=dt(2023, 10, 20, 10, 30, 39),
                resolution=512,
                channel=Channel.AIA1600,
            ),
        ],
        [
            "20231020_213842_2048_0304.jpg",
            IMGInfo(
                filename="20231020_213842_2048_0304.jpg",
                datetime_=dt(2023, 10, 20, 21, 38, 42),
                resolution=2048,
                channel=Channel.AIA304,
            ),
        ],
        [
            "20231020_220000_3072_HMIBC.jpg",
            IMGInfo(
                filename="20231020_220000_3072_HMIBC.jpg",
                datetime_=dt(2023, 10, 20, 22, 0),
                resolution=3072,
                channel=Channel.HMI_Colorized_Magnetogram,
            ),
        ],
        [
            "20231020_175015_1024_1600.jpg",
            IMGInfo(
                filename="20231020_175015_1024_1600.jpg",
                datetime_=dt(2023, 10, 20, 17, 50, 15),
                resolution=1024,
                channel=Channel.AIA1600,
            ),
        ],
    ],
)
def test_img_info(file_name: str, img_info: IMGInfo):
    # when
    result = IMGInfo.from_filename(file_name)

    # then
    assert result == img_info
