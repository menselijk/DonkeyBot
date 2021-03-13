import discord
from discord.ext import commands

""" 
    Server.py
    - Contains various specific guild related IDs
    - Naming scheme must specify the type for setup command (Channel/Role) 
"""

class Server():
    def __init__(self):

        #Server
        self.server = 817450914444869682

        #Channels
        self.generalChannel = 817450914604253206
        self.experimentChannel = 817450914918432830
        self.labChannel = 817450914918432831
        self.spamChannel = 817450914604253214
        self.minecraftChannel = 817450914604253214
        self.logChannel = 817450914604253214
        self.drawingArenaChannel = 750753280694550539

        #Roles
        self.goodRole = 817450914452602927
        self.badRole = 817450914452602926
        self.coolGuyRole = 817450914481832029
        self.regularRole = 817450914473705534
        self.notseriousRole = 817450914473705536

        #Important People
        self.robID = 534122161972183050

