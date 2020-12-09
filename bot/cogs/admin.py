from discord.ext import commands
import config

async def mod_only(ctx):
  try:
    return (ctx.author.id == 325238474418421761) # or ctx.author.permissions_in(ctx.bot.modchannel).send_messages)
  except:
    return False

class Admin(commands.Cog):
  @commands.command()
  @commands.is_owner()
  async def shutdown(self, ctx):
    await ctx.send('Bot is shutting down')
    await ctx.bot.logout()
  
  @commands.command()
  @commands.check(mod_only)
  async def prefix(self, ctx, *args):
    if not args:
      await ctx.send('Please specify a prefix')
      return
    ctx.bot.command_prefix = args[0]
    config.save('prefix', args[0])
    await ctx.send('Prefix changed to \"' + args[0] + '"')
  
  @commands.command()
  @commands.check(mod_only)
  async def add_course(self, ctx, *args):
    if not args or len(args) < 4:
      await ctx.send('Usage: add_course group course day time link')
      return
    
    group = args[0]
    courseName = args[1]
    day = args[2]
    timeSlot = int(args[3])
    link = args[4] if len(args) >= 5 else None

    courses = config.get('courses', {})
    if day not in courses:
      courses[day] = []
    if timeSlot >= len(courses[day]):
      courses[day].insert(timeSlot, [])
    courses[day][timeSlot].append({ 'group': group, 'courseName': courseName, 'link': link })
    config.save('courses', courses)
    await ctx.send(f'Saved course {courseName} for {group} on {day} in time slot {timeSlot}')

  @commands.command()
  @commands.check(mod_only)
  async def set_time_slots(self, ctx, *args):
    if not args:
      await ctx.send('Usage: set_time_slots timeBegin1-timeEnd1 timeBegin2-timeEnd2 ...')
      return
    
    timeSlots = [{ 'timeBegin': timeSlot.split('-')[0], 'timeEnd': timeSlot.split('-')[1] } for timeSlot in args]
    config.save('timeSlots', timeSlots)
    await ctx.send(f'Saved {len(timeSlots)} time slots')