__author__ = 'arnab'

import logging

logging.basicConfig(filename='debug.log', filemode='w', level=logging.DEBUG)
logging.basicConfig(filename='info.log', filemode='w', level=logging.INFO)
logging.basicConfig(filename='error.log', filemode='w', level=logging.ERROR)