from typing import Any

import matplotlib.pyplot as plt
import numpy as np


class MicrogridEnvironmentPlot:
    def __init__(self, days: int):
        super().__init__()
        self.days = days
        self.rewards: list = []
        self.loads: list = []
        self.prices: list = []
        self.battery_socs: list = []
        self.battery_socs_kWh: list = []
        self.energy_generated: list = []
        self.energy_sold: list = []
        self.energy_bought: list = []
        self.grid_buy_prices: list = []
        self.grid_sell_prices: list = []
        # self.actions: list = []

    def collect_info(self, info: dict[str, Any]):
        self.rewards.append(info["reward"])
        self.loads.append(info["loads"])
        self.prices.append(info["price"])
        self.battery_socs.append(info["battery_percent"])
        self.battery_socs_kWh.append(info["battery_kWh"])
        self.energy_generated.append(info["energy_generated"])
        self.energy_sold.append(info["energy_sold"])
        self.energy_bought.append(info["energy_bought"])
        self.grid_buy_prices.append(info["grid_buy_price"])
        self.grid_sell_prices.append(info["grid_sell_price"])
        # self.actions.append(info["action"])

    def reset(self):
        self.rewards.clear()
        self.loads.clear()
        self.prices.clear()
        self.battery_socs.clear()
        self.battery_socs_kWh.clear()
        self.energy_generated.clear()
        self.energy_sold.clear()
        self.energy_bought.clear()
        self.grid_buy_prices.clear()
        self.grid_sell_prices.clear()
        # self.actions.clear()

    def plot_figure(self):
        fig, axes = plt.subplots(nrows=7, ncols=1, figsize=(10, 20))
        fig.suptitle("Grid of Energy Data Plots", fontsize=16)
        fig.tight_layout(pad=3.0)

        for ax in axes:
            # ax.set_facecolor("silver")
            ax.grid(which="major", color="gray", ls="-", alpha=0.7)
            ax.grid(which="minor", color="gray", ls=":", alpha=0.2)

        self._plot_sale_prices(axes[0])
        self._plot_balance(axes[1])
        self._plot_energy_generated(axes[2])
        self._plot_battery(axes[3])
        self._plot_energy_sold_bought(axes[4])
        self._plot_grid_prices(axes[5])
        self._plot_loads(axes[6])
        # self._plot_actions(axes[7])

        for ax in axes[1:]:
            ax.sharex(axes[0])

        return fig

    def plot_to_file(self, file):
        fig = self.plot_figure()
        fig.savefig(file)

    def _plot_sale_prices(self, ax: plt.Axes):
        ax.set_title("SALE PRICES (Market + Action)")
        ax.plot(self.prices, color="k")
        ax.set_xlabel("Time (h)")
        ax.set_ylabel("€ cents")
        ax.set_xlim(0, self.days * 24)
        ax.set_xticks(np.arange(0, self.days * 24, step=24), np.arange(1, self.days + 1))
        ax.set_xticks(np.arange(0, self.days * 24, step=1), minor=True)

    def _plot_balance(self, ax: plt.Axes):
        balance = (
            np.array(self.energy_generated)
            + np.array(self.energy_bought)
            + np.negative(np.diff(self.battery_socs_kWh, prepend=0))
            - np.array(self.energy_sold)
            - np.array(self.loads).sum(axis=1)
        )
        ax.set_title("Energy Balance (Generated + Bought - Battery_Diff - Sold - Loads)")
        ax.plot(balance, color="k")
        ax.set_ylabel("kW")
        ax.set_ylim(-26, 26)

    def _plot_energy_generated(self, ax: plt.Axes):
        ax.set_title("ENERGY GENERATED")
        ax.plot(self.energy_generated, color="k")
        ax.set_ylabel("kW")
        ax.set_ylim(-10, 350)

    def _plot_battery(self, ax: plt.Axes):
        ax.set_title("BATTERY SoC")
        ax.plot(self.battery_socs_kWh, color="k")
        # ax.set_ylim(-0.01, 1.01)
        ax.set_ylim(-10, 510)
        # TODO add absolute soc on second scala

    def _plot_energy_sold_bought(self, ax: plt.Axes):
        ax.set_title("Energy Exchanged")
        ax.bar(
            np.arange(len(self.energy_sold)),
            self.energy_sold,
            color="navy",
            width=0.4,
            label="Energy sold",
        )
        ax.bar(
            np.arange(len(self.energy_bought)),
            np.negative(self.energy_bought),
            color="darkred",
            width=0.4,
            label="Energy purchased",
        )
        ax.set_ylabel("kW")
        ax.set_ylim(-350, 350)
        ax.legend(loc="upper right")

    def _plot_grid_prices(self, ax: plt.Axes):
        ax.set_title("GRID PRICES")
        ax.plot(self.grid_buy_prices, color="red", label="Buying prices")
        ax.plot(self.grid_sell_prices, color="green", label="Selling prices")
        ax.set_ylabel("GRID PRICES € cents")
        ax.set_ylim(0, max(8, *self.grid_buy_prices, *self.grid_sell_prices))
        ax.legend(loc="upper right")

    def _plot_loads(self, ax: plt.Axes):
        ax.set_title("Hourly Residential Loads")
        ax.plot(np.array(self.loads).sum(axis=1), color="k")
        # ax.boxplot(np.array(self.loads).T)
        ax.set_ylabel("kW")
        ax.set_ylim(0, 300.0)

    def _plot_actions(self, ax: plt.Axes):
        actions = self.actions  # Liste von Zahlen: 0 = price, 1 = excess, 2 = deficiency
        actions = list(map(int, self.actions))
        zeit = list(range(len(actions)))  # Zeit = Index

        # Plot
        ax.scatter(zeit, actions, c=actions, cmap="tab10", s=100)

        # Achsen-Labels
        ax.set_ylim(-0.5, 2.5)  # genug Platz für 3 Kategorien (0, 1, 2)
        ax.set_yticks([0, 1, 2])
        ax.set_yticklabels(["price", "excess", "deficiency"])

        ax.set_xlabel("step")
        ax.set_ylabel("action")
        ax.set_title("Actions per hour")
        ax.grid(True)
