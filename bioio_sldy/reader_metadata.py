#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List

import bioio_base.reader_metadata

###############################################################################


class ReaderMetadata(bioio_base.reader_metadata.ReaderMetadata):
    """
    Notes
    -----
    Defines metadata for the reader itself (not the image read),
    such as supported file extensions.
    """

    @staticmethod
    def get_supported_extensions() -> List[str]:
        """
        Returns a list of file extensions this plugin supports reading.
        """
        return ["sldy", "dir"]

    @staticmethod
    def get_reader() -> bioio_base.reader.Reader:
        """
        Returns the reader this plugin represents
        """
        from .reader import Reader

        return Reader

    @staticmethod
    def supports_directory_images() -> bool:
        """
        Returns True because a folder holding a .sldy and its .dir
        is readable as an image.
        """
        return True
