"""
file: __main__.py

This file implments the command line interface for blockable
"""

# Import modules
import os
import argparse

from .blockable import TMP_FOLDER
from .template import create_template
from .core import compile_site
from .netlify import create_config


def main():

    # Create working directory
    if os.path.isdir(TMP_FOLDER):
        os.system("rm -fdr " + TMP_FOLDER)
    os.mkdir(TMP_FOLDER)

    # Get arguments
    args = get_args()

    # Interpret arguments
    destination = interpret_args(args)

    # Move to final destination and clean up
    sudo(destination, "cp -r " + TMP_FOLDER + "/* " + destination + "/")
    os.system("rm -fdr " + TMP_FOLDER)


def interpret_args(args):

    # Get and prepare destination
    destination = get_absolute_path(args["destination"])
    if args["clean"]:
        sudo(destination, "rm -fdr " + destination)
    if not os.path.isdir(destination):
        sudo(destination, "mkdir " + destination)

    # Only create template if init
    if args["init"]:
        destination = args["source"]
        create_template()
        return destination

    # Change pwd to blockable instance
    if args["source"] != os.getcwd():
        os.chdir(args["source"])

    # Create config/site depending on netlify parameter
    if not args["netlify"]:
        compile_site()
    create_config()

    return destination


def sudo(folder, command):
    if os.access(folder, os.W_OK):
        os.system(command)
    else:
        os.system("sudo " + command)


def get_args():

    # Set up arguments
    parser = argparse.ArgumentParser(
            description='Python based static site generator'
            )
    parser.add_argument(
            'source',
            help='Set path to blockable folder'
            )
    parser.add_argument(
            'destination',
            nargs='?',
            default='public_html',
            help='Set path to output folder. Defaults to pwd/public_html'
            )
    parser.add_argument(
            '-C', '--clean',
            action="store_true",
            help='Deletes everything in the output folder'
            )
    parser.add_argument(
            '-N', '--netlify',
            action="store_true",
            help='Only compiles the Netlify components'
            )
    parser.add_argument(
            '-i',
            '--init',
            action="store_true",
            help='Create simple blockable site framework'
            )

    # Return parsed arguments
    return vars(parser.parse_args())


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
