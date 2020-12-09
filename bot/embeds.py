import config
import discord
from datetime import datetime

def make_courses_embed(day):
  day = day.lower()
  allCourses = config.get('courses', {})
  dayCourses = []
  if day in allCourses:
    dayCourses = allCourses[day]
  timeSlots = config.get('timeSlots', [])
  
  embed = discord.Embed(title=f'Courses on {day}', color=0x00ff00)
  maxGroupLength = max([0] + [max([len(course['group']) for course in coursesTimeSlot]) for coursesTimeSlot in dayCourses])
  maxCourseLength = max([0] + [max([len(course['courseName']) for course in coursesTimeSlot]) for coursesTimeSlot in dayCourses])
  maxLinkLength = max([0] + [max([(len('JOIN') if 'link' in course else 0) for course in coursesTimeSlot]) for coursesTimeSlot in dayCourses])
  for i, timeSlot in enumerate(timeSlots):
    groups = 'N/A' + ' ' * (maxGroupLength - 3)
    courses = 'N/A' + ' ' * (maxCourseLength - 3)
    links = 'N/A' + ' ' * (maxLinkLength - 3)
    if i < len(dayCourses):
      groups = '\n'.join([f'{course["group"]:>{maxGroupLength}}' for course in dayCourses[i]])
      courses = '\n'.join([f'{course["courseName"]:>{maxCourseLength}}' for course in dayCourses[i]])
      links = '\n'.join([(f'[JOIN]({course["link"]})' if 'link' in course else '') for course in dayCourses[i]])
    embed.add_field(name=f'{timeSlot["timeBegin"].strftime("%H:%M")} - {timeSlot["timeEnd"].strftime("%H:%M")}', value=groups, inline=True)
    embed.add_field(name='Course', value=courses, inline=True)
    embed.add_field(name='Link', value=links, inline=True)

  return embed

def make_current_course_embed():
  now = datetime.now()
  day = datetime.now().strftime('%A').lower()
  allCourses = config.get('courses', {})
  dayCourses = []
  if day in allCourses:
    dayCourses = allCourses[day]
  timeSlots = config.get('timeSlots', [])

  try:
    currentTimeSlot = next(timeSlot for timeSlot in timeSlots if now.time() <= timeSlot['timeEnd'].time())
    currentTimeSlotIdx = timeSlots.index(currentTimeSlot)

    if currentTimeSlot['timeBegin'].time() <= now.time() <= currentTimeSlot['timeEnd'].time():
      embed = discord.Embed(title=f'Current course (ends at {currentTimeSlot["timeEnd"].strftime("%H:%M")})', color=0x00ff00)
      groups = 'N/A'
      courses = 'N/A'
      links = 'N/A'
      if currentTimeSlotIdx < len(dayCourses):
        groups = '\n'.join([f'{course["group"]}' for course in dayCourses[currentTimeSlotIdx]])
        courses = '\n'.join([f'{course["courseName"]}' for course in dayCourses[currentTimeSlotIdx]])
        links = '\n'.join([(f'[JOIN]({course["link"]})' if 'link' in course else '') for course in dayCourses[currentTimeSlotIdx]])
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

def make_next_course_embed():
  now = datetime.now()
  day = datetime.now().strftime('%A').lower()
  allCourses = config.get('courses', {})
  dayCourses = []
  if day in allCourses:
    dayCourses = allCourses[day]
  timeSlots = config.get('timeSlots', [])

  try:
    nextTimeSlot = next(timeSlot for timeSlot in timeSlots if now.time() <= timeSlot['timeBegin'].time())
    nextTimeSlotIdx = timeSlots.index(nextTimeSlot)

    embed = discord.Embed(title=f'Next course (starts at {nextTimeSlot["timeBegin"].strftime("%H:%M")} - in {str(nextTimeSlot["timeBegin"] - now)})', color=0x00ff00)
    groups = 'N/A'
    courses = 'N/A'
    links = 'N/A'
    if nextTimeSlotIdx < len(dayCourses):
      groups = '\n'.join([f'{course["group"]}' for course in dayCourses[nextTimeSlotIdx]])
      courses = '\n'.join([f'{course["courseName"]}' for course in dayCourses[nextTimeSlotIdx]])
      links = '\n'.join([(f'[JOIN]({course["link"]})' if 'link' in course else '') for course in dayCourses[nextTimeSlotIdx]])
    embed.add_field(name=f'{nextTimeSlot["timeBegin"].strftime("%H:%M")} - {nextTimeSlot["timeEnd"].strftime("%H:%M")}', value=groups, inline=True)
    embed.add_field(name='Course', value=courses, inline=True)
    embed.add_field(name='Link', value=links, inline=True)

    return embed
  except StopIteration:
      embed = discord.Embed(title=f'No course coming up', color=0x00ff00)
      return embed