# Lint as: python3
"""Counts "valid" passports
Solution to part 1 of https://adventofcode.com/2020/day/4
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
from absl import flags

from functools import reduce

FLAGS = flags.FLAGS
flags.DEFINE_string("input", None, "Input file.")

flags.mark_flag_as_required("input")


def main(argv):
  if len(argv) > 2:
    raise app.UsageError('Too many command-line arguments.')
  any_count = 0
  all_count = 0
  with open(FLAGS.input) as fp:
    any_yes_answers = set()
    yes_answers = []
    for line in fp:
      if not line.strip():
        all_count += len(reduce(set.intersection, yes_answers))
        any_count += len(reduce(set.union, yes_answers))
        yes_answers = []
        continue
      yes_answers.append(set(line.strip()))

    all_count += len(reduce(set.intersection, yes_answers))
    any_count += len(reduce(set.union, yes_answers))
  print(f'Count of yes answers per group part 1: {any_count}')
  print(f'Count of yes answers per group part 2: {all_count}')


if __name__ == '__main__':
  app.run(main)

