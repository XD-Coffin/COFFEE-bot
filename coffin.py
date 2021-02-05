import wikipedia
import datetime
import youtube_dl
import random
from random import choice
import discord 
import asyncio
from discord.ext import commands, tasks
from lyrics_extractor import SongLyrics
import time
import requests
# import horoscope


# Settings
TOKEN = ''
client = commands.Bot(command_prefix = '#')
queue = []
status = ['Pic Credit: @The Nun','Pic Credit: @The Nun']
Client = discord.Client()

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

# ###### END OF SETTINGS.

# CHECKING ONLINE/OFFLINE STATUS. 
@client.event
async def on_ready():
    change_status.start()
    print("Bot is ready.")

# STATUS UPDATES:
@tasks.loop(seconds=20)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))

# Checking Ping
@client.command(aliases=['ping','ping_kati_xa'],help="Check Ping..")
async def _ping(ctx):
    await ctx.send(f'ping {round(client.latency * 1000)}ms xa.')



# Truth and Dare....
 
@client.command(aliases=['truth','t'],help="Truth questions..")
async def _truth(ctx): 
    questions=[" How old were you when you had sex for the first time?", " How many sexual partners did you have", "Tell me about your first kiss" , "How was your first sex experience?",  "Who do you want to makeout from here?", "Who do you think is the biggest pervert in here", "When was the last time you checked your ex profile?", "Have  you taken your naked picture", "With how many people you have sexted?", "What is your wildest fantasy?", "Have you ever wanted to cheat in a relationship?", "Who are u jealous of from this server", "How often do you watch porn?", "When was the last time you masturbated?", "Choose two of your fav celebs for a threesome", "What will you choose, one night stand or date with someone random", "When was the last time u cried for someone", "Your fav curse word" , "What turns you on?", "What’s the most embarrassing thing you’ve ever done?", "What is your dirtiest secret?" , "Have you ever lied to get out of a bad date?",  "Have you ever lied to get out of a bad date?","Have you ever watched another couple have sex?", "whats your deepest darkest secret", "Have you ever been friend-zoned?", "If so, by whom?", "Who is the person you most regret kissing?", "Why did you break up with your last boyfriend or girlfriend?", "What is your favorite type of porn?", "Have you ever fantasized about a teacher?", "Who is the sexiest person here?", "What would you do if you were the opposite sex for a week?", "What do you think the sexiest part of your body is?",  "What is the first dirty thing you would do if you woke up as the opposite sex?", "What is the most expensive thing you have stolen?", "Where’s the weirdest place you’ve had sex?", "If You Could Change One Thing On Your Body, What Would It Be?", "Have you ever cheated or been cheated on?",  "What Are The two Things You Notice In A Person At First Glance?"]
    alreadyasked=[]

    a = random.choice(questions)
    await ctx.send(f'question: {ctx.author.mention} {a}')
    
# JOINING VOICE CHANNEL 
@client.command(name='join',help="Join voice channel..")
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("Get connected to the voice channel.")
        return 
    else:
        channel= ctx.message.author.voice.channel
    await channel.connect()


# LEAVING VOICE CHANNEL
@client.command(name='dc',help="Disconnect from voice channel..")
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    await ctx.send("## Disconnecting Now ##....See you soon....")
    await voice_client.disconnect()

# PLAYING MUSIC IN VOICE CHANNEL
@client.command(name='play',help="Play songs in queue..")
async def play(ctx):
    while True:
        global queue
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            player = await YTDLSource.from_url(queue[0],loop=client.loop)
            voice_channel.play(player, after=lambda e: print('Player error: %s' %e)if e else None)
        
        await ctx.send('## Now Playing ## {}'.format(player.title))
        del(queue[0])


# PAUSING VOICE CHANNEL
@client.command(name='pause',help="Pause playing music..")
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.pause()

# RESUMING VOICE CHANNEL
@client.command(name='resume',help="Resume paused music..")
async def resume(ctx):
    server = ctx.message.guild
    voice_channel= server.voice_client

    voice_channel.resume()


# QUEUING VOICE CHANNEL
@client.command(name='q',help="Put songs in queue..")
async def queue_(ctx, url):
    global queue
    queue.append(url)
    await ctx.send(f"{url} added to queue !!")

# PAYING RESPECTS.
@client.command(aliases=['bug','gn','rev','k','op'],help="Pay respect to artists..")
async def _bug(ctx):
    await ctx.send(f"{ctx.author.mention} has paid their respect.")

@client.command(aliases=['donate'],help="Pay respect to artists..")
async def _donate(ctx):
    a = random.randrange(50)
    await ctx.send(f"{ctx.author.mention} has donated {a+1}$ to Ray.")


