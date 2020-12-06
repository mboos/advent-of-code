# Lint as: python3
"""Finds the highest boarding pass number
Solution to part 1 of https://adventofcode.com/2020/day/5
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_string("input", None, "Input file.")

flags.mark_flag_as_required("input")



def main(argv):
  if len(argv) > 2:
    raise app.UsageError('Too many command-line arguments.')
  highest = -1
  with open(FLAGS.input) as fp:
    for line in fp:
      seat = 0
      for char in line:
        if char in ['F', 'L']:
          r = 0
        elif char in ['B', 'R']:
          r = 1
        else:
          continue
        seat = (seat << 1) + r
      if seat > highest:
        highest = seat
  print(highest)


if __name__ == '__main__':
  app.run(main)

