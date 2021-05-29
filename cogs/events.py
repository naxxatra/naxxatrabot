from os import name, read
from discord import user
from discord.ext import commands
import discord
import time
import json
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord.ext.commands.core import Command, command



class events(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.command()
    async def add_event(self,ctx,title,*,description):
        if ctx.guild==None:
            await ctx.send("Sorry! This command can only run in servers")
        else:
            if ctx.author.guild_permissions.manage_guild:
                f = open("./event.json", "r+")
                user_dict= f.read()
                user_dict=json.loads(user_dict)
                f.close()
                if user_dict['channel'] != "":
                    chnl=int(user_dict['channel'])
                    dis_channel = self.bot.get_channel(chnl)   
                    user_list=[]
                    embed=discord.Embed(title=title,description=description,colour=discord.Colour(0xF6B35F))
                    embed.add_field(name="Attendees",value="Naxxatra")
                    embed.set_footer(text="If you want to participate/attend this event the please react with ✅")
                    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/761896483838492682/756a7be666993d92c2421dd8af6d21ef.png?size=4096")
                    msg= await dis_channel.send(embed=embed)
                    embed.set_author( name=f"Event ID: {msg.id}",icon_url="https://cdn.discordapp.com/icons/761896483838492682/756a7be666993d92c2421dd8af6d21ef.png?size=4096")
                    await msg.edit(embed=embed)
                    react = await msg.add_reaction('✅')
                    f = open("./event.json", "r")
                    user_list= f.read()
                    user_list=json.loads(user_list)
                    f.close()
                    f=open("./event.json","w")
                    user_list[msg.id]=[]
                    f.write(json.dumps(user_list))
                    f.close()
                    await ctx.send("Event created")
                else:
                    await ctx.send("Looks like the event channel is not set. Please set it using the command `n!set_channel [channel]` or using slash command.")

            else:
                await ctx.send("Sorry, You don't have permission to do that.")

    @cog_ext.cog_slash(name="add_event" , description = "Add a server event",
    options=[
               create_option(
                 name="title",
                 description="Add the title for the event",
                 option_type=3,
                 required=True
               ),
			    create_option(
                 name="description",
                 description="Add the description for the event",
                 option_type=3,
                 required=True,
               )
             ])
    async def _event_add(self, ctx: SlashContext, title: str , description: str):
        if ctx.guild==None:
            await ctx.send("Sorry! This command can only run in Servers")
        else:
            if ctx.author.guild_permissions.manage_guild:
                f = open("./event.json", "r+")
                user_dict= f.read()
                user_dict=json.loads(user_dict)
                f.close()
                if user_dict['channel'] != "":
                    chnl=int(user_dict['channel'])
                    dis_channel = self.bot.get_channel(chnl)   
                    user_list=[]
                    embed=discord.Embed(title=title,description=description,colour=discord.Colour(0xF6B35F))
                    embed.add_field(name="Attendees",value="Naxxatra")
                    embed.set_footer(text="If you want to participate/attend this event then please react with ✅")
                    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/761896483838492682/756a7be666993d92c2421dd8af6d21ef.png?size=4096")
                    msg= await dis_channel.send(embed=embed)
                    embed.set_author( name=f"Event ID: {msg.id}",icon_url="https://cdn.discordapp.com/icons/761896483838492682/756a7be666993d92c2421dd8af6d21ef.png?size=4096")
                    await msg.edit(embed=embed)
                    react = await msg.add_reaction('✅')
                    f = open("./event.json", "r")
                    user_list= f.read()
                    user_list=json.loads(user_list)
                    f.close()
                    f=open("./event.json","w")
                    user_list[msg.id]=[]
                    f.write(json.dumps(user_list))
                    f.close()
                    await ctx.send("Event created successfully")
                else:
                    await ctx.send("Looks like the event channel is not set. Please set it using the command `n!set_channel [channel]` or using slash command.")
            else:
                await ctx.send("Sorry, you don't have permission to do that")

    @commands.command()
    async def dm_event(self,ctx,msg_id,*,message):
        if ctx.guild==None:
            await ctx.send("Sorry! This command can only run in server")
        else:
            if ctx.author.guild_permissions.manage_guild:
                f = open("./event.json", "r+")
                user_dict= f.read()
                user_dict=json.loads(user_dict)
                f.close()
                chnl=int(user_dict['channel'])
                dis_channel = self.bot.get_channel(chnl)
                msg = await dis_channel.fetch_message(msg_id)
                z=msg.embeds[0].to_dict()
                
                embed=discord.Embed(title=f"{z['title']}",description=message,colour=discord.Colour(0xff0000))
                embed.set_thumbnail(url="https://cdn.discordapp.com/icons/761896483838492682/756a7be666993d92c2421dd8af6d21ef.png?size=4096")
                not_sent_user=[]
                for i in user_dict[str(msg_id)]:
                    user = await self.bot.fetch_user(i)
                    channel= await user.create_dm()
                    try:
                        await channel.send(embed=embed)
                    except:
                        not_sent_user.append(user.name)
                if len(not_sent_user)==0:
                    await ctx.send("All DMs sent")
                else:
                    await ctx.send(f"Could send DM to the following users:\n```{not_sent_user}```\n They may have their DMs turned of.")            
            else:
                await ctx.send("Sorry, You don't have permission to do that.")

    @cog_ext.cog_slash(name="dm_event",description="DM all the users registered for a event",
    options=[
        create_option(
            name="event_id",
            description="The message ID of the event",
            option_type=3,
            required=True
        ),
        create_option(
            name="message",
            description="Enter the message that you want to send to all the users reegistered for the event",
            option_type=3,
            required=True
        )
    ])
    async def _dm(self,ctx,event_id,message):
        if ctx.guild==None:
            await ctx.send("Sorry! This command can only run in server")
        else:
            if ctx.author.guild_permissions.manage_guild:
                await ctx.send("Sending")
                f = open("./event.json", "r+")
                user_dict= f.read()
                user_dict=json.loads(user_dict)
                f.close()
                chnl=int(user_dict['channel'])
                dis_channel = self.bot.get_channel(chnl)
                msg = await dis_channel.fetch_message(event_id)
                z=msg.embeds[0].to_dict()
                
                embed=discord.Embed(title=f"{z['title']}",description=message,colour=discord.Colour(0xff0000))
                embed.set_thumbnail(url="https://cdn.discordapp.com/icons/761896483838492682/756a7be666993d92c2421dd8af6d21ef.png?size=4096")
                not_sent_user=[]
                for i in user_dict[str(event_id)]:
                    user = await self.bot.fetch_user(i)
                    channel= await user.create_dm()
                    try:
                        await channel.send(embed=embed)
                    except:
                        not_sent_user.append(user.name)
                if len(not_sent_user)==0:
                    await ctx.send("All DMs sent")
                else:
                    await ctx.send(f"Could send DM to the following users:\n```{not_sent_user}```\n They may have their DMs turned of.")            
                    #await ctx.send("Done")
            else:
                await ctx.send("Sorry, You don't have permission to do that.")


    @commands.Cog.listener()
    async def on_reaction_add(self,reaction,user):
        f = open("./event.json", "r+")
        user_dict= f.read()
        user_dict=json.loads(user_dict)
        f.close()
        #print(reaction.channel.id)
        if str(reaction.message.id) in user_dict:
            if reaction.emoji == "✅" and user != self.bot.user:
                f=open("./event.json","w")
                userlist=user_dict[f"{reaction.message.id}"]
                userlist.append(user.id)
                user_dict[f"{reaction.message.id}"]=userlist
                f.write(json.dumps(user_dict))
                f.close()
                chnl=int(user_dict['channel'])
                dis_channel = self.bot.get_channel(chnl)
                msg = await dis_channel.fetch_message(reaction.message.id)
                z=msg.embeds[0].to_dict()   
                z['fields'][0]['value']="Naxxatra"
                for i in user_dict[f"{reaction.message.id}"]:
                    user = await self.bot.fetch_user(i)
                    #output=output+","+user.mention
                    z['fields'][0]['value'] += f", {user.mention}"
                y = discord.Embed.from_dict(z)
                await msg.edit(embed=y)


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,reaction):
        f = open("./event.json", "r+")
        user_dict= f.read()
        user_dict=json.loads(user_dict)
        f.close()
        user_id=reaction.user_id
        user= await self.bot.fetch_user(user_id)
        if str(reaction.message_id) in user_dict and user_id != self.bot.user.id:
                f=open("./event.json","w")
                userlist=user_dict[f"{reaction.message_id}"]
                userlist.remove(user.id)
                user_dict[f"{reaction.message_id}"]=userlist
                f.write(json.dumps(user_dict))
                f.close()
                chnl=int(user_dict['channel'])
                dis_channel = self.bot.get_channel(chnl)
                msg = await dis_channel.fetch_message(reaction.message_id)
                z=msg.embeds[0].to_dict()
                #print(z)           
                #print(user.id)
                list_n_embed=z['fields'][0]['value']
                list_n_embed=list_n_embed.replace(f", {user.mention}","")
                #print(z['fields'][0]['value'].replace(user.mention,""))
                z['fields'][0]['value']=list_n_embed

                y = discord.Embed.from_dict(z)
                await msg.edit(embed=y)

    @commands.command()
    async def add_image(self,ctx,msg_id,*,url=None):
        if ctx.guild==None:
            await ctx.send("Sorry! This command can only run in server")
        else:
            if ctx.author.guild_permissions.manage_guild:
                f = open("./event.json", "r+")
                user_dict= f.read()
                user_dict=json.loads(user_dict)
                f.close()
                chnl=int(user_dict['channel'])
                dis_channel = self.bot.get_channel(chnl)        
                msg = await dis_channel.fetch_message(msg_id)
                z=msg.embeds[0]
                if url ==None:
                    z.set_image(url=ctx.message.attachments[0].url)
                    await msg.edit(embed=z)
                else:
                    z.set_image(url=url)
                    await msg.edit(embed=z)
                await ctx.send("Image added to the event message")
            else:
                await ctx.send("Sorry, You don't have permission to do that.")

    @commands.command()
    async def end_event(self,ctx,msg_id):
        if ctx.guild==None:
            await ctx.send("Sorry! This command can only run in server")
        else:
            if ctx.author.guild_permissions.manage_guild:
                f = open("./event.json", "r+")
                user_dict= f.read()
                user_dict=json.loads(user_dict)
                f.close()
                chnl=int(user_dict['channel'])
                dis_channel = self.bot.get_channel(chnl)        
                try:
                    msg = await dis_channel.fetch_message(msg_id)
                    z=msg.embeds[0]
                    z.add_field(name="ENDED",value="This event has ended.",inline=False)
                    await msg.edit(embed=z)
                    
                    f=open("./event.json","w")
                    del user_dict[f"{msg_id}"]
                    f.write(json.dumps(user_dict))
                    f.close()
                    await ctx.send("Event Ended")
                except:
                    await ctx.send("Either the message id is incorrect or the event has already ended")

            else:
                await ctx.send("Sorry, You don't have permission to do that.")

    @cog_ext.cog_slash(name="end_event",description="End a particular event",
    options=[
        create_option(name="event_id",
        description="Enter the Event id of the event",
        option_type=3,
        required=True
        )
    ])
    async def _end_event(self,ctx,event_id):
        if ctx.guild==None:
            await ctx.send("Sorry! This command can only run in server")
        else:
            await ctx.send("Ending event...")
            if ctx.author.guild_permissions.manage_guild:
                f = open("./event.json", "r+")
                user_dict= f.read()
                user_dict=json.loads(user_dict)
                f.close()
                chnl=int(user_dict['channel'])
                dis_channel = self.bot.get_channel(chnl)        
                try:
                    msg = await dis_channel.fetch_message(event_id)
                    z=msg.embeds[0]
                    z.add_field(name="ENDED",value="This event has ended.",inline=False)
                    await msg.edit(embed=z)
                    
                    f=open("./event.json","w")
                    del user_dict[f"{event_id}"]
                    f.write(json.dumps(user_dict))
                    f.close()
                    await ctx.send("Event Ended")
                except:
                    await ctx.send("Either the message id is incorrect or the event has already ended")

            else:
                await ctx.send("Sorry, You don't have permission to do that.")

    @commands.command()
    async def set_channel(self,ctx,channel: discord.TextChannel):
        if ctx.guild==None:
            await ctx.send("Sorry! This command can only run in servers")
        else:
            if ctx.author.guild_permissions.manage_guild:
                f = open("./event.json", "r+")
                user_dict= f.read()
                user_dict=json.loads(user_dict)
                f.close()
                f=open("./event.json","w+")
                user_dict["channel"]=str(channel.id)
                print(user_dict)
                f.write(json.dumps(user_dict))
                f.close()
            else:
                await ctx.send("Sorry, You don't have permission to do that.")


    @cog_ext.cog_slash(name="set_channel",description="Select the channel you wish to select for event creation",
    options=[
        create_option(name="channel",
        description="Select the channel you wish to select for event creation",
        option_type=7,
        required=True
        )
    ])
    async def _set_channel(self,ctx,channel):
        if ctx.guild==None:
            await ctx.send("Sorry! This command can only run in servers")
        else:
            if ctx.author.guild_permissions.manage_guild:
                f = open("./event.json", "r+")
                user_dict= f.read()
                user_dict=json.loads(user_dict)
                f.close()
                f=open("./event.json","w+")
                user_dict["channel"]=str(channel.id)
                print(user_dict)
                f.write(json.dumps(user_dict))
                f.close()
                await ctx.send("Channel Set for events")
            else:
                await ctx.send("Sorry, You don't have permission to do that.")


def setup(bot):
    bot.add_cog(events(bot))


