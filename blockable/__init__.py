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


def load_css(asset_path):
    """
    This is a wrapper function for save_css that reads css from a file
    and returns the style tag for the stylesheet
    """

    # Open asset
    css = str()
    with open(asset_path, "r") as f:
        css = f.read()

    return save_css(css)


def load_js(asset_path):
    """
    This is a wrapper function for save_js that reads js from a file
    and returns the script tag for that script
    """

    # Open asset
    js = str()
    with open(asset_path, "r") as f:
        js = f.read()

    return save_js(js)


def save_js(js):

    # Save asset and get hash
    asset_path, hash_val = save_asset(js, "js")

    # Create script tag
    src = f"src='{asset_path}'"
    integrity = f"integrity='sha256-{hash_val}'"
    crossorigin = "crossorigin='anonymous'"
    _async = "async='async'"
    nonce = "nonce='8IBTHwOdqNKAWeKl7plt8g=='"
    defer = "defer async"
    style_tag = f"<script {src} {integrity} {crossorigin} {_async} {nonce} {defer}></script>"

    # Return tag
    return style_tag


def save_css(css):

    # Save asset and get hash
    asset_path, hash_val = save_asset(css, "css")

    # Create style tag
    href = f"href='{asset_path}'"
    style_tag = f"<link rel='stylesheet' type='text/css' {href}>"

    # Return tag
    return style_tag


def save_asset(asset, file_type):
    """
    This function takes in an asset and a file type, moves the asset
    to a destination folder with the name of the asset's hash, then returns
    the hash of the asset
    """

    # Get hashs
    import hashlib
    import base64
    sha_256 = hashlib.sha256(asset.encode('UTF-8'))
    hex_hash = sha_256.hexdigest()
    base_64_hash = base64.b64encode(sha_256.digest()).decode()

    asset_name = hex_hash + "." + file_type
    asset_path = "/" + file_type + "/" + asset_name

    # Move asset
    if not os.path.isdir(TMP_FOLDER + "/" + asset_path):
        with open(TMP_FOLDER + asset_path, 'w') as f:
            f.write(asset)

    # Return asset name
    return asset_path, base_64_hash
