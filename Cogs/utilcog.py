from discord.ext import commands
from tac import SoftCheck
from Bot.utils import addStreamer, resetStreamers, embed

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Util Cog Loaded!')

    @commands.hybrid_command()
    async def ping(self, ctx):
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command()
    async def check(self, ctx):
        """SoftCheck of the twitch api"""
        await ctx.send(embed=embed)
        await SoftCheck(ctx, ctx.guild.id)

    @commands.hybrid_group(fallback='add')
    async def streamers(self, ctx, name: str):
        await addStreamer(ctx, ctx.guild.id, name)
        await ctx.send('Adding streamer...', ephemeral=True)

    @streamers.command(name='reset', aliases=['rm'])
    async def reset(self, ctx):
        await resetStreamers(ctx, ctx.guild.id)
        await ctx.send('Streamers reset!', ephemeral=True)


async def setup(bot):
    await bot.add_cog(Utils(bot))

