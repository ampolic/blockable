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

    # Remove pychach from list
    if "__pycache__" in templates:
        templates.remove("__pycache__")

    # Define dict
    template_dict = {}

    # Add template type path
    sys.path.insert(1, template_type)

    # Import each template
    for template in templates:
        """
        This for loop works by calling the python import function
        and importing each file based on its name given in the templates list.
        The loop then adds each modules html function to a dict accessible by its name.
        Finally the loop removes the template module from the modules dict so that
        templates of the same name but different type may be loaded
        """

        # Import template module (ie: "from homepage import index as template_module" [except it only imports the html function])
        template_module = __import__(template + ".index", globals(), locals(), "html")
        
        # Add HTML function to dict
        template_dict[template] = template_module.html

        # Remove template from module directory
        sys.modules.pop(template)
        sys.modules.pop(template + ".index")

    # Remove template type path
    sys.path.remove(template_type)

    # Return dict
    return template_dict
