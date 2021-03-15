import os
import discord
from dotenv import load_dotenv
from constants import COMMANDS
import bot_functions

# Set up environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Create discord client
client = discord.Client()


# On Ready Event
@client.event
async def on_ready():
    """
    Confirm bot connection to the server
    :return:
    """
    print(
        f'{client.user} is connected to the following guilds:\n'
    )
    for guild in client.guilds:
        print(
            f'{guild.name}(id: {guild.id})'
        )


# Bot Commands
@client.event
async def on_message(message):
    """
    Process bot commands and respond with the
    corresponding bot_function
    :param message: Bot command starting with '!'
    :return:
    """
    response = None
    if message.content == COMMANDS['APOD']:
        print(f'Command: {message.content}, User: {message.author}')
        apod = bot_functions.Apod()
        response = apod.response()
    if response:
        if type(response) == list:
            # Multiple messages
            for msg in response:
                await message.channel.send(msg) \
                    if type(response) == str else \
                    await message.channel.send(**msg)  # dict msg
        else:
            # Single message
            await message.channel.send(response) \
                if type(response) == str else \
                await message.channel.send(**response)  # dict msg


# Run the bot
client.run(TOKEN)
