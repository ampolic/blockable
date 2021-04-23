"""
file: blockable.py

This file contains functions and constants used by the other various modules of
blockable
"""

# Set constant
TMP_FOLDER = "/tmp/blockable"


def get_template(template_path):
    # This function accepts a template path and returns the function of that template

    # Add template path
    import sys
    sys.path.insert(1, template_path)
    
    # Import html function then clean up sys path
    from index import main as template_function
    sys.modules.pop("index")
    sys.path.remove(template_path)

    return template_function


def parse_json(file_dir):
    # Open file and return parsed json
    import json
    with open(file_dir, 'r') as file:
        return json.load(file)
