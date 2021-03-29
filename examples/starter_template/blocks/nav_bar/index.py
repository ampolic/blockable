def html(data):

    from blockable import site_data

    site_color = site_data("settings/nav_bar")["site-color"]

    return "<p> The site color is: " + site_color
