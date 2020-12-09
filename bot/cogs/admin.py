from discord.ext import commands
import config
import embeds
from datetime import datetime

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
  async def dynamic_get_courses(self, ctx):
    day = datetime.now().strftime('%A')
    
    message = await ctx.send(embed=embeds.make_courses_embed(day))
    dynamicMessages = config.get('dynamicGetCourses', [])
    dynamicMessages.append([message.channel.id, message.id])
    config.save('dynamicGetCourses', dynamicMessages)
  
  @commands.command()
  @commands.check(mod_only)
  async def dynamic_current_course(self, ctx):    
    message = await ctx.send(embed=embeds.make_current_course_embed())
    dynamicMessages = config.get('dynamicCurrentCourse', [])
    dynamicMessages.append([message.channel.id, message.id])
    config.save('dynamicCurrentCourse', dynamicMessages)
  
  @commands.command()
  @commands.check(mod_only)
  async def dynamic_next_course(self, ctx):    
    message = await ctx.send(embed=embeds.make_next_course_embed())
    dynamicMessages = config.get('dynamicNextCourse', [])
    dynamicMessages.append([message.channel.id, message.id])
    config.save('dynamicNextCourse', dynamicMessages)
  
  @commands.command()
  @commands.check(mod_only)
  async def add_course(self, ctx, *args):
    if not args or len(args) < 4:
      await ctx.send('Usage: add_course group course day timeSlot link gapWeeks startWeek')
      return
    
    group = args[0]
    courseName = args[1]
    day = args[2]
    timeSlot = int(args[3])
    link = args[4] if len(args) >= 5 else None
    gapWeeks = int(args[5]) if len(args) >= 6 else 0
    startWeek = int(args[6]) if len(args) >= 7 else 0

    courses = config.get('courses', {})
    if day not in courses:
      courses[day] = []
    if timeSlot >= len(courses[day]):
      for i in range(timeSlot - len(courses[day]) + 1):
        courses[day].append([])
    courses[day][timeSlot].append({ 'group': group, 'courseName': courseName, 'link': link, 'gapWeeks': gapWeeks, 'startWeek': startWeek })
    config.save('courses', courses)
    await ctx.send(f'Saved course {courseName} for {group} on {day} in time slot {timeSlot}')

  @commands.command()
  @commands.check(mod_only)
  async def set_time_slots(self, ctx, *args):
    if not args:
      await ctx.send('Usage: set_time_slots timeBegin1-timeEnd1 timeBegin2-timeEnd2 ...')
      return
    
    timeSlots = [{ 'timeBegin': datetime.strptime(timeSlot.split('-')[0], '%H:%M'), 'timeEnd': datetime.strptime(timeSlot.split('-')[1], '%H:%M') } for timeSlot in args]
    config.save('timeSlots', timeSlots)
    await ctx.send(f'Saved {len(timeSlots)} time slots')
  
  @commands.command()
  @commands.check(mod_only)
  async def set_school_start(self, ctx, *args):
    if not args:
      await ctx.send('Usage: set_school_start YYYY-MM-DD')
    
    schoolStart = datetime.strptime(args[0], '%Y-%m-%d')
    config.save('schoolStart', schoolStart)
    await ctx.send(f'School start set to {schoolStart.strftime("%A %Y-%m-%d")}!')

  @commands.command()
  @commands.check(mod_only)
  async def save_config(self, ctx):
    config.save_current()
    await ctx.send('Saved!')
  
  @commands.command()
  @commands.check(mod_only)
  async def reload_config(self, ctx):
    config.reload()
    await ctx.send('Reloaded!')