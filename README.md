# gym-stock
Minimal example stock gym for Open AI

## Observation space
Opening price for each stock

Ex Stocks:["MSFT","AAPL","GOOG","FB"]
Observation Space: [100,2000,10000,5000]

## Actions Supported

3 actions for each stock
Hold Buy Sell (0,1,2)

## Setup
pip install -e gym-stock


## Tensorforce Example

```
from tensorforce import Agent, Environment
from gym.envs.registration import register
import gym
import gym_stock


# Custom environment
environment = Environment.create(
    environment='gym',level='Stock-v1', max_episode_timesteps=500
)

# PPO Agent
agent = Agent.create(
    agent='ppo', environment=environment, batch_size=10, learning_rate=1e-3
)


# Train for 10 episodes
for _ in range(100):
    states = environment.reset()
    terminal = False
    while not terminal:
        actions = agent.act(states=states)
        states, terminal, reward = environment.execute(actions=actions)
        agent.observe(terminal=terminal, reward=reward)

# Evaluate for 10 episodes
sum_rewards = 0.0
for _ in range(100):
    states = environment.reset()
    internals = agent.initial_internals()
    terminal = False
    while not terminal:
        actions, internals = agent.act(
            states=states, internals=internals,
            independent=True, deterministic=True
        )
        states, terminal, reward = environment.execute(actions=actions)
        sum_rewards += reward

print('Mean episode reward:', sum_rewards / 10)

# Close agent and environment
agent.close()
environment.close()

print('Mean episode reward:', sum_rewards)

# Close agent and environment
agent.close()
environment.close()
```
