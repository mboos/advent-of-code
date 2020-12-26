// Solution to https://adventofcode.com/2020/day/25
import Foundation

let inputFileURL = URL(fileURLWithPath: CommandLine.arguments[1])
var inputString = try String(contentsOf: inputFileURL)
let instructions = inputString.split(separator: "\n")
let cardCode = Int(String(instructions[0]))!
let doorCode = Int(String(instructions[1]))!

let DIVIDING_NUMBER = 20201227

func findLoopSize(key: Int, subjectNumber: Int) -> Int {
    var loopSize = 0
    var value = 1
    while value != key {
        loopSize += 1
        value *= subjectNumber
        value = value % DIVIDING_NUMBER
    }
    return loopSize
}

func findEncryptionKey(subjectNumber: Int, loopSize: Int) -> Int {
    var value = 1
    for _ in 1...loopSize {
        value *= subjectNumber
        value = value % DIVIDING_NUMBER
    }
    return value
}

let cardLoopSize = findLoopSize(key: cardCode, subjectNumber: 7)
let doorLoopSize = findLoopSize(key: doorCode, subjectNumber: 7)

let encryptionKey = findEncryptionKey(subjectNumber: cardCode, loopSize: doorLoopSize)
let encryptionKey2 = findEncryptionKey(subjectNumber: doorCode, loopSize: cardLoopSize)

print("Encryption key: \(encryptionKey) \(encryptionKey2)")