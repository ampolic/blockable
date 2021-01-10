# Templates.py
# This file creates and stores the dicts of every template type.
# Layout files should import these dicts to use in development.


def initalize_templates():
    """
    This function creates a global dict for each template type
    that other python files can import
    """

    # Generate list of template types
    template_types = ["layouts", "blocks"]

    # Create global dicts of templates
    for template_type in template_types:
        globals()[template_type] = import_templates(template_type)



def import_templates(template_type):
    """
    This function takes the name of a template type
    and returns a dictionary of the all the html functions.
    """

    # Import necessary modules
    import sys
    import os

    # Create list of all folders in template folder
    templates = os.listdir(template_type)

    # Define dict
    template_dict = {}

    # Import each template
    for template in templates:
        """
        This loop works by inserting the path to each template folder in the list
        of templates, importing the html function from the index file, adding
        the html function to a dictionary, and then finally removing the
        module from the directory so others of the same name can be imported
        and remove the template path so others can take its place.
        """
        
        # Add template path
        sys.path.insert(1, template_type + "/" + template)

        # Import html function from the index file in the newly added path
        from index import html
        
        # Add HTML function to dictionary
        template_dict[template] = html

        # Remove template from module directory
        sys.modules.pop("index")

        # Remove template path
        sys.path.remove(template_type + "/" + template)

    # Return dict
    return template_dict
