# Lint as: python3
"""
Solution to https://adventofcode.com/2020/day/16
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
from absl import flags
from dataclasses import dataclass
import re

FLAGS = flags.FLAGS
flags.DEFINE_string("input", None, "Input file.")

flags.mark_flag_as_required("input")

rule_pattern = re.compile(r'(?P<name>.+): (?P<min1>\d+)-(?P<max1>\d+) or (?P<min2>\d+)-(?P<max2>\d+)')


@dataclass(frozen=True)
class Rule:
  name: str
  min1: int
  max1: int
  min2: int
  max2: int

  def validate_value(self, value: int) -> bool:
    return (self.min1 <= value and value <= self.max1) or (self.min2 <= value and value <= self.max2)

  def validate_ticket(self, values: [int]) -> bool:
    return any(map(self.validate_value, values))


def read_ticket(line):
  return list(map(int, line.split(',')))

def main(argv):
  if len(argv) > 2:
    raise app.UsageError('Too many command-line arguments.')
  read_section = 'rules'
  rules = []
  your_ticket = None
  nearby_tickets = []
  with open(FLAGS.input) as fp:
    for line in fp:
      if read_section == 'rules':
        if 'your ticket:' in line:
          read_section = 'your ticket'
          continue
        match = rule_pattern.match(line)
        if match:
          rules.append(
              Rule(
                  match.group('name'), 
                  int(match.group('min1')),
                  int(match.group('max1')),
                  int(match.group('min2')),
                  int(match.group('max2')),
              ))
      elif read_section == 'your ticket':
        if 'nearby tickets:' in line:
          read_section = 'nearby tickets'
          continue
        if line.strip():
          your_ticket = read_ticket(line)
      elif read_section == 'nearby tickets':
        nearby_tickets.append(read_ticket(line))
  error_rate = 0
  good_tickets = []
  for ticket in nearby_tickets:
    good = True
    for value in ticket:
      if not any(map(lambda r: r.validate_value(value), rules)):
        error_rate += value
        good = False
    if good:
      good_tickets.append(ticket)
  print(f'Ticket scanning error rate: {error_rate}')

  candidates = [set(rules) for r in rules]
  for ticket in good_tickets:
    for value, column_candidates in zip(ticket, candidates):
      for rule in tuple(column_candidates):
        if not rule.validate_value(value):
          column_candidates.remove(rule)
  # Like a sudoku, remove remaining candidates by process of elimination
  while not all(len(c) == 1 for c in candidates):
    for c in candidates:
      if len(c) == 1:
        rule = tuple(c)[0]
        for other in candidates:
          if other != c:
            other.discard(rule)
  candidates = [c.pop() for c in candidates]
  departure_values = 1
  for value, rule in zip(your_ticket, candidates):
    if rule.name.startswith('departure'):
      departure_values *= value
  print(f'Product of departure values {departure_values}')


if __name__ == '__main__':
  app.run(main)

