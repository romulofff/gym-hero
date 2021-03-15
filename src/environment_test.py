import numpy as np
import gh_env

env = gh_env.GHEnv()
obs = env.reset()
done = False
total_reward = 0.0

rewards = []
for i in range(1000):
    done = False
    while not done:
        action = env.action_space.sample()
        obs, reward, done, _ = env.step(action)
        total_reward += reward
        # print(total_reward)

    # print("Recompensa total do agente: {}.".format(total_reward))

    
    rewards.append(total_reward)
    # print(rewards)
    total_reward = 0.0
    # print(total_reward)
    obs = env.reset()

print(np.mean(rewards)) 
