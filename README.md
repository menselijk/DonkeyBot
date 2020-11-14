# Donkey Bot

[![Discord](https://img.shields.io/discord/284028259027648513?color=7289DA&label=discord)](https://discord.gg/videogamedunkey)
[![Python](https://img.shields.io/pypi/pyversions/discord.py.svg)](https://pypi.org/project/discord.py/)

The source code for **Donkey** used on the videogamedunkey Discord server.

- Using the **discord.py** API wrapper: https://github.com/Rapptz/discord.py
- pipenv *(Optional)*: https://pypi.org/project/pipenv/

#### Contributing to Donkey

1. Fork the project (Creates a copy of the code that you can edit on github)

2. Follow **Setup Instructions** and make changes to your bot

3. Create a pull request and wait for someone to merge your code

### Setup Instructions

1. Create a test server using our [Discord Template](https://discord.new/hutdnmXDNQrU)

2. [Create a Discord developer application](https://discord.com/developers/applications)
    - Bot **>** Add Bot
    - Invite your bot to your test server: 
    
    `https://discordapp.com/oauth2/authorize?client_id=CLIENT_ID&scope=bot&permissions=8` where `CLIENT_ID` is copied from "General Information"
 
3. Create **.env** file in the main directory containing `BOT_TOKEN=token` where token is copied from the "Bot" page

4. Create virtual environment by running `pipenv install` or `pip install -U -r requirements.txt`

5. Run your bot and issue the setup command in your test server