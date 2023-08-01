#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib
import typing

import numpy as np
import pytest
from bioio_base import dimensions, exceptions, test_utilities

from bioio_sldy import Reader

from .conftest import LOCAL_RESOURCES_DIR


def test_sldy_reader_with_text_file(sample_text_file: pathlib.Path) -> None:
    with pytest.raises(exceptions.UnsupportedFileFormatError):
        test_utilities.run_image_file_checks(
            ImageContainer=Reader,
            image=sample_text_file,
            set_scene=None,
            expected_scenes=None,
            expected_current_scene=None,
            expected_shape=None,
            expected_dtype=None,
            expected_dims_order=None,
            expected_channel_names=None,
            expected_physical_pixel_sizes=None,
            expected_metadata_type=dict,
        )


@pytest.mark.parametrize("extension", ["sldy", "dir"])
@pytest.mark.parametrize(
    "filename, "
    "set_scene, "
    "expected_scenes, "
    "expected_shape, "
    "expected_dtype, "
    "expected_dims_order, "
    "expected_channel_names, "
    "expected_physical_pixel_sizes",
    [
        (
            "s1_t10_c1_z5",
            "20220726 endo diff1658874976",
            ("20220726 endo diff1658874976",),
            (10, 1, 5, 1736, 1776),
            np.uint16,
            dimensions.DEFAULT_DIMENSION_ORDER,
            ["0"],
            (None, 0.38388850322622897, 0.38388850322622897),
        ),
        (
            "s1_t1_c2_z40",
            "3500005564_20X_timelapse_202304201682033857",
            ("3500005564_20X_timelapse_202304201682033857",),
            (1, 2, 40, 1736, 1776),
            np.uint16,
            dimensions.DEFAULT_DIMENSION_ORDER,
            [
                "0",
                "1",
            ],
            (None, 0.3820158766750814, 0.3820158766750814),
        ),
    ],
)
def test_sldy_reader(
    extension: str,
    filename: str,
    set_scene: str,
    expected_scenes: typing.Tuple[str, ...],
    expected_shape: typing.Tuple[int, ...],
    expected_dtype: np.dtype,
    expected_dims_order: str,
    expected_channel_names: typing.List[str],
    expected_physical_pixel_sizes: typing.Tuple[float, float, float],
) -> None:
    # Construct full filepath
    uri = LOCAL_RESOURCES_DIR / f"{filename}.{extension}"

    # Run checks
    test_utilities.run_image_file_checks(
        ImageContainer=Reader,
        image=uri,
        set_scene=set_scene,
        expected_scenes=expected_scenes,
        expected_current_scene=set_scene,
        expected_shape=expected_shape,
        expected_dtype=expected_dtype,
        expected_dims_order=expected_dims_order,
        expected_channel_names=expected_channel_names,
        expected_physical_pixel_sizes=expected_physical_pixel_sizes,
        expected_metadata_type=dict,
    )
