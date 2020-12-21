# Lint as: python3
"""
Solution to https://adventofcode.com/2020/day/10
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
from absl import flags
from collections import Counter

FLAGS = flags.FLAGS
flags.DEFINE_string("input", None, "Input file.")

flags.mark_flag_as_required("input")


def count_jumps(adapters):
  prev = 0
  diffs = []
  for current in adapters:
    diffs.append(current - prev)
    prev = current
  return Counter(diffs)


def count_paths(adapters):
  paths = [1]
  for index, current in enumerate(adapters[1:], 1):
    count = 0
    for backtrack in range(1, index+1):
      prev = adapters[index - backtrack]
      if current - prev > 3:
        break
      count += paths[index - backtrack]
    paths.append(count)
  return paths[-1]

def main(argv):
  if len(argv) > 2:
    raise app.UsageError('Too many command-line arguments.')
  with open(FLAGS.input) as fp:
    adapters = [0] + list(sorted(map(int, fp)))
  adapters.append(max(adapters) + 3)
  jumps = count_jumps(adapters)
  print(f'Product of 1-jolt and 3-jolt differences: {jumps[1] * jumps[3]}')
  paths = count_paths(adapters)
  print(f'Total number of combinations: {paths}')

if __name__ == '__main__':
  app.run(main)

