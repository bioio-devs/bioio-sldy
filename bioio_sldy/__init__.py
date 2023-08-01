# -*- coding: utf-8 -*-

"""Top-level package for bioio_sldy."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("bioio-sldy")
except PackageNotFoundError:
    __version__ = "uninstalled"

__author__ = "Sean Meharry"
__email__ = "seanm@alleninstitute.org"


from .reader_metadata import ReaderMetadata

__all__ = ["ReaderMetadata"]
