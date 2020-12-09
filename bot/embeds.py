import config
import discord
from datetime import datetime, date, time, timedelta

def this_week(course):
  now = datetime.now()
  schoolStart = config.get('schoolStart', datetime.now())
  schoolWeek = (now - schoolStart).days // 7
  return schoolWeek % (course['gapWeeks'] + 1) == course['startWeek']

def get_time_slot_embed_content(coursesTimeSlot, maxGroupLength = 0, maxCourseLength = 0):
  groups = '\n'.join([f'{course["group"]:>{maxGroupLength}}' for course in coursesTimeSlot])
  courses = '\n'.join([f'{course["courseName"]:>{maxCourseLength}}' for course in coursesTimeSlot])
  links = '\n'.join([(f'[JOIN]({course["link"]})' if 'link' in course and course['link'] else 'N/A') for course in coursesTimeSlot])
  return groups, courses, links

def get_day_courses(day):
  allCourses = config.get('courses', {})
  dayCourses = []
  if day in allCourses:
    dayCourses = allCourses[day]
  dayCourses = [list(filter(this_week, timeSlotCourses)) for timeSlotCourses in dayCourses]
  return dayCourses

def format_timedelta(timeDelta: timedelta):
  minutes, seconds = divmod(timeDelta.seconds, 60)
  if minutes > 0:
    return f'{minutes} minutes'
  return f'{seconds} seconds'
  
def time_diff(time1: time, time2: time):
  return datetime.combine(date.today(), time2) - datetime.combine(date.today(), time1)

def make_courses_embed(day):
  day = day.lower()
  dayCourses = get_day_courses(day)

  timeSlots = config.get('timeSlots', [])
  
  embed = discord.Embed(title=f'Courses on {day}', color=0x00ff00)
  maxGroupLength = max([0] + [max([0] + [len(course['group']) for course in coursesTimeSlot]) for coursesTimeSlot in dayCourses])
  maxCourseLength = max([0] + [max([0] + [len(course['courseName']) for course in coursesTimeSlot]) for coursesTimeSlot in dayCourses])
  maxLinkLength = max([0] + [max([0] + [(len('JOIN') if 'link' in course else len('N/A')) for course in coursesTimeSlot]) for coursesTimeSlot in dayCourses])
  for i, timeSlot in enumerate(timeSlots):
    groups = 'N/A' + ' ' * (maxGroupLength - 3)
    courses = 'N/A' + ' ' * (maxCourseLength - 3)
    links = 'N/A' + ' ' * (maxLinkLength - 3)
    
    if i < len(dayCourses) and len(dayCourses[i]) > 0:
      groups, courses, links = get_time_slot_embed_content(dayCourses[i], maxGroupLength, maxCourseLength)

    embed.add_field(name=f'{timeSlot["timeBegin"].strftime("%H:%M")} - {timeSlot["timeEnd"].strftime("%H:%M")}', value=groups, inline=True)
    embed.add_field(name='Course', value=courses, inline=True)
    embed.add_field(name='Link', value=links, inline=True)

  return embed

def make_current_course_embed():
  now = datetime.now()
  
  day = datetime.now().strftime('%A').lower()
  dayCourses = get_day_courses(day)

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
        groups, courses, links = get_time_slot_embed_content(dayCourses[currentTimeSlotIdx])
      
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
  dayCourses = get_day_courses(day)
  
  timeSlots = config.get('timeSlots', [])

  try:
    nextTimeSlot = next(timeSlot for timeSlot in timeSlots if now.time() <= timeSlot['timeBegin'].time())
    nextTimeSlotIdx = timeSlots.index(nextTimeSlot)

    embed = discord.Embed(title=f'Next course (starts at {nextTimeSlot["timeBegin"].strftime("%H:%M")} - in {format_timedelta(time_diff(now.time(), nextTimeSlot["timeBegin"].time()))})', color=0x00ff00)
    groups = 'N/A'
    courses = 'N/A'
    links = 'N/A'

    if nextTimeSlotIdx < len(dayCourses) and len(dayCourses[nextTimeSlotIdx]) > 0:
      groups, courses, links = get_time_slot_embed_content(dayCourses[nextTimeSlotIdx])
    
    embed.add_field(name=f'{nextTimeSlot["timeBegin"].strftime("%H:%M")} - {nextTimeSlot["timeEnd"].strftime("%H:%M")}', value=groups, inline=True)
    embed.add_field(name='Course', value=courses, inline=True)
    embed.add_field(name='Link', value=links, inline=True)

    return embed
  except StopIteration:
      embed = discord.Embed(title=f'No upcoming course', color=0x00ff00)
      return embed