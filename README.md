# marketsim-python
Simulation of a perfectly competitive market

## Prerequisites
### matplotlib
```
python -m pip install -U pip
python -m pip install -U matplotlib
```

## To Do
 - Add units. Market prices are per unit X. Production requires Y to produce Z.
 - Create a mini-game out of the market simulation
 - Come up with a set of actions that the user can perform that will change market prices
 - Will need to create some sort of state machine "choose your own adventure" type thing
   where the user can select their next actions
 - Focus on creating a game model that is tied into the economic simulation.
 - Should also create some artificial politics or construction projects so there is some
   economic forces other than the actions that the player is taking. 

## Future Work
 - Refactor into separate factions
    - Faction has an array of producers for each item type.
      Null if that faction does not produce that good.
    - Faction has a single consumer which models demands of its
      population. Assume single faction per planet for now.
 - Create planets with biomes. Associate resources with each biome.
 - Create factions with characteristics of biomes they inhabit.
 - Specify economy type for factions.
 - Create system for modeling relationships between factions
    - At War, Unfriendly, Neutral, Friends, Allies
 - Setup faction relationships using adjacency matrix. Factions
   with stronger ties have stronger trade. Friendly factions will
   export goods which the other faction does not possess.
 - Modify demand function for goods using adjacency matrix
   Should be able to specify quantity demanded by each faction's
   consumers and producers. Maybe leave producers out if it gets
   too complicated.