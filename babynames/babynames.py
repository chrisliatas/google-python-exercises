#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re

"""Baby Names exercise

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 -Extract the year and print it
 -Extract the names and rank numbers and just print them
 -Get the names data into a dict and print it
 -Build the [year, 'name rank', ... ] list and print it
 -Fix main() to use the extract_names list
"""

def extract_names(filename):
  """
  Given a file name for baby.html, returns a list starting with the year string
  followed by the name-rank strings in alphabetical order.
  ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
  """
  names = []
  with open(filename) as f:
    doc = f.read()
  names += re.findall(r'Popularity in (\d+)', doc)
  #names.append(year.group(1))
  names_ranks = re.findall(r'<td>(\d+)</td><td>(\w+)</td><td>(\w+)', doc)
  d = {}
  for ranktup in names_ranks:
    d[ranktup[0]] = d.get(ranktup[0], []) + list(ranktup[1:])
  tl = []
  for k in d:
    tl.append(d[k][0] + ' ' + k)
    tl.append(d[k][1] + ' ' + k)
  return sorted(names + tl)


def remove_duplicates(names_list):
  new = []
  for entry in names_list[1:]:
    if not new:
      new.append(entry)
      continue
    name, rank = entry.split()
    if len(new) > 1:
      for idx, n in enumerate(new):
        if name in n:
          if int(rank) < int(n.split()[1]):
            new[idx] = entry
            break
          else:
            break
      else:
        new.append(entry)
    else:
      new.append(entry)
  new.insert(0, names_list[0])

  return new


def main():
  # This command-line parsing code is provided.
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]

  if not args:
    print 'usage: [--summaryfile] file [file ...]'
    sys.exit(1)

  # Notice the summary flag and remove it from args if it is present.
  summary = False
  if args[0] == '--summaryfile':
    summary = True
    del args[0]

  # For each filename, get the names, then either print the text output
  # or write it to a summary file
  for filename in args:
    text = '\n'.join(remove_duplicates(extract_names(filename))) + '\n'
    if summary:
      with open(filename + '.summary', 'w') as f:
        f.write(text)
    else:
      print text

if __name__ == '__main__':
  main()
  # l = extract_names('baby1990.html')
  # remove_duplicates(l)