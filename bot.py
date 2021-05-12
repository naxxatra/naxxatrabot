
import discord
from discord.ext import commands
import string
import os

import asyncio
from discord_slash import SlashCommand
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from dotenv import load_dotenv
import typing
import requests
import datetime
import json


load_dotenv()

def command_prefix(bot, message):
    if message.guild is None:
        return ''
    else:
        return 'n!'


async def get_prefix(ctx):
  return '' if ctx.guild is None else 'n!'

bot = commands.Bot(command_prefix)
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():   
  print(f'Logged in as {bot.user}!')
  activity = discord.Game(name=f"n!help | Naxxatra Bot")
  await bot.change_presence(activity=activity)

  
def apod_get():
	url = f"https://api.nasa.gov/planetary/apod?api_key={os.getenv('NASA_API_KEY')}"
	r=requests.get(url)
	content=r.json()
	embed=discord.Embed(title=content['title'], description=content['explanation'] , colour=discord.Colour(0x0B3D91))
	embed.set_author(name="NASA APOD", url="https://apod.nasa.gov/", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/NASA_logo.svg/1237px-NASA_logo.svg.png")
	embed.set_image(url=content['url'])
	embed.set_footer(text=content['date'])
	return embed

@bot.command(name="apod" ,description="Get NASA's APOD( Astronomy picture of the day )")
async def apod(ctx):
	await ctx.send(embed=apod_get())
	#print(r.content)

@slash.slash(name="apod",
             description="Get NASA's APOD( Astronomy picture of the day )")
async def _apod(ctx):
  await ctx.send(embed=apod_get())

def trivia_get(number):
	try:
		number=int(number)
	except:
		number='random'
	url=f"http://numbersapi.com/{number}"
	r=requests.get(url=url)
	#print(r.text)
	embed=discord.Embed(title="Trivia facts",description=r.text,colour=discord.Colour(0x32CD32))
	return embed

@bot.command()
async def trivia(ctx,*,arg='random'):
	await ctx.send(embed=trivia_get(arg))

@slash.slash(name="trivia",
             description="Get trivia facts about a specific number or a random number",
			    options=[
               create_option(
                 name="number",
                 description="Enter a number or get a fact about a random number",
                 option_type=4,
                 required=False
               )
             ]
			 )
async def _trivia( ctx: SlashContext, number: typing.Optional[int] = 'random',):
  await ctx.send(embed=trivia_get(number))



bot.run(os.getenv('DISCORD_TOKEN'))
