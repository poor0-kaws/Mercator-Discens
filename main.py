"""Teach an epsilon-greedy bandit through a financial-market example."""

import random


class MarketStrategy:
    """A trading strategy with a fixed return pattern in our toy market."""

    def __init__(
        self,
        name: str,
        expected_daily_return: float,
        daily_volatility: float,
    ) -> None:
        if daily_volatility < 0:
            raise ValueError("Daily volatility cannot be negative.")

        self.name = name
        self.expected_daily_return = expected_daily_return
        self.daily_volatility = daily_volatility

    def sample_daily_return(self, random_number_generator: random.Random) -> float:
        """Create one possible daily return for this strategy."""
        return random_number_generator.gauss(
            self.expected_daily_return,
            self.daily_volatility,
        )


class SimulatedMarket:
    """Reveal the return for only the strategy selected by the agent."""

    def __init__(
        self,
        strategies: list[MarketStrategy],
        random_number_generator: random.Random,
    ) -> None:
        if not strategies:
            raise ValueError("The market needs at least one strategy.")

        self.strategies = strategies
        self.random_number_generator = random_number_generator

    def get_daily_return(self, strategy_index: int) -> float:
        """Return today's result for the selected strategy."""
        strategy = self.strategies[strategy_index]
        return strategy.sample_daily_return(self.random_number_generator)


class EpsilonGreedyAgent:
    """Learn which strategy has produced the highest average return."""

    def __init__(
        self,
        number_of_strategies: int,
        random_number_generator: random.Random,
        starting_epsilon: float = 1.0,
        minimum_epsilon: float = 0.05,
        epsilon_decay: float = 0.995,
    ) -> None:
        if number_of_strategies < 1:
            raise ValueError("The agent needs at least one strategy.")

        if not 0 <= minimum_epsilon <= starting_epsilon <= 1:
            raise ValueError("Epsilon values must be between 0 and 1.")

        if not 0 < epsilon_decay <= 1:
            raise ValueError("Epsilon decay must be greater than 0 and at most 1.")

        self.number_of_strategies = number_of_strategies
        self.random_number_generator = random_number_generator
        self.epsilon = starting_epsilon
        self.minimum_epsilon = minimum_epsilon
        self.epsilon_decay = epsilon_decay

        # Each position in these lists belongs to one market strategy.
        self.estimated_returns = [0.0] * number_of_strategies
        self.selection_counts = [0] * number_of_strategies

    def choose_strategy(self) -> int:
        """Explore randomly or choose the best strategy found so far."""
        should_explore = self.random_number_generator.random() < self.epsilon

        if should_explore:
            return self.random_number_generator.randrange(self.number_of_strategies)

        best_estimate = max(self.estimated_returns)
        best_strategy_indexes = [
            index
            for index, estimate in enumerate(self.estimated_returns)
            if estimate == best_estimate
        ]

        # A random tie-break prevents strategy zero from getting an unfair head start.
        return self.random_number_generator.choice(best_strategy_indexes)

    def learn(self, strategy_index: int, daily_return: float) -> None:
        """Add one observed return to the selected strategy's running average."""
        self.selection_counts[strategy_index] += 1
        number_of_observations = self.selection_counts[strategy_index]
        old_estimate = self.estimated_returns[strategy_index]

        estimation_error = daily_return - old_estimate
        updated_estimate = old_estimate + estimation_error / number_of_observations
        self.estimated_returns[strategy_index] = updated_estimate

        decayed_epsilon = self.epsilon * self.epsilon_decay
        self.epsilon = max(self.minimum_epsilon, decayed_epsilon)

    def preferred_strategy_index(self) -> int:
        """Return the strategy with the highest estimated average return."""
        return max(
            range(self.number_of_strategies),
            key=lambda index: self.estimated_returns[index],
        )


def run_simulation(
    market: SimulatedMarket,
    agent: EpsilonGreedyAgent,
    number_of_days: int,
    starting_portfolio_value: float,
) -> float:
    """Run the learning loop and return the final portfolio value."""
    if number_of_days < 1:
        raise ValueError("The simulation needs at least one trading day.")

    if starting_portfolio_value <= 0:
        raise ValueError("The starting portfolio value must be positive.")

    portfolio_value = starting_portfolio_value

    for _ in range(number_of_days):
        strategy_index = agent.choose_strategy()
        daily_return = market.get_daily_return(strategy_index)
        agent.learn(strategy_index, daily_return)

        # A 1% return multiplies the portfolio by 1.01.
        portfolio_value *= 1 + daily_return

    return portfolio_value


def build_default_simulation(seed: int) -> tuple[SimulatedMarket, EpsilonGreedyAgent]:
    """Build the example market and agent used when this file runs."""
    random_number_generator = random.Random(seed)

    strategies = [
        MarketStrategy("Trend Following", 0.0008, 0.010),
        MarketStrategy("Mean Reversion", 0.0005, 0.007),
        MarketStrategy("Defensive", 0.0002, 0.003),
    ]

    market = SimulatedMarket(strategies, random_number_generator)
    agent = EpsilonGreedyAgent(len(strategies), random_number_generator)
    return market, agent


def format_percent(value: float) -> str:
    """Turn 0.0123 into the easier-to-read text '1.230%'."""
    return f"{value:.3%}"


def print_report(
    market: SimulatedMarket,
    agent: EpsilonGreedyAgent,
    starting_portfolio_value: float,
    ending_portfolio_value: float,
    number_of_days: int,
) -> None:
    """Print what the agent learned in a small table."""
    print(f"Simulated trading days: {number_of_days}")
    print(f"Starting portfolio: ${starting_portfolio_value:,.2f}")
    print(f"Ending portfolio:   ${ending_portfolio_value:,.2f}")
    print()
    print("Strategy         | Hidden mean | Learned mean | Days selected")
    print("-----------------|-------------|--------------|--------------")

    for index, strategy in enumerate(market.strategies):
        print(
            f"{strategy.name:<16} | "
            f"{format_percent(strategy.expected_daily_return):>11} | "
            f"{format_percent(agent.estimated_returns[index]):>12} | "
            f"{agent.selection_counts[index]:>13}"
        )

    preferred_index = agent.preferred_strategy_index()
    preferred_name = market.strategies[preferred_index].name
    print()
    print(f"Agent's preferred strategy: {preferred_name}")


def main() -> None:
    """Run one repeatable example from start to finish."""
    seed = 7
    number_of_days = 1_000
    starting_portfolio_value = 10_000.0

    market, agent = build_default_simulation(seed)
    ending_portfolio_value = run_simulation(
        market,
        agent,
        number_of_days,
        starting_portfolio_value,
    )
    print_report(
        market,
        agent,
        starting_portfolio_value,
        ending_portfolio_value,
        number_of_days,
    )


if __name__ == "__main__":
    main()
