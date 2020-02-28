from math import sqrt, floor
from functools import reduce

import random
from Cookbook import Products, getIngredientQuantity, getIngredients

class ItemDataRecord:
    marketPrice = 0
    totalLaborCost = 0
    totalMaterialCost = 0
    totalCost = 0
    totalBudget = 0
    quantity = 0
    revenue = 0
    profit = 0

class SimRecord:

    # Iteration index
    iteration = 0

    # Map for each item type to the item cost, price and quantity data
    data = []

    def __init__(self,iteration,producers,consumers,marketPrices):
        self.iteration = iteration
        self.data = [None] * len(Products)

        for t in Products:
            record = ItemDataRecord()
            record.marketPrice = marketPrices[t]
            record.totalBudget = reduce(lambda sum, consumer: sum + consumer.getItemBudget(t), consumers, 0.0)
            record.quantity = producers[t].quantity
            record.totalLaborCost = producers[t].totalLaborCosts()
            record.totalMaterialCost = producers[t].totalMaterialCost(marketPrices)
            record.totalCost = record.totalLaborCost + record.totalMaterialCost
            record.revenue = producers[t].quantity * marketPrices[t]
            record.profit = record.revenue - record.totalCost
            self.data[t] = record 

class Sim:
    """ Simulate a perfectly competitive economy. The economy may contain a variable number
        of consumers and a single producer for each item type. """

    # Number of steps in the simulation
    numSteps = 1000

    # Historical data
    history = []

    # Map between item type and the producer producing that item.  Indexed using Products enumeration.
    producers = []

    # List of consumers
    consumers = []

    # Map between item type and the market price. Indexed using Products enumeration.
    marketPrices = []

    # Constant in range [0.0,1.0] used to specify how quickly market price adapts.
    # Large values will result in slower adaptations to change in supply and demand.
    marketDelay = 0.5

    def __init__(self,numSteps):
        self.numSteps = numSteps
        self.marketPrices = [0] * len(Products)
        self.producers = [0] * len(Products)

    def addConsumer(self,totalBudget,demands):
        """ Add a consumer with the specified budget and demands to the simulation. """

        consumer = Consumer()
        consumer.totalBudget = totalBudget
        consumer.demands = demands
        self.consumers.append(consumer)

    def getProducer(self,productType):
        """ Returns the producer for the product type """
        return self.producers[productType]

    def setProducer(self,productType,efficiency,laborRate):
        """ Add a producer of the specified product type to the simulation. """

        producer = Producer(productType)
        producer.efficiency = efficiency
        producer.laborRate = laborRate

        self.producers[productType] = producer

    def simulate(self):
        """ Start the simulation """
        
        self.initializeMarketPrices()

        print("Simulating...")
        for i in range(self.numSteps):
            # Throw in an anomaly
            if i == floor(self.numSteps / 2):
                self.producers[Products.steel].efficiency /= 2

            # Update market prices, consumer demand and production quantities in that order
            self.updateMarketPrices()
            for consumer in self.consumers:
                consumer.updateDemands()
            self.updateProducerQuantities()

            # Record data and store in history
            self.history.append(SimRecord(i,self.producers,self.consumers,self.marketPrices))
        print("Done!")

    def initializeMarketPrices(self):
        """ Calculates initial guesses for the market prices """

        eps = 1E-6

        for t in Products:
            previousPrice = -1.0
            while abs(self.marketPrices[t] - previousPrice) > eps: 
                previousPrice = self.marketPrices[t]
                self.updateMarketPrices()
                self.updateProducerQuantities()

    def updateMarketPrices(self):
        """ Calculate the new market prices based on data from the previous iteration """

        # First, calculate new market prices using quantity and pricing data from previous iteration
        newMarketPrices = [0] * len(Products)
        for t in Products:
            producer = self.producers[t]

            # Market price is derive using the following relations
            #   1. Market price (p) is defined by point on supply/demand graph where consumers and producers agree on
            #      a particular market price for a particular quantity (q).
            #   2. Producers want to produce quantity where marginal costs (MC) = marginal revenue (MR). In other words,
            #      keep producing additional units until the unit costs outweigh the unit revenue.
            #
            #   Labor Cost (C_L) = rq(1+q/E)
            #   Material Cost (C_M) = q*Sum(n(type)*p(type)), where n = # of item type used in recipe
            #
            #   MR = dR/dq = d(pq)/dq = p
            #   MC = dTC/dq = dC_L/dq + dC_M/dq
            #      = r(1+2q/E) + Sum(n(type)*p(type))
            newMarketPrices[t] = producer.laborRate*(1 + 2*producer.quantity/producer.efficiency) + producer.unitMaterialCost(self.marketPrices)
    
        # Apply market price updates
        for t in Products:
            d = self.marketDelay
            self.marketPrices[t] = d*self.marketPrices[t] + (1 - d)*newMarketPrices[t]

    def updateProducerQuantities(self):
        """ Recalculate producer quantities based on new market prices and consumer demands """

        newQuantities = [0] * len(Products)
        for product in Products:
            consumerDemandedQuantity = reduce(lambda sum, consumer: sum + floor(consumer.getItemBudget(product)/self.marketPrices[product]), self.consumers, 0.0)
            producerDemandedQuantity = reduce(lambda sum, producer: sum + (getIngredientQuantity(producer.output,product)*producer.quantity), self.producers, 0.0)
            newQuantities[product] = consumerDemandedQuantity + producerDemandedQuantity
        
        # Batch update producer quantities
        for product in Products:
            self.producers[product].quantity = newQuantities[product]

class Producer:
    """ Represents a population of manufacturers for a single good. """

    # Production quantity
    quantity = 0

    # The item type produced by this producer
    output = Products.wood

    # Scaling factor to account for reduced labor efficiency
    # as the quantity output increases.
    efficiency = 1

    # Nominal labor rate for producing a single unit
    laborRate = 1

    def __init__(self,output):
        self.output = output

    def totalLaborCosts(self):
        """ Total labor costs for entire production quantity """
        return self.laborRate*self.quantity*(1 + self.quantity/self.efficiency)
    
    def totalMaterialCost(self,marketPrices):
        """ Total labor costs for entire production quantity """
        cost = 0
        for ingredient in Products:
            cost += self.quantity*getIngredientQuantity(self.output,ingredient)*marketPrices[ingredient]
        
        return cost
    
    def unitMaterialCost(self,marketPrices):
        """ Material costs to produce a single unit """
        cost = 0
        for ingredient in Products:
            cost += getIngredientQuantity(self.output,ingredient)*marketPrices[ingredient]
        
        return cost

class Consumer:
    """ Represents a population of consumers. Consumers have a total budget and
        demands for each type of good. Budget for each item type is allocated
        proportionally based on the demand for that object. """

    totalBudget = 100000
    demands = []

    def __init__(self):
        """Initialize a Consumer object with equal demand for each item type."""

        # Initialize demands for each item type
        self.demands = [100] * len(Products)

    def updateDemands(self):  
        """Randomly change consumer demands for each item type"""

        for item in Products:
            self.demands[item] += random.randint(-1,1)

            # Don't allow negative demand
            if self.demands[item] < 0:
                self.demands[item] = 0

    def getItemBudget(self,productType):
        """ Gets the allocated budget for the specified item type """

        return self.totalBudget * self.demands[productType] / sum(self.demands)