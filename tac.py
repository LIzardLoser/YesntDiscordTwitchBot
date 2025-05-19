import requests
import os
import random as rand
from Bot.utils import findWordInFile

running = True
# This is a simple script to check the uptime of Twitch streamers using the DecAPI service. -- tac : Twitch Api Checker

def randString(streamer, serverId):
    choices = []
    for line in open(f'Servers/{serverId}/LiveChoices.txt', 'r'):
        choices.append(line.replace('{streamer}', streamer).strip('\n'))
    return rand.choice(choices)


async def SoftCheck(ctx, serverId):
    try:
        path = f'Servers/{serverId}'
        string = ''  
        if not os.path.exists(path):
            os.makedirs(path)
            await ctx.send('Directory created, please add streamers to the file.', ephemeral=True)
            return
        file = open(f'Servers/{serverId}/streamers.txt', 'r') 
        for line in file:
            line = line.strip('\n')
            req = requests.get('https://decapi.me/twitch/uptime/' + line)
            if req.text == f'{line} is offline':
                #await ctx.send(f'{line} is offline')
                string += f"\n{line.replace('_','\_')} is offline"
            else:
                #await ctx.send(f'{line}: {req.text}')
                string += f"\n{line.replace('_','\_')}: {req.text}"
        await ctx.send(string + '\nCheck complete!', ephemeral=True)
    except Exception as e:
        await ctx.send('Please add streamers to the file.', ephemeral=True)
        print(e)
        


async def HardCheck(bot):
    serverId = 1372412397528158288 #will be filled when loopibng through servers
    file = open(f'Servers/{serverId}/streamers.txt', 'r')
    listtxt = open(f'Servers/{serverId}/list.txt', 'r')
    thing = {}
    ctx = bot.get_channel(listtxt.readline(1))
    #print(ctx.id)
    try:
        thing = eval(listtxt.readline(0))
        for name in thing:
            if not findWordInFile(name, f'Servers/{serverId}/streamers.txt'):
                thing.remove(name)
                print(f'{name} removed from list')
    except:
        thing = {}
    for line in file:
        line = line.strip('\n')
        req = requests.get('https://decapi.me/twitch/uptime/' + line)
        if req.text == f'{line} is offline':
            thing.update({line: False})
        else:
            if not thing.get(line) or thing.get(line) == False:
                print(f'{line} is online')
                thing.update({line: True})
                await ctx.send(f'Join {line}\'s stream: https://www.twitch.tv/{line}')
                #await ctx.send(f"{randString(line)} \n https://www.twitch.tv/{line}")

    listtxt = open(f'Servers/{serverId}/list.txt', 'w')
    listtxt.write(f"{str(thing)}\n{str(ctx.id)}\n")
    listtxt.close()

async def rewrite():
    '''
    this will be a rewrite of hardcheck
    loop through each folder
    and then check each channelid file in each folder
    '''

