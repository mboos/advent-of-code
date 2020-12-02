# Lint as: python3
"""Finds 3 expense items that sum to the target value and returns their product.

Solution to part 2 of https://adventofcode.com/2020/day/1
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_integer("target", 2020, "Target value")
flags.DEFINE_string("input", None, "Input file.")

flags.mark_flag_as_required("input")


def main(argv):
  if len(argv) > 3:
    raise app.UsageError('Too many command-line arguments.')
  target = FLAGS.target
  with open(FLAGS.input) as fp:
    values = sorted(map(int, fp))
  for i, low in enumerate(values[:-2]):
    first = i + 1
    last = len(values) - 1
    while first < last:
      vsum = low + values[first] + values[last]
      if vsum < target:
        first += 1
      elif vsum > target:
        last -= 1
      else:
        print(low*values[first]*values[last])
        break

if __name__ == '__main__':
  app.run(main)
