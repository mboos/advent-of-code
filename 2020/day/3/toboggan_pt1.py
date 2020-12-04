# Lint as: python3
"""Counts potential tree collisions
Solution to part 1 of https://adventofcode.com/2020/day/3
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re

from absl import app
from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_string("input", None, "Input file.")

flags.mark_flag_as_required("input")


def main(argv):
  if len(argv) > 2:
    raise app.UsageError('Too many command-line arguments.')
  factor = 3
  count = 0
  with open(FLAGS.input) as fp:
    for y, line in enumerate(fp):
      x = (y * factor) % (len(line)-1)
      if line[x] == '#':
        count += 1
  print(count)


if __name__ == '__main__':
  app.run(main)

