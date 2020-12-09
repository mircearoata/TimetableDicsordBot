import json
import os

configPath = os.path.dirname(os.path.realpath(__file__)) + '\..\config.json'

data = None

def read():
  return json.load(open(configPath, 'r'))

def write(data):
  return json.dump(data, open(configPath, 'w+'))

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