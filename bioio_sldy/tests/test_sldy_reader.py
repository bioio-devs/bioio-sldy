#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib
import typing

import fsspec
import numpy as np
import pytest
from bioio import BioImage
from bioio_base import dimensions, exceptions, io
from bioio_base import reader as base_reader
from bioio_base import test_utilities

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


@pytest.mark.parametrize("protocol", ["file", "memory"])
def test_bioimage_detects_directory_image(
    protocol: str, tmp_path: pathlib.Path
) -> None:
    fs = fsspec.filesystem(protocol)
    root = f"{tmp_path}/experiment"
    fs.makedirs(root)
    for suffix in (".sldy", ".dir"):
        fs.put(
            str(LOCAL_RESOURCES_DIR / f"s1_t10_c1_z5{suffix}"),
            f"{root}/s1_t10_c1_z5{suffix}",
            recursive=True,
        )

    try:
        img = BioImage(f"{protocol}://{root}")
        assert isinstance(img.reader, Reader)
        assert img.dims.T == 10
        assert img.get_image_data("YX", T=0, C=0, Z=0).ndim == 2
    finally:
        fs.rm(root, recursive=True)


def test_sldy_reader_with_empty_directory(tmp_path: pathlib.Path) -> None:
    with pytest.raises(exceptions.UnsupportedFileFormatError):
        Reader(tmp_path)


@pytest.mark.parametrize(
    "url, expected_uri",
    [
        (
            "https://s3.us-west-2.amazonaws.com/my-bucket/experiment",
            "s3://my-bucket/experiment",
        ),
        (
            "https://my-bucket.s3.us-west-2.amazonaws.com/experiment",
            "s3://my-bucket/experiment",
        ),
        (
            "https://my.dotted.bucket.s3.amazonaws.com/experiment",
            "s3://my.dotted.bucket/experiment",
        ),
    ],
)
def test_s3_https_url_is_read_as_anonymous_s3(
    monkeypatch: pytest.MonkeyPatch,
    url: str,
    expected_uri: str,
) -> None:
    # Arrange
    calls: typing.List[typing.Tuple[typing.Any, typing.Dict[str, typing.Any]]] = []
    pathlike_to_fs = io.pathlike_to_fs

    def fake_pathlike_to_fs(
        uri: typing.Any, enforce_exists: bool, fs_kwargs: typing.Dict[str, typing.Any]
    ) -> typing.Any:
        calls.append((uri, fs_kwargs))
        return pathlike_to_fs(
            str(LOCAL_RESOURCES_DIR / "s1_t10_c1_z5.sldy"), enforce_exists, {}
        )

    monkeypatch.setattr(io, "pathlike_to_fs", fake_pathlike_to_fs)
    monkeypatch.setattr(base_reader, "pathlike_to_fs", fake_pathlike_to_fs)

    # Act
    supported = Reader.is_supported_image(url)
    Reader(url)

    # Assert
    assert supported
    assert calls == [(expected_uri, {"anon": True})] * 2


@pytest.mark.parametrize("method", [Reader, Reader.is_supported_image])
@pytest.mark.parametrize(
    "url",
    [
        "https://example.org/experiment",  # not S3, nothing to list with
        "http://example.org/experiment/",  # plain http is not S3 either
        "https://example.org/experiment/image.sldy",  # .dir folder not findable
        "https://s3.example.org/my-bucket/experiment",  # s3. host but not AWS
    ],
)
def test_unlistable_http_url_raises_specific_error(
    method: typing.Any, url: str
) -> None:
    with pytest.raises(exceptions.UnsupportedFileFormatError, match="can't be listed"):
        method(url)
