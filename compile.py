# Compile.py
# This file will ultimately end up creating a folder will all the
# files needed for a website given the input layout and data files

# Import modules
import sys


def main():
    # Import Blocks
    blocks = import_blocks()
    
    # Import Layouts
    layouts = import_layouts()
    
    # Get HTML
    data = layouts["homepage"].html(blocks)
    
    # Print HTML
    print(data)

def import_blocks():
    """
    This function takes in an array of blocks and returns
    a dictionary of block html functions
    """

    # Add blocks system path and import blocks
    sys.path.insert(1, 'blocks')
    from about.index import html as about 
    sys.path.remove('blocks')
 
    # Create dict of blocks
    blocks = {"about" : about}
    
    # Return dict of blocks
    return blocks

def import_layouts():
    """
    This function takes in an array of layouts and returns
    a dictionary of the layouts html functions
    """

    # Add layouts system path and import layouts
    sys.path.insert(1, 'layouts')
    from homepage import index as homepage
    sys.path.remove('layouts')
   
    # Create dict of layouts
    layouts = {"homepage" : homepage}

    # Return dict of layouts
    return layouts


# Boilerplate
if __name__ == "__main__":
    main()
