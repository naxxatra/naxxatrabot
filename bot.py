
import discord
from discord.ext import commands
import string
import os

import asyncio
from discord_slash import SlashCommand
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option,create_choice
from dotenv import load_dotenv
import typing
import requests
import datetime
import random
import json
import wolframalpha
load_dotenv()
from discord_components import DiscordComponents, Button, ButtonStyle
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
ddb = DiscordComponents(bot)

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
		link=f"https://discord.com/invite/{r.json()['code']}"
		await ctx.send("Click the button join Youtube Together in VC",
		components=[Button(style=ButtonStyle.URL,label="Youtube Together", url=link),
		]
		)
	
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
									'target_application_id': '880218394199220334', 
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

#Command for making polls
@bot.command()
async def make_poll(ctx, question, opt_a, opt_b, opt_c = "", opt_d = "", opt_e = "",opt_f = ""): #This can make polls upto 6 options long. Needs minimum of two options
    await ctx.message.delete() #Deletes the command message from the channel as soon as the bot reads it
    options = [opt_a, opt_b, opt_c, opt_d, opt_e, opt_f] #Storing all the options as a list
    body = ""

    for i in range(len(options)):
        if options[i] != "": #Checks if something was passed into the option before adding it to the body
            body = body + chr(65 + i) + ") " + options[i] + "\n" #Adds the option to the embed body
        else: #If one of the options is empty, all the following options are also empty. 
            break #Breaking cuz there's no need to check further
	
    rgb = (random.randint(0,255), random.randint(0,255), random.randint(0,255)) #Randomly generates colour each time the poll is generated.
    embd = discord.Embed(title = question,
                         description= body,
                         colour = discord.Color.from_rgb(rgb[0],rgb[1], rgb[2])) #making the embed
    msg = await ctx.send(embed = embd) #Sending the message

    option_emojis = ['\U0001f1e6',"\U0001f1e7","\U0001f1e8","\U0001f1e9","\U0001f1ea","\U0001f1eb"] #Emojis from :regional_indicator_a: to :regional_indicator_f:
    for i in range(len(options)): 
        if options[i] != "": #Checks if something is passed into the option before reacting with the emoji
            await msg.add_reaction(option_emojis[i])
        else: #if one option is empty, all the following ones are empty. Hence break.
            break


		
@bot.command()
async def help(ctx,*,params=None):
	if params=="youtube" or params=="yt":
		embed = discord.Embed(title="Naxxatra Bot Help", colour=discord.Colour(0xff0000), description="***Youtube Together***")

		embed.set_image(url="https://i.imgur.com/J5EETHu.png")
		embed.set_thumbnail(url="https://cdn.discordapp.com/icons/761896483838492682/756a7be666993d92c2421dd8af6d21ef.webp")

		embed.add_field(name="How to create a new watch party/youtube together:", value="\\> Join a VC (voice chat)\n\\> Run the command( `n!youtube` or  `n!yt` or you can also use the slash command `/youtube`)\n\\> Click on the blue hyperlink that the bot sent\nYou have successfully created the watch party/Youtube together",inline=False)
		embed.add_field(name="How To Use YouTube Together in a VC:", value="\\>  For the first time it will ask for authorization. You should authorize it. \n\\> After that it will take a few minutes to load.\n\\> You can then search for a YouTube video or paste the link.",inline=False)
		embed.add_field(name="How To Join an existing Watch Party/ Youtube Together:", value="\\> If someone has started the watch party in a VC then you can just hover your mouse over that channel & you will see a button to join activity.\n**OR**\n\\> You could just click on the previous hyperlink that the bot sent initially.",inline=False)
		await ctx.send(embed=embed)
	else:
		embed = discord.Embed(title="Naxxatra Bot Help", colour=discord.Colour(0x2900ff), url="https://naxxatra.com/")

		embed.set_thumbnail(url="https://cdn.discordapp.com/icons/761896483838492682/756a7be666993d92c2421dd8af6d21ef.webp")
		embed.set_footer(text="<>-Optional, []-Required")

		embed.add_field(name="`n!apod`", value="This command gives you the NASA's APOD (Astronomy Picture Of The Day)",inline=False)
		embed.add_field(name="`n!trivia <number>`", value="This command gives you a trivia fact about the number entered or a random number if no number is given",inline=False)
		embed.add_field(name="`n!search [question]`", value="Get answers to almost everything. Powered by Wolfram Alpha API",inline=False)
		embed.add_field(name="`n!youtube`", value="Watch youtube together with everyone in a VC",inline=False)
		embed.add_field(name="***SLASH COMMANDS***", value="All the above commands can also be used through Slash Commands. \nFor eg. You can use `/apod` for using n!apod command. \nSlash commands are easier to use.\n\n\n[Website](https://naxxatra.com/)\n[Github](https://github.com/naxxatra/naxxatrabot)",inline=False)

		await ctx.send(embed=embed)
	

