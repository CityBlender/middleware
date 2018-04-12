import json
import os
import errno
import shutil

def dumpJson(filename, data, dump_dir):

  # set up input
  dump_dir = dump_dir
  dump_file_path = dump_dir + filename
  dump_directory = os.path.dirname(dump_file_path)

  # check if directory exists, create if not
  try:
    os.makedirs(dump_directory)
  except OSError as e:
    if e.errno != errno.EEXIST:
      raise

  # dump JSON file
  with open(dump_file_path, 'w') as fp:
    json.dump(data, fp)

def removeDirectory(directory):
  input_dir = os.path.dirname(directory)
  shutil.rmtree(input_dir)