# Lint as: python3
"""
Solution to https://adventofcode.com/2020/day/11
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


def count_neighbours(seats, cx, cy):
  count = 0
  min_x = max(cx - 1, 0)
  max_x = min(cx + 2, len(seats[0]))
  min_y = max(cy - 1, 0)
  max_y = min(cy + 2, len(seats))
  for x in range(min_x, max_x):
    for y in range(min_y, max_y):
      if x != cx or y != cy:
        if seats[y][x] == '#':
          count += 1
  return count


def find_visible_neighbours(seats):
  dirx = -1, 0, 1, -1,  1, -1, 0, 1
  diry = -1, -1, -1, 0, 0, 1, 1, 1
  max_dist = max(len(seats), len(seats[0]))
  neighbours = []
  for y, row in enumerate(seats):
    neighbours.append([])
    for x, seat in enumerate(row):
      neighbours[-1].append([])
      for dx, dy in zip(dirx, diry):
        for d in range(1, max_dist):
          ax = x + d * dx
          ay = y + d * dy
          if ax < 0 or ax >= len(seats[0]):
            break
          if ay < 0 or ay >= len(seats):
            break
          if seats[ay][ax] != '.':
            neighbours[-1][-1].append((ax, ay))
            break
  return neighbours


def count_visible_neighbours(seats, neighbours, x, y):
  count = 0
  for nx, ny in neighbours[y][x]:
    if seats[ny][nx] == '#':
      count += 1
  return count


def print_seats(seats):
  for line in seats:
    print(''.join(line))
  print()

def main(argv):
  if len(argv) > 2:
    raise app.UsageError('Too many command-line arguments.')
  with open(FLAGS.input) as fp:
    seats = list(map(lambda s: list(str.strip(s)), fp))
  changes = True
  occupied = 0
  while changes:
    changes = set()
    for y, row in enumerate(seats):
      for x, seat in enumerate(row):
        neighbours = count_neighbours(seats, x, y)
        if seat == 'L' and neighbours == 0:
          changes.add((x, y, '#'))
          occupied += 1
        elif seat == '#' and neighbours >= 4:
          changes.add((x, y, 'L'))
          occupied -= 1
    for x, y, seat in changes:
      seats[y][x] = seat
    #print_seats(seats)
  print(f'Occupied seats: {occupied}')

  for y, row in enumerate(seats):
    for x, seat in enumerate(row):
      if seat != '.':
        seats[y][x] = 'L'
  visible_neighbours = find_visible_neighbours(seats)

  changes = True
  occupied = 0
  while changes:
    changes = set()
    for y, row in enumerate(seats):
      for x, seat in enumerate(row):
        neighbours = count_visible_neighbours(seats, visible_neighbours, x, y)
        if seat == 'L' and neighbours == 0:
          changes.add((x, y, '#'))
          occupied += 1
        elif seat == '#' and neighbours >= 5:
          changes.add((x, y, 'L'))
          occupied -= 1
    for x, y, seat in changes:
      seats[y][x] = seat
  print(f'Occupied seats in part 2: {occupied}')

if __name__ == '__main__':
  app.run(main)

