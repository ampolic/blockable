#!/usr/bin/python3 -B
#
# Blockable.py
# This file implements all the necessary functions for blockable.

# Import modules and set constants
import json
import os

CONFIG_FILE_NAME = 'netlify.json'
FIELDS_FILE_NAME = 'fields.json'
IMPORT_KEY = "import"
TMP_FOLDER = "/tmp/blockable"
CSS_FILE = "stylesheet.css"
JS_FILE = "javascript.js"
NETLIFY_INDEX = """
<!doctype html>
<html>
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Content Manager</title>
    </head>
    <body>
        <!-- Include the script that builds the page and powers Netlify CMS -->
        <script src="https://unpkg.com/netlify-cms@^2.0.0/dist/netlify-cms.js"></script>
    </body>
</html>
"""

def main():
    # Import arg parse
    import argparse
    
    # Set up arguments
    parser = argparse.ArgumentParser(description='Python based static site generator')
    parser.add_argument('source', help='Set path to blockable folder')
    parser.add_argument('-N', '--netlify', action="store_true", help='Only compiles the Netlify components')
    parser.add_argument('-i', '--init', action="store_true", help='Create simple blockable site framework')
    parser.add_argument('-O', '--output', help='Set path to output folder')


    # Create working tmp folder
    if not os.path.isdir(TMP_FOLDER):
        os.mkdir(TMP_FOLDER)  

    # Parse arguments
    args = vars(parser.parse_args())
    if args["init"]:
        # Only create template
        desination = args["source"]
        create_template()
    else:
        # Get desination and mv into blockable source
        desination = get_desination(args["output"])
        if args["source"] != os.getcwd():
            os.chdir(args["source"])
       
        # Create config/site depending on netlify arg
        if not args["netlify"]: 
            compile_site()
        create_config()


    # Move to final destination and clean up
    if not os.path.isdir(desination):
        os.mkdir(desination)

    os.system("cp -r " + TMP_FOLDER + "/* " + desination + "/")
    os.system("rm -fdr " + TMP_FOLDER)

def get_desination(desination):
    # If a destination is passed in, get absolute path
    if desination:
        return get_absolute_path(desination)
    else:
        return get_absolute_path("public_html")

def create_template():
    # Create basic blockable instance folders
    for folder in ["assets", "layouts", "blocks"]:
        os.mkdir(TMP_FOLDER + "/" + folder)
    for layout in ["homepage"]:
        os.mkdir(TMP_FOLDER + "/layouts/" + layout)
    for block in ["nav_bar", "about"]:
        os.mkdir(TMP_FOLDER + "/blocks/" + block)
    for asset in ["css", "js", "images"]:
        os.mkdir(TMP_FOLDER + "/assets/" + asset)


    # Create and save json files
    netlify_config = {
        "backend": {"name": "github","repo": "user/repo_name","branch": "main","site_domain": "cms.netlify.com","api_root": "https://api.github.com"},
        "media_folder": "assets/images",
        "collections": [
            {"label": "Settings", "name": "settings", "files": [
                {"label": "Nav Bar", "name": "nav_bar", "import": "blocks/nav_bar"}
                ]
            },
            {"label": "Pages","name": "pages","files": [
                {"import": "layouts/homepage", "label": "Homepage", "name": "index"},
                ]
            }
        ]
    }
    homepage_fields = [
        {"label": "Title", "name": "title", "widget": "string"},
	{"label": "About", "name":"about", "import": "blocks/about"}
    ]
    about_fields = [
        {"label": "About", "name": "about", "widget": "string"}
    ]
    nav_bar_fields = [
        {"label": "Site Color", "name": "site-color", "widget": "color"}
    ]

    save_json(TMP_FOLDER + "/netlify.json", netlify_config)
    save_json(TMP_FOLDER + "/layouts/homepage/" + FIELDS_FILE_NAME, homepage_fields)
    save_json(TMP_FOLDER + "/blocks/about/" + FIELDS_FILE_NAME, about_fields)
    save_json(TMP_FOLDER + "/blocks/nav_bar/" + FIELDS_FILE_NAME, nav_bar_fields)


def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def get_absolute_path(path):
    # Remove end /
    if path[-1] == "/":
        path = path[:-1]

    # Add pwd
    if path[0] == "/":
        return path
    else:
        return os.getcwd() + "/" + path

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
            data = parse_json("data/" + path)
            template_path = "layouts/" + layout
            template_function =  get_template_function(template_path)
            html = execute_template(template_function, template_path, data)
            save(html, data_file[:-5])

    # Move assets
    move_assets()

def site_data(path):
    # Function to be imported and allow access to site data
    return parse_json("data/" + path + ".json")

