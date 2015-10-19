#!/usr/local/bin/python2.7
# encoding: utf-8
import codecs
import json
import os
import sys

from urllib2 import URLError, HTTPError

from jinja2 import Environment, FileSystemLoader
from logger import logging

from runner import generate_file
log = logging.getLogger('development')


def create():
    env = Environment(loader=FileSystemLoader("."))
    try:
        configuration = env.get_template('WebGrab++.config.xml.template')
        sections = json.loads(open('template_variables.json').read())
        country_name = sections['country_name']

        if country_name is None:
            raise Exception(sections['no_country_config'])

        channel_folder = os.path.join(os.path.dirname(__file__), 'channels')
        channel_list = generate_file(channel_folder)
        log.info("I'm writting the file")
        log.debug(channel_list.values())
        template_vars = {'xml_entries': "\n".join(channel_list.values()),
                         'country_name': country_name}
        configured = configuration.render(template_vars)
        configuration_template = codecs.open(sections['template_name'], 'w',
                                             "utf8")
        configuration_template.write(configured)
        configuration_template.close()
        log.info("Application finished")
    except HTTPError as e:
        msg = "Network error.\nCode: {code}\nReason:{reason}"\
            .format(code=e.code, reason=e.reason)
        log.debug(msg)
        log.error(msg)
    except URLError as e:
        msg = "Network error.\nCode: {code}\nReason:{reason}"\
            .format(code=e.code, reason=e.reason)
        log.debug(msg)
        log.error(msg)
    except IOError as e:
        msg = "Obtained an IOError. {}.\nDid you "\
            "create the template_variables.json file?".format(e)
        log.error(msg)


if __name__ == "__main__":
    sys.exit(create())
