"""
file: netlify.py

This file handles the creation of netlify configs based on the
blockable config files
"""


# Import modules and set constants
import json
import os
from .blockable import TMP_FOLDER, parse_json

CONFIG_FILE_NAME = 'config.json'
FIELDS_FILE_NAME = 'fields.json'
IMPORT_KEY = "import"
NETLIFY_INDEX = """
<!doctype html>
<html>
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>Content Manager</title>
    </head>
    <body>
        <!-- Include the script that builds the page and powers Netlify CMS -->
        <script src="https://unpkg.com/netlify-cms@^2.0.0/dist/netlify-cms.js">
        </script>
    </body>
</html>
"""


def create_config():
    # Import main Netlify config
    netlify_config = parse_json(CONFIG_FILE_NAME)

    # Parse Netlify config
    parse_config(netlify_config)

    # Create admin folder
    if not os.path.isdir(TMP_FOLDER + "admin"):
        os.mkdir(TMP_FOLDER + "admin")

    # Populate netlify admin folder
    with open(TMP_FOLDER + "admin/" + 'index.html', 'w') as f:
        f.write(NETLIFY_INDEX)
    with open(TMP_FOLDER + "admin/" + 'config.yml', 'w') as f:
        json.dump(netlify_config, f, indent=4)


def parse_config(netlify_config):
    # Get list of collections and then reset list
    collections = netlify_config["collections"]
    netlify_config["collections"] = list()

    # Loop though each collection and parse template_files
    for collection in collections:
        if "files" in collection:
            for layout in collection["files"]:
                import_layout(layout, collection["name"], "file")
        else:
            import_layout(collection, collection["name"], "folder")

        # Add collection to config
        netlify_config["collections"].append(collection)


def import_layout(layout, collection_name, layout_type):
    """
    This function imports a layout by importing the fields and
    removing/adding some extra keys to the dictionary
    """
    # Add file/folder key
    if layout_type == "file":  # layout based collection
        layout_file = layout["name"] + ".json"
        layout[layout_type] = "data/" + collection_name + "/" + layout_file
    else:  # data based collection
        layout[layout_type] = "data/" + collection_name
        layout["create"] = True

    # Import fields
    import_fields(layout)

    # Remove extra field keys
    layout.pop("widget")
    layout.pop("collapsed")

    # Add extra field keys
    layout["format"] = "json"


def import_fields(data):
    # Recursively import fields

    # Check if data has imports
    if IMPORT_KEY not in data:
        return

    # Get import info
    file_dir = data.pop(IMPORT_KEY)

    # Check if final key is in data and create if not
    if "fields" not in data:
        data["fields"] = list()

    # Load json
    fields = parse_json(file_dir + '/' + FIELDS_FILE_NAME)

    # Parse for imports
    for field in fields:
        import_fields(field)

    # Turn into field object
    data["widget"] = "object"
    data["collapsed"] = True
    data["fields"] = fields
