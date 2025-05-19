import discord
from discord.ext import commands
from Bot.utils import token, addAllCogs
import asyncio
from tac import HardCheck

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)
running = True
waitTime = 10 # seconds
channel = 1372412397985333361
iterations = 0

async def main():
    while running:
        global iterations
        iterations += 1
        print(f"Iteration {iterations}")
        await HardCheck(client)
        await asyncio.sleep(waitTime)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await addAllCogs(client)  
    await client.tree.sync()                               # Remove this when production
    await main()  # Start the main loop in the background


client.run(token=token)