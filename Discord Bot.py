# This example requires the 'message_content' privileged intent to function.

import asyncio
import discord
from discord.ext import commands
from Cogs.Music import Music
from Cogs.commands import bot_commands

#intents

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/help"))
    print(f"Logged in as {bot.user} using discord.py {discord.__version__}")
    print('------')
#end

async def main():
    async with bot:
        await bot.add_cog(Music(bot))
        await bot.add_cog(bot_commands(bot))
        await bot.start('Token here')
#end

asyncio.run(main())

