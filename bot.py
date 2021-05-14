
import discord
from discord.ext import commands
import string
import os

import asyncio
from discord_slash import SlashCommand
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
import typing
import requests
import datetime
import json
import wolframalpha
client = wolframalpha.Client(os.getenv('WOLFRAM_ID'))




def command_prefix(bot, message):
    if message.guild is None:
        return ''
    else:
        return 'n!'


async def get_prefix(ctx):
  return '' if ctx.guild is None else 'n!'

bot = commands.Bot(command_prefix, case_insensitive=True)
slash = SlashCommand(bot, sync_commands=True)
bot.remove_command('help')

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

def get_wolfram(query):
	res = client.query(query)
	answer = next(res.results).text
	return answer

@bot.command()
async def search(ctx,*,arg):

	embed=discord.Embed(title=f"{arg}",description=f"{get_wolfram(arg)}",colour=discord.Colour(0xFF7F50))
	embed.set_author(name="Wolfram Alpha",url="https://www.wolframalpha.com/",icon_url="https://i.imgur.com/uX2g1SL.png")
	embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
	await ctx.send(embed=embed)





@slash.slash(name="search",
             description="Get answers to almost everything. Powered by Wolfram Alpha API",
			    options=[
               create_option(
                 name="question",
                 description="Type your question/query",
                 option_type=3,
                 required=True
               )
             ]
			 )
async def _search_web( ctx: SlashContext, question):
	res = client.query(question)
	#print(next(res.results).text)
	repl = str(next(res.results).text)
	##embed=discord.Embed(title=question, description=repl,colour=discord.Colour(0xFF7F50))
	#embed.set_author(name="Wolfram Alpha",url="https://www.wolframalpha.com/",icon_url="https://i.imgur.com/uX2g1SL.png")
	#embed.set_footer(text=f"Requested by: {ctx.author}",icon_url=ctx.author.avatar_url)
	await ctx.send("Results from Wolfram Alpha: ```\n"+repl+"\n```")


@bot.command(aliases=['youtube','youtubetogether'])
#@bot.command()
async def yt(ctx):
	try:
		channel = ctx.author.voice.channel
		url = f"https://discord.com/api/v9/channels/{channel.id}/invites"
		params = {
									'max_age': 86400,
									'max_uses': 0,
									'target_application_id': '755600276941176913', 
									'target_type': 2,
									'temporary': False,
									'validate': None
								}
		headers={'content-type': 'application/json','Authorization': f"Bot {os.getenv('DISCORD_TOKEN')}"}
		r=requests.post(url, data=json.dumps(params), headers=headers)
		#embed=discord.Embed(title="Youtube Together", description="Click on the title to join",url=f"https://discord.com/invite/{r.json()['code']}")
		embed = discord.Embed(title="Youtube Together",colour=discord.Colour(0xFF0000))
		embed.description = f"[Click Here to Join Youtube Together in the VC](https://discord.com/invite/{r.json()['code']})"
		await ctx.send(embed=embed)
	
	except AttributeError:
		await ctx.send("You Are not in a VC")
	except:
		await ctx.send("There is some error in starting Youtube Togther or I don't have permission to create invite in that channel")

@slash.slash(name="youtube_together",description="Watch youtube together with everyone in a VC")
async def yt_t(ctx: SlashContext):
	try:
		channel = ctx.author.voice.channel
		#print(channel)
		url = f"https://discord.com/api/v9/channels/{channel.id}/invites"
		params = {
									'max_age': 86400,
									'max_uses': 0,
									'target_application_id': '755600276941176913', 
									'target_type': 2,
									'temporary': False,
									'validate': None
								}
		headers={'content-type': 'application/json','Authorization': f"Bot {os.getenv('DISCORD_TOKEN')}"}
		r=requests.post(url, data=json.dumps(params), headers=headers)
		#print(r.json())
		#embed=discord.Embed(title="Youtube Together", description="Click on the title to join",url=f"https://discord.com/invite/{r.json()['code']}")
		embed = discord.Embed(title="Youtube Together",colour=discord.Colour(0xFF0000))
		embed.description = f"[Click Here to Join Youtube Together in the VC](https://discord.com/invite/{r.json()['code']})"
		await ctx.send(embed=embed)
	
	except AttributeError:
		await ctx.send("You Are not in a VC")
	except:
		await ctx.send("There is some error in starting Youtube Togther or I don't have permission to create invite in that channel")

@bot.command()
async def help(ctx):
	embed = discord.Embed(title="Naxxatra Bot Help", colour=discord.Colour(0x2900ff), url="https://naxxatra.com/")

	embed.set_thumbnail(url="https://cdn.discordapp.com/icons/761896483838492682/756a7be666993d92c2421dd8af6d21ef.webp")
	embed.set_footer(text="<>-Optional, []-Required")

	embed.add_field(name="`n!apod`", value="This command gives you the NASA's APOD (Astronomy Picture Of The Day)",inline=False)
	embed.add_field(name="`n!trivia <number>`", value="This command gives you a trivia fact about the number entered or a random number if no number is given",inline=False)
	embed.add_field(name="`n!search [question]`", value="Get answers to almost everything. Powered by Wolfram Alpha API",inline=False)
	embed.add_field(name="`n!youtube`", value="Watch youtube together with everyone in a VC",inline=False)
	embed.add_field(name="***SLASH COMMANDS***", value="All the above commands can also be used through Slash Commands. \nFor eg. You can use `/apod` for using n!apod command. \nSlash commands are easier to use.\n\n\n[Website](https://naxxatra.com/)\n[Github](https://github.com/naxxatra/naxxatrabot)",inline=False)

	await ctx.send(embed=embed)

@slash.slash(name="help",description="Get all the commands you can use with this bot")
async def _help(ctx:SlashContext):
	embed = discord.Embed(title="Naxxatra Bot Help", colour=discord.Colour(0x2900ff), url="https://naxxatra.com/")

	embed.set_thumbnail(url="https://cdn.discordapp.com/icons/761896483838492682/756a7be666993d92c2421dd8af6d21ef.webp")
	embed.set_footer(text="<>-Optional, []-Required")

	embed.add_field(name="`n!apod`", value="This command gives you the NASA's APOD (Astronomy Picture Of The Day)",inline=False)
	embed.add_field(name="`n!trivia <number>`", value="This command gives you a trivia fact about the number entered or a random number if no number is given",inline=False)
	embed.add_field(name="`n!search [question]`", value="Get answers to almost everything. Powered by Wolfram Alpha API",inline=False)
	embed.add_field(name="`n!youtube`", value="Watch youtube together with everyone in a VC",inline=False)
	embed.add_field(name="***SLASH COMMANDS***", value="All the above commands can also be used through Slash Commands. \nFor eg. You can use `/apod` for using n!apod command. \nSlash commands are easier to use.\n\n\n[Website](https://naxxatra.com/)\n[Github](https://github.com/naxxatra/naxxatrabot)",inline=False)

	await ctx.send(embed=embed)

bot.run(os.getenv('DISCORD_TOKEN'))