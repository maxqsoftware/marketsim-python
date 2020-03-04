from math import sqrt, floor
from functools import reduce
import random
from Cookbook import ProductType, getIngredientQuantity, getIngredients

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
        self.data = [None] * len(ProductType)

        for t in ProductType:
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

    # Historical data
    history = []

    # Map between item type and the producer producing that item.  Indexed using ProductType enumeration.
    producers = []

    # List of consumers
    consumers = []

    # Map between item type and the market price. Indexed using ProductType enumeration.
    marketPrices = []

    # Constant in range [0.0,1.0] used to specify how quickly market price adapts.
    # Large values will result in slower adaptations to change in supply and demand.
    marketDelay = 0.75

    def __init__(self):
        self.marketPrices = [0.0] * len(ProductType)

        # Initialize a default set of consumers
        self.consumers = []

        for i in range(5):
            self.consumers.append(Consumer.default())

        # Intialize a default set of producers
        self.producers = [None] * len(ProductType)
        for product in ProductType:
            self.producers[product] = Producer(product)

    def step(self,i):
        """ Simulates one step of the simulation. """

        self.updateMarketPrices()
        for consumer in self.consumers:
            consumer.updateDemands()
        self.updateProducerQuantities()

        # Record data and store in history
        self.history.append(SimRecord(i,self.producers,self.consumers,self.marketPrices))


    def initializeMarketPrices(self):
        """ Calculates initial guesses for the market prices """

        print("Initializing market prices...")
        eps = 1E-3
        iteration = 0
        solutionConverged = False
        error = [-1.0] * len(ProductType)
        previousMarketPrices = [1] * len(ProductType)
        while not solutionConverged: 
            iteration += 1
            if iteration > 1000:
                print("Market prices failed to converge after 1000 iterations... exiting.")
                exit()

            self.updateMarketPrices()
            self.updateProducerQuantities()

            # Calculate error and determine if the market prices for all ProductType
            # have converged to within the specified error limit
            solutionConverged = True
            for product in ProductType:
                error[product] =  self.marketPrices[product] - previousMarketPrices[product]
                if abs(error[product]) > eps:
                    solutionConverged = False
                previousMarketPrices[product] = self.marketPrices[product]
           
        print("Solution converged after " + str(iteration) + " iterations")
        for product in ProductType:
            print("{0:30s}\t${1:0.2f}".format(product.name, self.marketPrices[product]))

    def updateMarketPrices(self):
        """ Calculate the new market prices based on data from the previous iteration """

        # First, calculate new market prices using quantity and pricing data from previous iteration
        newMarketPrices = [0] * len(ProductType)
        for t in ProductType:
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
        for t in ProductType:
            d = self.marketDelay
            self.marketPrices[t] = d*self.marketPrices[t] + (1 - d)*newMarketPrices[t]

    def updateProducerQuantities(self):
        """ Recalculate producer quantities based on new market prices and consumer demands """

        newQuantities = [0] * len(ProductType)
        for product in ProductType:
            consumerDemandedQuantity = reduce(lambda sum, consumer: sum + floor(consumer.getItemBudget(product)/self.marketPrices[product]), self.consumers, 0.0)
            producerDemandedQuantity = reduce(lambda sum, producer: sum + (getIngredientQuantity(producer.output,product)*producer.quantity), self.producers, 0.0)
            newQuantities[product] = consumerDemandedQuantity + producerDemandedQuantity
        
        # Batch update producer quantities
        for product in ProductType:
            self.producers[product].quantity = newQuantities[product]

class Producer:
    """ Represents a population of manufacturers for a single good. """

    # Production quantity
    quantity = 0

    # The item type produced by this producer
    output = ProductType.water

    # Scaling factor to account for reduced labor efficiency
    # as the quantity output increases.
    efficiency = 10000

    # Nominal labor rate for producing a single unit
    laborRate = 0.1

    def __init__(self,output):
        self.output = output

    def totalLaborCosts(self):
        """ Total labor costs for entire production quantity """
        return self.laborRate*self.quantity*(1 + self.quantity/self.efficiency)
    
    def totalMaterialCost(self,marketPrices):
        """ Total labor costs for entire production quantity """
        cost = 0
        for ingredient in ProductType:
            cost += self.quantity*getIngredientQuantity(self.output,ingredient)*marketPrices[ingredient]
        
        return cost
    
    def unitMaterialCost(self,marketPrices):
        """ Material costs to produce a single unit """
        cost = 0
        for ingredient in ProductType:
            cost += getIngredientQuantity(self.output,ingredient)*marketPrices[ingredient]
        
        return cost

class Consumer:
    """ Represents a population of consumers. Consumers have a total budget and
        demands for each type of good. Budget for each item type is allocated
        proportionally based on the demand for that object. """

    budget = 100000
    demands = []

    def __init__(self,budget,demands):
        """Initialize a Consumer object with equal demand for each item type."""
        self.budget = budget
        self.demands = demands

    @classmethod
    def default(cls):
        """Initialize a Consumer object with equal demand for each item type."""
        demands = [100] * len(ProductType)
        return cls(1000000,demands)

    def updateDemands(self):  
        """Randomly change consumer demands for each item type"""
        for item in ProductType:
            self.demands[item] += random.randint(-1,1)

            # Don't allow negative demand
            if self.demands[item] < 0:
                self.demands[item] = 0

    def getItemBudget(self,productType):
        """ Gets the allocated budget for the specified item type """
        return self.budget * self.demands[productType] / sum(self.demands)