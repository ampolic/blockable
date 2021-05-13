"""
file: blocks.py

This file is meant to be imported by developers so they can
access all the block functions in their "blocks" folder
"""


def initalize_blocks():
    # Import modules
    import os
    from .blockable import get_template

    # Loop though list of blocks and add them to global name space
    for block in os.listdir("blocks"):
        globals()[block] = get_template("blocks/" + block)


# Boiler plate
initalize_blocks()
