import os
import discord.ext.commands
from config import Config
from migrations import migrations
from cogs.admin import Admin
from cogs.interaction import Interaction
from cogs.dynamicMessages import DynamicMessages
from cogs.courseStart import CourseStart

assert(os.environ.get('TIMETABLE_BOT_TOKEN'))

global_config = Config('global')

class Bot(discord.ext.commands.Bot):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.version = '0.0.0'
    self.add_cog(Admin())
    self.add_cog(Interaction())
    self.add_cog(DynamicMessages(self))
    self.add_cog(CourseStart(self))
    self.configs = {}
    migrations(self.configs)

  async def on_ready(self):
    print('We have logged in as {0.user}'.format(self))
    self.configs = {guild.id: Config(guild.id) for guild in self.guilds}
    self.get_cog('DynamicMessages').start()
    self.get_cog('CourseStart').start()

  async def get_prefix(self, message): ##first we define get_prefix
    return self.configs[message.guild.id].get('prefix', ';')


client = Bot(';')
client.run(os.environ.get('TIMETABLE_BOT_TOKEN'))