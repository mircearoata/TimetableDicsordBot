from discord.ext import commands
import embeds
from datetime import datetime

class Interaction(commands.Cog):
  @commands.command()
  async def version(self, ctx):
    await ctx.send(ctx.bot.version)
  
  @commands.command()
  async def get_courses(self, ctx, *args):
    day = datetime.now().strftime('%A')
    if args:
      day = args[0]
    
    await ctx.send(embed=embeds.make_courses_embed(day))