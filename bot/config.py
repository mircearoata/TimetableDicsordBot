import jsonpickle
import os

CONFIG_ROOT = os.path.dirname(os.path.realpath(__file__)) + '/../config/'

class Config:
  def __init__(self, guild_id):
    if guild_id == 'global':
      self.config_path = CONFIG_ROOT + 'config.json'
    else:
      self.config_path = CONFIG_ROOT + str(guild_id) + '/config.json'
    self.data = None

  def read(self):
    with open(self.config_path, 'r+') as f:
      return jsonpickle.decode(f.read())

  def write(self, data):
    with open(self.config_path, 'w+') as f:
      f.write(jsonpickle.encode(data, indent=2))

  def get(self, key: str, default=None):
    if not self.data:
      self.data = self.read()
    try:
      return self.data[key]
    except:
      return default

  def save(self, key: str, value):
    self.data[key] = value
    self.write(self.data)

  def save_current(self):
    self.write(self.data)

  def reload(self):
    self.data = self.read()