@slash.slash(name="help",description="Get all the commands you can use with this bot",
			    options=[
               create_option(
                 name="command",
                 description="Get help regarding specific command",
                 option_type=3,
                 required=False,
				 choices=[create_choice(
					 name="Youtube",
					 value="youtube"
				 )]
               )
             ])
async def _help(ctx:SlashContext,command=None):
	if command=="youtube":
		embed = discord.Embed(title="Naxxatra Bot Help", colour=discord.Colour(0xff0000), description="***Youtube Together***")

		embed.set_image(url="https://i.imgur.com/J5EETHu.png")
		embed.set_thumbnail(url="https://cdn.discordapp.com/icons/761896483838492682/756a7be666993d92c2421dd8af6d21ef.webp")

		embed.add_field(name="How to create a new watch party/youtube together:", value="\\> Join a VC (voice chat)\n\\> Run the command( `n!youtube` or  `n!yt` or you can also use the slash command `/youtube`)\n\\> Click on the blue hyperlink that the bot sent\nYou have successfully created the watch party/Youtube together",inline=False)
		embed.add_field(name="How To Use YouTube Together in a VC:", value="\\>  For the first time it will ask for authorization. You should authorize it. \n\\> After that it will take a few minutes to load.\n\\> You can then search for a YouTube video or paste the link.",inline=False)
		embed.add_field(name="How To Join an existing Watch Party/ Youtube Together:", value="\\> If someone has started the watch party in a VC then you can just hover your mouse over that channel & you will see a button to join activity.\n**OR**\n\\> You could just click on the previous hyperlink that the bot sent initially.",inline=False)
		await ctx.send(embed=embed)
	else:
		embed = discord.Embed(title="Naxxatra Bot Help", colour=discord.Colour(0x2900ff), url="https://naxxatra.com/")
		embed.set_thumbnail(url="https://cdn.discordapp.com/icons/761896483838492682/756a7be666993d92c2421dd8af6d21ef.webp")
		embed.set_footer(text="<>-Optional, []-Required")
		embed.add_field(name="`n!apod`", value="This command gives you the NASA's APOD (Astronomy Picture Of The Day)",inline=False)
		embed.add_field(name="`n!trivia <number>`", value="This command gives you a trivia fact about the number entered or a random number if no number is given",inline=False)
		embed.add_field(name="`n!search [question]`", value="Get answers to almost everything. Powered by Wolfram Alpha API",inline=False)
		embed.add_field(name="`n!youtube`", value="Watch youtube together with everyone in a VC",inline=False)
		embed.add_field(name="***SLASH COMMANDS***", value="All the above commands can also be used through Slash Commands. \nFor eg. You can use `/apod` for using n!apod command. \nSlash commands are easier to use.\n\n\n[Website](https://naxxatra.com/)\n[Github](https://github.com/naxxatra/naxxatrabot)",inline=False)
		await ctx.send(embed=embed)

print("Loading events cogs")
bot.load_extension("cogs.events")

bot.run(os.getenv('DISCORD_TOKEN'))
