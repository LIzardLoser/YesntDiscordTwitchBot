import requests
import os
import random as rand
from Bot.utils import findWordInFile, PathChecks

running = True
# This is a simple script to check the uptime of Twitch streamers using the DecAPI service. -- tac : Twitch Api Checker

def randString(streamer, serverId):
    choices = []
    for line in open(f'Servers/{serverId}/LiveChoices.txt', 'r'):
        choices.append(line.replace('{streamer}', streamer).strip('\n'))
    return rand.choice(choices)

async def SoftCheck(ctx, serverId, ping):
    '''Checks the api, if ping then it sends the stream link and not the uptimes.'''
    try:
        paths = await PathChecks(serverId, ctx)
        streamers = paths[2]
        string = ''  
        file = open(streamers, 'r') 
        for line in file:
            line = line.strip('\n')
            req = requests.get('https://decapi.me/twitch/uptime/' + line)
            if req.text == f'{line} is offline':
                #await ctx.send(f'{line} is offline')
                string += f"\n{line.replace('_','\_')} is offline"
            else:
                #await ctx.send(f'{line}: {req.text}')
                string += f"\n{line.replace('_','\_')}: {req.text}"
                if ping == True:
                    await ctx.send(f'Join {line}\'s stream: https://www.twitch.tv/{line}')
        if ping == False:
            await ctx.send(string + '\nCheck complete!', ephemeral=True)
    except Exception as e:
        await ctx.send('Please add streamers to the file.', ephemeral=True)
        print(e)
        
####These check and return needed variables#######
def serverIdChecker():
    serverIds = []
    for folder in os.listdir('Servers'):
        serverIds.append(folder)
    return serverIds

def channelIdChecker(id):
    file = open(f'Servers/{id}/list.txt', 'r')
    return int(file.readlines()[1].strip('\n'))

def ListChecker(id):
    file = open(f'Servers/{id}/list.txt', 'r')
    return file.readlines()[0].strip()
##################################################

async def HardCheck(bot, id, channelId, streamerList):
    '''The Main function that checks the streamers and sends messages to the channel.'''
    paths = await PathChecks(id)
    file = open(paths[2], 'r')
    thing = {}
    channel = bot.get_channel(channelId)
    try:
        thing = streamerList
        for name in list(thing):
            if findWordInFile(name, f'Servers/{id}/streamers.txt') == False:
                thing.pop(name)
                print(f'{name} removed')
    except Exception as e:
        print(e)
    
    for line in file:
        line = line.strip('\n')
        req = requests.get('https://decapi.me/twitch/uptime/' + line)
        if req.text == f'{line} is offline':
            thing.update({line: False})
        else:
            if not thing.get(line) or thing.get(line) == False:
                print(f'{line} is online')
                thing.update({line: True})
                await channel.send(f'Join {line}\'s stream: https://www.twitch.tv/{line}')
                #await ctx.send(f"{randString(line)} \n https://www.twitch.tv/{line}")

    listtxtt = open(f'Servers/{id}/list.txt', 'w')
    listtxtt.write(f"{str(thing)}\n{str(channel.id)}\n")
    listtxtt.close()
    file.close()



async def MainLoop(bot):
    '''Main loop that checks all servers and channels'''
    for serverid in serverIdChecker():
        try:
            channelId = channelIdChecker(serverid)
            strList = eval(ListChecker(serverid))
            if (strList == None) or (channelId == None) or (channelId == 0):
                return
            await HardCheck(bot, serverid, channelId, strList)
        except Exception as e:
            print(e)
            if('list.txt' in str(e)):
                file = open(f'Servers/{serverid}/list.txt', 'w')
                file.write("{}\n")
                file.write("0\n")
                file.close()
                print('List File created')
            elif ('streamers.txt' in str(e)):
                file = open(f'Servers/{serverid}/streamers.txt', 'w')
                file.close()
                print('Streamers File created')

            try:
                os.makedirs(f'Servers/{serverid}')
            except Exception as e:
                print(e)

