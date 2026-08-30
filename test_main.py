import random
import unittest

from main import EpsilonGreedyAgent, MarketStrategy, SimulatedMarket, run_simulation


class EpsilonGreedyAgentTests(unittest.TestCase):
    def test_learn_calculates_a_running_average(self) -> None:
        agent = EpsilonGreedyAgent(
            number_of_strategies=1,
            random_number_generator=random.Random(1),
        )

        agent.learn(strategy_index=0, daily_return=0.01)
        agent.learn(strategy_index=0, daily_return=0.03)

        self.assertAlmostEqual(agent.estimated_returns[0], 0.02)
        self.assertEqual(agent.selection_counts[0], 2)

    def test_simulation_runs_one_market_choice_per_day(self) -> None:
        random_number_generator = random.Random(1)
        strategies = [MarketStrategy("Always Flat", 0.0, 0.0)]
        market = SimulatedMarket(strategies, random_number_generator)
        agent = EpsilonGreedyAgent(1, random_number_generator)

        ending_value = run_simulation(
            market=market,
            agent=agent,
            number_of_days=10,
            starting_portfolio_value=100.0,
        )

        self.assertEqual(ending_value, 100.0)
        self.assertEqual(agent.selection_counts, [10])


if __name__ == "__main__":
    unittest.main()
