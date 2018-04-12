import pathlib
import dropbox
import os

dropbox_token = str(os.getenv('DROPBOX_TOKEN'))


def uploadToDrobpox(filename, input_dir, output_dir):

  folder = pathlib.Path(input_dir)    # located in this folder
  filename = filename         # file name
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


