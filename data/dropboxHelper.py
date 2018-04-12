import pathlib
import dropbox
import os

dropbox_token = str(os.getenv('DROPBOX_TOKEN'))

def dumpToDrobpox():
  dbx = dropbox.Dropbox(dropbox_token)

  folder = pathlib.Path("data/")    # located in this folder
  filename = "test.txt"         # file name
  filepath = folder / filename  # path object, defining the file

  # target location in Dropbox
  target = "/Documents/UCL/Fuinki Blender/data/songkick-json-dumps/"              # the target folder
  targetfile = target + filename   # the target path and file name

  # Create a dropbox object using an API v2 key
  d = dropbox.Dropbox(dropbox_token)

  # open the file and upload it
  with filepath.open("rb") as f:
    # upload gives you metadata about the file
    # we want to overwite any previous version of the file
    meta = d.files_upload(f.read(), targetfile, mode=dropbox.files.WriteMode("overwrite"))


  # rootdir = '/tmp/test'

  # dbx.files_upload('file.txt', '/home/Documents/UCL/')

  # print ("Attempting to upload...")
  # # walk return first the current folder that it walk, then tuples of dirs and files not "subdir, dirs, files"
  # for dir, dirs, files in os.walk(rootdir):
  #     for file in files:
  #         try:
  #             file_path = os.path.join(dir, file)
  #             dest_path = os.path.join('/test', file)
  #             print('Uploading %s to %s' % (file_path, dest_path))
  #             with open(file_path) as f:
  #                 dbx.files_upload(f, dest_path, mute=True)
  #         except Exception as err:
  #             print("Failed to upload %s\n%s" % (file, err))

  # print("Finished upload.")


