import random
import time
from collections import deque

import matplotlib.pyplot as plt
import numpy as np
import progressbar
import tensorflow.keras as keras
from skimage.transform import resize
from tensorflow.config import list_physical_devices
from tensorflow.keras import Model, Sequential
from tensorflow.keras.layers import Conv2D, Dense, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.python.keras.layers.core import Flatten

import gymhero_env

print("Num GPUs Available: ", len(list_physical_devices('GPU')))

enviroment = gymhero_env.GymHeroEnv()
# enviroment.render()

# print('Number of states: {}'.format(enviroment.observation_space))
# print('Number of actions: {}'.format(enviroment.action_space.n))


class Agent:
    def __init__(self, enviroment, optimizer):

        # Initialize atributes
        self._state_size = (640, 720, 4)
        self._action_size = enviroment.action_space.n
        self._optimizer = optimizer

        self.expirience_replay = deque(maxlen=2000)

        # Initialize discount and exploration rate
        self.gamma = 0.6
        self.epsilon = 0.1

        # Build networks
        self.q_network = self._build_compile_model()
        self.target_network = self._build_compile_model()
        self.alighn_target_model()

    def store(self, state, action, reward, next_state, terminated):
        self.expirience_replay.append(
            (state, action, reward, next_state, terminated))

    def _build_compile_model(self):
        inputs = keras.Input(shape=(192, 216, 3), name='grayscale_img')
        x = Conv2D(filters=16, kernel_size=(8, 8), strides=(
            4, 4), kernel_initializer='random_uniform', bias_initializer='random_uniform', activation='relu')(inputs)
        x = Conv2D(filters=32, kernel_size=(4, 4), strides=(
            2, 2), kernel_initializer='random_uniform', bias_initializer='random_uniform', activation='relu')(x)
        x = Flatten()(x)
        x = Dense(256, kernel_initializer='random_uniform',
                  bias_initializer='random_uniform', activation='relu')(x)
        outputs = Dense(5, kernel_initializer='random_uniform',
                        bias_initializer='random_uniform', activation=None)(x)

        model = keras.Model(inputs=inputs, outputs=outputs)
        # model.summary()

        model.compile(optimizer='rmsprop',
                      loss='categorical_crossentropy', metrics=[])
        return model

    def alighn_target_model(self):
        self.target_network.set_weights(self.q_network.get_weights())

    def act(self, state):
        state = state[np.newaxis, ...]

        if np.random.rand() <= self.epsilon:
            return enviroment.action_space.sample()

        q_values = self.q_network.predict(state)
        return np.argmax(q_values)

    def retrain(self, batch_size):

        minibatch = random.sample(self.expirience_replay, batch_size)

        for state, action, reward, next_state, terminated in minibatch:
            # retrain_time = time.time()
            state = preprocess(state)
            state = state[np.newaxis, ...]

            target = self.q_network.predict(state)

            if terminated:
                target[0][action] = reward
            else:
                next_state = preprocess(next_state)
                next_state = next_state[np.newaxis, ...]

                t = self.target_network.predict(next_state)
                target[0][action] = reward + self.gamma * np.amax(t)
            # fit_time = time.time()
            self.q_network.fit(state, target, epochs=1, verbose=0)
            # print("Fit time", time.time()-fit_time)

            # print("Retrain_time:", time.time()-retrain_time)

    def save_training(self):
        self.q_network.save("result_traning")


def preprocess(image):
    preproc = resize(image, output_shape=(192, 216, 3))
    return preproc


optimizer = Adam(learning_rate=0.01)
agent = Agent(enviroment, optimizer)

batch_size = 16
num_of_episodes = 100
timesteps_per_episode = 3000
agent.q_network.summary()

rewards = []
mean_r_per_episode = []
current_reward = 0.0
start_time = time.time()
for e in range(0, num_of_episodes):
    start_episode_time = time.time()
    # Reset the enviroment
    state = enviroment.reset()
    # Initialize variables
    reward = 0
    terminated = False

    bar = progressbar.ProgressBar(maxval=timesteps_per_episode/10, widgets=[
                                  progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()

    for timestep in range(timesteps_per_episode):
        # start_step_time = time.time()
        # Run Action
        state = preprocess(state)

        action = agent.act(state)

        # Take action
        next_state, reward, terminated, info = enviroment.step(action)
        agent.store(state, action, reward, next_state, terminated)
        state = next_state
        current_reward += reward

        if terminated:
            agent.alighn_target_model()
            rewards.append(reward)
            total_reward = current_reward
            current_reward = 0.0
            break

        if len(agent.expirience_replay) > batch_size:
            agent.retrain(batch_size)

        if timestep % 10 == 0:
            bar.update(timestep/10 + 1)
        # print(time.time()-start_step_time)

    bar.finish()
    mean_r_per_episode.append(np.mean(rewards))

    print("Mean Reward: {}".format(np.mean(rewards)))
    print("Total Reward: {}".format(total_reward))

    if (e + 1) % 10 == 0:
        print("**********************************")
        print("Episode: {}".format(e + 1))
        # enviroment.render()
        print("**********************************")
    print("Episode {} had {} steps and trained in {} seconds.".format(e,
                                                                      timestep, time.time()-start_episode_time))

print("Training done in {} seconds.".format(time.time()-start_time))
agent.save_training()


plt.plot(mean_r_per_episode)
plt.savefig("result.png")
plt.show()
