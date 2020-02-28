from Market import Sim
from Cookbook import Products
import matplotlib.pyplot as plotter

class MarketPlotter:
    @staticmethod
    def plot(sim):
        """ Plots simulation data """

        MarketPlotter.plotMarketPrice(sim)
        MarketPlotter.plotQuantity(sim)

        plotter.show()

    @staticmethod
    def plotMarketPrice(sim):
        plotter.figure()
        i = 1
        for t in Products:
            iteration = list(map(lambda x: x.iteration, sim.history))
            marketPrice = list(map(lambda x: x.data[t].marketPrice, sim.history))

            plotter.subplot(2,2,i)
            plotter.plot(iteration,marketPrice)
            plotter.xlabel("Iteration")
            plotter.ylabel("Market Price ($)")
            plotter.title(t.name)
            plotter.grid(True)
            plotter.tight_layout()
            i += 1
        plotter.show(block=False)

    @staticmethod
    def plotQuantity(sim):
        plotter.figure()
        i = 1
        for t in Products:
            iteration = list(map(lambda x: x.iteration, sim.history))
            quantity = list(map(lambda x: x.data[t].quantity, sim.history))

            plotter.subplot(2,2,i)
            plotter.plot(iteration,quantity)
            plotter.xlabel("Iteration")
            plotter.ylabel("Quantity")
            plotter.title(t.name)
            plotter.grid(True)
            plotter.tight_layout()
            i += 1
        plotter.show(block=False)

    @staticmethod
    def plotProfitAndRevenue(sim):
        plotter.figure()
        i = 1
        for t in Products:
            iteration = list(map(lambda x: x.iteration, sim.history))
            profit = list(map(lambda x: x.data[t].profit, sim.history))
            revenue = list(map(lambda x: x.data[t].revenue, sim.history))

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

    @staticmethod
    def plotCosts(sim):
        plotter.figure()
        i = 1
        for t in Products:
            iteration = list(map(lambda x: x.iteration, sim.history))
            totalLaborCost = list(map(lambda x: x.data[t].totalLaborCost, sim.history))
            totalMaterialCost = list(map(lambda x: x.data[t].totalMaterialCost, sim.history))
            totalCost = list(map(lambda x: x.data[t].totalCost, sim.history))

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
   