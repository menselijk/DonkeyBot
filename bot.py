import os
import sys, traceback
from cogs.Server import Server
from dotenv import load_dotenv
load_dotenv() #Load .env file, contains bot secret

import discord
from discord.ext import commands

client = commands.Bot(command_prefix=commands.when_mentioned_or('>'), help_command=None)

initial_extensions = ['cogs.mod', 'cogs.basic','cogs.fun','cogs.experiment','cogs.rob','cogs.lab', 'cogs.minecraft'] #Add cog filenames here

@client.event
async def on_ready():
    print("Logged in")

    presence = discord.Activity(type=discord.ActivityType.watching, name="ASTRO alts")
    await client.change_presence(activity=presence)

    if __name__ == '__main__':
        for extension in initial_extensions:
            client.load_extension(extension)
    
    if ("restart" in sys.argv):
        respChanel = client.get_channel(int(sys.argv[2]))
        await respChanel.send("Restarted :white_check_mark:")

client.run(os.getenv("BOT_TOKEN"), reconnect=True)