from discord.ext import tasks, commands
import config
import embeds
from datetime import datetime

class DynamicMessages(commands.Cog):
  def __init__(self, bot):
    super().__init__()
    self.bot = bot
  
  def start(self):
    self.update_dynamic_get_courses.start()
    self.update_dynamic_current_course.start()
    self.update_dynamic_next_course.start()

  @tasks.loop(seconds=5.0)
  async def update_dynamic_get_courses(self):
    day = datetime.now().strftime('%A')
    embed = embeds.make_courses_embed(day)
    dynamicMessages = config.get('dynamicGetCourses', [])
    for messageData in dynamicMessages:
      message = await self.bot.get_channel(int(messageData[0])).fetch_message(int(messageData[1]))
      if message:
        await message.edit(embed=embed)

  @tasks.loop(seconds=5.0)
  async def update_dynamic_current_course(self):
    embed = embeds.make_current_course_embed()
    dynamicMessages = config.get('dynamicCurrentCourse', [])
    for messageData in dynamicMessages:
      message = await self.bot.get_channel(int(messageData[0])).fetch_message(int(messageData[1]))
      if message:
        await message.edit(embed=embed)

  @tasks.loop(seconds=5.0)
  async def update_dynamic_next_course(self):
    embed = embeds.make_next_course_embed()
    dynamicMessages = config.get('dynamicNextCourse', [])
    for messageData in dynamicMessages:
      message = await self.bot.get_channel(int(messageData[0])).fetch_message(int(messageData[1]))
      if message:
        await message.edit(embed=embed)
