import logging
import os

path = os.getcwd()

logging.basicConfig(filename = f'{path}/error.log', level=logging.WARNING)

logging.debug(f'Logs are a go!')