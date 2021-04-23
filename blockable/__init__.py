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
    """
    This function is meant to be imported by developers as a means
    of importing assets into their templates. The asset_path should be the path
    to the desired asset starting from the root of your blockable project and 
    the function will return a string of the final url of the given asset
    """

    # Get root folder of asset path
    first_slash = asset_path.find("/")
    root_folder = asset_path[:first_slash]
    
    # Check if asset is in template folder
    if root_folder == "assets":
        # Set final path
        final_path = asset_path[first_slash:]
    else:
        # Get position of informational dividers
        second_slash = asset_path.find("/", first_slash+1)
        final_slash = asset_path.rfind("/")
        final_period = asset_path.find(".")

        # Extract information about the asset from path
        template_type = root_folder
        template_name = asset_path[first_slash+1:second_slash]
        file_name = asset_path[final_slash+1:final_period]
        file_type = asset_path[final_period+1:]

        # Edge case for non css/js files
        if file_type == "js" or file_type == "css":
            file_folder = file_type
        else:
            file_folder = "media"

        # Set asset location
        final_folder = "/" + file_folder + "/" + template_type
        final_path = final_folder + "/" + template_name + "_" + file_name + "." + file_type

        # Move asset
        try:
            os.system("cp " + asset_path + " " + TMP_FOLDER + final_path)
        except:
            os.system("mkdir -p " + final_folder)
            os.system("cp " + asset_path + " " + TMP_FOLDER + asset_path)

    
    return final_path


def is_identical(string, path):
    # This function checks if a file and string are identical

    # Get path contents
    with open(path, 'r') as f:
        path_contents = f.read()

    # Check for hash collision
    if string == path_contents:
        return True
    else:
        return False


def dynamic_css(css):
    """
    This function is meant to be imported by the developers ....

    """
    # Get hash of css
    hash_val = abs(hash(css))

    # Loop until empty hash slot is found
    while True:
        # Get path
        dynamic_css_path = TMP_FOLDER + "/css/dynamic_css/" + str(hash_val) + ".css"

        # Check if css file already exists
        if os.path.isdir(dynamic_css_path):
            # Check if existing file is hash collision
            if is_identical(css, dynamic_css_path):
                break
            else:
                hash_val += 1
        else:
            # Save css
            with open(dynamic_css_path, 'w') as f:
                f.write(str(css))
            break

    return "/css/dynamic_css/" + str(hash_val) + ".css"
