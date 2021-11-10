"""
file: __init__.py

This file contains functions meant to imported by developers
for creating sites
"""

# Import modules
import os
import hashlib
import base64
from PIL import Image
from .blockable import TMP_FOLDER, parse_json


def site_data(path):
    # Function to be imported and allow access to site data
    return parse_json("data/" + path + ".json")


def load_img(asset_path, **kwargs):
    """
    Loads an image from a blockable instance, converts it to webp,
    scales it to multiple sizes and moves it to the img folder.
    Returns img tag with nice setting (svg are unchanged)
    """

    # Remove possible slash at beginning
    if asset_path[0] == '/':
        asset_path = asset_path[1:]

    # Get file type
    dot_index = asset_path.rfind(".")
    file_type = asset_path[dot_index+1:]

    # Get name based on sha256 hash
    sha256_hash = hashlib.sha256()
    with open(asset_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    asset_name = sha256_hash.hexdigest()

    # Ensure img folder is present
    if not os.path.isdir(TMP_FOLDER + "/" + "img"):
        os.mkdir(TMP_FOLDER + "/" + "img")

    # Don't modify if svg
    if file_type == "svg":
        destination = f"/img/{asset_name}.svg"
        os.system(f"cp {asset_path} {TMP_FOLDER}{destination}")
    else:
        # Open image and save as webp
        destination = f"/img/{asset_name}.webp"
        with Image.open(asset_path) as image:
            image.save(f"{TMP_FOLDER}{destination}", format="webp")

    # Start img tag
    img_tag = f"<img src='{destination}'"

    # Loop though kwords
    for kword in kwargs.keys():

        # Get value
        value = str(kwargs[kword])

        # Get key by removing possible _
        if kword[0] == '_':
            key = kword[1:]
        else:
            key = kword

        # Add arg to tag
        img_tag += f" {key}='{value}'"

    # Close tag
    img_tag += ">"

    # Return image tag
    return img_tag


def load_custom(asset_path):
    """
    Loads any asset from a blockable instance and moves it to
    a custom folder. Returns path to moved asset
    """

    # Get file type
    dot_index = asset_path.rfind(".")
    file_type = asset_path[dot_index+1:]

    # Get name based on sha256 hash
    sha256_hash = hashlib.sha256()
    with open(asset_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    asset_name = sha256_hash.hexdigest()

    # Add file type to asset name and get destination
    asset_name = asset_name + "." + file_type
    destination = "/" + "custom" + "/" + asset_name

    # Ensure custom folder is present
    if not os.path.isdir(TMP_FOLDER + "/" + "custom"):
        os.mkdir(TMP_FOLDER + "/" + "custom")

    # Copy asset to destination
    os.system("cp " + asset_path + " " + TMP_FOLDER + destination)

    # Return path to image destination
    return destination


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
    style_tag = f"""<script {src} {integrity} {crossorigin} {_async} {nonce} {defer}>
    </script>"""

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
