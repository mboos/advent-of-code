# Lint as: python3
"""Counts potential bag colour enclosures
Solution to part 1 of https://adventofcode.com/2020/day/7
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
from absl import flags

import re
from collections import defaultdict

FLAGS = flags.FLAGS
flags.DEFINE_string("input", None, "Input file.")

flags.mark_flag_as_required("input")


def main(argv):
  if len(argv) > 2:
    raise app.UsageError('Too many command-line arguments.')
  parents = defaultdict(list)
  children = defaultdict(list)
  parent_pattern = re.compile(r'(.+?) bags? contains?')
  child_pattern = re.compile(r'(\d+) (.+?) bags?')
  with open(FLAGS.input) as fp:
    for line in fp:
      parent_match = re.match(parent_pattern, line)
      parent = parent_match.groups()[0]
      for child_match in re.finditer(child_pattern, line):
        child = child_match.groups()[1]
        count = int(child_match.groups()[0])
        parents[child].append(parent)
        children[parent].append((child, count))
  matches = set()
  colour = 'shiny gold'
  stack = [colour]
  while stack:
    candidate = stack.pop()
    if candidate in matches:
      continue
    if candidate != colour:
      matches.add(candidate)
    stack.extend(parents[candidate])
  print(f'Number of bags you can use: {len(matches)}')
  requirements = -1 
  stack = [(colour, 1)]
  while stack:
    child, count = stack.pop()
    requirements += count
    stack.extend([(grandchild, gcount*count) for (grandchild, gcount) in children[child]])
  print(f'You need {requirements}')

if __name__ == '__main__':
  app.run(main)

