# Lint as: python3
"""
Solution to https://adventofcode.com/2020/day/17
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
from absl import flags
from collections import defaultdict

FLAGS = flags.FLAGS
flags.DEFINE_string("input", None, "Input file.")

flags.mark_flag_as_required("input")


def cycle(points):
  candidate_points = defaultdict(lambda: 0)
  next_points = set()
  for p in points:
    neighbour_points = [()]
    for coord in p:
      n1 = [n + (coord-1,) for n in neighbour_points]
      n2 = [n + (coord,) for n in neighbour_points]
      n3 = [n + (coord+1,) for n in neighbour_points]
      neighbour_points = n1 + n2 + n3
    count = 0
    for n in neighbour_points:
      if n == p:
        continue
      if n in points:
        count += 1
      else:
        candidate_points[n] += 1
    if count in [2, 3]:
      next_points.add(p)
  for p, count in candidate_points.items():
    if count == 3:
      next_points.add(p)
  return next_points


def read_grid(dimensions):
  coords = set()
  supplement_dims = (0,) * (dimensions - 2)
  with open(FLAGS.input) as fp:
    for y, line in enumerate(fp):
      for x, cube in enumerate(line.strip()):
        if cube == '#':
          coords.add((x, y) + supplement_dims)
  return coords


def main(argv):
  if len(argv) > 2:
    raise app.UsageError('Too many command-line arguments.')

  coords = read_grid(3)
  for _ in range(6):
    coords = cycle(coords)
  print(f'Active after 6 cycles in 3D: {len(coords)}')
  coords = read_grid(4)
  for _ in range(6):
    coords = cycle(coords)
  print(f'Active after 6 cycles in 4D: {len(coords)}')

if __name__ == '__main__':
  app.run(main)

