// Solution to https://adventofcode.com/2020/day/24
import Foundation

let inputFileURL = URL(fileURLWithPath: CommandLine.arguments[1])
var inputString = try String(contentsOf: inputFileURL)
let instructions = inputString.split(separator: "\n").map{ String($0) }

/*
 \ / \ / \ /
  | A | B |
 / \ / \ / \
| F | * | C |
 \ / \ / \ /
  | E | D |
 / \ / \ / \
 
  -1 0 1
-1 A B
 0 F * C
 1   E D

NW = (-1,-1)
NE = (0, -1)
W = (-1, 0)
E = (1, 0)
SW = (0, 1)
SE = (1, 1)
*/

struct Coordinates : Hashable {
    let x: Int
    let y: Int

    init(_ x: Int, _ y: Int) {
        self.x = x
        self.y = y
    }
}

let tileDirections = ["nw": Coordinates(-1, -1),
                      "ne": Coordinates(0, -1),
                      "w": Coordinates(-1, 0),
                      "e": Coordinates(1, 0),
                      "sw": Coordinates(0, 1),
                      "se": Coordinates(1, 1)]

let pattern = "(s|n)?(e|w)"
let regex = try NSRegularExpression(pattern: pattern, options: [])
let coordinates: [Coordinates] = instructions.map { 
    (directionString) -> (Coordinates) in
    let range = NSMakeRange(0, directionString.length)
    var x = 0, y = 0
    regex.enumerateMatches(in: directionString,
                           options: [],
                           range: range) { (match, _, stop) in
        guard let match = match else { return }
        if let range = Range(match.range, in: directionString) {
            let direction = String(directionString[range])
            let delta = tileDirections[direction]!
            x += delta.x
            y += delta.y
        }
    }
    return Coordinates(x, y)
}
var blackTiles = Set<Coordinates>()
coordinates.forEach { coord in 
    if blackTiles.contains(coord) {
        blackTiles.remove(coord)
    } else {
        blackTiles.insert(coord)
    }
}

print("Number of black tiles: \(blackTiles.count)")

func getNeighbours(tile: Coordinates) -> [Coordinates] {
    var neighbours = [Coordinates]()
    for (_, delta) in tileDirections {
        neighbours.append(Coordinates(tile.x + delta.x, tile.y + delta.y))
    }
    return neighbours
}

func countBlackNeighbours(tile: Coordinates, blackTiles: Set<Coordinates>) -> Int {
    var count = 0
    for neighbour in getNeighbours(tile: tile) {
        if blackTiles.contains(neighbour) {
            count += 1
        }  
    }
    return count
}

for _ in 1...100 {
    var toWhite = Set<Coordinates>()
    var toBlack = Set<Coordinates>()
    for tile in blackTiles {        
        let blackNeighbours = countBlackNeighbours(tile: tile, 
                                                   blackTiles:blackTiles)
        if blackNeighbours == 0 || blackNeighbours > 2 {
            toWhite.insert(tile)
        }
        for neighbour in getNeighbours(tile: tile) {
            if !blackTiles.contains(neighbour) {
                let blackNeighbours = countBlackNeighbours(tile: neighbour, 
                                                           blackTiles:blackTiles)
                if blackNeighbours == 2 {
                    toBlack.insert(neighbour)
                }
            }
        }
    }
    blackTiles.formUnion(toBlack)
    blackTiles.subtract(toWhite)
}

print("Number of black tiles after 100 days: \(blackTiles.count)")