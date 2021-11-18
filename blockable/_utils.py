"""
file: _utils.py

This file contains functions meant to imported by
other parts of blockable
"""


def remove_slash(path):
    """
    This function accepts a path and removes
    a slash if there is one
    """

    # Remove possible slash at beginning
    if path[0] == '/':
        path = path[1:]

    return path


def get_filetype(path):
    """
    This funciton accepts a path to an asset
    and returns the file type of the asset
    """

    # Get file type
    dot_index = path.rfind(".")
    filetype = path[dot_index+1:]

    return filetype
