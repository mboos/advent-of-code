# Lint as: python3
"""Find the product of potential tree collisions
Solution to part 2 of https://adventofcode.com/2020/day/3
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
  slopes = (1,1), (3,1), (5,1), (7,1), (1,2)
  counts = []
  with open(FLAGS.input) as fp:
    lines = list(fp)
  for slopex, slopey in slopes:
    count = 0
    for y, line in enumerate(lines):
      if y % slopey != 0:
        continue
      x = int(y / slopey * slopex) % (len(line)-1)
      if line[x] == '#':
        count += 1
    counts.append(count)
  prod = 1
  print(counts)
  for c in counts:
    prod *= c
  print(prod)


if __name__ == '__main__':
  app.run(main)

