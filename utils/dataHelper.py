import json
import os
import errno
import shutil
import requests

def getJson(url):
  # get API response
  response = requests.get(url)
  # parse respons as JSON
  data = json.loads(response.text)
  # return JSON object
  return data


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

  print('Successfully dumped ' + '\033[92m' + filename + '\033[0m' + ' to ' + dump_dir)

def removeDirectory(directory):
  input_dir = os.path.dirname(directory)
  shutil.rmtree(input_dir)

def printGreen(string):
  prefix = '\033[92m'
  suffix = '\033[0m'
  green = prefix + string + suffix
  return green

def printBold(string):
  prefix = '\033[1m'
  suffix = '\033[0m'
  bold = prefix + string + suffix
  return bold