# Save groups of mods in a HoI profile

import os, json

DLC_LOAD = "dlc_load.json"
SUFFIX = '.hoi4profile'

def main():
  import sys
  if len(sys.argv) < 2:
    print_usage()
    fatal("Must provide action, check help")
  
  action = sys.argv[1]
  args = []
  if len(sys.argv) > 2:
    args = sys.argv[2:]
  (root, saves_dir) = get_paths()

  if action == "help":
    print_usage()
    exit(1)
  elif action == "save":
    save(root, saves_dir, args)
  elif action == "list":
    list_profiles(root, saves_dir, args)
  elif action == "activate":
    activate(root, saves_dir, args)


def activate(path, saves_dir, args):
  if len(args) < 1:
    fatal('Must provide the profile name to activate')

  name = args[0]
  if name.endswith(SUFFIX):
    name = name.replace(SUFFIX, '')

  profile = read_profile(saves_dir, name)
  new_mods = list(profile["enabled_mods"])

  save_current(path, new_mods)
  print(f'Successfully activated {profile["name"]}')

def save(path, saves_dir, args):
  '''Save the current profile by a name'''

  if len(args) < 0:
    fatal("Must provide name")

  mods = get_current(path)
  profile = {
    "name": ' '.join(args),
    "enabled_mods": mods
  }

  filename = save_profile(saves_dir, profile)

  print(f'Saved successfully as {filename}')

def list_profiles(path, saves_dir, args):
  '''List all saved profiles'''
  for save in get_saves(saves_dir):
    print(save)

def get_current(path):
  with open(os.path.join(path, DLC_LOAD), 'r') as f:
    current = json.load(f)
  return list(current["enabled_mods"])

def save_current(path, new_mods):
  with open(os.path.join(path, DLC_LOAD), 'r+') as f:
    current = json.load(f)
    current["enabled_mods"] = new_mods
    f.seek(0)
    json.dump(current, f)
    f.truncate()

def get_saves(saves_dir):
  for file in os.listdir(saves_dir):
    if os.path.isfile(os.path.join(saves_dir, file)) and file.endswith(SUFFIX):
      yield file

def read_profile(saves_dir, name):
  filename = name_to_filename(name)
  path = os.path.join(saves_dir, filename)
  if not os.path.exists(path):
    fatal(f'Profile {filename} does not exist in {saves_dir}')

  with open(path, 'r') as f:
    return json.load(f)

def save_profile(saves_dir, content):
  filename = name_to_filename(content["name"])
  path = os.path.join(saves_dir, filename)

  with open(path, 'w') as f:
    json.dump(content, f)

  return filename

def name_to_filename(name):
  name = str(name).replace(' ', '_').lower()
  return name + SUFFIX


def get_paths():
  root = os.path.expandvars(os.environ['HOI_ROOT'])
  saves = os.path.expandvars(os.environ['HOI_PROFILER_SAVES_ROOT'])

  if not saves:
    fatal("You must set HOI_ROOT environment variable for the documents folder where mods are")
    
  if not saves:
    fatal("You must set HOI_PROFILER_SAVES_ROOT where you wish to save the profile files")

  # Create the saves folder if it does not exist
  if not os.path.exists(saves):
    os.mkdir(saves)

  return (root, saves)

def print_usage():
  options = {
    'list': ('list\t', 'List the current profiles'),
    'save': ('save NAME', 'save the current profile with given name'),
    'activate': ('activate NAME', 'activate a sepecific profile, overwrites the current mod selection in HoI')
  }

  print('USAGE:')
  for option in options:
    (usage, descp) = options[option]
    print(f'\t{usage}\t\t| {descp}')

def fatal(message):
  print(message)
  exit(1)

if __name__ == "__main__":
  main()