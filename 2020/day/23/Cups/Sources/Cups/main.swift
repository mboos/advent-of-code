import Foundation


class Node<T> {
  let value: T
  var next: Node<T>?

  init(value: T) {
    self.value = value
  }

  init(value: T, next: Node<T>) {
    self.value = value
    self.next = next
  }
}


func print_list(_ head: Node<Int>) {
  print(head.value, terminator: "")
  var node = head.next!
  while node.value != head.value {
    print(node.value, terminator: "")
    node = node.next!
  }
  print("")
}


let puzzleInput = CommandLine.arguments[1]
let puzzleNumbers: [Int] = puzzleInput.compactMap { Int(String($0)) } 

func partOne(_ puzzleNumbers: [Int]) {
  let maxValue = puzzleNumbers.max()!
  let minValue = puzzleNumbers.min()!
  var head = Node(value: puzzleNumbers.first!)
  var current = head
  puzzleNumbers.dropFirst(1).forEach {
    current.next = Node(value: $0, next: head)
    current = current.next!
  }

  var targetValue = 0
  for _ in 1...100 {
    let removed = head.next!
    head.next = head.next?.next?.next?.next
    targetValue = head.value
    repeat {
      targetValue = targetValue - 1
      if targetValue < minValue {
        targetValue = maxValue
      }
    } while removed.value == targetValue || removed.next?.value == targetValue || removed.next?.next?.value == targetValue
    var destination = head
    while destination.value != targetValue {
      destination = destination.next!
    }
    removed.next?.next?.next = destination.next
    destination.next = removed
    head = head.next!
  }

  var node = head
  while node.value != 1 {
    node = node.next!
  }
  var result = ""
  while node.next?.value != 1 {
    node = node.next!
    result += String(node.value)
  }
  print("Part one: \(result)")
}

partOne(puzzleNumbers)


func partTwo(_ puzzleNumbers: [Int]) {
  let maxValue      =  1000000
  let numiterations = 10000000
  let maxInput = puzzleNumbers.max()!
  let minValue = puzzleNumbers.min()!
  var lookup = Dictionary<Int, Node<Int>>(minimumCapacity: maxValue)
  var head = Node(value: puzzleNumbers.first!)
  lookup[head.value] = head
  var current = head
  puzzleNumbers.dropFirst(1).forEach {
    current.next = Node(value: $0, next: head)
    current = current.next!
    lookup[$0] = current
  }
  for value in (maxInput+1)...maxValue {
    current.next = Node(value: value, next: head)
    current = current.next!
    lookup[value] = current
  }

  var targetValue = 0
  for _ in 1...numiterations {
    let removed = head.next!
    head.next = head.next?.next?.next?.next
    targetValue = head.value
    repeat {
      targetValue = targetValue - 1
      if targetValue < minValue {
        targetValue = maxValue
      }
    } while removed.value == targetValue || removed.next?.value == targetValue || removed.next?.next?.value == targetValue
    let destination = lookup[targetValue]!
    removed.next?.next?.next = destination.next
    destination.next = removed
    head = head.next!
  }

  let one = lookup[1]!
  let result = one.next!.value * one.next!.next!.value
  print("Part two: \(result)")
}

partTwo(puzzleNumbers)
