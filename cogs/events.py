from discord.ext import commands
import discord
import time
import json

from discord.ext.commands.core import Command, command
def lst_vert(list):
    out=""
    for i in list:
        out=out+i+'\n'
    return out


class events(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def add_event(self,ctx,title,*,description):
        user_list=[]
        embed=discord.Embed(title=title,description=description,colour=discord.Colour(0xF6B35F))
        embed.add_field(name="Attendees",value="Naxxatra")
        embed.set_thumbnail(url="https://cdn.discordapp.com/icons/761896483838492682/756a7be666993d92c2421dd8af6d21ef.png?size=4096")
        msg=await ctx.send(embed=embed)
        react = await msg.add_reaction('✅')
        f = open("./event.json", "r")
        user_list= f.read()
        user_list=json.loads(user_list)
        f.close()
        f=open("./event.json","w")
        user_list[msg.id]=[]
        f.write(json.dumps(user_list))
        f.close()

    @commands.command()
    async def dm_event(self,ctx,msg_id,*,message):
        f = open("./event.json", "r+")
        user_dict= f.read()
        user_dict=json.loads(user_dict)
        f.close()
        chnl=int(user_dict['channel'])
        dis_channel = self.bot.get_channel(chnl)
        msg = await dis_channel.fetch_message(msg_id)
        z=msg.embeds[0].to_dict()
        
        embed=discord.Embed(title=f"{z['title']}",description=message)
        embed.set_thumbnail(url="https://cdn.discordapp.com/icons/761896483838492682/756a7be666993d92c2421dd8af6d21ef.png?size=4096")
        for i in user_dict[str(msg_id)]:
            user = await self.bot.fetch_user(i)
            channel= await user.create_dm()
            await channel.send(embed=embed)

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
        if str(reaction.message_id) in user_dict:
                print("here")
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


def setup(bot):
    bot.add_cog(events(bot))


