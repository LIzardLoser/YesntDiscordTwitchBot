import os
import discord
token = open('Bot/token.txt').readline().strip()

async def addAllCogs(client):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'Cogs.{filename[:-3]}')
            print(f'Loaded {filename[:-3].upper()} Cog')

async def addStreamer(serverId, name):
    try:
        path = f'Servers/{serverId}'
        if not os.path.exists(path):
            os.makedirs(path)
        file = open(f'Servers/{serverId}/streamers.txt')
        for line in file:
            if name in line:
                return 'Streamer already in file.'
        file = open(f'Servers/{serverId}/streamers.txt', 'a')
        file.write(name + '\n')
        file.close()
        return f"Adding **{name}** to file"
    except Exception as e:
        if ('Errno 2' in str(e)):
            file = open(f'Servers/{serverId}/streamers.txt', 'w')
            file.write(name + '\n')
            file.close()
            return f"Adding **{name}** to file"
        print(e)
        return f"Error: {e}"

async def resetStreamers(serverId):
    try:
        path = f'Servers/{serverId}'
        if not os.path.exists(path):
            os.makedirs(path)
            file = open(f'Servers/{serverId}/streamers.txt', 'w')
            file.close()
            return 'No directory, Making one\nplease add streamers to the file.'
        file = open(f'Servers/{serverId}/streamers.txt', 'w')
        file.close()
        return 'Streamers reset!'
    except Exception as e:
        print(e)
        return f"Error: {e}"

async def setChannel(serverId, channel):
    try:
        path = f'Servers/{serverId}'
        if not os.path.exists(path):
            os.makedirs(path)
        file = open(f'Servers/{serverId}/list.txt', 'w')
        file.write("{}\n")
        file.write(str(channel.id) + '\n')
        file.close()
        return f'Channel set to {channel.mention}!'
    except Exception as e:
        print(e)
        return f"Error: {e}"


embed= discord.Embed(title="title", description="description", color=0x0000FF)
embed.add_field(name="field", value="value", inline=False)

HelpEmbed = discord.Embed(title="Basic Help", color=0xff0000)
HelpEmbed.description = "First use **/setchannel** to set the channel that the bot will send the Ping to\n" \
"Then use **/streamers add** to add streamers to the file"
HelpEmbed.add_field(name="Commands", value="**/ping** **/streamers add** **/streamers remove** **/streamers reset** **/setchannel** **/helpstream**", inline=False)
HelpEmbed.add_field(name="/ping", value="Displays Test Embed", inline=False)
HelpEmbed.add_field(name="/streamers add", value="Adds a streamer to the file", inline=False)
HelpEmbed.add_field(name="/streamers remove", value="Removes a streamer from the file", inline=False)
HelpEmbed.add_field(name="/streamers reset", value="Resets the streamers file", inline=False)
HelpEmbed.add_field(name="/setchannel", value="Sets the channel that the bot will send the Ping to", inline=False)
HelpEmbed.add_field(name="/helpstream", value="Displays this message", inline=False)



def findWordInFile(word, file):
    with open(file) as f:
        for line in f:
            if word in line:
                return True
            
    return False
