# Netlify.py
# This file will create a config.yml for netlify to use
# based on the netlify.json file

# Import modules and set constants
import json

CONFIG_FILE_NAME = 'netlify.json'
FIELDS_FILE_NAME = 'fields.json'
IMPORT_KEY = "import"

def main():
    # Import main Netlify config
    netlify_config = parse_json(CONFIG_FILE_NAME)

    # Parse Netlify config
    parse_config(netlify_config)
    
    # Save final netlify config file
    with open('config.yml', 'w') as netlify_yml_config:
        json.dump(netlify_config, netlify_yml_config, indent=4)


def parse_config(netlify_config):
    # Get list of collections and then reset list
    collections = netlify_config["collections"]
    netlify_config["collections"] = list()

    # Loop though each collection and parse template_files
    for collection in collections:
        # Parse for imports
        parse_for_imports(collection, "files")

        # Add collection to config
        netlify_config["collections"].append(collection)


def parse_for_imports(data, import_type):
    """
    This function takes in a dictionary and checks if anything needs
    importing than imports it with the given type. It then calls itself
    on the newly imported data and imports it with the type 'field'
    """

    # Check if data has imports
    if IMPORT_KEY not in data:
        return

    # Get import data
    data_imports = data.pop(IMPORT_KEY)

    # Check if final key is in data and create if not
    if import_type not in data:
        data[import_type] = list()

    # Loop though each data import
    for data_import in data_imports:
        # Get import info
        file_dir = data_import["location"]
        object_name = data_import["name"]
        object_label = data_import["label"]
    
        # Load json
        imported_data = parse_json(file_dir + '/' + FIELDS_FILE_NAME)
    
        # Parse for imports
        parse_for_imports(imported_data, "fields")
    
        # Create object
        if import_type == "files":
            fields_object = {"label": object_label, "name": object_name, "file": "site/content/" + object_name + ".json", "fields": imported_data["fields"]}

        if import_type == "fields":
            fields_object = {"label": object_label, "name": object_name, "widget": "object", "collapsed": True, "fields": imported_data["fields"]}

        # Add object to data file
        data[import_type].append(fields_object)


def parse_json(file_dir):
    """
    This function accepts the directory of a json file and returns
    a parsed version of the json file
    """

    # Open file and return parsed json
    with open(file_dir, 'r') as file:
        return json.load(file)

# Boilerplate
if __name__ == "__main__":
    main()
