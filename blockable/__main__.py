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

    # Rsync flags
    rsync_flags = "-r --stats "

    if args["clean"]:
        rsync_flags += "--delete "
    if args["port"]:
        rsync_flags += "-e 'ssh -p " + args['port'] + "' "

    # Move to final destination and clean up
    os.system(f"rsync {rsync_flags} {TMP_FOLDER} {destination}")
    os.system(f"rm -fdr {TMP_FOLDER}")


def interpret_args(args):

    # Get and prepare destination
    destination = get_absolute_path(args["destination"])

    # Only create template if init
    if args["init"]:
        destination = args["source"]
        create_template()
        return destination

    # Change pwd to blockable instance
    if args["source"] != os.getcwd():
        os.chdir(args["source"])

    # Set final environment variable
    if args["final"]:
        os.environ["BLOCKABLE_FINAL"] = str(1)
    else:
        os.environ["BLOCKABLE_FINAL"] = str(0)

    # Create config/site depending on netlify parameter
    if args["netlify"]:
        create_config()

    if args["only_netlify"]:
        create_config()
    else:
        compile_site()

    return destination


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
            help='Set path to output folder. Defaults to pwd/public_html'
            )
    parser.add_argument(
            '-C', '--clean',
            action="store_true",
            help='Deletes everything in the output folder'
            )
    parser.add_argument(
            '-n', '--netlify',
            action="store_true",
            help='Compiles the Netlify components'
            )
    parser.add_argument(
            '-N', '--only-netlify',
            action="store_true",
            help='Only compiles the Netlify components'
            )
    parser.add_argument(
            '-p',
            '--port',
            help='Set the port for rsync to use'
            )
    parser.add_argument(
            '-f',
            '--final',
            action="store_true",
            help='Compiles final optimized version of the site'
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
    if path[0] == "/" or ("@" in path and ":" in path):
        return path
    else:
        return os.getcwd() + "/" + path


# Boiler plate
main()
