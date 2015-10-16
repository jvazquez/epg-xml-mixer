# -*- coding: utf-8 -*-

"""
Author: Jorge Omar Vazquez <jorgeomar.vazquez@gmail.com>
"""
import json
import logging
import logging.config
import os

DEFAULT_LEVEL = logging.INFO
logging_path = os.path.join(os.path.dirname(__file__), 'logging.json')


if os.path.exists(logging_path):
    with open(logging_path, 'rt') as f:
        config = json.load(f)
        logging.config.dictConfig(config)
else:
    logging.basicConfig(level=DEFAULT_LEVEL)