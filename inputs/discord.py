import asyncio
import discord
from discord.ext import tasks

discord_bot_token = None
discord_channel_id = None

translate_speech = None

client = discord.Client(intents=discord.Intents.all())

def discord_init(interperet_speech):
	global translate_speech
	translate_speech = interperet_speech

	client.run(discord_bot_token)


@client.event
async def on_message(message):
    if (message.author == client.user):
        return

    print('on_message content: ' + message.content + ', channel: ' + message.channel)
    print(message.content)
    translate_speech(message.content)

@client.event
async def on_ready():
    print('Discord bot logged in as: ' + client.user.name + ', ' + client.user.id)
    task_loop.start()

@tasks.loop(seconds=10)
async def task_loop():
    global speech_text
    if (speech_text != None):
        await client.get_channel(int(discord_channel_id)).send(speech_text)
        speech_text = None