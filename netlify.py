# Netlify.py
# This file will create a config.yml for netlify to use
# based on the netlify.json file

# Import modules and set constants
import json

CONFIG_FILE_NAME = 'netlify.json'
COLLECTION_FILE_NAME = 'netlify.json'

def main():
    # Import json file
    with open(CONFIG_FILE_NAME, 'r') as netlify_json_config:
        netlify_config = json.load(netlify_json_config)

    # Get list of collections and then reset list
    collections = netlify_config["collections"]
    netlify_config["collections"] = list()

    # Loop though each collection and parse file directory then add to config
    for collection in collections:

        # Get list of file directories in collection and reset list
        file_dirs = collection["files"]
        collection["files"] = list()

        # Loop though directory in list and add it to the collection
        for file_dir in file_dirs:
            with open(file_dir + '/' + COLLECTION_FILE_NAME, 'r') as field_file:
                collection["files"].append(json.load(field_file))

    # Add collection to config
    netlify_config["collections"].append(collection)

    # Create file
    with open('config.yml', 'w') as netlify_yml_config:
        json.dump(netlify_config, netlify_yml_config, indent=4)

# Boilerplate
if __name__ == "__main__":
    main()
