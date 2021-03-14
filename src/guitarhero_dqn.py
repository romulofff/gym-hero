import random
from collections import deque

import gym
import numpy as np
import progressbar
import tensorflow.keras as keras
from tensorflow.keras import Model, Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.python.keras.layers.core import Flatten

import gh_env

enviroment = gh_env.GHEnv()
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
        inputs = keras.Input(shape=(640,720,3), name='grayscale_img')
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
            state = state[np.newaxis, ...]
            
            target = self.q_network.predict(state)

            if terminated:
                target[0][action] = reward
            else:
                next_state = next_state[np.newaxis, ...]

                t = self.target_network.predict(next_state)
                target[0][action] = reward + self.gamma * np.amax(t)

            self.q_network.fit(state, target, epochs=1, verbose=0)


optimizer = Adam(learning_rate=0.01)
agent = Agent(enviroment, optimizer)

batch_size = 32
num_of_episodes = 100
timesteps_per_episode = 1000
agent.q_network.summary()

for e in range(0, num_of_episodes):
    # Reset the enviroment
    state = enviroment.reset()
    
    # Initialize variables
    reward = 0
    terminated = False

    bar = progressbar.ProgressBar(maxval=timesteps_per_episode/10, widgets=[
                                  progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()

    for timestep in range(timesteps_per_episode):
        # Run Action
        action = agent.act(state)

        # Take action
        next_state, reward, terminated, info = enviroment.step(action)
        agent.store(state, action, reward, next_state, terminated)
        state = next_state

        if terminated:
            agent.alighn_target_model()
            break

        if len(agent.expirience_replay) > batch_size:
            agent.retrain(batch_size)

        if timestep % 10 == 0:
            bar.update(timestep/10 + 1)

    bar.finish()
    if (e + 1) % 10 == 0:
        print("**********************************")
        print("Episode: {}".format(e + 1))
        enviroment.render()
        print("**********************************")
