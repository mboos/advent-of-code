# Lint as: python3
"""
Solution to https://adventofcode.com/2020/day/17
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


class Operator:
  def __init__(self, left, op, right):
    self.left = left
    self.op = op
    self.right = right

  def eval(self):
    if self.op == '+':
      return self.left.eval() + self.right.eval()
    elif self.op == '*':
      return self.left.eval() * self.right.eval()

  def __repr__(self):
    return '(' + repr(self.left) + self.op + repr(self.right) + ')'


class Value:
  def __init__(self, val):
    self.val = val

  def eval(self):
    return self.val

  def __repr__(self):
    return str(self.eval())


num_pattern = re.compile(r'\d+')


def findParenthesesMatch(text):
  num_match = num_pattern.match(text)
  if num_match:
    return len(num_match.group(0))
  assert text[0] == '('
  count = 1
  index = 1
  while count > 0:
    if text[index] == '(':
      count += 1
    elif text[index] == ')':
      count -= 1
    index += 1
  return index


def parseEquation(text):
  currentNode = None
  while text:
    num_match = num_pattern.match(text)
    if num_match:
      val_string = num_match.group(0)
      currentNode = Value(int(val_string))
      text = text[len(val_string):]
    elif text.startswith(' + ') or text.startswith(' * '):
      op = text[1]
      text = text[3:]
      next_node_length = findParenthesesMatch(text)
      currentNode = Operator(currentNode, op, parseEquation(text[:next_node_length]))
      text = text[next_node_length:]
    elif text.startswith('('):
      next_node_length = findParenthesesMatch(text)
      currentNode = parseEquation(text[1:next_node_length-1])
      text = text[next_node_length:]
  assert currentNode is not None
  return currentNode


def parseEquation2(text):
  currentNode = None
  while text:
    num_match = num_pattern.match(text)
    if num_match:
      val_string = num_match.group(0)
      currentNode = Value(int(val_string))
      text = text[len(val_string):]
    elif text.startswith(' + '):
      text = text[3:]
      next_node_length = findParenthesesMatch(text)
      currentNode = Operator(currentNode, '+', parseEquation2(text[:next_node_length]))
      text = text[next_node_length:]
    elif text.startswith(' * '):
      text = text[3:]
      return Operator(currentNode, '*', parseEquation2(text))
    elif text.startswith('('):
      next_node_length = findParenthesesMatch(text)
      currentNode = parseEquation2(text[1:next_node_length-1])
      text = text[next_node_length:]
  assert currentNode is not None
  return currentNode


def main(argv):
  if len(argv) > 2:
    raise app.UsageError('Too many command-line arguments.')
  total = 0
  total2 = 0
  with open(FLAGS.input) as fp:
    for line in fp:
      total += parseEquation(line.strip()).eval()
      total2 += parseEquation2(line.strip()).eval()
  print(f'Sum of lines: {total}')
  print(f'Sum of lines with addition first: {total2}')

if __name__ == '__main__':
  app.run(main)

