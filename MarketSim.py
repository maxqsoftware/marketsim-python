from enum import IntEnum
import random
from math import sqrt, floor
from functools import reduce
import matplotlib.pyplot as plotter

# Enumeration of all the different item types
class ItemType(IntEnum):
    wood = 0
    ore = 1
    steel = 2
    shovel = 3


class Consumer:
    """ Represents a population of consumers. Consumers have a total budget and
        demands for each type of good. Budget for each item type is allocated
        proportionally based on the demand for that object. """

    totalBudget = 100000
    demands = []

    def __init__(self):
        """Initialize a Consumer object with equal demand for each item type."""

        # Initialize demands for each item type
        self.demands = [100] * len(ItemType)

    def updateDemands(self):  
        """Randomly change consumer demands for each item type"""

        for item in ItemType:
            self.demands[item] += random.randint(-1,1)

            # Don't allow negative demand
            if self.demands[item] < 0:
                self.demands[item] = 0

    def getItemBudget(self,itemType):
        """ Gets the allocated budget for the specified item type """

        return self.totalBudget * self.demands[itemType] / sum(self.demands)

class Producer:
    """ Represents a population of manufacturers for a single good. """

    # The item type produced by this producer
    productType = ItemType.wood

    # Required quantity of each material needed to produce a single unit of the product
    materialQuantities = []

    # Scaling factor to account for reduced labor efficiency
    # as the quantity output increases.
    efficiency = 1

    # Nominal labor rate for producing a single unit
    laborRate = 1

    # Production quantity
    quantity = 0

    def __init__(self,productType):
        self.productType = productType
        self.materialQuantities = [0] * len(ItemType)

        # Setup raw material dependencies
        if productType == ItemType.steel:
            self.materialQuantities[ItemType.ore] = 5
        elif productType == ItemType.shovel:
            self.materialQuantities[ItemType.steel] = 2
            self.materialQuantities[ItemType.wood] = 2

    def totalLaborCosts(self):
        """ Total labor costs for entire production quantity """
        return self.laborRate*self.quantity*(1 + self.quantity/self.efficiency)
    
    def totalMaterialCost(self,marketPrices):
        """ Total labor costs for entire production quantity """
        cost = 0
        for itemType in ItemType:
            cost += self.quantity*self.materialQuantities[itemType]*marketPrices[itemType]
        
        return cost
    
    def unitMaterialCost(self,marketPrices):
        """ Material costs to produce a single unit """
        cost = 0
        for itemType in ItemType:
            cost += self.materialQuantities[itemType]*marketPrices[itemType]
        
        return cost

class ItemDataRecord:
    marketPrice = 0
    totalLaborCost = 0
    totalMaterialCost = 0
    totalCost = 0
    totalBudget = 0
    quantity = 0
    revenue = 0
    profit = 0

class EconSimRecord:

    # Iteration index
    iteration = 0

    # Map for each item type to the item cost, price and quantity data
    data = []

    def __init__(self,iteration,producers,consumers,marketPrices):
        self.iteration = iteration
        self.data = [None] * len(ItemType)

        for t in ItemType:
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

