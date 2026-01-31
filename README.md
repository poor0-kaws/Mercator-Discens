# Reinforcement Learning: Multi-Armed Bandit

This project implements a simple **Multi-Armed Bandit** agent from scratch using Python. It demonstrates the fundamental trade-off between **Exploration** (trying new things) and **Exploitation** (sticking with what works) in Reinforcement Learning.

## 🧠 Core Concepts

### The Environment (`Casino`)
- Simulates a row of 3 slot machines ("levers").
- Each lever has a secret, fixed probability of winning (a "true probability").
- When pulled, a lever returns a `1` (Win) or `0` (Loss) based on this probability.

### The Agent
- **Goal**: Find and pull the lever with the highest win rate to maximize rewards.
- **Strategy**: **Epsilon-Greedy**
    - **Exploration ($\epsilon$)**: With probability $\epsilon$, the agent picks a random lever to gather data.
    - **Exploitation**: Otherwise, it picks the lever with the highest estimated win rate so far.
    - **Decay**: Over time, $\epsilon$ decreases, meaning the agent explores less and exploits more as it learns.

## 🛠️ Code Structure

- **`Casino` Class**: initialized with `num_levers=3`. Randomly assigns a "true probability" to each lever.
- **`Agent` Class**:
    - `choose_action()`: Decides whether to explore or exploit.
    - `learn()`: Updates the estimated probability of the chosen lever based on the result.
    - Formula: $Estimate = \frac{Total Wins}{Total Attempts}$

## 🚀 How to Run

1. Ensure you have NumPy installed:
   ```bash
   pip install numpy
   ```

2. Run the simulation:
   ```bash
   python main.py
   ```

## 📊 Sample Output

After 1000 episodes (pulls), the program prints a comparison between the **True Probability** (hidden from the agent) and the **Agent's Learned Probability**.

```text
Slot Machine 1 | True Probability: 0.12 | Agent Probability: 0.15 | Total Attempts: 64
Slot Machine 2 | True Probability: 0.78 | Agent Probability: 0.76 | Total Attempts: 852
Slot Machine 3 | True Probability: 0.34 | Agent Probability: 0.31 | Total Attempts: 84
```

*Note: The agent successfully identifies Slot Machine 2 as the best option and allocates the vast majority of its attempts to it.*
