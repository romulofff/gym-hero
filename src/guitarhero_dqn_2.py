import os
import itertools as it
from random import randint, random, sample
from time import sleep, time

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import tensorflow.keras as keras
from numpy.core.fromnumeric import reshape
from skimage import color
from skimage.io import imsave
from skimage.transform import resize
from skimage.util import crop
from tensorflow.keras import layers
from tensorflow.keras.layers import Conv2D, Dense, Flatten
from tensorflow.keras.models import Sequential
from tqdm import trange

import gh_env

dropout_prob = 0.3

gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)


def preprocess(image):  # color 210 x 160
    preproc_img = color.rgb2gray(image)  # gray 210 x 160
    preproc_img = crop(preproc_img, ((75), (0)))
    preproc_img = resize(preproc_img, output_shape=(
        96, 108), anti_aliasing=False)  # 110 x 84
    return preproc_img


def create_network(available_actions_count):
    inputs = keras.Input(shape=(IMG_WIDTH, IMG_HEIGHT, 1), name='frame')
    x = layers.Conv2D(filters=32, kernel_size=(4, 4), strides=(2, 2), padding='same',
                      kernel_initializer='glorot_normal', bias_initializer=tf.constant_initializer(0.1), activation='relu')(inputs)
    x = layers.Conv2D(filters=64, kernel_size=(4, 4), strides=(2, 2), padding='same',
                      kernel_initializer='glorot_normal', bias_initializer=tf.constant_initializer(0.1), activation='relu')(x)
    x = layers.Flatten()(x)
    x = layers.Dense(512, kernel_initializer='glorot_normal',
                     bias_initializer=tf.constant_initializer(0.1), activation='relu')(x)
    x = layers.Dropout(dropout_prob)(x)
    q = layers.Dense(available_actions_count, kernel_initializer='glorot_normal',
                     bias_initializer=tf.constant_initializer(0.1), activation=None)(x)

    model = keras.Model(inputs=inputs, outputs=q, name='vizdoom_agent_model')

    model.compile(optimizer='adam', loss='mse')

    return model


EPSILON = 0.1


def choose_action(state, episode):
    if random() < EPSILON:
        return randint(0, len(actions) - 1)

    state = np.array(state)
    state = state[np.newaxis, ...]
    q_values = model.predict(state)

    return np.argmax(q_values[0])


IMG_HEIGHT = 108
IMG_WIDTH = 96
IMG_CHANNELS = 1


class ReplayMemory:
    def __init__(self, capacity):
        channels = 1
        state_shape = (capacity, IMG_WIDTH, IMG_HEIGHT, channels)
        self.s1 = np.zeros(state_shape, dtype=np.float32)
        self.s2 = np.zeros(state_shape, dtype=np.float32)
        self.a = np.zeros(capacity, dtype=np.int32)
        self.r = np.zeros(capacity, dtype=np.float32)
        self.isterminal = np.zeros(capacity, dtype=np.float32)

        self.capacity = capacity
        self.size = 0
        self.pos = 0

    def add_transition(self, s1, action, s2, isterminal, reward):
        self.s1[self.pos, :, :, 0] = s1
        self.a[self.pos] = action
        if not isterminal:
            self.s2[self.pos, :, :, 0] = s2
        self.isterminal[self.pos] = isterminal
        self.r[self.pos] = reward

        self.pos = (self.pos + 1) % self.capacity
        self.size = min(self.size + 1, self.capacity)

    def get_sample(self, sample_size):
        i = sample(range(0, self.size), sample_size)
        return self.s1[i], self.a[i], self.s2[i], self.isterminal[i], self.r[i]


REPLAY_CAPACITY = 1000  # 1E6
NUM_STEPS = 10000  # 10E6
NUM_EPISODES = 100

BATCH_SIZE = 2

discount_factor = 0.99


env = gh_env.GHEnv()
replayMemory = ReplayMemory(REPLAY_CAPACITY)

done = False
observation = env.reset()

mean_r_per_episode = []
rewards = []
current_reward = 0.0
num_actions = env.action_space.n  # Muda de acordo com a dificuldade


actions = [list(a) for a in it.product([0, 1], repeat=num_actions)]
model = create_network(len(actions))
model.summary()

for episode in range(NUM_EPISODES):
    # print('episode: {}\n'.format(episode))
    for _ in trange(NUM_STEPS):
        start_time = time()
        old_state = preprocess(observation)
        action = choose_action(old_state, episode)
        observation, reward, done, info = env.step(actions[action])
        current_reward += reward
        new_state = preprocess(observation) if not done else None
        replayMemory.add_transition(
            old_state, action, new_state, int(done), reward)

        if replayMemory.size > BATCH_SIZE:
            s1, a, s2, terminal, r = replayMemory.get_sample(BATCH_SIZE)
            q2 = np.max(model.predict(s2), axis=1)
            target_q = model.predict(s1)

            # new_value = reward + discount_factor * q2 * (1 - terminal)
            target_q[np.arange(target_q.shape[0]), a] = reward + \
                discount_factor * q2 * (1 - terminal)
            model.train_on_batch(x=s1, y=target_q)

        if done:
            observation = env.reset()
            rewards.append(current_reward)
            current_reward = 0.0
            #print(' --- done --- ')
        # print("Tempo:",time.time()-start_time)
    # print(rewards)
    mean_r_per_episode.append(np.mean(rewards))
    print('mean r: ' + str(np.mean(rewards)))
    rewards = []

    if episode % 5 == 0:
        model.save(os.path.join("..", "agents",
                                "agente_ep_{}_{}".format(episode, time())))

env.close()


plt.plot(mean_r_per_episode)
plt.show()
