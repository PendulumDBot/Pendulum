import logging
import os

path = os.getcwd()

logging.basicConfig(filename = f'{path}/src/error.log', level=logging.DEBUG)

logging.debug(f'Logs are a go!')