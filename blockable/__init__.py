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
from ._utils import remove_slash, get_filetype


def get_pages(collection, sort=None, reverse=False):
    """
    Function to get a list of every data file in a collection
    sorted alphabetically by a value in the data file if a sort
    key is provided. Returns a path to the data file
    """

    # Get pages and append collection to each
    pages = os.listdir(f"data/{collection}")
    pages = [f"{collection}/{page[:-5]}" for page in pages]

    if sort is None:
        return pages
    else:
        return sort_pages(pages, sort, reverse=reverse)


def sort_pages(pages, sort, reverse=False):
    """
    Function to sort a list of pages based
    on the value of the sort key within each
    pages date file
    """

    # Construction list of tuples with page and sort value
    page_tuples = [(page, get_page(page)[sort]) for page in pages]

    # Sort list based on second value in tuple
    page_tuples = sorted(page_tuples, key=lambda x: x[1], reverse=reverse)

    # Return list of first value of tuples
    return [page_tuple[0] for page_tuple in page_tuples]


def get_page(page):
    """
    This function returns all the data for a given path.
    Page should be given as {collection}/{page_name}
    """
    return parse_json("data/" + page + ".json")


def move_asset(asset_path):
    """
    Moves any asset from a blockable instance to an asset
    folder. Returns path to moved asset
    """

    # Remove slash and get file type
    asset_path = remove_slash(asset_path)
    filetype = get_filetype(asset_path)

    # Get name based on sha256 hash
    sha256_hash = hashlib.sha256()
    with open(asset_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    asset_name = sha256_hash.hexdigest()

    # Add file type to asset name and get destination
    asset_name = asset_name + "." + filetype
    destination = "/" + "asset" + "/" + asset_name

    # Ensure asset folder is present
    if not os.path.isdir(TMP_FOLDER + "/" + "asset"):
        os.mkdir(TMP_FOLDER + "/" + "asset")

    # Copy asset to destination
    os.system("cp " + asset_path + " " + TMP_FOLDER + destination)

    # Return path to image destination
    return destination


def load_img(asset_path, **kwargs):
    """
    Loads an image from a blockable instance, converts it to webp,
    scales it to multiple sizes and moves it to the img folder.
    Returns img tag with nice setting (svg are unchanged)
    """

    # Remove slash and get file type
    asset_path = remove_slash(asset_path)
    filetype = get_filetype(asset_path)

    # Get name based on sha256 hash
    sha256_hash = hashlib.sha256()
    with open(asset_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    asset_name = sha256_hash.hexdigest()

    # Set destination folder
    destination = f"/img/{asset_name}/"

    # Ensure img folder is present
    if not os.path.isdir(TMP_FOLDER + "/" + "img"):
        os.mkdir(TMP_FOLDER + "/" + "img")

    # Ensure hash folder is present
    if not os.path.isdir(f"{TMP_FOLDER}{destination}"):
        os.mkdir(f"{TMP_FOLDER}{destination}")

    # Don't modify if svg
    if filetype == "svg":
        # Move and get sizes
        os.system(f"cp {asset_path} {TMP_FOLDER}{destination}original.svg")
        sizes = list()

        # Start img tag
        img_tag = f"<img src='{destination}original.svg'"
    else:
        # Move and get sizes
        sizes = convert_img(asset_path, asset_name)

        # Start img tag
        img_tag = f"<img src='{destination}original.webp'"

    # Add sizes
    if sizes is not None:
        # Start srcset
        img_tag += " srcset='"

        # Populate srcset
        for size in sizes:
            size = str(size)
            img_tag += f"{destination}{size}.webp {size}w,"

        # End srcset
        img_tag += "'"

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


def convert_img(asset_path, asset_name):
    # Get folder and open image
    folder = f"/img/{asset_name}/"
    with Image.open(asset_path) as image:

        # Create list of sizes
        width = 240
        sizes = list()
        while width < image.size[0]:
            sizes.append(width)
            width *= 2

        # Save for each width
        image.save(f"{TMP_FOLDER}{folder}original.webp", format="webp", )
        for size in reversed(sizes):
            image.thumbnail((size, image.height))
            image.save(f"{TMP_FOLDER}{folder}{str(size)}.webp",
                       format="webp", )

    return sizes


def load_css(asset_path):
    """
    This is a wrapper function for save_css that reads css from a file
    and returns the style tag for the stylesheet
    """

    # Remove possible starting slash
    asset_path = remove_slash(asset_path)

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

    # Remove possible starting slash
    asset_path = remove_slash(asset_path)

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
