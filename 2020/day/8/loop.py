# Lint as: python3
"""Find value of accumulator at start of loop
Solution to https://adventofcode.com/2020/day/8
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_string("input", None, "Input file.")

flags.mark_flag_as_required("input")


def process_code(the_code):
  line = 0
  accumulator = 0
  visited = set()
  while line < len(the_code):
    if line in visited:
      return accumulator, False
    visited.add(line)
    op, num = the_code[line]
    num = int(num)
    if op == 'jmp':
      line += num
      continue
    elif op == 'acc':
      accumulator += num
    line += 1
  return accumulator, True


def main(argv):
  if len(argv) > 2:
    raise app.UsageError('Too many command-line arguments.')
  with open(FLAGS.input) as fp:
    the_code = [line.split() for line in fp]
  accumulator, _ = process_code(the_code)
  print(f'Accumulator value at beginning of loop: {accumulator}')
  for line in range(len(the_code)):  # A terrible, unpythonic hack
    op, num = the_code[line]
    if op == 'jmp':
      the_code[line] = 'nop', num
      acc, terminates = process_code(the_code)
      if terminates:
        print(f'Accumulator value at end of fixed code {acc}')
        return
      the_code[line] = 'jmp', num
    elif op == 'nop':
      the_code[line] = 'jmp', num
      acc, terminates = process_code(the_code)
      if terminates:
        print(f'Accumulator value at end of fixed code {acc}')
        return
      the_code[line] = 'nop', num


if __name__ == '__main__':
  app.run(main)

