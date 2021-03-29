
def html(data):

    HTML = ""

    for service in data["services"]:
        HTML += "Name: " + service["name"]
        HTML += "Price: " + service["price"]
        HTML += "Photo: " + service["photo"]


    return HTML
