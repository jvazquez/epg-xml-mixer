#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

"""
Author: Jorge Omar Vazquez <jorgeomar.vazquez@gmail.com>
"""
import json
import pickledb
import sys


from HTMLParser import HTMLParser

from logger import logging
from lxml import etree
from lxml.etree import tostring


from jinja2 import Environment, FileSystemLoader

log = logging.getLogger('development')


def create():
    try:
        sections = json.loads(open('template_variables.json').read())

        country_name = sections['country_name']
        if country_name is None:
            raise Exception(sections['no_country_config'])
        if len(sys.argv) != 3:
            raise Exception("you need two files to compare.")

        xml_file = sys.argv[1]
        new_xml = sys.argv[2]
        generate_diff(xml_file, new_xml)

        log.info("Application finished")
    except IOError as e:
        msg = "Obtained an IOError. {}.\nDid you "\
            "create the template_variables.json file?".format(e)
        log.error(msg)


def generate_diff(xml_file, new_xml):
    parser = etree.XMLParser()
    new_parser = etree.XMLParser()

    xml_file_db = pickledb.load('original.db', False)

    channel = open(xml_file, 'r').read()
    new_channels = open(new_xml, 'r').read()

    root = etree.fromstring(channel, parser)
    nodes = root.xpath('//channel')

    root_new = etree.fromstring(new_channels, new_parser)
    nodes_new = root_new.xpath('//channels/channel')

    for node in nodes:
        # the_id = node.get('xmltv_id').encode('utf8')
        the_id = HTMLParser().unescape(node.get('xmltv_id')).lower()\
                .replace(' ', '')
        xml_file_db.set(the_id, True)

    for node in nodes_new:
        the_id = HTMLParser().unescape(node.get('xmltv_id')).lower()\
                .replace(' ', '')
        was_found = xml_file_db.get(the_id)
        if was_found is None:
            raw_node = tostring(node).strip()
            print "Add {} to the file".format(raw_node)

if __name__ == "__main__":
    sys.exit(create())
