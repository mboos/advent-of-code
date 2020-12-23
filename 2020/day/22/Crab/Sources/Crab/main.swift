import Foundation


struct Queue<T: Hashable> : Hashable {
  private var nqStack = [T]()
  private var dqStack = [T]()

  var isEmpty: Bool {
    return dqStack.isEmpty && nqStack.isEmpty
  }

  var count: Int {
    return dqStack.count + nqStack.count
  }

  mutating func enqueue(_ element: T) {
    nqStack.append(element)
  }

  mutating func dequeue() -> T? {
    if dqStack.isEmpty {
      dqStack = nqStack.reversed()
      nqStack.removeAll()
    }
    return dqStack.popLast()
  }

  func toArray() -> [T] {
    return dqStack.reversed() + nqStack
  }

  static func == (lhs: Queue<T>, rhs: Queue<T>) -> Bool {
    let lhsList = lhs.dqStack.reversed() + lhs.nqStack
    let rhsList = rhs.dqStack.reversed() + rhs.nqStack
    return lhsList.elementsEqual(rhsList)
  }

  func hash(into hasher: inout Hasher) {
    for t in dqStack.reversed() {
      hasher.combine(t)
    }
    for t in nqStack {
      hasher.combine(t)
    }
  }

  func subQueue(count num: Int) -> Queue<T> {
    var newQ = Queue<T>()
    var tempDQ = dqStack
    while newQ.count < num {
      if tempDQ.isEmpty {
        tempDQ = nqStack.reversed()
      }
      newQ.enqueue(tempDQ.popLast()!)
    }
    return newQ
  }
}

struct Game: Hashable {
  let players: (Queue<Int>, Queue<Int>)

  static func == (lhs: Game, rhs: Game) -> Bool {
    let (leftPlayerOne, leftPlayerTwo) = lhs.players
    let (rightPlayerOne, rightPlayerTwo) = rhs.players
    return leftPlayerOne == rightPlayerOne && leftPlayerTwo == rightPlayerTwo
  }

  func hash(into hasher: inout Hasher) {
    let (one, two) = players
    hasher.combine(one)
    hasher.combine(two)
  }
}

let inputFileURL = URL(fileURLWithPath: CommandLine.arguments[1])
let inputString = try String(contentsOf: inputFileURL)

var cardsOne = Queue<Int>()
var cardsTwo = Queue<Int>()
var currentPlayer = 1
for line in inputString.split(separator: "\n") {
  if line == "Player 1:" {
    currentPlayer = 1
    continue
  } 
  if line == "Player 2:" {
    currentPlayer = 2
    continue
  }
  if currentPlayer == 1 {
    cardsOne.enqueue(Int(String(line))!)
  }
  else {
    cardsTwo.enqueue(Int(String(line))!)
  }
}

var playerOne = cardsOne
var playerTwo = cardsTwo

while !playerOne.isEmpty && !playerTwo.isEmpty {
  let cardOne = playerOne.dequeue()!
  let cardTwo = playerTwo.dequeue()!
  if cardOne > cardTwo {
    playerOne.enqueue(cardOne)
    playerOne.enqueue(cardTwo)
  } 
  else if cardOne < cardTwo {
    playerTwo.enqueue(cardTwo)
    playerTwo.enqueue(cardOne)
  }
}

var winner = playerOne
if playerOne.isEmpty {
  winner = playerTwo
}

func score(winner: Queue<Int>) -> Int {
  var cards = [Int]()
  var player = winner
  while !player.isEmpty {
    cards.append(player.dequeue()!)
  }
  cards.append(0)
  var total = 0
  for (num, card) in cards.reversed().enumerated() {
    total += num * card
  }
  return total
}

print("Winning player's score: \(score(winner: winner))") 


var previousGames = Dictionary<Game, (Int, Queue<Int>)>()


func recursiveCombat(game: Game) -> (Int, Queue<Int>) {
  var (playerOne, playerTwo) = game.players
  var previousRounds = Set<Game>()
  var roundWinner = 0
  var roundNum = 0

  while !playerOne.isEmpty && !playerTwo.isEmpty {
    roundNum += 1
    let currentRound = Game(players: (playerOne, playerTwo))
    if let (score, cards) = previousGames[game] {
      for round in previousRounds {
        previousGames[round] = (score, cards)
      }
      return (score, cards)
    }
    if previousRounds.contains(currentRound) {
      for round in previousRounds {
        previousGames[round] = (1, playerOne)
      }
      return (1, playerOne)
    }
    previousRounds.insert(currentRound)
    let cardOne = playerOne.dequeue()!
    let cardTwo = playerTwo.dequeue()!    
    if cardOne <= playerOne.count && cardTwo <= playerTwo.count {
      (roundWinner, _) = recursiveCombat(game: Game(players:(playerOne.subQueue(count: cardOne), playerTwo.subQueue(count: cardTwo))))
    } 
    else if cardOne > cardTwo {
      roundWinner = 1
    }
    else if cardTwo > cardOne {
      roundWinner = 2
    }

    if roundWinner == 1 {
      playerOne.enqueue(cardOne)
      playerOne.enqueue(cardTwo)
    }
    else {
      playerTwo.enqueue(cardTwo)
      playerTwo.enqueue(cardOne)
    }
  }
  if playerTwo.isEmpty {
    for round in previousRounds {
      previousGames[round] = (1, playerOne)
    }
    return (1, playerOne)
  }
  else {
    for round in previousRounds {
      previousGames[round] = (2, playerTwo)
    }
    return (2, playerTwo)
  }
}

var (newWinner, winningCards) = recursiveCombat(game: Game(players: (cardsOne, cardsTwo)))

print("Winning recursive player's score: \(score(winner: winningCards))")
