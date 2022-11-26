import inputs.stt as stt
import inputs.discord as discord
import inputs.email as email_stuff
import configparser
import time
import threading

use_stt = None
use_discord = None
use_email = None

def import_configs():
    global use_stt
    global use_discord
    global use_email

    config = configparser.ConfigParser()
    config.read('./config_files/config.ini')

    use_stt = config['other']['use_tts']
    use_discord = config['other']['use_discord']
    use_email = config['other']['use_email']

    if (use_stt):
        stt.picovoice_key = config['api keys']['picovoice']

    if (use_discord):
        discord.discord_bot_token = config['discord']['discord_bot_token']
        discord.discord_channel_id = config['discord']['discord_channel_id']

    if (use_email):
        email_stuff.sender_email = config['emails']['assistants_email']
        email_stuff.receiver_email = config['emails']['my_email']
        email_stuff.password = config['emails']['assistants_email_password']

import_configs()

def interperet_input(inStr):
    print(inStr)


if (use_stt):
    print('start stt')
    stt_thread = threading.Thread(target = stt.stt_init, args=(interperet_input,))
    stt_thread.start()

if (use_email):
    print('start email')
    email_stuff.email_init(interperet_input)

if (use_discord):
    print('start discord')
    discord.discord_init(interperet_input)