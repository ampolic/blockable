"""
file: core.py

This file implements all the functions necessary for blockable to
compile a project folder into a folder of html
"""

# Import modules and set constants
import os
from .blockable import TMP_FOLDER, parse_json


def compile_site():
    # Get data dict
    data_dict = get_data_dict()

    # Make all folders
    prepare_desination()

    # Get collection
    collection_list = os.listdir("data")

    # Loop though data
    for collection in collection_list:
        data_file_list = os.listdir("data/" + collection)
        for data_file in data_file_list:

            # Get path
            path = collection + "/" + data_file

            # Get layout
            if path in data_dict:
                layout = data_dict[path]
            elif collection in data_dict:
                layout = data_dict[collection]
            else:
                break

            # Get data and html then save
            from .blockable import get_template

            data = parse_json("data/" + path)
            html = str(get_template("layouts/" + layout)(data))
            save(html, data_file[:-5])

    # Move assets
    move_assets()


def get_data_dict():
    """
    This function creates a returns a mapping from the directory of a
    json data file to the directory of the layout it uses
    """

    # Initialize dict
    data_dict = {}

    # Populate dict
    netlify_config = parse_json("netlify.json")
    for collection in netlify_config["collections"]:
        if "files" in collection:  # Collection is layout-based
            for page in collection["files"]:

                # Get import info
                import_name = page["import"]
                break_point = import_name.find("/")

                # Ensure import is layout
                if import_name[:break_point] == "layouts":
                    layout_name = collection["name"]
                    data_file = layout_name + "/" + page["name"] + ".json"
                    data_dict[data_file] = import_name[break_point+1:]

        else:  # Collection is data-based
            # Get import info
            import_name = collection["import"]
            break_point = import_name.find("/")

            # Ensure import is layout
            if import_name[:break_point] == "layouts":
                data_dict[collection["name"]] = import_name[break_point+1:]

    return data_dict


def prepare_desination():
    # Create new destination folder
    os.mkdir(TMP_FOLDER + "/" + "admin")

    # Create asset directories
    for asset in ["css", "js"]:
        os.mkdir(TMP_FOLDER + "/" + asset)


def move_assets():
    # Move everything in assets folder
    asset_list = os.listdir("assets")
    for asset in asset_list:
        os.system("cp -r assets/" + asset + " " + TMP_FOLDER)


def save(html, page_name):
    # Save html with given name
    with open(TMP_FOLDER + "/" + page_name + '.html', 'w') as f:
        f.write(html)
