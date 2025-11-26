import datetime
from pathlib import Path
from typing import Any, Dict

import pytest

from bioio_sldy.reader import Reader

RESOURCE_DIR = Path(__file__).parent / "resources"

TEST_CASES = [
    pytest.param(
        "s1_t1_c2_z40.dir",
        {
            "Binning": None,
            "Column": None,
            "Dimensions Present": "TCZYX",
            "Image Size C": 2,
            "Image Size T": 1,
            "Image Size X": 1776,
            "Image Size Y": 1736,
            "Image Size Z": 40,
            "Imaged By": None,
            "Imaging Datetime": datetime.datetime(2023, 4, 24, 0, 37, 55),
            "Objective": "20x NA 0.80000001",
            "Pixel Size X": 0.3820158766750814,
            "Pixel Size Y": 0.3820158766750814,
            "Pixel Size Z": None,
            "Position Index": 0,
            "Row": None,
            "Timelapse": True,
            "Timelapse Interval": datetime.timedelta(seconds=1800),
            "Total Time Duration": datetime.timedelta(
                days=3, seconds=28800, microseconds=77000
            ),
        },
        id="s1_t1_c2_z40",
    ),
    pytest.param(
        "s1_t10_c1_z5.dir",
        {
            "Binning": None,
            "Column": None,
            "Dimensions Present": "TCZYX",
            "Image Size C": 1,
            "Image Size T": 10,
            "Image Size X": 1776,
            "Image Size Y": 1736,
            "Image Size Z": 5,
            "Imaged By": None,
            "Imaging Datetime": datetime.datetime(2022, 7, 27, 15, 36, 36),
            "Objective": "20x NA 0.80000001",
            "Pixel Size X": 0.38388850322622897,
            "Pixel Size Y": 0.38388850322622897,
            "Pixel Size Z": None,
            "Position Index": 0,
            "Row": None,
            "Timelapse": True,
            "Timelapse Interval": datetime.timedelta(seconds=1200),
            "Total Time Duration": datetime.timedelta(
                seconds=86396, microseconds=755000
            ),
        },
        id="s1_t10_c1_z5",
    ),
]


@pytest.mark.parametrize("filename, expected_dict", TEST_CASES)
def test_sldy_standard_metadata(filename: str, expected_dict: Dict[str, Any]) -> None:
    # Arrange
    reader = Reader(RESOURCE_DIR / filename)

    # Act
    sm_dict = reader.standard_metadata.to_dict()

    # Assert
    for key, expected in expected_dict.items():
        assert key in sm_dict, f"Key '{key}' missing from standard_metadata.to_dict()"
        result = sm_dict[key]

        # timedelta: allow slight tolerance
        if isinstance(expected, datetime.timedelta):
            assert isinstance(result, datetime.timedelta)
            diff = abs(result.total_seconds() - expected.total_seconds())
            assert (
                diff < 1e-3
            ), f"{key} expected {expected}, got {result} (delta={diff}s)"

        # floats: approx compare
        elif isinstance(expected, float):
            assert result == pytest.approx(expected, rel=1e-9, abs=1e-12)

        # exact match for everything else
        else:
            assert result == expected, f"{key} expected {expected}, got {result}"
