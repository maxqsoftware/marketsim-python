from MarketPlotter import MarketPlotter
from Market import Sim
from Cookbook import Products

sim = Sim(100)
sim.marketDelay = 0.75

sim.addConsumer(100000,[10,40,30,100])
sim.addConsumer(50000,[50,0,20,50])

# NOTE: Currently only supports one producer for each item type
sim.setProducer(Products.wood,10000,0.1)
sim.setProducer(Products.ore,10000,0.25)
sim.setProducer(Products.steel,1000,0.5)
sim.setProducer(Products.shovel,1000,1.0)

sim.simulate()

MarketPlotter.plot(sim)


# TODO
#  - Change relationships to adjacency tables where appropriate
#  - Add a more complex goods structure and see how it holds up
#  - Refactor into separate factions
#     - Faction has an array of producers for each item type.
#       Null if that faction does not produce that good.
#     - Faction has a single consumer which models demands of its
#       population. Assume single faction per planet for now.
#  - Create planets with biomes. Associate resources with each biome.
#  - Create factions with characteristics of biomes they inhabit.
#  - Specify economy type for factions.
#  - Create system for modeling relationships between factions
#     - At War, Unfriendly, Neutral, Friends, Allies
#  - Setup faction relationships using adjacency matrix. Factions
#    with stronger ties have stronger trade. Friendly factions will
#    export goods which the other faction does not possess.
#  - Modify demand function for goods using adjacency matrix
#    Should be able to specify quantity demanded by each faction's
#    consumers and producers. Maybe leave producers out if it gets
#    too complicated.