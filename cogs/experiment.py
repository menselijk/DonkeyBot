import discord
from discord.ext import commands
from .Server import Server

from tinydb import TinyDB, where
from tinydb.operations import set

import re
import datetime

class ExperimentCog(commands.Cog, Server):
    def __init__(self, client):
        self.client = client
        self.events = TinyDB('database/events.json')
        self.users = TinyDB('database/users.json')

        Server.__init__(self)

        #Experiment channel combo
        self.combo = self.events.get(where('name') == 'experiment')['combo']

    def regex_count_search(self, text):
        # Credit: glaze#0563
        text = re.sub(
            #urls.
            r'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?' r'|'
            #emoji
            r'<:.+?:\d+>' r'|'
            #animated emoji
            r'<a:.+?:\d+>' r'|'
            #mentions
            r'<@.+?\d+>' r'|'
            r'<@!.+?\d+>' r'|'
            #role mentions
            r'<@&.+?\d+>' r'|'
            #channel mentions.
            r'<#.+?\d+>' r'|'
            ,
            #empty string.
            ' ', text)
        
        return re.search(r'\d+', text)
    
    def regex_count(self, value):
        return 0 if value is None else self.regex_count_search(value).group()

    @commands.Cog.listener()
    async def on_member_join(self, member):

        #Give saved roles
        server = self.client.get_guild(self.server)

        roles = [] if self.users.get(where('id') == member.id) is None else self.users.get(where('id') == member.id)['roles']

        for role in roles:
            await member.add_roles(server.get_role(role))

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):

        if (before.channel.id == self.experimentChannel):

            #Change nickname if someone removes their combo in an edit
            beforeCount = self.regex_count(before.content)
            if (beforeCount not in after.content):
                await after.channel.send(after.author.mention + " edited their message\n> " + before.content)
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        
        member = message.author

        #Punish griefers
        if ((message.channel.id == self.experimentChannel) and (not member.bot and not member.guild_permissions.manage_messages)): #User was not staff or bot
            try:
                regEx = self.regex_count(message.content)
                firstInt = 0 if regEx is None else regEx
                
                await message.channel.send("> " + firstInt + "\n<@" + str(member.id) + ">")
                
                #Remove good role, add bad role
                if (message.guild.get_role(self.goodRole) in member.roles):
                    await member.remove_roles(message.guild.get_role(self.goodRole))
                await member.add_roles(message.guild.get_role(self.badRole))
                self.users.upsert({ 'id': member.id, 'roles': [ self.badRole ] }, where('id') == member.id)
            except:
                pass
    
    @commands.Cog.listener()
    async def on_message(self, message):

        member = message.author

        if (message.channel.id == self.experimentChannel):

            canPost = True
    
            #Check for staff members and enforce slowmode
            if (member.guild_permissions.manage_messages and not member.bot):
                
                if (message.guild.get_role(self.badRole) in member.roles):
                    canPost = False
                else:
                    now = datetime.datetime.now()

                    if ('experimentTS' in self.users.get(where('id') == member.id)):

                        last = datetime.datetime.strptime(self.users.get(where('id') == member.id)['experimentTS'], "%Y-%m-%d %H:%M:%S")

                        if ((now - last).total_seconds() >= message.channel.slowmode_delay):
                            self.users.upsert({ 'experimentTS': str(datetime.datetime.strftime(now, "%Y-%m-%d %H:%M:%S")) }, where('id') == member.id)
                        else:
                            canPost = False
                            try:
                                await member.send("That channel has slowmode and you can't bypass it! haha!")
                            except:
                                pass #Cannot send message to this user
                    else:
                        self.users.upsert({ 'experimentTS': str(datetime.datetime.strftime(now, "%Y-%m-%d %H:%M:%S")) }, where('id') == member.id)

            if canPost:
                count = int(self.combo)
                nextCountStr = str(count+1) #Expected next combo

                #Successful combo
                regEx = self.regex_count(message.content)
                firstInt = 0 if regEx is None else regEx
                if (firstInt == nextCountStr):

                    self.combo = count + 1
                    self.events.update(set('combo', str(self.combo)), where('name') == 'experiment')
                    
                    #Give good role to first time participants
                    if (message.guild.get_role(self.goodRole) not in member.roles):
                        await member.add_roles(message.guild.get_role(self.goodRole))
                        self.users.upsert({ 'id': member.id, 'roles': [ self.goodRole ] }, where('id') == member.id)
                
                #Unsuccessful combo
                elif (not member.bot):

                    best = message.channel.topic.split("Best: ", 1)[1] #Get record from topic

                    countdownMessage = "<@" + str(member.id) + "> broke <#718251019661869156> <:luigisad:406759665058185226>"
                    if (count > int(best)): #If new record, append to message
                        countdownMessage += " **(NEW BEST: " + str(count) + ")**"
                        await message.channel.edit(topic="Best: " + str(count))

                    countdownMessage += "\n> " + message.content

                    #Send previous message
                    lastmsg = await message.channel.history(limit=2).flatten()
                    try:
                        countdownMessage += "\nPrevious message:\n> " + lastmsg[1].content
                    except:
                        pass

                    notifChannel = message.guild.get_channel(self.labChannel)
                    await notifChannel.send(countdownMessage)

                    #Remove good role, add bad role
                    if (message.guild.get_role(self.goodRole) in member.roles):
                        await member.remove_roles(message.guild.get_role(self.goodRole))
                    await member.add_roles(message.guild.get_role(self.badRole))
                    self.users.upsert({ 'id': member.id, 'roles': [ self.badRole ] }, where('id') == member.id)

                    #Delete all messages in the channel
                    messagesDeleted = await message.channel.purge(limit=100)
                    while (len(messagesDeleted) != 0):
                        messagesDeleted = await message.channel.purge(limit=100)

                    #Reset combo
                    self.combo = 0
                    self.events.update(set('combo', str(self.combo)), where('name') == 'experiment')
            else:
                await message.delete()
            
def setup(client):
    client.add_cog(ExperimentCog(client))
