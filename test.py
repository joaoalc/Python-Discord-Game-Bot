# Work with Python 3.6
import discord
import numpy as np
from PIL import Image


def readTOKEN(path):
    file = open(path)
    f = file.readline()
    return f


TOKEN = readTOKEN("C://Users//joaoa//Documents//Python Discord Bot Project//my_bot//Token.txt")


def ScaleImage(filePath, nTimes):
    #Game start
    im = Image.open(filePath)
    img = np.array(im)
    width, height = im.size
    #im.show()
    img = np.repeat(np.repeat(img,nTimes, axis=0), nTimes, axis=1)

    #for i in range(1, width * n - 1, n):
    #    for e in range(0, height * n - 1, 12):
    #        img[i-1,e] = [196,196,196]
    #        img[i-1,e+1] = [196,196,196]
    #        img[i-1,e+2] = [196,196,196]
    #        img[i-1,e+3] = [196,196,196]
    #        img[i-2,e] = [196,196,196]
    #       img[i-2,e+1] = [196,196,196]
    #        img[i-2,e+2] = [196,196,196]
    #       img[i-2,e+3] = [196,196,196]

    mage = Image.fromarray(img, 'RGBA')
    mage.save('C://Users//joaoa//Documents//Python Discord Bot Project//my_bot//Current_Map//a.png')
    #mage.show()
    return




def FindPlayer(author, players):
    for i in range(0, len(players)):
        if author == players[i]:
            return i
    return -1


client = discord.Client()


playerlimit = 6
minplayers = 1
numPlayers = 0
players = []
repeatplayer = False
areyousure = False
numMaps = 3

Boss = "test" #It's going to be a player

phase = 0


@client.event
async def on_message(message):
    global playerlimit
    global numPlayers
    global players
    global repeatplayer
    global areyousure
    global phase
    global numMaps
    global Boss
     #we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if phase == 0:
        if message.content.startswith('<game start') and numPlayers == 0:
            msg = "{0.author.mention}".format(message) + " wants to start a game, but they need 2+ players. Say <game join to join the match."
            await message.channel.send(msg)
            numPlayers = 1
            players.append(message.author)
            phase += 1
            #msg = 'Hello {0.author.mention}'.format(message)
            #await message.channel.send(msg)
    if phase == 1:
        if message.content.startswith('<game join') and numPlayers < playerlimit:
            repeatplayer = False
            for i in range(0, numPlayers, 1):
                #print(players[0].name)
                if message.author == players[i]:
                    repeatplayer = True
            if not repeatplayer:
                numPlayers += 1
                players.append(message.author)
                await message.channel.send(message.author.name + " joined the queue")
            if repeatplayer:
                await message.channel.send(message.author.name + " is already on queue.")
                repeatplayer = False
        if message.content.startswith('<game leave'):
            repeatplayer = False
            for i in range(0, numPlayers, 1):
                if players[i] == message.author:
                    repeatplayer = True
                    del(players[i])
                    numPlayers -= 1
            if numPlayers == 0:
                phase = 0
                await message.channel.send("Nobody's left, so the game was closed")
            else:
                if repeatplayer:
                    await message.channel.send(message.author.name + " has left the queue.")
                if not repeatplayer:
                    await message.channel.send(message.author.name + ", you're not in the game so you can't leave it.")
        if message.content.startswith('<begin') and message.author == players[0]:
            if numPlayers >= minplayers:
                await message.channel.send("Are you sure you wanna start the game, " + message.author.name + "?")
                areyousure = True
        if message.content.startswith('<yes') and message.author == players[0] and areyousure == True:
            phase += 1
            await message.channel.send("Choose a map! (Type <1 to <" + str(numMaps) + ") (not implemented)")
        if message.content.startswith('<no') and message.author == players[0] and areyousure == True:
            areyousure = False
            await message.channel.send(">:[")
    if phase == 2:
        if message.content.startswith('<map list'):
            if message.author.dm_channel == None:
                await message.author.create_dm()
            for i in range(0, numMaps, 1):
                ScaleImage("C://Users//joaoa//Documents//Python Discord Bot Project//my_bot//Maps//Map" + str(i + 1) + ".png",6)
                await message.author.dm_channel.send("Map " + str(i + 1) + ":", file=discord.File('C://Users//joaoa//Documents//Python Discord Bot Project//my_bot//Current_Map//a.png'))
        for i in range(0, numMaps, 1):
            if message.content.startswith('<' + str(i)):
                phase += 1
                ScaleImage("C://Users//joaoa//Documents//Python Discord Bot Project//my_bot//Maps//Map" + str(i) + ".png", 12)
                await message.channel.send("The map chosen was Map" + str(i) + ":", file=discord.File("C://Users//joaoa//Documents//Python Discord Bot Project//my_bot//Current_Map//a.png"))
                await message.channel.send("Choose your classes. Most players can use \"<class list\" to get the list of classes \nIf you began the game, you are the boss. Use \"<boss list\" to get the list of bosses")
    if phase == 3:
        if FindPlayer(message.author, players) != -1 and FindPlayer(message.author, players) != 0:
            if message.content.startswith('<class list'):
                #IfDmChannel(message.author)
                if message.author.dm_channel == None:
                    await message.author.create_dm()
                await message.author.dm_channel.send("Type <(class name) (eg: <knight) to get a description of the class.\nType <pick class (eg: <pick knight) to select a class\nList of classes:\n")
                
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')




client.run(TOKEN)