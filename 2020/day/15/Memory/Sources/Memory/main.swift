// Solution to https://adventofcode.com/2020/day/15
import Foundation

//var input = [19,0,5,1,10,13]
let inputFileURL = URL(fileURLWithPath: CommandLine.arguments[1])
var inputString = try String(contentsOf: inputFileURL)
inputString = inputString.trimmingCharacters(in: .whitespacesAndNewlines)
let input = inputString.split(separator: ",").compactMap { Int($0) } 

func findNumber(input: [Int], target: Int) -> Int {
  var lastOccurrences: [Int:Int] = [:]
  for (index, number) in input.dropLast().enumerated() {
    lastOccurrences[number] = index
  }

  var index = input.count - 1
  var previousNumber = input.last!
  var currentNumber: Int
  while index < target-1 {
    if let lastIndex = lastOccurrences[previousNumber] {
      currentNumber = index - lastIndex 
    } else {
      currentNumber = 0
    }
    lastOccurrences[previousNumber] = index
    index += 1
    previousNumber = currentNumber
  }
  return previousNumber
}

print("Number 2020: \(findNumber(input: input, target: 2020))")
print("Number 30000000: \(findNumber(input: input, target: 30000000))")


