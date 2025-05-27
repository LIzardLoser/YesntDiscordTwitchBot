import discord
from discord.ext import commands
from tac import SoftCheck
from Bot.utils import addStreamer, resetStreamers, removeStreamer, setChannel, HelpEmbed, embed

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Util Cog Loaded!')

    @commands.hybrid_command()
    async def ping(self, ctx):
        await SoftCheck(ctx, ctx.guild.id, True)
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(aliases=['h'])
    async def helpstream(self, ctx):
        '''Displays help embed'''
        await ctx.send(embed=HelpEmbed, ephemeral=True)

    @commands.hybrid_command()
    async def check(self, ctx):
        """SoftCheck of the twitch api"""
        await SoftCheck(ctx, ctx.guild.id, False)

    @commands.hybrid_command()
    async def setchannel(self, ctx, channel: discord.TextChannel):
        result = await setChannel(ctx.guild.id, channel)
        await ctx.send(result, ephemeral=True)

    @commands.hybrid_group(fallback='add')
    async def streamers(self, ctx, name: str):
        result = await addStreamer(ctx.guild.id, name)
        await ctx.send(result, ephemeral=True)

    @streamers.command(name='remove', aliases=['rm'])
    async def remove(self, ctx, name: str):
        result = await removeStreamer(ctx.guild.id, name)
        await ctx.send(result, ephemeral=True)

    @streamers.command(name='reset', aliases=['rst'])
    async def reset(self, ctx):
        result = await resetStreamers(ctx.guild.id)
        await ctx.send(result, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Utils(bot))

