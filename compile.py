# Compile.py
# This file will ultimately end up creating a folder will all the
# files needed for a website given the input layout and data files

# Import modules
from templates import initalize_templates


def main():
   
    # Initialize templates
    initalize_templates()

    #Import layouts
    from templates import layouts

    # Print layout as test
    print(layouts['homepage']())




# Boilerplate
if __name__ == "__main__":
    main()
