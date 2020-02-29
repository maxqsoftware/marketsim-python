from enum import IntEnum

class Products(IntEnum):
    """ Enumeration of all the different product types """
    helium = 0
    carbon = 1
    lead = 2
    iron = 3
    aluminum = 4
    titanium = 5
    copper = 6
    silver = 7
    gold = 8
    platinum = 9
    tungsten = 10
    water = 11
    methane = 12
    superConductor = 13
    carbonNanotubes = 14
    graphene = 15
    electronics = 16
    hullPlating = 17
    nanomedicine = 18
    miningEquipment = 19
    fertilizer = 20
    hydrogenFuelCell = 21
    nuclearFuelCell = 22
    solarCell = 23
    shieldGenerator = 24
    thrusters = 25
    fissionReactor = 26
    spacecraft = 27
    phosphorus = 28
    uranium = 29
    
    @staticmethod
    def names():
        namesList = []
        for product in Products:
            namesList.append(product.name)
        return namesList

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
_set(Products.hydrogenFuelCell,Products.water, 1)
_set(Products.hydrogenFuelCell,Products.electronics,5)
_set(Products.hydrogenFuelCell,Products.platinum,10)

_set(Products.miningEquipment, Products.tungsten, 5)
_set(Products.miningEquipment, Products.titanium, 5)
_set(Products.miningEquipment, Products.iron, 10)

_set(Products.superConductor, Products.helium, 10)

_set(Products.fertilizer, Products.phosphorus, 5)

_set(Products.carbonNanotubes, Products.carbon, 5)

_set(Products.graphene, Products.carbon, 5)

_set(Products.electronics, Products.graphene, 1)
_set(Products.electronics, Products.copper, 1)

_set(Products.hullPlating, Products.titanium, 10)
_set(Products.hullPlating, Products.aluminum, 10)

_set(Products.nuclearFuelCell, Products.uranium, 10)
_set(Products.nuclearFuelCell, Products.lead, 50)
_set(Products.nuclearFuelCell, Products.electronics, 50)

_set(Products.solarCell, Products.graphene, 10)

_set(Products.shieldGenerator, Products.superConductor, 10)
_set(Products.shieldGenerator, Products.electronics, 10)

_set(Products.thrusters, Products.copper, 5)
_set(Products.thrusters, Products.tungsten, 5)

_set(Products.fissionReactor, Products.nuclearFuelCell, 6)
_set(Products.fissionReactor, Products.electronics, 1)

_set(Products.spacecraft, Products.fissionReactor, 1)
_set(Products.spacecraft, Products.shieldGenerator, 4)
_set(Products.spacecraft, Products.thrusters, 8)