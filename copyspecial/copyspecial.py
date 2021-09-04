#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import commands

"""Copy Special exercise
"""

# get_special_paths(dir) -- returns a list of the absolute paths of the special files in the given directory
def get_special_paths(dir):
  flist = []
  filenames = os.listdir(dir)
  for filename in filenames:
    # print filename
    if re.search(r'__(\w+)__', filename):
      flist.append(os.path.abspath(os.path.join(dir, filename)))
  # print '\n'.join(flist)
  return flist

# copy_to(paths, dir) given a list of paths, copies those files into the given directory
def copy_to(paths, dir):
  # Get user home (optional)
  home = os.path.expanduser("~")
  # check dir exists
  if not os.path.isdir(home + dir):
    inpt = raw_input(dir + ' Does not exist. Should I create it? (y/N): ')
    if inpt == 'y':
      os.makedirs(home + dir)
    else:
      print '\nAborting...'
      sys.exit(0)
  for path in paths:
    shutil.copy(path, home + dir)


# zip_to(paths, zippath) given a list of paths, zip those files up into the given zipfile
def zip_to(paths, zippath):
  # command to run: zip -j zipfile <list all the files>
  # Build command
  cmd = 'zip -j ' + zippath
  for path in paths:
    cmd += ' ' + path
  # cmd = 'zip -j ' + zippath + ' ' + ' '.join(paths)
  print 'Command to run: ', cmd
  (status, output) = commands.getstatusoutput(cmd)
  if status:  ## Error case, print the command's output to stderr and exit
    sys.stderr.write(output)
    sys.exit(status)  # or sys.exit(1)
  print output

# Write functions and modify main() to call them


def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  tozip = ''
  if args[0] == '--tozip':
    tozip = args[1]
    del args[0:2]

  if len(args) == 0:
    print "error: must specify one or more dirs"
    sys.exit(1)

  # +++your code here+++
  # Call your functions
  if todir:
    for dir in args:
      copy_to(get_special_paths(dir), todir)

  if tozip:
    for dir in args:
      zip_to(get_special_paths(dir), tozip)


if __name__ == "__main__":
  main()
