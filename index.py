import inputs.stt as stt
import configparser
import time

def import_configs():
    config = configparser.ConfigParser()
    config.read('./config_files/config.ini')
    stt.picovoice_key = config['api keys']['picovoice']

import_configs()

def interperet_input(inStr):
    print(inStr)

stt.stt_init(interperet_input)