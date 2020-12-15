/**
 * Solution to https://adventofcode.com/2020/day/13
 */

import java.io.File

fun gcf(a: Long, b: Long): Long {
  var tmp: Long
  var aa = a
  var bb = b
  while (bb != 0L) {
    tmp = aa % bb
    aa = bb
    bb = tmp
  }
  return aa
}

fun lcm(vals: List<Long>): Long {
  return vals.reduce{a, b -> a*b/gcf(a,b)}
}

fun main(args: Array<String>) {
  var input: String = args[0]
  var raw: String = File(input).readText()
  var secondLine: String = raw.split("\n")[1]

  // Part 1
  var desiredDepartureTime: Long = raw.split("\n")[0].toLong()
  var waitTime = Long.MAX_VALUE
  var bestRoute: Long = 0
  for (routeLabel in secondLine.split(",")) {
    if (routeLabel.equals("x")) {
      continue
    }
    var routeNum = routeLabel.toLong()
    var remainder = desiredDepartureTime % routeNum
    var potentialWaitTime: Long
    if (remainder > 0) {
      potentialWaitTime = routeNum - remainder
    } else {
      potentialWaitTime = 0
    }
    if (potentialWaitTime < waitTime) {
      waitTime = potentialWaitTime
      bestRoute = routeNum
    }
  }
  println("Product of route num and wait time: ${bestRoute * waitTime}")

  // Part 2
  var increment: Long
  var startTime = 0L
  while (true) {
    var failedYet: Boolean = false
    var goodNums: MutableList<Long> = ArrayList()
    for ((index, routeName) in secondLine.split(",").withIndex()) {
      if (routeName.equals("x")) {
        continue
      }
      var routeNum = routeName.toInt()
      if ((startTime + index) % routeNum != 0L) {
        failedYet = true
      } else {
        goodNums.add(routeNum.toLong())
      }
    }
    if (!failedYet) {
      break
    }
    increment = lcm(goodNums)
    startTime += increment
  }
  println("Earliest timestamp: ${startTime}")
}
