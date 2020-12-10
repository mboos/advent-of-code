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


class Node:
  def __init__(self, value, left=None, right=None):
    self.value = value
    self.left = left
    self.right = right
    if left:
      left.right = self
    if right:
      right.left = self

class SortedList:
  def __init__(self):
    self.start = None
    self.end = None

  def insert(self, value):
    if not self.start:
      self.start = Node(value)
      self.end = self.start
      return
    if value > self.end.value:
      self.end = Node(value, left=self.end)
      return
    right = self.end
    left = right.left
    while right:
      if not left:
        self.start = Node(value, right=right)
        return
      if value > left.value and value <= right.value:
        Node(value, left=left, right=right)
        return
      right = left
      left = left.left

  def remove(self, value):
    node = self.start
    while node:
      if node.value == value:
        if node == self.start:
          self.start = node.right
          self.start.left = None
        elif node == self.end:
          self.end = node.left
          self.end.right = None  # making assumption that list will always have 25 once removals begin
        else:
          node.left.right = node.right
          node.right.left = node.left
        return
      node = node.right

  def is_sum_of_two(self, target_value):
    first = self.start
    last = self.end
    while first != last:
      sum_of_two = first.value + last.value
      if sum_of_two == target_value:
        return True
      elif sum_of_two > target_value:
        last = last.left
      else:
        first = first.right
    return False

  def sum(self):
    node = self.start
    total = 0
    while node:
      total += node.value
      node = node.right
    return total


def main(argv):
  if len(argv) > 2:
    raise app.UsageError('Too many command-line arguments.')
  with open(FLAGS.input) as fp:
    numbers = list(map(int, fp))
  last_25 = SortedList()
  for num in numbers[:25]:
    last_25.insert(num)
  for index in range(25, len(numbers)):
    if not last_25.is_sum_of_two(numbers[index]):
      found_sum = numbers[index]
      print(f'First number that isn\'t a sum of two: {found_sum}')
      break
    last_25.remove(numbers[index-25])
    last_25.insert(numbers[index])

  for index, start_num in enumerate(numbers):
    weakness_list = SortedList()
    weakness_list.insert(start_num)
    for next_num in numbers[index+1:]:
      weakness_list.insert(next_num)
      if weakness_list.sum() == found_sum:
        answer = weakness_list.start.value + weakness_list.end.value
        print(f'Sum of smallest and largest: {answer}')
        return


if __name__ == '__main__':
  app.run(main)

