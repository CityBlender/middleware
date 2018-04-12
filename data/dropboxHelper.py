import pathlib
import dropbox
import os

dropbox_token = str(os.getenv('DROPBOX_TOKEN'))

def uploadToDrobpox(filename, input_dir, output_dir):

  folder = pathlib.Path(input_dir)    # located in this folder
  filename = filename # file name
  file_path = folder / filename  # path object, defining the file

  # target location in Dropbox
  target = "/Documents/UCL/Fuinki Blender"+output_dir # the target folder
  target_file = target + filename   # the target path and file name

  # Create a dropbox object using an API v2 key
  dbx = dropbox.Dropbox(dropbox_token)

  # open the file and upload it
  with file_path.open("rb") as f:
    # upload gives you metadata about the file
    # we want to overwite any previous version of the file
    meta = dbx.files_upload(f.read(), target_file, mode=dropbox.files.WriteMode("overwrite"))


