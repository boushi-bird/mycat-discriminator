from os.path import dirname, normpath, join

def relative_path(current_file, target_path):
  return normpath(join(dirname(current_file), target_path))
