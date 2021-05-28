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



    @commands.Cog.listener()
    async def on_reaction_add(self,reaction,user):
        #print(reaction.channel.id)
        if reaction.emoji == "✅" and user != self.bot.user:
            f = open("./event.json", "r+")
            user_dict= f.read()
            user_dict=json.loads(user_dict)
            f.close()
            f=open("./event.json","w")
            userlist=user_dict[f"{reaction.message.id}"]
            userlist.append(user.id)
            user_dict[f"{reaction.message.id}"]=userlist
            f.write(json.dumps(user_dict))
            f.close()
            chnl=int(user_dict['channel'])
            dis_channel = self.bot.get_channel(chnl)
            msg = await dis_channel.fetch_message(reaction.message.id)
            #embed=discord.Embed(title="title",description="description",colour=discord.Colour(0xF6B35F))
            #output="Naxxatra"
            #for i in user_dict[f"{reaction.message.id}"]:
                #user = await self.bot.fetch_user(i)
                #output=output+","+user.name

            #embed.add_field(name="Attendees",value=output) 
            z=msg.embeds[0].to_dict()           
            z['fields'][0]['value'] += f", {user.name}"
            y = discord.Embed.from_dict(z)
            await msg.edit(embed=y)

    @commands.command()
    async def get_msg(self,ctx,msg_id):
        f = open("./event.json", "r+")
        user_dict= f.read()
        user_dict=json.loads(user_dict)
        f.close()
        chnl=int(user_dict['channel'])
        dis_channel = self.bot.get_channel(chnl)        
        msg = await dis_channel.fetch_message(msg_id)
        embeds = msg.embeds
        for embed in embeds:
            await ctx.send(str(embed.to_dict()))

    @commands.command()
    async def test(self,ctx):
        z={'fields': [{'name': 'Attendees', 'value': 'Naxxatra,DiluteWater', 'inline': True}], 'color': 16167775, 'type': 'rich', 'description': 'description', 'title': 'title'}
        y = discord.Embed.from_dict(z)
        await ctx.send(embed=y)

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


