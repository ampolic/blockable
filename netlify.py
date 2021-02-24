# Netlify.py
# This file will create a config.yml for netlify to use
# based on the netlify.json file

# Import modules and set constants
import json

CONFIG_FILE_NAME = 'netlify.json'
TEMPLATE_FILE_NAME = 'netlify.json'
FIELD_FILE_NAME = 'netlify.json'
IMPORT_PREFIX = 'import_'


def main():
    # Import main netlify config
    netlify_config = parse_json(CONFIG_FILE_NAME)

    # Parse Netlify config
    netlify_config = parse_config(netlify_config)
    
    # Save final netlify config file
    with open('config.yml', 'w') as netlify_yml_config:
        json.dump(netlify_config, netlify_yml_config, indent=4)



def parse_config(netlify_config):

    # Get list of collections and then reset list
    collections = netlify_config["collections"]
    netlify_config["collections"] = list()

    # Loop though each collection and parse template_files
    for collection in collections:

        # Parse collection for imports
        parse_for_imports(collection)

        # Add collection to config
        netlify_config["collections"].append(collection)
   
    return netlify_config


def parse_for_imports(data):
    """
    This function looks for a key in a given data set that begins
    with the IMPORT_PREFIX and then proceeds to recursively parse and
    attach all the json files to the var data
    """

    # Get import key
    import_key = get_key_by_prefix(data, IMPORT_PREFIX)
    
    # Base case (no import key was found)
    if not import_key:
        return

    # Create final key by removing import prefix
    final_key = import_key[len(IMPORT_PREFIX):]

    # Get list of dirs from data and remove it from data
    file_dirs = data.pop(import_key)

    # Check if final key is in data and create if not
    if final_key not in data:
        data[final_key] = list()

    # Loop though each file dir
    for file_dir in file_dirs:

        # Load json
        imported_data = parse_json(file_dir + '/' + TEMPLATE_FILE_NAME)

        # Parse data for imports
        parse_for_imports(imported_data)

        # Check data of imported data
        if type(imported_data) == list:
            # Add as list
            data[final_key] += imported_data
        else:
            # Add as dictionary
            data[final_key].append(imported_data)


def get_key_by_prefix(dictionary, prefix):
    """
    This function checks if any of a dictionaries keys
    contains a given prefix and returns the key if so
    """

    # Loop though each key and check if it contains prefix
    for key in dictionary:
        if prefix in key:
            return key

    # Return empty string if nothing is found
    return ""
    

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
