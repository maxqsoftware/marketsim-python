from MarketPlotter import MarketPlotter
from Market import Sim
from Cookbook import Products
from math import floor

sim = Sim()

sim.initializeMarketPrices()

print("Simulating...")

for i in range(1000):
    if i == 500:
        sim.producers[Products.carbon].efficiency *= 2
    
    sim.step(i)

print("Done!")

MarketPlotter.plot(sim)