# Lint as: python3
"""
Solution to https://adventofcode.com/2020/day/20
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
from absl import flags
from collections import defaultdict
import re

FLAGS = flags.FLAGS
flags.DEFINE_string("input", None, "Input file.")

flags.mark_flag_as_required("input")


def canonical_edge(edge):
  backwards = ''.join(reversed(edge))
  return min(edge, backwards)


def collect_edges(tiles):
  edge_to_tile_map = defaultdict(list)
  tile_to_edge_map = defaultdict(list)
  for num, tile in tiles.items():
    edges = []
    edges.append(canonical_edge(find_top_edge(tile)))
    edges.append(canonical_edge(find_right_edge(tile)))
    edges.append(canonical_edge(find_bottom_edge(tile)))
    edges.append(canonical_edge(find_left_edge(tile)))
    tile_to_edge_map[num] = edges
    for edge in edges:
      edge_to_tile_map[edge].append(num)
  return edge_to_tile_map, tile_to_edge_map


def rotate_cw(tile):
  new_tile = []
  for col in zip(*reversed(tile)):
    new_tile.append(''.join(col))
  return new_tile


def rotate_180(tile):
  return rotate_cw(rotate_cw(tile))


def rotate_ccw(tile):
  return rotate_cw(rotate_180(tile))


def flip_vertical(tile):
  return list(reversed(tile))


def flip_horizontal(tile):
  return [''.join(reversed(t)) for t in tile]


def find_top_edge(tile):
  return tile[0]


def find_left_edge(tile):
  return ''.join(t[0] for t in tile)


def find_bottom_edge(tile):
  return tile[-1]


def find_right_edge(tile):
  return ''.join(t[-1] for t in tile)


def build_image(tiles, start_corner, e2t, t2e):
  full_grid = []
  # rotate corner if necessary to be top-left
  current_tile = tiles[start_corner]
  tile_size = len(current_tile) - 2
  tile_num = start_corner
  row_num = start_corner
  edges = [len(e2t[edge]) for edge in t2e[start_corner]]
  if edges[0] == 1 and edges[1] == 1:
    current_tile = rotate_ccw(current_tile)
  elif edges[1] == 1 and edges[2] == 1:
    current_tile = rotate_180(current_tile)
  elif edges[2] == 1 and edges[3] == 1:
    current_tile = rotate_cw(current_tile)
  while current_tile:
    bottom_edge = find_bottom_edge(current_tile)
    full_grid.extend(list(line[1:-1]) for line in current_tile[1:-1])
    right_edge = find_right_edge(current_tile)
    while len(e2t[canonical_edge(right_edge)]) == 2:
      matches = e2t[canonical_edge(right_edge)]
      if matches[0] == tile_num:
        tile_num = matches[1]
      else:
        tile_num = matches[0]
      current_tile = tiles[tile_num]
      left_index = t2e[tile_num].index(canonical_edge(right_edge))
      if left_index == 0:
        current_tile = rotate_ccw(current_tile)
      elif left_index == 1:
        current_tile = rotate_180(current_tile)
      elif left_index == 2:
        current_tile = rotate_cw(current_tile)
      left_edge = find_left_edge(current_tile)
      if left_edge != right_edge:
        current_tile = flip_vertical(current_tile)
      right_edge = find_right_edge(current_tile)
      for row, addition in zip(full_grid[-tile_size:], current_tile[1:-1]):
        row.extend(addition[1:-1])
    matches = e2t[canonical_edge(bottom_edge)]
    if matches[0] == row_num:
      if len(matches) > 1:
        tile_num = matches[1]
      else:
        break
    else:
      tile_num = matches[0]
    row_num = tile_num
    current_tile = tiles[tile_num]
    top_index = t2e[tile_num].index(canonical_edge(bottom_edge))
    if top_index == 1:
      current_tile = rotate_ccw(current_tile)
    elif top_index == 2:
      current_tile = rotate_180(current_tile)
    elif top_index == 3:
      current_tile = rotate_cw(current_tile)
    top_edge = find_top_edge(current_tile)
    if top_edge != bottom_edge:
      current_tile = flip_horizontal(current_tile)
  full_grid = [''.join(line) for line in full_grid]
  return full_grid


new_tile_pattern = re.compile(r'Tile (\d+):')
monster = ['                  # ',
           '#    ##    ##    ###',
           ' #  #  #  #  #  #   ']
m_height = len(monster)
m_width = len(monster[0])
m_count = sum(sum(1 for c in l if c == '#') for l in monster)


def main(argv):
  if len(argv) > 2:
    raise app.UsageError('Too many command-line arguments.')
  tiles = {}
  current_tile = []
  tile_num = None
  with open(FLAGS.input) as fp:
    for line in fp:
      if tile_num is None:
        m = new_tile_pattern.match(line)
        tile_num = int(m.group(1))
        continue
      if not line.strip():
        tiles[tile_num] = current_tile
        current_tile = []
        tile_num = None
        continue
      current_tile.append(line.strip())
  edge_to_tile_map, tile_to_edge_map = collect_edges(tiles)
  corner_prod = 1
  for tile in tiles:
    outer_edges = sum(1 for edge in tile_to_edge_map[tile] if len(edge_to_tile_map[edge]) == 1)
    if outer_edges == 2:
      corner_prod *= tile
      last_corner = tile
  print(f'Product of corner tiles: {corner_prod}')
  full_grid = build_image(tiles, last_corner, edge_to_tile_map, tile_to_edge_map)
  # from pprint import pprint
  # pprint(full_grid)
  grids = [list(full_grid)]
  grids.append(rotate_cw(full_grid))
  grids.append(rotate_cw(grids[1]))
  grids.append(rotate_cw(grids[2]))
  grids.append(flip_horizontal(full_grid))
  grids.append(flip_vertical(full_grid))
  grids.append(flip_horizontal(grids[1]))
  grids.append(flip_vertical(grids[1]))
  for grid in grids:
    found = set()
    for row in range(len(grid) - m_height + 1):
      for col in range(len(grid) - m_width + 1):
        failed = False
        for g_line, m_line in zip(grid[row:], monster):
          for g_char, m_char in zip(g_line[col:], m_line):
            if m_char == '#' and g_char == '.':
              failed = True
              break
          if failed:
            break
        if not failed:
          found.add((row, col))
    if found:
      total = - len(found)*m_count
      for line in grid:
        for c in line:
          if c == '#':
            total += 1
      print(f'Water roughness: {total}')
      return


if __name__ == '__main__':
  app.run(main)

