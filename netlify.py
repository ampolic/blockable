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
    # Add layout file/folder
    layout[layout_type] = "data/" + collection_name + "/" + layout["name"] + ".json"

    # Import fields
    import_fields(layout)

    # Remove extra field keys
    layout.pop("widget")
    layout.pop("collapsed")


def import_fields(data):
    """
    This function recursively import fields
    """
    # Check if data has imports
    if IMPORT_KEY not in data:
        return

    # Get import info
    file_dir = data.pop(IMPORT_KEY)
    name = data["name"]
    label = data["label"]

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
