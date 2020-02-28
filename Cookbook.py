from enum import IntEnum

class Products(IntEnum):
    """ Enumeration of all the different product types """
    wood = 0
    ore = 1
    steel = 2
    shovel = 3

# Adjacency matrix containing ingredients
_ingredients = [[0 for i in range(len(Products))] for j in range(len(Products))]

def getIngredients(product):
    """ Returns an array mapping between ingredient type and the quantity in product. """
    return _ingredients[product]

def getIngredientQuantity(product,ingredient):
    """ Returns the quantity of the ingredient used to make the product. """
    return _ingredients[product][ingredient]
    
def _set(product,ingredient,value):
    _ingredients[product][ingredient] = value

# -----------------------------------------------------------------------------------

# Setup the material dependencies
_set(Products.steel,Products.ore,4)
_set(Products.shovel,Products.steel,2)
_set(Products.shovel,Products.wood,2)
