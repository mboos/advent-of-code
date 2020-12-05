# Lint as: python3
"""Counts "valid" passports
Solution to part 2 of https://adventofcode.com/2020/day/4
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re
from collections import defaultdict

from absl import app
from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_string("input", None, "Input file.")

flags.mark_flag_as_required("input")


# byr (Birth Year) - four digits; at least 1920 and at most 2002.
# iyr (Issue Year) - four digits; at least 2010 and at most 2020.
# eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
# hgt (Height) - a number followed by either cm or in:
#     If cm, the number must be at least 150 and at most 193.
#     If in, the number must be at least 59 and at most 76.
# hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
# ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
# pid (Passport ID) - a nine-digit number, including leading zeroes.
# cid (Country ID) - ignored, missing or not.

def validate_byr(value):
  if not re.fullmatch(r'[0-9]{4}', value):
    return False
  v = int(value)
  return v >= 1920 and v <= 2002

def validate_iyr(value):
  if not re.fullmatch(r'20[0-9]{2}', value):
    return False
  v = int(value)
  return v >= 2010 and v <= 2020

def validate_eyr(value):
  if not re.fullmatch(r'20[0-9]{2}', value):
    return False
  v = int(value)
  return v >= 2020 and v <= 2030

def validate_hgt(value):
  if re.fullmatch(r'\d+cm', value):
    cm = int(value[:-2])
    return cm >= 150 and cm <= 193
  if re.fullmatch(r'\d+in', value):
    inches = int(value[:-2])
    return inches >= 59 and inches <= 76

def validate_hcl(value):
  return re.fullmatch(r'#[0123456789abcdef]{6}', value)

def validate_ecl(value):
  return value in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

def validate_pid(value):
  return re.fullmatch(r'[0-9]{9}', value)

def validate_cid(value):
  return True

FIELDS = {
    'byr': validate_byr,
    'iyr': validate_iyr,
    'eyr': validate_eyr,
    'hgt': validate_hgt,
    'hcl': validate_hcl,
    'ecl': validate_ecl,
    'pid': validate_pid,
}


def main(argv):
  if len(argv) > 2:
    raise app.UsageError('Too many command-line arguments.')
  count = 0
  records = []
  current = defaultdict(list)
  with open(FLAGS.input) as fp:
    for line in fp:
      if not line.strip():
        records.append(current)
        current = defaultdict(list)
        continue
      for token in line.split():
        key, value = token.split(':')
        current[key].append(value)
    if current:
      records.append(current)
    for r in records:
      if all([len(r[f]) == 1 and validator(r[f][0]) for f, validator in FIELDS.items()]):
        count += 1
  print(count)


if __name__ == '__main__':
  app.run(main)

