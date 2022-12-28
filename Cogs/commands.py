#modules

import discord
from discord.ext import commands

class bot_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    #end

    # Allows users with admin role to purge chat
    @commands.command(pass_context=True)
    async def purge(self, ctx, limit: int):
        """Allows Members to Purge there msg's or an admin to purge chat"""
        await ctx.message.delete()
        await ctx.channel.purge(limit=limit)
        await ctx.send('Cleared by <@{.author.id}>'.format(ctx))
    #end

    @commands.command(aliases=["av", "pfp"])
    @commands.guild_only()
    async def avatar(self, ctx,  *, user: discord.Member = None):
        """ Get the avatar of you or someone else """
        user = user or ctx.author

        avatars_list = []

        def target_avatar_formats(target):
            formats = ["JPEG", "PNG", "WebP"]
            if target.is_animated():
                formats.append("GIF")
            return formats

        if not user.avatar and not user.guild_avatar:
            return await ctx.send(f"**{user}** has no avatar set, at all...")

        if user.avatar:
            avatars_list.append("**Account avatar:** " + " **-** ".join(
                f"[{img_format}]({user.avatar.replace(format=img_format.lower(), size=1024)})"
                for img_format in target_avatar_formats(user.avatar)
            ))

        embed = discord.Embed(colour=user.top_role.colour.value)

        if user.guild_avatar:
            avatars_list.append("**Server avatar:** " + " **-** ".join(
                f"[{img_format}]({user.guild_avatar.replace(format=img_format.lower(), size=1024)})"
                for img_format in target_avatar_formats(user.guild_avatar)
            ))
            embed.set_thumbnail(url=user.avatar.replace(format="png"))

        embed.set_image(url=f"{user.display_avatar.with_size(256).with_static_format('png')}")
        embed.description = "\n".join(avatars_list)

        await ctx.send(f"🖼 Avatar to **{user}**", embed=embed)
    #end

