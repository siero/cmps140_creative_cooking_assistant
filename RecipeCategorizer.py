from collections import defaultdict
from wordlists import list_of_adjectivals
from ingredient_cuisine_mapping import ingredient_cuisine_mapping


def get_cuisine(words):
    """
    Given an array of words, return a dictionary whose keys are cuisines
    associated with this recipe and whose values are frequencies measuring
    occurrences.

    >>> get_cuisine(["Apple Pie Spice", "Prosciutto", "black pepper"])
    defaultdict(<type 'int'>, {'Italian': 1})
    >>> get_cuisine(["Apple", "Prosciutto", "Pasta", "Stuffed Chicken Breast",
    ...              "Israeli", "American"])
    defaultdict(<type 'int'>, {'Israeli': 1, 'American': 1, 'Italian': 2})
    """
    cuisines = defaultdict(int)  # Maps cuisine to frequency of occurrence
    for word in words:
        #Check for nationality adjectives like "American" or "Japanese"
        if word in list_of_adjectivals:
            cuisines[word] += 1
        # Check for cuisines strongly associated with certain ingredients
        if word in ingredient_cuisine_mapping:
            for cuisine in ingredient_cuisine_mapping[word]:
                cuisines[cuisine] += 1
    return cuisines
