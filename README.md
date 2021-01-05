# Blockable

Blockable is Ampolic's custom-made, block based static site generator written in python. The philosophy behind
blockable is that a large majority of websites use the same snippets of HTML over and over again just with
different content. We believe snippets like this should be made into "blocks" which can be reused as many times
as need be when developing your website.

### NOTE: Blockable is still a work in progress and not ready for use yet

## Motivation/FAQ

### Why static sites?

In our experience a majority of sites rarely change and/or have anywhere near enough content to warrant the
use of an SQL database. This makes CMS's like Wordpress impractical and unnecessarily slow for most websites.

### Why not just use Hugo or Jekyll?

One of the most important things we wanted in a site generator was well integrated support for reusing the same snippet
of code with different content. While I'm aware Hugo and Jekyll have ways of reusing code, they're weren't as fledged out as I 
would have liked.

In addition to reusing code snippets, I wanted to write the HTML in a complete coding language (even if that sometimes means 
just typing return along with a large block of HTML in quotes). Once again, I'm aware that lots of templating engine support simple
for and while loops however I believe these lack the power of a real language.

### Why python?

I just like python

## Documentation

Blockable is still a work in progress (see goals for more information), however in its current state, Blockable is designed
to work like so:

When creating a website, there should be three primary folders: Blocks, Layouts, and Assets. The assets folder should contain
a folder for each type of asset you want site wide (css, js, fonts, images, etc.). The blocks and layouts folder mimic each other
in that each folder should contain a folder for each block/layout you want to create. These folders should then contain an index.py and
__init__.py file. See the example file structure below:

TODO File Structure Image

Index.py should define two functions. The first function should be called html() and should accept one variable which will contain all
the content for the html and should return the html to be displayed. The second function should be called fields() and it should return
an object of all the content needed by the html function (this is still a work in progress).

When writing your layouts, you can use blocks by accessing the global block dictionary and passing it the data variable like so:

blocks["nav_bar"](data)

## Goals

- Write more complete documentation
- Write support for fields function
