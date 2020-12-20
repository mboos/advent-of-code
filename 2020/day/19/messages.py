# Lint as: python3
"""
Solution to https://adventofcode.com/2020/day/19
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


string_pattern = re.compile(r'"(.+)"')


def assemble_regex(rules, number = '0', repeats=()):
  m = string_pattern.match(rules[number])
  if m:
    return m.group(1)
  expression = '('
  for rule in rules[number].split():
    if rule == '|':
      expression += '|'
    else:
      expression += assemble_regex(rules, rule, repeats)
  return expression + ')'


def check_pattern(rules, number, text):
  if not text:
    return False, [0,]
  m = string_pattern.match(rules[number])
  if m:
    return text.startswith(m.group(1)), [len(m.group(1)),]
  burned = False
  total_indices = []
  indices = [0]
  for rule in rules[number].split():
    if rule == '|':
      if not burned:
        total_indices += indices
      burned = False
      indices = [0]
    else:
      if burned:
        continue
      new_indices = []
      for index in indices:
        matches, deltas = check_pattern(rules, rule, text[index:])
        if matches:
          new_indices += [index + d for d in deltas]
      if not new_indices:
        burned = True
      indices = new_indices
  if not burned:
    total_indices += indices
  if not total_indices:
    return False, [0]
  if number == '0' and len(text) not in total_indices:
    return False, [0,]
  return True, total_indices


rule_pattern = re.compile(r'(\d+): ([^\n]+)')


def main(argv):
  if len(argv) > 2:
    raise app.UsageError('Too many command-line arguments.')
  rules = {}
  lines = []
  rule_section = True
  with open(FLAGS.input) as fp:
    for line in fp:
      if rule_section:
        if not line.strip():
          rule_section = False
          continue
        m = rule_pattern.match(line)
        rules[m.group(1)] = m.group(2)
      else:
        lines.append(line.strip())
  master_pattern = re.compile(assemble_regex(rules) + '$')
  count = 0
  count2 = 0
  for line in lines:
    matches0 = master_pattern.match(line) is not None
    if master_pattern.match(line):
      count += 1
    matches, _ = check_pattern(rules, '0', line)
    if matches:
      count2 += 1
  print(f'Lines that match rule 0: {count} {count2}')

  rules['8'] = '42 | 42 8'
  rules['11'] = '42 31 | 42 11 31'
  count = 0
  for line in lines:
    matches, _ = check_pattern(rules, '0', line)
    if matches:
      count += 1
  print(f'Lines that match rule 0 with adapted rules: {count}')



if __name__ == '__main__':
  app.run(main)

