# Blockable.py
# This file implements all the necessary functions for blockable. Running it, will
# currently print out all the layouts html return.


DESINATION = "public_html"
CSS_FILE = "stylesheet.css"
JS_FILE = "javascript.js"


# Import modules
from netlify import parse_json
import os


def main():
    # Get list of layouts
    layouts_list = os.listdir("layouts")

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
            data = parse_json("data/" + path)
            html = layouts(layout, data)
            save(html, data_file[:-5])


    # Move assets
    move_assets()


def get_data_dict():
    """
    This function creates a returns a mapping from the directory of a json data file
    to the directory of the layout it uses
    """

    # Dict where key is data path and value is layout
    data_dict = {}

    # Get config 
    netlify_config = parse_json("netlify.json")

    # Get page list from file collections
    for collection in netlify_config["collections"]:
        if "files" in collection:
            for page in collection["files"]:

                # Get import info
                import_name = page["import"]
                break_point = import_name.find("/")

                # Ensure import is layout
                if import_name[:break_point] != "layouts":
                    break

                # Add to dict
                data_dict[collection["name"] + "/" + page["name"] + ".json"] = import_name[break_point+1:]
        else:
 
           # Get import info
           import_name = collection["import"]
           break_point = import_name.find("/")

           # Ensure import is layout
           if import_name[:break_point] != "layouts":
               break
           
           # Add to dict
           data_dict[collection["name"]] = import_name[break_point+1:]

    return data_dict




def prepare_desination():
    # Delete
    os.system("rm -fdr " + DESINATION)

    # Create directories
    os.mkdir(DESINATION)
    os.mkdir(DESINATION + "/css/")
    os.mkdir(DESINATION + "/js/")
    os.mkdir(DESINATION + "/css/layouts/")
    os.mkdir(DESINATION + "/js/layouts/")
    os.mkdir(DESINATION + "/css/blocks/")
    os.mkdir(DESINATION + "/js/blocks/")


def move_assets():

    # Move everything in assets folder
    asset_list = os.listdir("assets")
    for asset in asset_list:
        os.system("cp -r assets/" + asset + " " + DESINATION)

    # Move css and javascript in layouts folder
    layouts_list = os.listdir("layouts")

    for layout in layouts_list:
        if os.path.isfile("layouts/" + layout + "/" + CSS_FILE):
            os.system('cp ' + "layouts/" + layout + "/" + CSS_FILE + " " + DESINATION + "/css/layouts/" + layout + ".css")

        if os.path.isfile("layouts/" + layout + "/" + JS_FILE):
            os.system('cp ' + "layouts/" + layout + "/" + JS_FILE + " " + DESINATION + "/js/layouts/" + layout + ".js")


    # Move css and javascript in blocks folder
    blocks_list = os.listdir("blocks")

    for layout in blocks_list:
        if os.path.isfile("blocks/" + layout + "/" + CSS_FILE):
            os.system('cp ' + "blocks/" + layout + "/" + CSS_FILE + " " + DESINATION + "/css/blocks/" + layout + ".css")

        if os.path.isfile("blocks/" + layout + "/" + JS_FILE):
            os.system('cp ' + "blocks/" + layout + "/" + JS_FILE + " " + DESINATION + "/js/blocks/" + layout + ".js")



def save(html, page_name):
    """
    This function will save the layout given a file name
    and html
    """

    # Save file
    with open(DESINATION + "/" + page_name + '.html', 'w') as page:
        page.write(html);


def layouts(layout, data):
    """
    This function accepts a layout name and a data json then calls the html
    function of the given layout, passing it the data parameter. The function
    returns whatever html the layout function returns
    """

    # Import modules
    import sys

    # Add template path
    sys.path.insert(1, "layouts/" + layout)
    
    # Import html function from the index file
    from index import html as layout_function

    # Remove template from module directory
    sys.modules.pop("index")
    
    # Remove template path
    sys.path.remove("layouts/" + layout)

    
    # Add html function to dictionary
    html = layout_function(data)
    
    # Return html
    return html


def blocks(block, data):
    """
    This function accepts a block name and a data json then calls the html
    function of the given block, passing it the data parameter. The function
    returns whatever html the block function returns
    """

    # Import modules
    import sys

    # Add template path
    sys.path.insert(1, "blocks/" + block)
    
    # Import html function from the index file
    from index import html as block_function
    
    # Add html function to dictionary
    html = block_function(data)
    
    # Remove template from module directory
    sys.modules.pop("index")
    
    # Remove template path
    sys.path.remove("blocks/" + block)

    # Return html
    return html



# Boilerplate
if __name__ == "__main__":
    main()
