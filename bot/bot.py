import os
import discord
from discord.ext import commands
import config
import sys
import traceback
from cogs.admin import Admin
from cogs.interaction import Interaction
from cogs.dynamicMessages import DynamicMessages

assert(os.environ.get('TIMETABLE_BOT_TOKEN'))

class Bot(discord.ext.commands.Bot):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.version = '0.0.0'
    self.add_cog(Admin())
    self.add_cog(Interaction())
    self.add_cog(DynamicMessages(self))

  async def on_ready(self):
    # self.modchannel = self.get_channel(int(config.get('mod_channel')))
    # assert (self.modchannel, 'I couldn't fetch the mod channel, please check the config')
    print('We have logged in as {0.user}'.format(self))
    self.get_cog('DynamicMessages').start()

  async def on_error(self, event, *args, **kwargs):
    type, value, tb = sys.exc_info()
    if event == 'on_message':
        channel = ' in #' + args[0].channel.name
    else:
        channel = ''
    tbs = '```TimetableBot v' + self.version + '\n\n' + type.__name__ + ' exception handled in ' + event + channel + ' : ' + str(
        value) + '\n\n'
    for string in traceback.format_tb(tb):
        tbs = tbs + string
    tbs = tbs + '```'
    print(tbs.replace('```', ''))
    # await self.get_channel(self.modchannel).send(tbs)

client = Bot(config.get('prefix', ';'))
client.run(os.environ.get('TIMETABLE_BOT_TOKEN'))