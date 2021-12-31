import os
import time
import sched
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print([f'{guild.name}' for guild in client.guilds])

client.run(TOKEN)