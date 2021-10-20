import jsonpickle
import pathlib
import os
from datetime import datetime

CONFIG_ROOT = os.path.dirname(os.path.realpath(__file__)) + '/../config/'

class Config:
  def __init__(self, guild_id):
    if guild_id == 'global':
      self.config_path = CONFIG_ROOT + 'config.json'
    else:
      self.config_path = CONFIG_ROOT + str(guild_id) + '/config.json'
    self.data = None
    self.fname = pathlib.Path(self.config_path)
    if not os.path.exists(self.config_path):
      os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
      self.write({})
    self.last_modified = datetime.fromtimestamp(self.fname.stat().st_mtime)

  def modified_outside(self):
    modified_time = datetime.fromtimestamp(self.fname.stat().st_mtime)
    if modified_time > self.last_modified:
      return True
    pass

  def read(self):
    with open(self.config_path, 'r+') as f:
      return jsonpickle.decode(f.read())

  def write(self, data):
    with open(self.config_path, 'w+') as f:
      f.write(jsonpickle.encode(data, indent=2))
    self.last_modified = datetime.fromtimestamp(self.fname.stat().st_mtime)

  def get(self, key: str, default=None):
    if not self.data or self.modified_outside():
      if not self.data:
        print(f'Loading config {self.config_path}')
      else:
        print(f'Reloading config {self.config_path}, file changed externally')
      self.data = self.read()
    try:
      return self.data[key]
    except:
      return default

  def save(self, key: str, value):
    if self.modified_outside():
      self.data = self.read()
    self.data[key] = value
    self.write(self.data)

  def save_current(self):
    self.write(self.data)

  def reload(self):
    self.data = self.read()