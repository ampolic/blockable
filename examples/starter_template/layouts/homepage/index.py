# index.py
import sys


def html(data):
    from blockable import blocks
    HTML = "<h1>This is a header</h1>"
    HTML += blocks("about", data["about"]
    return HTML
