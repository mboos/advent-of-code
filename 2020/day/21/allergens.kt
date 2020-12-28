/**
 * Solution to https://adventofcode.com/2020/day/21
 */

import java.io.File

fun main(args: Array<String>) {
  var input: String = args[0]
  var potentialAllergens = mutableMapOf<String, MutableSet<String>>()
  var allIngredients = mutableListOf<String>()
  var pattern: Regex = Regex("((\\w+ )+)\\(contains (\\w+(, \\w+)*)\\)\n?")
  File(input).forEachLine { line ->
    var match = pattern.matchEntire(line)
    var ingredients = match!!.groupValues[1].split(" ").filter { it.isNotBlank() }
    allIngredients.addAll(ingredients)
    match.groupValues[3].split(", ").forEach { element ->
      if (element.isNotBlank()) {
        if (element in potentialAllergens) {
          potentialAllergens[element] = potentialAllergens[element]!!.intersect(ingredients) as MutableSet<String>
        } else {
          potentialAllergens[element] = ingredients.toMutableSet()
        }
      }
    }
  }
  
  var allPotentialIngredients = mutableSetOf<String>()
  potentialAllergens.values.forEach { ingredients ->
    allPotentialIngredients.addAll(ingredients)
  }

  var safeIngredients = 0
  allIngredients.forEach { ingredient -> 
    if (!allPotentialIngredients.contains(ingredient)) {
      safeIngredients += 1
    }
  }
  println("Safe ingredients: ${safeIngredients}")

  val foundIngredients = mutableSetOf<String>()
  val foundAllergens = mutableMapOf<String,String>()
  var unmatchedAllergens = true
  while (unmatchedAllergens) {
    unmatchedAllergens = false
    potentialAllergens.forEach { allergen, ingredients ->
      if (!(allergen in foundAllergens)) {
	unmatchedAllergens = true
        if (potentialAllergens[allergen]!!.size == 1) {
	  foundIngredients.addAll(ingredients)
	  foundAllergens[allergen] = ingredients.first()
	} else {
	  potentialAllergens[allergen]!!.removeAll(foundIngredients)
	}
      }
    }
  }

  println("Ingredients: ${foundAllergens.toSortedMap().values.joinTo(StringBuffer(""), ",").toString()}")
}
