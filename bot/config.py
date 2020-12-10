import jsonpickle
import os

configPath = os.path.dirname(os.path.realpath(__file__)) + '/../config/config.json'

data = None

def read():
  with open(configPath, 'r+') as f:
    return jsonpickle.decode(f.read())

def write(data):
  with open(configPath, 'w+') as f:
    f.write(jsonpickle.encode(data, indent=2))

def get(key: str, default=None):
  global data
  if not data:
    data = read()
  try:
    return data[key]
  except:
    return default

def save(key: str, value):
  global data
  data[key] = value
  write(data)

def save_current():
  global data
  write(data)

def reload():
  global data
  data = read()