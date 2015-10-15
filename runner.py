#!/usr/local/bin/python2.7
# encoding: utf-8
import json
import sys

from jinja2 import Environment, FileSystemLoader


def create():
    if len(sys.argv) == 3:
        env = Environment(loader=FileSystemLoader("."))
        configuration = env.get_template('WebGrab++.config.xml.template')
        sections = json.loads(open('template_variables.json').read())
        the_entries = {}
        country_name = sections['country_name']
        template_vars = {'xml_entries': the_entries,
                         'country_name': country_name}
        configured = configuration.render(template_vars)
        configuration_template = open(sections['template_name'], 'w')
        configuration_template.write(configured)
        configuration_template.close()


def iterate_xml_entries():
    """
    This method will open each xml file and extract the channels.
    return
        dict
    """
    pass


if __name__ == "__main__":
    sys.exit(create())