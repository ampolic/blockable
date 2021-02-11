# index.py
import sys


def html():
    from templates import blocks
    HTML = "<h1>This is a header</h1>"
    HTML += blocks["about"]()
    return HTML