class EconSim:
    """ Simulate a perfectly competitive economy. The economy may contain a variable number
        of consumers and a single producer for each item type. """

    # Number of steps in the simulation
    numSteps = 1000

    # Historical data
    history = []

    # Map between item type and the producer producing that item.  Indexed using ItemType enumeration.
    producers = []

    # List of consumers
    consumers = []

    # Map between item type and the market price. Indexed using ItemType enumeration.
    marketPrices = []

    # Constant in range [0.0,1.0] used to specify how quickly market price adapts.
    # Large values will result in slower adaptations to change in supply and demand.
    marketDelay = 0.5

    def __init__(self,numSteps):
        self.numSteps = numSteps
        self.marketPrices = [0] * len(ItemType)
        self.producers = [0] * len(ItemType)

    def addConsumer(self,totalBudget,demands):
        """ Add a consumer with the specified budget and demands to the simulation. """

        consumer = Consumer()
        consumer.totalBudget = totalBudget
        consumer.demands = demands
        self.consumers.append(consumer)

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
                self.producers[ItemType.steel].efficiency /= 10

            # Update market prices, consumer demand and production quantities in that order
            self.updateMarketPrices()
            for consumer in self.consumers:
                consumer.updateDemands()
            self.updateProducerQuantities()

            # Record data and store in history
            self.history.append(EconSimRecord(i,self.producers,self.consumers,self.marketPrices))
        print("Done!")

    def initializeMarketPrices(self):
        """ Calculates initial guesses for the market prices """

        for t in ItemType:
            r = self.producers[t].laborRate
            E = self.producers[t].efficiency
            M = self.producers[t].unitMaterialCost(self.marketPrices)
            # Total allocated budget for this item type across all consumers
            B = reduce(lambda sum, consumer: sum + consumer.getItemBudget(t), self.consumers, 0.0)

            self.marketPrices[t] = r + sqrt(r*r + 8*B*r/E) + M

    def updateMarketPrices(self):
        """ Calculate the new market prices based on data from the previous iteration """

        # First, calculate new market prices using quantity and pricing data from previous iteration
        newMarketPrices = [0] * len(ItemType)
        for t in ItemType:
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
        for t in ItemType:
            d = self.marketDelay
            self.marketPrices[t] = d*self.marketPrices[t] + (1 - d)*newMarketPrices[t]

    def updateProducerQuantities(self):
        """ Recalculate producer quantities based on new market prices and consumer demands """

        newQuantities = [0] * len(ItemType)
        for t in ItemType:
            p = self.marketPrices[t]
            consumerDemandedQuantity = reduce(lambda sum, consumer: sum + floor(consumer.getItemBudget(t)/p), self.consumers, 0.0)
            producerDemandedQuantity = reduce(lambda sum, producer: sum + (producer.materialQuantities[t]*producer.quantity), self.producers, 0.0)
            newQuantities[t] = consumerDemandedQuantity + producerDemandedQuantity
        
        # Batch update producer quantities
        for t in ItemType:
            self.producers[t].quantity = newQuantities[t]

    def plot(self):
        """ Plots simulation data """

        # # Unpack all of the data
        # for t in ItemType:
        #     iteration = list(map(lambda x: x.iteration, self.history))
        #     marketPrice = list(map(lambda x: x.data[t].marketPrice, self.history))
        #     totalLaborCost = list(map(lambda x: x.data[t].totalLaborCost, self.history))
        #     totalMaterialCost = list(map(lambda x: x.data[t].totalMaterialCost, self.history))
        #     totalCost = list(map(lambda x: x.data[t].totalCost, self.history))
        #     totalBudget = list(map(lambda x: x.data[t].totalBudget, self.history))
        #     quantityProduced = list(map(lambda x: x.data[t].quantityProduced, self.history))
        #     revenue = list(map(lambda x: x.data[t].revenue, self.history))
        #     profit = list(map(lambda x: x.data[t].profit, self.history))
            
        self.plotMarketPrice()
        self.plotProfitAndRevenue()
        self.plotCosts()
        self.plotQuantity()

        plotter.show()

    def plotMarketPrice(self):
        plotter.figure()
        i = 1
        for t in ItemType:
            iteration = list(map(lambda x: x.iteration, self.history))
            marketPrice = list(map(lambda x: x.data[t].marketPrice, self.history))

            plotter.subplot(2,2,i)
            plotter.plot(iteration,marketPrice)
            plotter.xlabel("Iteration")
            plotter.ylabel("Market Price ($)")
            plotter.title(t.name)
            plotter.grid(True)
            plotter.tight_layout()
            i += 1
        plotter.show(block=False)

    def plotQuantity(self):
        plotter.figure()
        i = 1
        for t in ItemType:
            iteration = list(map(lambda x: x.iteration, self.history))
            quantity = list(map(lambda x: x.data[t].quantity, self.history))

            plotter.subplot(2,2,i)
            plotter.plot(iteration,quantity)
            plotter.xlabel("Iteration")
            plotter.ylabel("Quantity")
            plotter.title(t.name)
            plotter.grid(True)
            plotter.tight_layout()
            i += 1
        plotter.show(block=False)

    def plotProfitAndRevenue(self):
        plotter.figure()
        i = 1
        for t in ItemType:
            iteration = list(map(lambda x: x.iteration, self.history))
            profit = list(map(lambda x: x.data[t].profit, self.history))
            revenue = list(map(lambda x: x.data[t].revenue, self.history))

            plotter.subplot(2,2,i)
            plotter.plot(iteration,profit)
            plotter.plot(iteration,revenue)
            plotter.xlabel("Iteration")
            plotter.ylabel("Profit ($)")
            plotter.legend(["Profit","Revenue"])
            plotter.title(t.name)
            plotter.grid(True)
            plotter.tight_layout()
            i += 1
        plotter.show(block=False)

    def plotCosts(self):
        plotter.figure()
        i = 1
        for t in ItemType:
            iteration = list(map(lambda x: x.iteration, self.history))
            totalLaborCost = list(map(lambda x: x.data[t].totalLaborCost, self.history))
            totalMaterialCost = list(map(lambda x: x.data[t].totalMaterialCost, self.history))
            totalCost = list(map(lambda x: x.data[t].totalCost, self.history))

            plotter.subplot(2,2,i)
            plotter.plot(iteration,totalLaborCost)
            plotter.plot(iteration,totalMaterialCost)
            plotter.plot(iteration,totalCost)
            plotter.xlabel("Iteration")
            plotter.ylabel("Cost ($)")
            plotter.legend(["Labor","Materials","Total"])
            plotter.title(t.name)
            plotter.grid(True)
            plotter.tight_layout()
            i += 1
        plotter.show(block=False)
   

# --------- SETUP --------------

sim = EconSim(1000)
sim.marketDelay = 0.9

sim.addConsumer(100000,[10,40,30,100])
sim.addConsumer(50000,[50,0,20,50])

# NOTE: Currently only supports one producer for each item type
sim.setProducer(ItemType.wood,10000,0.1)
sim.setProducer(ItemType.ore,10000,0.25)
sim.setProducer(ItemType.steel,1000,0.5)
sim.setProducer(ItemType.shovel,1000,1.0)

sim.simulate()
sim.plot()
