# Lint as: python3
"""Finds 2 expense items that sum to the target value and returns their product.
Solution to part 1 of https://adventofcode.com/2020/day/1
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re

from absl import app
from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_integer("target", 2020, "Target value")
flags.DEFINE_string("input", None, "Input file.")

flags.mark_flag_as_required("input")


pattern = re.compile(r"(?P<min>\d+)-(?P<max>\d+) (?P<letter>\w): (?P<password>\w+)")
def parse(line):
  m = re.match(pattern, line)
  return int(m.group('min')), int(m.group('max')), m.group('letter'), m.group('password')


def count(letter, password):
  c = 0
  for p in password:
    if p == letter:
      c += 1
  return c

def main(argv):
  if len(argv) > 2:
    raise app.UsageError('Too many command-line arguments.')
  with open(FLAGS.input) as fp:
    rows = list(map(parse, fp))
  valid = 0
  for fmin, fmax, letter, password in rows:
    c = count(letter, password)
    if fmin <= c and c <= fmax:
      valid += 1
  print(valid)


if __name__ == '__main__':
  app.run(main)

