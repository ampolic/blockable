# index.py

def html(data):
    from blockable import blocks

    HTML = "<h1>The title is: " + data["title"] + "</h1>" + "\n"
    HTML += blocks("about", data["about"]) + "\n"
    HTML += blocks("nav_bar", {})

    return HTML
