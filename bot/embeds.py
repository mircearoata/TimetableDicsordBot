import discord
from datetime import datetime
from utils import get_day_courses, format_timedelta, time_diff

def get_groups_content(groups, config):
  allGroups = config.get('groups', [])
  if(sorted(groups) == sorted(allGroups)):
    return f'**__@everyone__**'
  return ', '.join(f'**__{group}__**' for group in sorted(groups))

def get_time_slot_embed_content(coursesTimeSlot, config):
  groups = '\n'.join([get_groups_content(course['groups'], config) for course in coursesTimeSlot])
  courses = '\n'.join([f'__{course["courseName"]}__' for course in coursesTimeSlot])
  links = '\n'.join([(f'**__[JOIN]({course["link"]})__**' if 'link' in course and course['link'] else 'N/A') for course in coursesTimeSlot])
  return groups, courses, links

def make_courses_embed(day, config):
  day = day.lower()
  dayCourses = get_day_courses(day, config)

  timeSlots = config.get('timeSlots', [])
  
  embed = discord.Embed(title=f'Courses on {day}', color=0x00ff00)
  for i, timeSlot in enumerate(timeSlots):
    groups = 'N/A'
    courses = 'N/A'
    links = 'N/A'
    
    if i < len(dayCourses) and len(dayCourses[i]) > 0:
      groups, courses, links = get_time_slot_embed_content(dayCourses[i], config)

    embed.add_field(name=f'{timeSlot["timeBegin"].strftime("%H:%M")} - {timeSlot["timeEnd"].strftime("%H:%M")}', value=groups, inline=True)
    embed.add_field(name='Course', value=courses, inline=True)
    embed.add_field(name='Link', value=links, inline=True)

  return embed

def make_current_course_embed(config):
  now = datetime.now()
  
  day = datetime.now().strftime('%A').lower()
  dayCourses = get_day_courses(day, config)

  timeSlots = config.get('timeSlots', [])

  try:
    currentTimeSlot = next(timeSlot for timeSlot in timeSlots if now.time() <= timeSlot['timeEnd'].time())
    currentTimeSlotIdx = timeSlots.index(currentTimeSlot)

    if currentTimeSlot['timeBegin'].time() <= now.time() <= currentTimeSlot['timeEnd'].time():
      embed = discord.Embed(title=f'Current course (ends at {currentTimeSlot["timeEnd"].strftime("%H:%M")} - in {format_timedelta(time_diff(now.time(), currentTimeSlot["timeEnd"].time()))})', color=0x00ff00)
      groups = 'N/A'
      courses = 'N/A'
      links = 'N/A'
      
      if currentTimeSlotIdx < len(dayCourses) and len(dayCourses[currentTimeSlotIdx]) > 0:
        groups, courses, links = get_time_slot_embed_content(dayCourses[currentTimeSlotIdx], config)
      
      embed.add_field(name=f'{currentTimeSlot["timeBegin"].strftime("%H:%M")} - {currentTimeSlot["timeEnd"].strftime("%H:%M")}', value=groups, inline=True)
      embed.add_field(name='Course', value=courses, inline=True)
      embed.add_field(name='Link', value=links, inline=True)

      return embed
    else:
      embed = discord.Embed(title=f'No course right now', color=0x00ff00)
      return embed
  except StopIteration:
      embed = discord.Embed(title=f'No course right now', color=0x00ff00)
      return embed

def make_next_course_embed(config):
  now = datetime.now()
  
  day = datetime.now().strftime('%A').lower()
  dayCourses = get_day_courses(day, config)
  
  timeSlots = config.get('timeSlots', [])

  try:
    nextTimeSlot = next(timeSlot for timeSlot in timeSlots if now.time() <= timeSlot['timeBegin'].time())
    nextTimeSlotIdx = timeSlots.index(nextTimeSlot)

    embed = discord.Embed(title=f'Next course (starts at {nextTimeSlot["timeBegin"].strftime("%H:%M")} - in {format_timedelta(time_diff(now.time(), nextTimeSlot["timeBegin"].time()))})', color=0x00ff00)
    groups = 'N/A'
    courses = 'N/A'
    links = 'N/A'

    if nextTimeSlotIdx < len(dayCourses) and len(dayCourses[nextTimeSlotIdx]) > 0:
      groups, courses, links = get_time_slot_embed_content(dayCourses[nextTimeSlotIdx], config)
    
    embed.add_field(name=f'{nextTimeSlot["timeBegin"].strftime("%H:%M")} - {nextTimeSlot["timeEnd"].strftime("%H:%M")}', value=groups, inline=True)
    embed.add_field(name='Course', value=courses, inline=True)
    embed.add_field(name='Link', value=links, inline=True)

    return embed
  except StopIteration:
      embed = discord.Embed(title=f'No upcoming course', color=0x00ff00)
      return embed

def make_course_embed(timeSlot, course, config):
  groups, courses, links = get_time_slot_embed_content([course], config)
  
  embed = discord.Embed(title=f'{course["courseName"]} ({timeSlot["timeBegin"].strftime("%H:%M")} - {timeSlot["timeEnd"].strftime("%H:%M")})', color=0x00ff00)
  embed.add_field(name=f'{timeSlot["timeBegin"].strftime("%H:%M")} - {timeSlot["timeEnd"].strftime("%H:%M")}', value=groups, inline=True)
  embed.add_field(name='Course', value=courses, inline=True)
  embed.add_field(name='Link', value=links, inline=True)
  
  return embed