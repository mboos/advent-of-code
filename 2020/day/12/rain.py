# Lint as: python3
"""
Solution to https://adventofcode.com/2020/day/12
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
from absl import flags
import math
import re

FLAGS = flags.FLAGS
flags.DEFINE_string("input", None, "Input file.")

flags.mark_flag_as_required("input")

direction_pattern = re.compile(r'(?P<type>[NSWELRF])(?P<amount>\d+)')


class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y)

  def __mul__(self, factor):
    return Point(self.x * factor, self.y * factor)


def read_direction(line):
  m = direction_pattern.match(line)
  instruction, amount = m.group('type', 'amount')
  return instruction, int(amount)


def main(argv):
  if len(argv) > 2:
    raise app.UsageError('Too many command-line arguments.')
  with open(FLAGS.input) as fp:
    directions = list(map(read_direction, fp))
  coordinate = Point(0, 0)
  orientation = 0
  cardinals = {
      'N': Point(0, 1),
      'S': Point(0, -1),
      'E': Point(1, 0),
      'W': Point(-1, 0),
  }
  for instruction, amount in directions:
    if instruction in cardinals:
      coordinate += cardinals[instruction] * amount
    elif instruction == 'L':
      orientation += amount
    elif instruction == 'R':
      orientation -= amount
    elif instruction == 'F':
      rads = math.radians(orientation)
      dx = math.cos(rads)
      dy = math.sin(rads)
      coordinate += Point(dx, dy) * amount
  print(f'Manhattan distance: {abs(coordinate.x) + abs(coordinate.y)}')

  coordinate = Point(0, 0)
  waypoint = Point(10, 1)
  for instruction, amount in directions:
    if instruction in cardinals:
      waypoint += cardinals[instruction] * amount
    elif instruction in 'LR':
      rads = math.radians(amount)
      c = math.cos(rads)
      if instruction == 'L':
        s = math.sin(rads)
      else:
        s = -math.sin(rads)
      wx = waypoint.x * c - waypoint.y * s
      wy = waypoint.x * s + waypoint.y * c
      waypoint = Point(wx, wy)
    elif instruction == 'F':
      coordinate += waypoint * amount
  print(f'Manhattan distance with waypoint: {abs(coordinate.x) + abs(coordinate.y)}')


if __name__ == '__main__':
  app.run(main)

