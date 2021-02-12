from discord.ext import tasks, commands
import config
import embeds
from datetime import datetime

UPDATE_INTERVAL = 5.0
FAIL_COUNT = 20 * 60 / UPDATE_INTERVAL

class DynamicMessages(commands.Cog):
  def __init__(self, bot):
    super().__init__()
    self.bot = bot
    self.failed = {}
  
  def start(self):
    self.update_dynamic_get_courses.start()
    self.update_dynamic_current_course.start()
    self.update_dynamic_next_course.start()

  async def try_edit_message(self, channelID, messageID, *args, **kwargs):
    channel = self.bot.get_channel(channelID)
    if not channel:
      print(f'Channel {channelID} not found.')
      return False
    message = await channel.fetch_message(messageID)
    if not message:
      print(f'Message {channelID}/{messageID} not found.')
      return False
    try:
      await message.edit(*args, **kwargs)
    except:
      return False
    return True

  async def update_messages(self, messages, embed):
    toRemove = []
    for messageData in messages:
      messageStr = f'{messageData[0]}/{messageData[1]}'
      if not await self.try_edit_message(int(messageData[0]), int(messageData[1]), embed=embed):
        if messageStr not in self.failed:
          self.failed[messageStr] = 0
        self.failed[messageStr] += 1
        if self.failed[messageStr] > FAIL_COUNT:
          toRemove.append(messageData)
      else:
        self.failed.pop(messageStr, None)
    return toRemove

  @tasks.loop(seconds=UPDATE_INTERVAL)
  async def update_dynamic_get_courses(self):
    day = datetime.now().strftime('%A')
    embed = embeds.make_courses_embed(day)
    dynamicMessages = config.get('dynamicGetCourses', [])

    toRemove = await self.update_messages(dynamicMessages, embed)
    
    for remove in toRemove:
      dynamicMessages.remove(remove)
    if len(toRemove) > 0:
      config.save('dynamicGetCourses', dynamicMessages)

  @tasks.loop(seconds=UPDATE_INTERVAL)
  async def update_dynamic_current_course(self):
    embed = embeds.make_current_course_embed()
    dynamicMessages = config.get('dynamicCurrentCourse', [])
    
    toRemove = await self.update_messages(dynamicMessages, embed)
    
    for remove in toRemove:
      dynamicMessages.remove(remove)
    if len(toRemove) > 0:
      config.save('dynamicCurrentCourse', dynamicMessages)

  @tasks.loop(seconds=UPDATE_INTERVAL)
  async def update_dynamic_next_course(self):
    embed = embeds.make_next_course_embed()
    dynamicMessages = config.get('dynamicNextCourse', [])

    toRemove = await self.update_messages(dynamicMessages, embed)
    
    for remove in toRemove:
      dynamicMessages.remove(remove)
    if len(toRemove) > 0:
      config.save('dynamicNextCourse', dynamicMessages)
