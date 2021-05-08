"""
file: __init__.py

This file contains functions meant to imported by developers
for creating sites
"""

# Import modules
import os
from .blockable import TMP_FOLDER, parse_json


def site_data(path):
    # Function to be imported and allow access to site data
    return parse_json("data/" + path + ".json")


def assets(asset_path):
    # This is a wrapper function for save_asset that reads an asset from a file

    # Get asset type
    file_type = asset_path[asset_path.rfind(".")+1:]

    # Open asset
    asset = str()
    with open(asset_path, "r") as f:
        asset = f.read()

    # Save asset and return path
    return save_asset(asset, file_type)


def dynamic_css(css):
    # This is a wrapper function for save_asset that sets the file type to css
    return save_asset(css, "css")


def save_asset(asset, file_type):
    """
    This function takes in an asset and a file type, moves the asset
    to a destination folder with the name of the asset's hash, then returns
    the path to the asset
    """

    # Get hash and path
    import hashlib
    hash_val = hashlib.sha256(asset.encode('UTF-8')).hexdigest()
    asset_path = file_type + "/" + hash_val + "." + file_type

    # Move asset
    if not os.path.isdir(TMP_FOLDER + "/" + asset_path):
        with open(TMP_FOLDER + "/" + asset_path, 'w') as f:
            f.write(asset)

    # Return path
    return asset_path
