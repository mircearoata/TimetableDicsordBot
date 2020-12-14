from discord.channel import TextChannel
from utils import get_day_courses
from discord.ext import tasks, commands
import config
import embeds
from datetime import datetime

UPDATE_INTERVAL = 5.0

class CourseStart(commands.Cog):
  def __init__(self, bot):
    super().__init__()
    self.bot = bot
    self.lastCheck = datetime.now()

  def start(self):
    self.check_course_start.start()

  @tasks.loop(seconds=UPDATE_INTERVAL)
  async def check_course_start(self):
    now = datetime.now()
    day = now.strftime('%A')
    timeSlots = config.get('timeSlots', [])
    currentTimeSlot = next((timeSlot for timeSlot in timeSlots if timeSlot['timeBegin'].time() <= now.time() <= timeSlot['timeEnd'].time()), None)
    previousTimeSlot = next((timeSlot for timeSlot in timeSlots if timeSlot['timeBegin'].time() <= self.lastCheck.time() <= timeSlot['timeEnd'].time()), None)
    self.lastCheck = datetime.now()
    if currentTimeSlot and (not previousTimeSlot or currentTimeSlot != previousTimeSlot):
      dayCourses = get_day_courses(day)
      timeSlotIdx = timeSlots.index(currentTimeSlot)

      if timeSlotIdx < len(dayCourses):
        for course in dayCourses[timeSlotIdx]:
          embed = embeds.make_course_embed(currentTimeSlot, course)
          await self.bot.get_channel(int(config.get('courseStartChannel'))).send(', '.join(course['groups']) + ' your course is starting', embed=embed, delete_after=config.get('notificationLifespan', 5 * 60))
        if config.get('courseStartMentionEveryone', False):
          await self.bot.get_channel(int(config.get('courseStartChannel'))).send('@everyone', delete_after=config.get('notificationLifespan', 5 * 60))
