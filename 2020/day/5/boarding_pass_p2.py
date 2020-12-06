# Lint as: python3
"""Finds the missing boarding pass number
Solution to part 2 of https://adventofcode.com/2020/day/5
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
  found_seats = set()
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
      found_seats.add(seat)
      if seat > highest:
        highest = seat
  print(f'Highest seat nubmer: {highest}')
  possible_seats = set(range(highest+1))
  for candidate in possible_seats - found_seats:
    if candidate + 1 in found_seats and candidate - 1 in found_seats:
      print(f'Found your seat: {candidate}')


if __name__ == '__main__':
  app.run(main)

