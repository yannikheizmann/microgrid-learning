from itertools import permutations
from types import SimpleNamespace

import pytest

from rl_microgrid.microgrid.actions import (
    CompositeBasicAction,
    CompositeCarAction,
    EnergyDeficiencyAction,
    EnergyExcessAction,
    EnergySource,
    EnergyFeed,
    PriceAction,
    PriceLevel,
)
from rl_microgrid.config.configuration.microgrid import BatteryConfig, ExternalGridConfig
from rl_microgrid.microgrid.components import Battery, ExternalGrid


@pytest.mark.parametrize("index,level", enumerate(PriceLevel))
def test_price_levels(index, level):
    action = PriceAction.from_action_space(index)
    assert action.price_level == level
    assert action.to_action_space() == index


@pytest.mark.parametrize("index", [-1, 5])
def test_invalid_price(index):
    with pytest.raises(ValueError):
        PriceAction.from_action_space(index)


@pytest.mark.parametrize("action_type", [CompositeBasicAction, CompositeCarAction])
def test_composite_round_trip(action_type):
    for index in range(action_type.calc_action_space()):
        assert action_type.from_action_space(index).to_action_space() == index


@pytest.mark.parametrize(
    "action_type,enum,keyword,attribute",
    [
        (EnergyDeficiencyAction, EnergySource, "possible_sources", "energy_source_priority"),
        (EnergyExcessAction, EnergyFeed, "possible_feeds", "energy_feed_priority"),
    ],
)
def test_energy_priority_permutations(action_type, enum, keyword, attribute):
    components = [enum.EXTERNAL_GRID, enum.BATTERY]
    for index, order in enumerate(permutations(components)):
        action = action_type.from_action_space(index, **{keyword: components})
        assert getattr(action, attribute) == order
        assert action.to_action_space() == index
    for index in [-1, 2]:
        with pytest.raises(ValueError):
            action_type.from_action_space(index, **{keyword: components})


@pytest.mark.parametrize("stored,required,expected", [(100, 500, 400), (0, 500, 500), (100, 50, 0)])
def test_battery_first_buys_remaining_demand(stored, required, expected):
    """Regression for the under-purchasing bug described in the old manual guide."""
    battery = Battery(BatteryConfig(CHARGING_RATE=1, DISCHARGE_COEFFICIENT=1))
    battery.charge(stored)
    grid = ExternalGrid(ExternalGridConfig())
    microgrid = SimpleNamespace(battery=battery, external_grid=grid)
    sources = [EnergySource.BATTERY, EnergySource.EXTERNAL_GRID]
    action = EnergyDeficiencyAction(sources, tuple(sources))
    action.set_missing_energy(required)
    result = action.execute(microgrid, 0)
    assert result.energy_bought == pytest.approx(expected)
    assert result.price == pytest.approx(grid.buy(expected))
