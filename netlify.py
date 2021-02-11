# Netlify.py
# This file will create a config.yml for netlify to use
# based on the netlify.json file

# Import modules and set constants
import json

CONFIG_FILE_NAME = 'netlify.json'
TEMPLATE_FILE_NAME = 'netlify.json'
FIELD_FILE_NAME = 'netlify.json'


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

        # Parse collection
        collection = parse_collection(collection, "template_files", "files")

        # Add collection to config
        netlify_config["collections"].append(collection)
   
    return netlify_config


def parse_collection(collection, template_dir_key, template_final_key):

    # check if data_dict contains a dir key and get dir list if so
    if template_dir_key in collection:
        template_dir_list = collection[template_dir_key]
        collection.pop(template_dir_key)
    else:
        return collection

    # Check if final key is in data_dict and create if not
    if template_final_key not in collection:
        collection[template_final_key] = list()

    for template_dir in template_dir_list:

        # Load template
        template = parse_json(template_dir + '/' + TEMPLATE_FILE_NAME)

        # Parse template
        template = parse_template(template, "field_files", "fields")

        # Add template to collection
        collection[template_final_key].append(template)

    # Return collection
    return collection



def parse_template(template, field_dir_key, field_final_key):

    # Check if template has field files
    if field_dir_key in template:
        # Get list of dirs then remove dict
        field_dirs = template[field_dir_key]
        template.pop(field_dir_key)
    else:
        # Add template to collection
        return template
    
    # Check if fields list exists and create it if it doesn't
    if field_final_key not in template:
        template[field_final_key] = list()
    
    # Loop though field file dirs and to fields list
    for field_dir in field_dirs:
    
        # Load field
        fields = parse_json(field_dir + '/' + FIELD_FILE_NAME)

        # Add field to template
        template[field_final_key] += fields
        
    return template



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
