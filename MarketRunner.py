from MarketPlotter import MarketPlotter
from Market import Sim
from Cookbook import Products

sim = Sim(1000)
sim.marketDelay = 0.75
sim.simulate()
MarketPlotter.plot(sim)

# TODO
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