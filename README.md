# Blockable

Blockable is Ampolic's custom-made, block based static site generator written in python. The philosophy behind
blockable is that a large majority of websites use the same snippets of HTML repeatedly just with
different content. We believe snippets like this should be made into "blocks" which can be reused as many times
as need be when developing your website.

### NOTE: Blockable is still a work in progress and not ready for use yet

## Motivation/FAQ

### Why static sites?

In our experience, a majority of sites rarely change there website enough to warrant a call to an SQL server 
on every load. This makes CMS's like Wordpress impractical for most websites and unnecessarily slow.

### Why not just use Hugo or Jekyll?

One of the most important things we wanted in a site generator was well integrated support for reusing the same snippet
of code with different content. While I'm aware Hugo and Jekyll have ways of reusing code, they're weren't as fledged out as we 
would have liked.

In addition to reusing code snippets, we wanted to write the HTML in a complete coding language (even if that sometimes means 
just typing return along with a large block of HTML in quotes). Once again, I'm aware that lots of templating engine support simple
for and while loops however we believe these lack the power of a real language.

### Why not use a templating engine like Jinja?

Why learn a templating engine syntax when you can just write python and use a data object to access content?

### Why python?

I just like python

## Terminology

There are a lot of custom site generators out there and all of them use different terminology to mean different things. So to clear
things up, below is a list of the terms and how we will be using them.

### Page

A page is an HTML file. This means that every unique URL will lead to a unique page (assuming no redirects or frames). How a page looks is
determined by the __layout__ it uses.

### Layout

A layout is template used to generate a page. Layouts can be unique to a page or used by multiple pages. Which layout which page
uses is determined by the __data__ file.

### Data/Content

Data/Content is generated by a CMS like Netilfy and is stored in JSON files in the data folder. Each page has a unique data file associated
with it which specifies the layout to be used and the content to be displayed.

### Blocks

Blocks are snippets of HTML that can be used when creating page layouts.

### Templates

We use template as a catch all term to represent files capable of generating HTML when given a data file. Every type of template has a dictionaries associated
with it which is created by the file templates.py. These dictionaries can be imported when writing template (such as layouts) but be mindful to avoid recursive 
uses of templates. By default there are two types of templates, layouts and blocks. However more templates can easily be added when needed.


## Documentation

Blockable is still a work in progress (see goals for more information), however in its current state, Blockable is designed
to work like so:

When creating a website, there should be three primary folders: Blocks, Layouts, and Assets. The assets folder should contain
a folder for each type of asset you want site wide (css, js, fonts, images, etc.). The blocks and layouts folder mimic each other
in that each folder should contain a folder for each block/layout you want to create. These folders should then contain an index.py and a 
stylesheet.css and javascript.js if necessary. See the example file structure below:

TODO File Structure Image

Index.py should define one main function called html() it and should accept one variable which will contain all the content
for the html and should return the html to be displayed.

When writing your layouts, you can use blocks by importing the block function from the module "blockable" and then pass it the block you want along
with the data you'd like to give that block

  ```python
  from blockable import blocks
  blocks("nav_bar", data["nav_bar"])
  ```

# Netlify

Currently Blockable only supports Netlify as a CMS although support for more CMSs is planned in the future. In order to use Netlify,
developers should create a netlify.json file and fill it out like a normal config.yml for Netlify (See Netlify documentation for information).
The only difference is that when defining the each item in a collection, developers should add a "import" dictionary into each file instead of
of just adding fields. This means each file dictionary should contain the following keys:

import (the location of the file you'd like to import such as "layouts/homepage")  
name (the unique name of this import)  
label (the non unique label of this import)  

Folder collections can also be created by simply adding the above keys in the list of collections instead of in the "files" key of a collection you
define yourself.   

Next place a fields.json file in every layout folder and block folder that contains every netlify field you want to add. To import blocks
into layouts, use the same format as for importing layouts (import, name, and label)

Finally, run

  ```
  python netlify.py
  ```
which will generate a working config.yml for Netlify to use.
