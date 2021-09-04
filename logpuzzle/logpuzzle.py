#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""

  hostname = filename.split('_')[1]
  with open(filename) as f:
    text = f.read()
  matches = re.findall(r'GET (\S+jpg) HTTP', text)  # find all jpg paths
  nodups = list(set(matches))  # Remove duplicates
  urls = []
  for item in nodups:
    if '-' in item:
      urls.append(item)

  return ['http://' + hostname + path for path in urls]


def chck_dir_create(dest_dir):
  if dest_dir[0] is '~':
    path = os.path.expanduser("~") + dest_dir.replace('~', '')
  if not os.path.exists(path):
    if raw_input('Should I create the dir? (y/n): ') == 'y':
      os.makedirs(path)
      return path
    else:
      print dest_dir + ' Does not exist. Aborting...'
      sys.exit(1)
  else:
    return path


def alphanum_sorted_nicely(l):
  """ Sorts the given iterable in the way that is expected.

      Required arguments:
      l -- The iterable to be sorted.

      """
  convert = lambda text: int(text) if text.isdigit() else text
  alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
  return sorted(l, key=alphanum_key)


def sort_img_urls_nicely(urls):
  tl = []
  final = []
  for u in urls:
    l = u.split('/')
    s = l[len(l)-1].split('-')
    tl.append(s[len(s)-1])
    # print re.search(r'(\S+)\.jpg', l[len(l)-1]).group(1)
  # print '\n'.join(sorted(tl))
  for piece in sorted(tl):
    for ur in urls:
      if piece in ur:
        # print piece + 'in... ' + ur
        final.append(ur)
  # print '\n'.join(final)

  # sys.exit(0)
  return final


def create_img_index_html(dest_dir):
  path = chck_dir_create(dest_dir)
  img_tags = ''
  for img_file in alphanum_sorted_nicely(os.listdir(path)):
    img_tags += '<img src=\"' + path + '/' + img_file + '\">'
  with open(path + '/index.html', 'w') as f:
    f.write('<verbatim>\n<html>\n<body>\n' + img_tags + '\n</body>\n</html>')
  print path + '/index.html file created!'


def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  count = 0
  # Check directory exists and expand path
  path = chck_dir_create(dest_dir)
  srtd_img_urls = sort_img_urls_nicely(img_urls)
  for image_url in srtd_img_urls:
    if not os.path.exists(path + '/img' + str(count)):
      urllib.urlretrieve(image_url, path + '/img' + str(count))
      print 'Retrieving... ' + image_url
    count += 1
  create_img_index_html(dest_dir)


def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
