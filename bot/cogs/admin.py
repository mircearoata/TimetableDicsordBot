from discord.ext import commands
import config
import embeds
from datetime import datetime
import typing

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

    await ctx.message.delete()
  
  @commands.command()
  @commands.check(mod_only)
  async def dynamic_current_course(self, ctx):    
    message = await ctx.send(embed=embeds.make_current_course_embed())
    dynamicMessages = config.get('dynamicCurrentCourse', [])
    dynamicMessages.append([message.channel.id, message.id])
    config.save('dynamicCurrentCourse', dynamicMessages)

    await ctx.message.delete()
  
  @commands.command()
  @commands.check(mod_only)
  async def dynamic_next_course(self, ctx):    
    message = await ctx.send(embed=embeds.make_next_course_embed())
    dynamicMessages = config.get('dynamicNextCourse', [])
    dynamicMessages.append([message.channel.id, message.id])
    config.save('dynamicNextCourse', dynamicMessages)

    await ctx.message.delete()
  
  @commands.command()
  @commands.check(mod_only)
  async def add_course(self, ctx, *args):
    if not args or len(args) < 4:
      await ctx.send('Usage: add_course @group1,@group2... course day timeSlot noNotify link gapWeeks startWeek')
      return
    
    groups = args[0].split(',')
    courseName = args[1]
    day = args[2]
    timeSlot = int(args[3])
    noNotify = args[4] if len(args) >= 5 else False
    link = args[5] if len(args) >= 6 else None
    gapWeeks = int(args[6]) if len(args) >= 7 else 0
    startWeek = int(args[7]) if len(args) >= 8 else 0

    courses = config.get('courses', {})
    if day not in courses:
      courses[day] = []
    if timeSlot >= len(courses[day]):
      for i in range(timeSlot - len(courses[day]) + 1):
        courses[day].append([])
    courses[day][timeSlot].append({ 'groups': groups, 'courseName': courseName, 'link': link, 'gapWeeks': gapWeeks, 'startWeek': startWeek, 'noNotify': not noNotify })
    config.save('courses', courses)
    await ctx.send(f'Saved course {courseName} for {len(groups)} groups on {day} in time slot {timeSlot}{f" (once every {gapWeeks + 1} weeks, starting week {startWeek + 1})"if gapWeeks > 0 else ""}{" without notification" if noNotify else ""}')
  
  @commands.command()
  @commands.check(mod_only)
  async def remove_course(self, ctx, day: str, timeSlot: int, removeIdx: typing.Optional[int]):
    if not day or not timeSlot:
      await ctx.send('Usage: remove_course day timeSlot [removeIdx]')
      return
    
    courses = config.get('courses', {})
    
    if day not in courses:
      await ctx.send(f'Course not found!')
      return
    if timeSlot >= len(courses[day]):
      await ctx.send(f'Course not found!')
      return
    
    if len(courses[day][timeSlot]) > 1 and not removeIdx:
      await ctx.send('More than 1 course in that time slot. Choose one:\n' + '\n'.join(f'{idx}. {course["courseName"]} for {len(course["groups"])} groups' for idx, course in enumerate(courses[day][timeSlot])))
      return  

    if not removeIdx:
      removeIdx = 0

    removed = courses[day][timeSlot].pop(removeIdx)
    config.save('courses', courses)
    await ctx.send(f'Removed course {removed["courseName"]} on {day} in time slot {timeSlot}')

  @commands.command()
  @commands.check(mod_only)
  async def set_groups(self, ctx, *args):
    if not args:
      await ctx.send('Usage: set_groups @group1 @group2 ...')
      return
    
    groups = args
    config.save('groups', groups)
    await ctx.send(f'Saved {len(groups)} groups')
  
  @commands.command()
  @commands.check(mod_only)
  async def set_course_start_channel(self, ctx, channel: str):
    if not channel:
      await ctx.send('Usage: set_course_start_channel #channel')
      return
    
    config.save('courseStartChannel', channel[2:-1])
    await ctx.send(f'Course start notificaions will be sent in {channel}')

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
  async def set_notification_lifetime(self, ctx, lifespan: int):
    if not lifespan:
      await ctx.send('Usage: set_notification_lifetime seconds')
      return
    
    config.save('notificationLifespan', lifespan)
    await ctx.send(f'Notifications will be deleted after {lifespan} seconds')

  @commands.command()
  @commands.check(mod_only)
  async def set_course_start_everyone(self, ctx, mentionEveryone: bool):
    if mentionEveryone == None:
      await ctx.send('Usage: set_course_start_everyone True/False')
      return
    
    config.save('courseStartMentionEveryone', mentionEveryone)
    await ctx.send(f'Course start notifications will {"not " if not mentionEveryone else ""}mention everyone')

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