# SECRET COMMAND.
# @client.command(name='love',help="Secret command..")
# async def love(ctx):
#     while True:
#         await ctx.send("Timi mero ho.")

# CHECK QUEUE LIST.
@client.command(name='ql',help="Check queue list..")
async def ql(ctx):
    for i in range(len(queue)):
        await ctx.send(f"{i} - {queue[i]}")

# Check Wikipedia.
@client.command(name='wiki',help="Helps with you homework..")
async def wiki(ctx,word):
    result = wikipedia.summary(word,sentences=2) 
    await ctx.send(f"According to wikipedia {result}")

# Lyrics Finder.
@client.command(name='lyrics',help="Finds lyrics of the songs")
async def lyrics(ctx,lyr):
    extract_lyrics = SongLyrics("AIzaSyCsCDLwP1nuvU_jUGXNoSLP-UZgkIjqeaQ","db8bfd43f907ee403")
    temp=extract_lyrics.get_lyrics(str(lyr))
    res = temp['lyrics']
    await ctx.send(f"COFFEE TIME:  {res}")
    # a = extract_lyrics.get_lyrics(lyr)
    # await ctx.send(f"COFFEE TIME:  {temp(a)}")
    # print(extract_lyrics.get_lyrics(lyr))


# Love calculator:
@client.command(name='lovecalc',help="Love calculator write partner1 partner2")
async def lovecalc(ctx,p1,p2):
    try:
        array=[40, 75, 80, 90, 95]
        if p1 == "Coffin" and p2 == "Lilo":
            await ctx.send(f"Love percentage = 101%")
        elif p1 == "Coffin" and p2 == "Abu":
            await ctx.send(f"Love percentage = 101%")
        elif p1 == "sugoisenpai" and p2 == "chipuri":
            await ctx.send(f"Love percentage = 101%")
        elif p1 == "aalu" and p2 == "pidalu":
            await ctx.send(f"Love percentage = 95%")
        elif p1 == "Atom" and p2 == "Abu":
            await ctx.send(f"Love percentage = 101%")
        else:
            await ctx.send(f"Love percentage ={array[random.randrange(4)]}")
        
    except:
        await ctx.send(f"Read the help of this ")


@client.command(name='Confess', help='Type Confessions.')
async def Confess(ctx, a):
    # await ctx.send("!!clear 1")
    # time.sleep(5)
    await ctx.send(f"Confession aayo hai : {a}")

# HORESCOPE
# @client.command(name='horescope', help="Horescope tha paunuhos.")
# async def Horescope(ctx,a):
#     b = Horoscope.get_todays_horoscope(a)
#     await ctx.send(f"VAWISA ANDHAKAR XA: {b}")


client.run(TOKEN)



# @client.command(aliases=['join'])
# async def _join(ctx):
#     channel = ctx.message.author.voice.channel
#     if not channel:
#         await ctx.send("Get connected to a channel before calling me.")
#         return
#     voice = get(client.voice_clients,guild=ctx.guild)
#     if voice and voice.is_connected():
#         await voice.move_to(channel)
#     else:
#         voice = await channel.connect()
#         audioSource = discord.FFmpegPCMAudio('file.mp3')
#         voice.play(audioSource,after=None)

# @client.command(aliases=['dc','leave'])
# async def _leave(ctx):
#     await ctx.voice_client.disconnect()

# @client.command(aliases=['play','p'])
# async def _play(ctx, url):
#     channel = ctx.message.author.voice.channel
#     if not channel:
#         await ctx.send("Let me join at 1'st")
#     voice = get(client.voice_clients, guild=ctx.guild)
#     if voice and voice.is_connected():
#         await voice.move_to(channel)
#     else:
#         voice = await channel.connect()
#         player = await voice.create_ytdl_player(url)
#         player.start()


        



# Voice SIRI


###################Music bot##################
# @client.command(aliases=["join"],pass_context=True)
# async def _join(ctx):
#     channel = ctx.author.voice.channel
#     await channel.connect()

# @client.command(aliases=['dc'],pass_context=True)
# async def _leave(ctx):
#     await ctx.voice_client.disconnect()

# @client.command(pass_context=True)
# async def leave(ctx):
#     server = ctx.message.server
#     voice_client = client.voice_client_in(server)
#     await voice_client.disconnect()

# @client.command(pass_context=True)
# async def play(ctx, url):
#     server=ctx.message.server
#     voice_client = client.voice_client_in(server)
#     player = await voice_client.create_ytdl_player(url)
#     players[server.id] = player
#     player.start()



#########Voice Assistant##############



# @client.event
# async def on_number_join(member):
#     print(f'{member} has joined a server.')

# @client.event
# async def on_number_remove(member):
#     print(f'{member} has left the server.')
