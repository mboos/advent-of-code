# Lint as: python3
"""Counts "valid" passports
Solution to part 1 of https://adventofcode.com/2020/day/4
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_string("input", None, "Input file.")

flags.mark_flag_as_required("input")


# byr (Birth Year)
# iyr (Issue Year)
# eyr (Expiration Year)
# hgt (Height)
# hcl (Hair Color)
# ecl (Eye Color)
# pid (Passport ID)

FIELDS = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid')


def main(argv):
  if len(argv) > 2:
    raise app.UsageError('Too many command-line arguments.')
  count = 0
  records = []
  current = {}
  with open(FLAGS.input) as fp:
    for line in fp:
      if not line.strip():
        records.append(current)
        current = {}
        continue
      for token in line.split():
        key, value = token.split(':')
        current[key] = value
    if current:
      records.append(current)
    for r in records:
      if all([f in r for f in FIELDS]):
        count += 1
  print(count)


if __name__ == '__main__':
  app.run(main)

