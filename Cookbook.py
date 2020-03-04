from enum import IntEnum

class Units:
    g = 0.001
    kg = 1.0
    ton = 2000.0
    mm = 0.001
    cm = 0.01
    m = 1.0
    km = 1000.0
    each = 1.0

class Product:
    quantity = 0
    ingredients = {}

    def __init__(self,quantity,ingredients):
        self.quantity = quantity
        self.ingredients = ingredients

    def getQuantity(self):
        return self.quantity.quantity

class ProductType(IntEnum):
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
        for product in ProductType:
            namesList.append(product.name)
        return namesList

# Adjacency matrix containing ingredients
_ingredients = [[0 for i in range(len(ProductType))] for j in range(len(ProductType))]

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
_set(ProductType.hydrogenFuelCell,ProductType.water, 1 * Units.kg)
_set(ProductType.hydrogenFuelCell,ProductType.electronics, 5)
_set(ProductType.hydrogenFuelCell,ProductType.platinum,10)

_set(ProductType.miningEquipment, ProductType.tungsten, 5)
_set(ProductType.miningEquipment, ProductType.titanium, 5)
_set(ProductType.miningEquipment, ProductType.iron, 10)

_set(ProductType.superConductor, ProductType.helium, 10)

_set(ProductType.fertilizer, ProductType.phosphorus, 5)

_set(ProductType.carbonNanotubes, ProductType.carbon, 5)

_set(ProductType.graphene, ProductType.carbon, 5)

_set(ProductType.electronics, ProductType.graphene, 1)
_set(ProductType.electronics, ProductType.copper, 1)

_set(ProductType.hullPlating, ProductType.titanium, 10)
_set(ProductType.hullPlating, ProductType.aluminum, 10)

_set(ProductType.nuclearFuelCell, ProductType.uranium, 10)
_set(ProductType.nuclearFuelCell, ProductType.lead, 50)
_set(ProductType.nuclearFuelCell, ProductType.electronics, 50)

_set(ProductType.solarCell, ProductType.graphene, 10)

_set(ProductType.shieldGenerator, ProductType.superConductor, 10)
_set(ProductType.shieldGenerator, ProductType.electronics, 10)

_set(ProductType.thrusters, ProductType.copper, 5)
_set(ProductType.thrusters, ProductType.tungsten, 5)

_set(ProductType.fissionReactor, ProductType.nuclearFuelCell, 6)
_set(ProductType.fissionReactor, ProductType.electronics, 1)

_set(ProductType.spacecraft, ProductType.fissionReactor, 1)
_set(ProductType.spacecraft, ProductType.shieldGenerator, 4)
_set(ProductType.spacecraft, ProductType.thrusters, 8)