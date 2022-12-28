#modules
import discord

from discord.ext import commands
from Cogs.q import Queue
from Cogs.audio import Audio

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice = None
        self.q = Queue()

    @commands.command(name="play", description="Plays a song from Youtube")
    async def play(self, ctx, *, query):
        """
        Plays a song from Youtube
        """
        if ctx.channel.name == 'music':
            if not self.voice:
                await self.join(ctx)
            song = Audio(query)
            self.q.add(song)
            if self.voice.is_playing():
                title = "Added to the queue"
            else:
                title = "Playing now"
                self.play_next()
            # get id
            videoID = song.url.split("watch?v=")[1].split("&")[0]
            thumbnail_url = f"https://img.youtube.com/vi/{videoID}/0.jpg"
            embed = discord.Embed(title=title, 
                              description=f"[{song.title}]({song.url})",  
                              color=0x0000ff)
            embed.set_image(url=thumbnail_url)
            await ctx.send(embed=embed)  
        else: 
            await ctx.send("You can only use this in ``Music`` channel")

    @commands.command(name="resume", description="Resumes the paused song")
    async def resume(self, ctx):
        """Resumes the paused song"""
        if ctx.channel.name == 'music':
            self.voice.resume()
        else:
            await ctx.send("You can only use this in ``Music`` channel")
        

    @commands.command(name="stop", description="Stops playing the song")
    async def stop(self, ctx):
        """Stops playing the song"""
        if ctx.channel.name == 'music':
            self.voice.stop()
        else:
            await ctx.send("You can only use this in ``Music`` channel")
        
    @commands.command(name="skip", description="Skips to the next song in the queue")
    async def skip(self, ctx):
        """Skips to the next song in the queue"""
        if ctx.channel.name == 'music':
            self.voice.stop()
            self.play_next()
        else:
            await ctx.send("You can only use this in ``Music`` channel")
    

    @commands.command(name="join", description="Joins your voice channel")
    async def join(self, ctx):
        """
        Joins your voice channel
        """
        if ctx.channel.name == 'music':
            self.voice = await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You can only use this in ``Music`` channel")
        

    @commands.command(name="leave", description="Leaves the voice channel")
    async def leave(self, ctx):
        """Leaves the voice channel"""
        if ctx.channel.name == 'music':
            await self.voice.disconnect()
            self.voice = None
        else:
            await ctx.send("You can only use this in ``Music`` channel")
        
       
    @commands.command(name="queue", description="View the queue", aliases=["q"])
    async def queue(self, ctx):
        """View the queue"""
        if ctx.channel.name == 'music':
            a = self.q.peek()
            await ctx.send(f"Next: {a.title}" if a else "Nothing in the queue")
        else:
            await ctx.send("You can only use this in ``Music`` channel")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Missing Argument")
        elif isinstance(error, commands.errors.CommandInvokeError):
            print(error)
            await ctx.send(f"Command Invoke Error")
    
    def play_next(self, error=None):
        if error is not None:
            print(error, type(error))
        if self.q.peek():
            self.voice.play(self.q.poll().sound, after=self.play_next)