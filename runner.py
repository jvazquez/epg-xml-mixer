#!/usr/local/bin/python2.7
# encoding: utf-8
import codecs
import json
import os
import sys
import zipfile

from HTMLParser import HTMLParser
from StringIO import StringIO
from urllib2 import urlopen, URLError, HTTPError

from logger import logging
from lxml import etree
from lxml.etree import tostring


from jinja2 import Environment, FileSystemLoader

log = logging.getLogger('development')


def create():
    env = Environment(loader=FileSystemLoader("."))
    try:
        configuration = env.get_template('WebGrab++.config.xml.template')
        sections = json.loads(open('template_variables.json').read())

        country_name = sections['country_name']
        if country_name is None:
            raise Exception(sections['no_country_config'])

        if ' ' in country_name:
            log.error("Please do the following"
                      "Download the zip file and place it on the channels "
                      "folder \n If you have any old entry (ini or xml) "
                      "inside there, delete them "
                      "Unzip the zipfile and then delete the zip file "
                      "execute python manual_runner.py")
            sys.exit()
        url = sections['url_webgrab'].format(country_name=country_name)
        log.debug("Performing step one. Download zip from {url}"
                  .format(url=url))
        zip_resource = obtain_zip_file(url)
        unzip_into_folder(zip_resource)
        channel_folder = os.path.join(os.path.dirname(__file__), 'channels')
        channel_list = generate_file(channel_folder)
        log.info("I'm writting the file")
        log.debug(channel_list.values())

        template_vars = {'xml_entries': "\n".join(channel_list.values()),
                         'country_name': country_name}
        configured = configuration.render(template_vars)
        configuration_template = codecs.open(sections['template_name'], 'w',
                                             'utf8')
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


def obtain_zip_file(url):
    """
    Will perform a get and obtain the zip file

    params
        url string A string that is used to perform the get
    """
    msg = "Starting to download url {}".format(url)
    log.info(msg)
    zip_resource = None
    response = urlopen(url)
    zip_resource = response.read()
    return zip_resource


def unzip_into_folder(channels_zip_stream):
    """
    Receives a zip resource file  and extracts it into the channels folder
    """
    channel_folder = os.path.join(os.path.dirname(__file__), 'channels')
    log.info("I'm removing any possible old entry")
    _clean_old_entries(channel_folder)
    zipdata = StringIO()
    zipdata.write(channels_zip_stream)
    channels_zip_file = zipfile.ZipFile(zipdata)
    log.debug("I'm unzipping into {chan}."
              .format(chan=channel_folder))

    for name in channels_zip_file.namelist():
        channels_zip_file.extract(name, channel_folder)


def _clean_old_entries(channel_folder):
    for channel_files in os.listdir(channel_folder):
        is_xml = channel_files.endswith('.xml')
        is_ini = channel_files.endswith('.ini')
        if is_xml or is_ini:
            target = os.path.join(channel_folder, channel_files)
            os.remove(target)


def generate_file(channel_folder):

    all_the_channels = {}
    log.info(channel_folder)
    # parser = etree.XMLParser(recover=True, encoding="utf8")
    parser = etree.XMLParser()
    for channel_entries in os.listdir(channel_folder):
        target = os.path.join(channel_folder, channel_entries)
        is_xml = target.endswith('.xml')
        if is_xml:
            channel = open(target, 'r').read()
            # root = etree.parse(target, parser=parser)
            root = etree.fromstring(channel, parser)
            nodes = root.xpath('//channels/channel')
            for node in nodes:
                # the_id = node.get('xmltv_id').encode('utf8')
                the_id = node.get('xmltv_id')
                if the_id not in all_the_channels.keys():
                    name = HTMLParser().unescape(tostring(node).strip())
                    all_the_channels.update({the_id: name})
    return all_the_channels


if __name__ == "__main__":
    sys.exit(create())
