"""
file: core.py

This file implements all the functions necessary for blockable to
compile a project folder into a folder of html
"""

# Import modules and set constants
import os
from .blockable import TMP_FOLDER, parse_json, get_template
from .netlify import CONFIG_FILE_NAME

# Set constant
STATIC_FOLDER = "static"


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

            # Get layout and web page
            if path in data_dict:  # layout based collection
                layout = data_dict[path]
                web_path = data_file[:-5]
            elif collection in data_dict:  # data based collection
                layout = data_dict[collection]
                web_path = collection + "/" + data_file[:-5]

                # Ensure layout folder exists
                if not os.path.isdir(TMP_FOLDER + collection):
                    os.mkdir(TMP_FOLDER + collection)

                # Move file if layout based collection has been created first
                if os.path.exists(f"{TMP_FOLDER}{collection}.html"):
                    os.system(f"mv {TMP_FOLDER}{collection}.html {TMP_FOLDER}{collection}/index.html")
            else:
                break


            # Get data and html then save
            data = parse_json("data/" + path)
            html = str(get_template("layouts/" + layout)(data))
            save(html, web_path)

    # Move assets
    move_assets()


def get_data_dict():
    """
    This function creates a returns a mapping from the directory of a
    json data file to the directory of the layout it uses
    """

    # Get config
    try:
        netlify_config = parse_json(CONFIG_FILE_NAME)
    except FileNotFoundError:
        pwd = os.getcwd()
        print(f"""No {CONFIG_FILE_NAME} found in {pwd}.
                Is {pwd} a blockable instance?""")
        quit()

    # Initialize dict
    data_dict = {}

    # Populate dict
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

    if not os.path.isdir(TMP_FOLDER + "admin"):
        # Create new destination folder
        os.mkdir(TMP_FOLDER + "admin")

    # Create asset directories
    for asset in ["css", "js"]:
        os.mkdir(TMP_FOLDER + asset)


def move_assets():
    # Move everything in static folder

    # If no static folder, do nothing
    if not os.path.isdir(STATIC_FOLDER):
        return

    # Get list of assets
    asset_list = os.listdir(STATIC_FOLDER)

    # Move remaining assets
    for asset in asset_list:
        os.system(f"cp -r {STATIC_FOLDER}/{asset} {TMP_FOLDER}")


def save(html, web_path):
    """
    Save html for given web path (should start with "/") unless a
    data collection folder is present, then it saves as index
    """

    # Save as index if a data-based collection folder exists at web path
    if os.path.isdir(f"{TMP_FOLDER}{web_path}"):
        with open(f"{TMP_FOLDER}{web_path}/index.html", 'w') as f:
            f.write(html)
    else:
        with open(f"{TMP_FOLDER}{web_path}.html", 'w') as f:
            f.write(html)
