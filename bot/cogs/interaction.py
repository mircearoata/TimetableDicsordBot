import discord
from discord.ext import commands
import config
import operator
import json
from datetime import datetime

def make_courses_embed(day):
  day = day.lower()
  dayCourses = config.get('courses', {})[day]
  timeSlots = config.get('timeSlots', [])
  
  embed = discord.Embed(title=f'Courses on {day}', color=0x00ff00)
  maxGroupLength = max([max([len(course['group']) for course in coursesTimeSlot]) for coursesTimeSlot in dayCourses])
  maxCourseLength = max([max([len(course['courseName']) for course in coursesTimeSlot]) for coursesTimeSlot in dayCourses])
  maxLinkLength = max([max([(len('JOIN') if 'link' in course else 0) for course in coursesTimeSlot]) for coursesTimeSlot in dayCourses])
  for i, timeSlot in enumerate(timeSlots):
    groups = 'N/A' + ' ' * (maxGroupLength - 3)
    courses = 'N/A' + ' ' * (maxCourseLength - 3)
    links = 'N/A' + ' ' * (maxLinkLength - 3)
    if i < len(dayCourses):
      groups = '\n'.join([f'{course["group"]:>{maxGroupLength}}' for course in dayCourses[i]])
      courses = '\n'.join([f'{course["courseName"]:>{maxCourseLength}}' for course in dayCourses[i]])
      links = '\n'.join([(f'[JOIN]({course["link"]})' if 'link' in course else '') for course in dayCourses[i]])
    embed.add_field(name=f'{timeSlot["timeBegin"]} - {timeSlot["timeEnd"]}', value=groups, inline=True)
    embed.add_field(name='Course', value=courses, inline=True)
    embed.add_field(name='Link', value=links, inline=True)

  return embed

class Interaction(commands.Cog):  
  @commands.command()
  async def version(self, ctx):
    await ctx.send(ctx.bot.version)
  
  @commands.command()
  async def get_courses(self, ctx, *args):
    day = datetime.now().strftime('%A')
    if args:
      day = args[0]
    
    await ctx.send(embed=make_courses_embed(day))