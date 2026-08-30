# Multi-Armed Bandit for Trading Strategy Selection

Suppose you have several trading strategies, but you can run only one each day. Do you keep using the strategy that has paid the most so far, or test another one that might turn out better?

That choice is the multi-armed bandit problem. This project teaches one solution, called epsilon-greedy, by applying it to a small simulated financial market.

## What the program models

The example contains three strategies:

| Strategy | Hidden average daily return | Daily volatility |
| --- | ---: | ---: |
| Trend Following | 0.080% | 1.000% |
| Mean Reversion | 0.050% | 0.700% |
| Defensive | 0.020% | 0.300% |

Think of each strategy as one arm of the bandit. On every simulated trading day, the agent follows this loop:

1. Pick a strategy.
2. Observe only that strategy's return.
3. Update its estimated average return.
4. Repeat with slightly less random exploration.

The hidden averages let us check the agent's work after the simulation. The agent can't read them while learning.

## Exploration and exploitation

Epsilon is the chance that the agent explores. An epsilon of `1.0` means it always tries a random strategy; an epsilon of `0.05` means it explores on roughly 5 out of every 100 days.

When the agent doesn't explore, it exploits what it has learned by choosing the strategy with the highest estimated average return. Its estimate is a running average, so every observed day counts without storing a long return history:

```text
new estimate = old estimate + (new return - old estimate) / number of observations
```

## Run it

You need Python 3.10 or newer. The project uses only Python's standard library, so there are no packages to install.

```bash
python3 main.py
```

The random seed is fixed, which makes the example repeatable. A run prints the simulated portfolio value, the return estimates, and how often the agent selected each strategy.

```text
Simulated trading days: 1000
Starting portfolio: $10,000.00
Ending portfolio:   $28,395.10

Strategy         | Hidden mean | Learned mean | Days selected
-----------------|-------------|--------------|--------------
Trend Following  |      0.080% |       0.120% |           863
Mean Reversion   |      0.050% |       0.039% |            60
Defensive        |      0.020% |       0.038% |            77

Agent's preferred strategy: Trend Following
```

## Read the code

The program lives in [`main.py`](main.py):

- `MarketStrategy` describes one simulated strategy's average return and volatility.
- `SimulatedMarket` reveals a return only for the selected strategy.
- `EpsilonGreedyAgent` chooses strategies and learns their running averages.
- `run_simulation` connects the market and the agent for a chosen number of days.

The small interface matters. The learning loop only asks the market for one return and tells the agent what happened; it doesn't need to know how either class works inside.

[`test_main.py`](test_main.py) checks the running-average math and confirms that one market choice happens per simulated day. Run it with:

```bash
python3 -m unittest -v
```

## Try your own experiment

Edit the values inside `build_default_simulation()` to add strategies or change their return patterns. You can also change the seed, number of days, or starting portfolio value inside `main()`.

Try making two strategies almost equal. The agent will need more observations to tell them apart. Then raise `minimum_epsilon` and watch it keep exploring even after it finds a favorite.

## What this does not prove

This is a teaching simulation, not a trading system or financial advice. It assumes that each strategy's average return and volatility stay fixed, daily returns follow a normal distribution, and switching strategies costs nothing. Real markets change over time; they also include fees, slippage, taxes, liquidity limits, and losses that don't fit a normal distribution.

A production research project would need historical out-of-sample testing, transaction costs, risk limits, and a model that can react when market conditions change.
