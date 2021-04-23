"""
file: __main__.py

This file implments the command line interface for blockable
"""

# Import modules
import os
from .blockable import TMP_FOLDER

def main():
    # Import modules
    import argparse
    from .template import create_template
    from .generator import compile_site
    from .netlify import create_config

    # Set up arguments
    parser = argparse.ArgumentParser(description='Python based static site generator')
    parser.add_argument('source', help='Set path to blockable folder')
    parser.add_argument('-N', '--netlify', action="store_true", help='Only compiles the Netlify components')
    parser.add_argument('-i', '--init', action="store_true", help='Create simple blockable site framework')
    parser.add_argument('-O', '--output', help='Set path to output folder. Defaults to pwd/public_html')


    # Create working tmp folder
    if os.path.isdir(TMP_FOLDER):
        os.system("rm -fdr " + TMP_FOLDER)
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


def get_absolute_path(path):
    # Remove end /
    if path[-1] == "/":
        path = path[:-1]

    # Add pwd
    if path[0] == "/":
        return path
    else:
        return os.getcwd() + "/" + path


# Boiler plate
main()
