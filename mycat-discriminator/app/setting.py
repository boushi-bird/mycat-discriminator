from dotenv import load_dotenv
from os import environ

from path_util import relative_path

env_file = relative_path(__file__, '../.env')

load_dotenv(env_file, verbose=True)

def env(key):
  return environ.get(key)

def env_path(key):
  return relative_path(env_file, env(key))
