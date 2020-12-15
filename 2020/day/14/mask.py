# Lint as: python3
"""
Solution to https://adventofcode.com/2020/day/12
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
from absl import flags
import re

FLAGS = flags.FLAGS
flags.DEFINE_string("input", None, "Input file.")

flags.mark_flag_as_required("input")

mask_pattern = re.compile(r'mask = (?P<mask>.+)')
mem_pattern = re.compile(r'mem\[(?P<address>\d+)] = (?P<value>\d+)')


def main(argv):
  if len(argv) > 2:
    raise app.UsageError('Too many command-line arguments.')
  memory = {}
  mask = ''
  mask_mask = 0
  with open(FLAGS.input) as fp:
    for line in fp:
      match = mask_pattern.match(line)
      if match:
        mask = match.group('mask')
      else:
        match = mem_pattern.match(line)
        address = match.group('address')
        raw_value = int(match.group('value'))
        value = 0
        for i, ch in enumerate(reversed(mask)):
          bit = raw_value & 1
          if ch == 'X':
            value += bit << i
          elif ch == '1':
            value += 1 << i
          raw_value = raw_value >> 1
        memory[address] = value
  total = 0
  for key, value in memory.items():
    total += value
  print(f'Sum of values in memory: {total}')

  memory = {}
  with open(FLAGS.input) as fp:
    for line in fp:
      match = mask_pattern.match(line)
      if match:
        mask = match.group('mask')
      else:
        match = mem_pattern.match(line)
        raw_address = int(match.group('address'))
        value = int(match.group('value'))
        addresses = [0]
        for i, ch in enumerate(reversed(mask)):
          bit = raw_address & 1
          if ch == '1':
            addresses = [a + (1 << i) for a in addresses]
          elif ch == '0':
            addresses = [a + (bit << i) for a in addresses]
          else:
            addresses += [a + (1 << i) for a in addresses]
          raw_address = raw_address >> 1
        for address in addresses:
          memory[address] = value
  total = 0
  for key, value in memory.items():
    total += value
  print(f'Sum of values in memory: {total}')

if __name__ == '__main__':
  app.run(main)

