# Blockable.py
# This file implements all the necessary functions for blockable. Running it, will
# currently print out all the layouts html return.


def main():
    # Import modules
    import os

    # Get list of layouts
    layouts_list = os.listdir("layouts")

    # Get data
    data = []

    # Compile and save layouts
    for layout in layouts_list:
        html = layouts(layout, data)
        save(layout, html)




def save(layout, html):
    """
    This function will save the layout given a file name
    and html
    """

    # Temp, just print out layout name then html
    print(layout)
    print(html)



def layouts(layout, data):
    """
    This function accepts a layout name and a data json then calls the html
    function of the given layout, passing it the data parameter. The function
    returns whatever html the layout function returns
    """

    # Import modules
    import sys

    # Add template path
    sys.path.insert(1, "layouts/" + layout)
    
    # Import html function from the index file
    from index import html as layout_function

    # Remove template from module directory
    sys.modules.pop("index")
    
    # Remove template path
    sys.path.remove("layouts/" + layout)

    
    # Add html function to dictionary
    html = layout_function(data)
    
    # Return html
    return html


def blocks(block, data):
    """
    This function accepts a block name and a data json then calls the html
    function of the given block, passing it the data parameter. The function
    returns whatever html the block function returns
    """

    # Import modules
    import sys

    # Add template path
    sys.path.insert(1, "blocks/" + block)
    
    # Import html function from the index file
    from index import html as block_function
    
    # Add html function to dictionary
    html = block_function(data)
    
    # Remove template from module directory
    sys.modules.pop("index")
    
    # Remove template path
    sys.path.remove("blocks/" + block)

    # Return html
    return html



# Boilerplate
if __name__ == "__main__":
    main()
