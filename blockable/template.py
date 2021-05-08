"""
file: template.py

This implements the functions necessary to create a template blockable
instance for people to get started with
"""

# Import modules and set constants
import os
import json
from .blockable import TMP_FOLDER
from .netlify import FIELDS_FILE_NAME as FFN


def create_template():
    # Create basic blockable instance folders
    for folder in ["assets", "layouts", "blocks", "data"]:
        os.mkdir(TMP_FOLDER + "/" + folder)
    for layout in ["homepage"]:
        os.mkdir(TMP_FOLDER + "/layouts/" + layout)
    for block in ["nav_bar", "about"]:
        os.mkdir(TMP_FOLDER + "/blocks/" + block)
    for asset in ["css", "js", "images"]:
        os.mkdir(TMP_FOLDER + "/assets/" + asset)

    # Create and save json files
    netlify_config = {
        "backend": {
            "name": "github",
            "repo": "user/repo_name",
            "branch": "main",
            "site_domain": "cms.netlify.com",
            "api_root": "https://api.github.com"
        },
        "media_folder": "assets/images",
        "collections": [
            {
                "label": "Settings",
                "name": "settings",
                "files": [
                    {
                        "label": "Nav Bar",
                        "name": "nav_bar",
                        "import": "blocks/nav_bar"
                    }
                ]
            },
            {
                "label": "Pages",
                "name": "pages",
                "files": [
                    {
                        "import": "layouts/homepage",
                        "label": "Homepage",
                        "name": "index"
                    },
                ]
            }
        ]
    }
    homepage_fields = [
        {"label": "Title", "name": "title", "widget": "string"},
        {"label": "About", "name": "about", "import": "blocks/about"}
    ]
    about_fields = [
        {"label": "About", "name": "about", "widget": "string"}
    ]
    nav_bar_fields = [
        {"label": "Site Color", "name": "site-color", "widget": "color"}
    ]

    save_json(TMP_FOLDER + "/netlify.json", netlify_config)
    save_json(TMP_FOLDER + "/layouts/homepage/" + FFN, homepage_fields)
    save_json(TMP_FOLDER + "/blocks/about/" + FFN, about_fields)
    save_json(TMP_FOLDER + "/blocks/nav_bar/" + FFN, nav_bar_fields)


def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
