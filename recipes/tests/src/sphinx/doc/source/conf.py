import os
import sys
import sphinx_rtd_theme
sys.path.insert(0, os.path.abspath('.'))

project = 'Testdocumentation'

extensions = [
    'sphinx-prompt',
    'sphinx.ext.todo',
    #'breathe',
    'sphinx_rtd_theme',
    'sphinxcontrib.plantuml'
]

exclude_patterns = []

html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    # Table of contents options
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False,
    # Miscellaneous options
    'display_version': True,
    'logo_only': False,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': 'blob',
    'style_nav_header_background': '#2980B9',    
}

# Display todos by setting to True
todo_include_todos = True

# Breathe Configuration
# !!! Don't change the two lines below !!!
#breathe_projects = { project:os.environ['SPHINX_DOXYGEN_XML_PATH'] }
#breathe_default_project = project

# PlantUML configuration
plantuml = 'java -jar {}/plantuml.jar'.format(os.environ['PLANTUML_PATH'])
plantuml_output_format = 'svg'