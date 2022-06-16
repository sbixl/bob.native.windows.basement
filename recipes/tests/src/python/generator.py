import os
import argparse

from datetime import date
from jinja2 import Environment, FileSystemLoader
from jinja2 import exceptions as jinjaExceptions

if __name__ == '__main__':

    print("Running simple Codegenerator...")

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--outDir'
                        , help='absolute path to the output directory the generated file should be saved'
                        , nargs=1, required=True)

    args = parser.parse_args()

    outDir = args.outDir[0]

    env = Environment(loader=FileSystemLoader(os.path.dirname(os.path.realpath(__file__))))

    file = "template.jinja"

    try:
        template = env.get_template(file)
    except jinjaExceptions.TemplateNotFound:
        raise jinjaExceptions.TemplateNotFound(str('Template file \'{}\' not found!'.format(file)))

    rendered = template.render(
        Name="TestFile",
        Date=date.today().strftime("%B %d, %Y")
    )

    outputFile = open(os.path.join(outDir, 'GeneratedFile.txt'), 'w')
    outputFile.write(rendered)
    outputFile.close()