def get_data_dict():
    """
    This function creates a returns a mapping from the directory of a json data file
    to the directory of the layout it uses
    """

    # Initialize dict
    data_dict = {}

    # Populate dict
    netlify_config = parse_json("netlify.json")
    for collection in netlify_config["collections"]:
        if "files" in collection: # Collection is layout-based
            for page in collection["files"]:

                # Get import info
                import_name = page["import"]
                break_point = import_name.find("/")

                # Ensure import is layout
                if import_name[:break_point] == "layouts":
                    data_dict[collection["name"] + "/" + page["name"] + ".json"] = import_name[break_point+1:]

        else: # Collection is data-based

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
        for template in ["", "layouts", "blocks"]:
            os.mkdir(TMP_FOLDER + "/" + asset + "/" + template)

def move_assets():
    # Move everything in assets folder
    asset_list = os.listdir("assets")
    for asset in asset_list:
        os.system("cp -r assets/" + asset + " " + TMP_FOLDER)

def save(html, page_name):
    # Save html with given name
    with open(TMP_FOLDER + "/" + page_name + '.html', 'w') as page:
        page.write(html);

def create_template_namespaces():
    # Create a global namespace for each template type

    # Import
    import types
    import functools

    # Loop though template types
    for template_type in ["layouts", "blocks"]:
        # Create global namespace for template type and get template list
        globals()[template_type] = types.SimpleNamespace()
        template_list = os.listdir(template_type)

        # Loop though templates and add functions to namespace
        for template in template_list:
            template_path = template_type + "/" + template
            template_function = get_template_function(template_path)
            
            # Bind a partial template function that only accepts data...to the attribute "template" of the namespace
            setattr(globals()[template_type], template, functools.partial(execute_template, template_function, template_path))

def get_template_function(template_path):
    """
    This function accepts a template path and a data json then calls the html
    function of the given template, passing it the data parameter and returns
    the templates output
    """

    # Add template path
    import sys
    sys.path.insert(1, template_path)
    
    # Import html function then clean up sys path
    from index import html as template_function
    sys.modules.pop("index")
    sys.path.remove(template_path)

    return template_function

def execute_template(template_function, template_path, data):
    # Returns html for template and handles css/js moves and insertions

    # Run template
    html = template_function(data)
    
    # Get list of inline styles and remove from html
    inline_style_list = get_inline_styles(html)
    for inline_style in inline_style_list:
        html = html.replace("<style>" + inline_style + "</style>", "")
    
    # Add inline styles to inline stylesheet
    inline_stylesheet = ""
    while len(inline_style_list) != 0:
        inline_stylesheet += inline_style_list.pop()
    
    # Save inline stylesheet
    if inline_stylesheet:
        inline_stylesheet_abs_path = get_inline_stylesheet_abs_path(template_path)
        with open(TMP_FOLDER + inline_stylesheet_abs_path, "w") as inline_stylesheet_file:
            inline_stylesheet_file.write(inline_stylesheet)
        html = ("<link rel='stylesheet' href='" + inline_stylesheet_abs_path + "'>") + ("\n" + html)

    # Copy CSS
    if os.path.isfile(template_path + "/" + CSS_FILE):
        os.system('cp ' + template_path + "/" + CSS_FILE + " " + TMP_FOLDER + "/css/" + template_path + ".css")
        html = ("<link rel='stylesheet' href='/css/" + template_path + ".css'>") + ("\n" + html)


    # Copy JS
    if os.path.isfile(template_path + "/" + JS_FILE):
        os.system('cp ' + template_path + "/" + JS_FILE + " " + TMP_FOLDER + "/js/" + template_path + ".js")
        html = (html + "\n") + ("<script src='/js/" + template_path + ".js'></script>")

    return html


def get_inline_stylesheet_abs_path(template_path):
    # Change ending if stylesheet already exists
    inline_stylesheet_abs_path = "/css/" + template_path + "_is0.css"
    while True:
        i = 1
        if os.path.isfile(TMP_FOLDER + inline_stylesheet_abs_path):
            inline_stylesheet_abs_path = "/css/" + template_path + "_is" + str(i) + ".css"
            i += 1
        else:
            return inline_stylesheet_abs_path

def get_inline_styles(html):
    # Find start and end tags until no more start tags
    inline_style_list = list()
    start_point = html.find("<style>")
    while start_point != -1:
        end_point = html.find("</style>", start_point)
        inline_style = html[start_point + len("<style>"):end_point]
        inline_style_list.append(inline_style)
        start_point = html.find("<style>", end_point)

    return inline_style_list

def create_config():
    # Import main Netlify config
    netlify_config = parse_json(CONFIG_FILE_NAME)

    # Parse Netlify config
    parse_config(netlify_config)
 
    # Create admin folder 
    if not os.path.isdir(TMP_FOLDER + "/admin"):
        os.mkdir(TMP_FOLDER + "/admin")
    
    # Populate netlify admin folder
    with open(TMP_FOLDER + "/admin/" + 'index.html', 'w') as netlify_index_file:
        netlify_index_file.write(NETLIFY_INDEX)
    with open(TMP_FOLDER + "/admin/" + 'config.yml', 'w') as netlify_yml_config:
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
    # Recursively import fields
    
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
    # Open file and return parsed json
    with open(file_dir, 'r') as file:
        return json.load(file)

# Boilerplate
if __name__ == "__main__":
    main()
else:
    create_template_namespaces()
