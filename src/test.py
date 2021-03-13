import gh_env

env = gh_env.GHEnv()
obs = env.reset()
done = False
total_reward = 0.0

while not done:
    action = env.action_space.sample()
    obs, reward, done, _ = env.step(action)
    total_reward += reward

print("Recompensa total do agente: {}.".format(total_reward))
