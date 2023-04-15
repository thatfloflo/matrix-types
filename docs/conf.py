# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import tomllib
from pathlib import Path
from datetime import date
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project_root_path = Path(__file__).parent.parent
with open(project_root_path / "pyproject.toml", "rb") as f:
    pyproject_toml = tomllib.load(f)

_authors = ", ".join(x[:x.find("<")].strip() for x in pyproject_toml['tool']['poetry']['authors'])

project = pyproject_toml['tool']['poetry']['name']
copyright = f'2022-{date.today().year}, {_authors}'
author = _authors
release = pyproject_toml['tool']['poetry']['version']

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
    'sphinx_toolbox',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx_toolbox.github',
    'sphinx_toolbox.sidebar_links',
    'sphinx_toolbox.more_autodoc.no_docstring',
    'sphinx_toolbox.more_autodoc.generic_bases',
    'sphinx_toolbox.more_autodoc.genericalias',
    'sphinx_toolbox.more_autodoc.regex',
    # 'sphinx_toolbox.more_autodoc.sourcelink',
    'sphinx_toolbox.more_autodoc.typehints',
    'sphinx_toolbox.more_autodoc.typevars',
    'sphinx_toolbox.more_autodoc.variables',
    'sphinx_toolbox.tweaks.param_dash',
    'sphinx_autodoc_typehints',
]

github_username = 'thatfloflo'
github_repository = 'matrix-types'

autoapi_dirs = ['../matrix_types']
autodoc_default_options = {
    'members': True,
    'private-members': False,
    'inherited-members': True,
    'undoc-members': True,
    'show-inheritance': False,
    'ignore-module-all': False,
    'class-doc-from': 'class',
}
autodoc_class_signature = 'separated'
autoclass_content = 'class'
autodoc_member_order = 'groupwise'
autodoc_typehints = 'both'
autodoc_typehints_format = 'short'
autodoc_type_aliases = {'MatrixT': 'matrix_types.MatrixT'}
autodoc_preserve_defaults = True
typehints_defaults = 'comma'
autodoc_show_sourcelink = True
python_use_unqualified_type_names = True

default_role = 'py:obj'

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'body_max_width': 'none',
    'style_external_links': True,
    'prev_next_buttons_location': 'both',
    'style_nav_header_background': '#2980B9',  # Default: #2980B9
}
html_css_files = [
    'style.css',
]
html_context = {
    "display_github": True,
    "github_user": "lart-bangor",
    "github_repo": "research-client",
    "github_version": "docs",
    "conf_py_path": "/docs/source/",
}
html_show_sphinx = False
html_static_path = ['_static']


rst_epilog = f"""
.. |project| replace:: *{project}*
"""
