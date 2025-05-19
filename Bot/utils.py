import os
import discord
token = open('Bot/token.txt').readline().strip()

async def addAllCogs(client):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'Cogs.{filename[:-3]}')
            print(f'Loaded {filename[:-3].upper()} Cog')

async def addStreamer(ctx, serverId, name):
    serverId = ctx.guild.id
    path = f'Servers/{serverId}'
    if not os.path.exists(path):
        os.makedirs(path)
    file = open(f'Servers/{serverId}/streamers.txt', 'a')
    file.write(name + '\n')
    file.close()

async def resetStreamers(ctx, serverId):
    path = f'Servers/{serverId}'
    if not os.path.exists(path):
        os.makedirs(path)
        await ctx.send('No directory, Making one\nplease add streamers to the file.', ephemeral=True)
    file = open(f'Servers/{serverId}/streamers.txt', 'w')
    file.close()


embed= discord.Embed(title="title", description="description", color=0xff0000)
embed.add_field(name="field", value="value", inline=False)

def findWordInFile(word, file):
    with open(file) as f:
        for line in f:
            if word in line:
                return True
            