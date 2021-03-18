import itertools as it
import os
import time
from datetime import datetime
from random import randint, random, sample

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

IMG_HEIGHT = 54
IMG_WIDTH = 48
IMG_CHANNELS = 1

REPLAY_CAPACITY = 1000  # 1E6
NUM_EPOCHS = 2
NUM_TRAIN_EPISODES = 50
NUM_TEST_EPISODES = 1

BATCH_SIZE = 32

discount_factor = 0.99
dropout_prob = 0.3

f = open('log.txt', 'w', buffering=1)


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
    preproc_img = crop(preproc_img, ((150), (0)))
    preproc_img = resize(preproc_img, output_shape=(
        IMG_WIDTH, IMG_HEIGHT), anti_aliasing=False)  # 110 x 84
    # imsave("images/preproc.png", preproc_img)
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


def learn(model, state, target_q):
    loss = model.train_on_batch(x=state, y=target_q)
    return loss


def get_q_values(model, state):
    return model.predict(state)


def get_best_action(model, state):
    s = state.reshape([1, IMG_WIDTH, IMG_HEIGHT, 1])
    v = get_q_values(model, s)
    print(v, file=f)
    return tf.argmax(v[0])


def learn_from_memory(model):
    """ Learns from a single transition (making use of replay memory).
    s2 is ignored if s2_isterminal """

    # Get a random minibatch from the replay memory and learns from it.
    if replayMemory.size > BATCH_SIZE:
        s1, a, s2, isterminal, r = replayMemory.get_sample(BATCH_SIZE)

        q2 = np.max(get_q_values(model, s2), axis=1)
        target_q = get_q_values(model, s1)
        # target differs from q only for the selected action. The following means:
        # target_Q(s,a) = r + gamma * max Q(s2,_) if not isterminal else r
        target_q[np.arange(target_q.shape[0]), a] = r + \
            discount_factor * (1 - isterminal) * q2
        learn(model, s1, target_q)


def perform_learning_step(observation, model, epoch):
    """ Makes an action according to eps-greedy policy, observes the result
    (next state, reward) and learns from the transition"""

    def exploration_rate(epoch):
        """# Define exploration rate change over time"""
        start_eps = 1.0
        end_eps = 0.1
        const_eps_epochs = 0.1 * NUM_EPOCHS  # 10% of learning time
        eps_decay_epochs = 0.6 * NUM_EPOCHS  # 60% of learning time

        if epoch < const_eps_epochs:
            return start_eps
        elif epoch < eps_decay_epochs:
            # Linear decay
            return start_eps - (epoch - const_eps_epochs) / \
                               (eps_decay_epochs - const_eps_epochs) * \
                (start_eps - end_eps)
        else:
            return end_eps

    s1 = preprocess(observation)

    # With probability eps make a random action.
    eps = exploration_rate(epoch)

    if random() <= eps:
        a = randint(0, len(actions) - 1)
    else:
        # Choose the best action according to the network.
        a = get_best_action(model, s1)

    observation, reward, isterminal, info = env.step(actions[a])

    s2 = preprocess(observation) if not isterminal else None

    # Remember the transition that was just experienced.
    replayMemory.add_transition(s1, a, s2, isterminal, reward)

    learn_from_memory(model)

    return observation, reward, isterminal, info


if __name__ == '__main__':

    env = gh_env.GHEnv()
    replayMemory = ReplayMemory(REPLAY_CAPACITY)

    num_actions = env.action_space.n  # Muda de acordo com a dificuldade
    train_scores_list = []
    test_scores_list = []
    actions = [list(a) for a in it.product([0, 1], repeat=num_actions)]
    model = create_network(len(actions))
    model.summary()

    time_start = time.time()

    for epoch in range(NUM_EPOCHS):
        print("\nEpoch %d\n-------" % (epoch + 1))

        print("Training...")
        train_scores = []
        train_completion = []
        training_time = time.time()

        for training_episode in trange(NUM_TRAIN_EPISODES, leave=True):
            episode_reward = 0.0
            done = False
            observation = env.reset()

            while not done:
                observation, reward, done, info = perform_learning_step(
                    observation, model, epoch)
                episode_reward += reward
            # print("Train Completion: %.2f%" % info["hitted_notes_count"]/env.n_notes)
            train_completion.append(info["hitted_notes_count"]/env.n_notes)
            train_scores.append(episode_reward)

        train_elapsed_time = time.time() - training_time
        train_completion = np.array(train_completion)
        train_scores = np.array(train_scores)
        train_scores_list.append(train_scores.mean())
        print("Results: mean: %.1f±%.1f," % (train_scores.mean(), train_scores.std()),
              "min: %.1f," % train_scores.min(), "max: %.1f," % train_scores.max(), "Mean song accuracy: %.2f%." % train_completion.mean()*100)

        if epoch % 5 == 0:
            model.save(os.path.join("..", "agents",
                                    "agente_epoch_{}_{}".format(epoch, datetime.now().strftime("%d-%m-%Y-%H-%M"))))

        print("\nTesting...")
        test_scores = []
        test_completion = []
        testing_time = time.time()

        for testing_episode in trange(NUM_TEST_EPISODES, leave=True):
            episode_reward = 0.0
            done = False
            observation = env.reset()

            while not done:
                state = preprocess(observation)
                action = get_best_action(model, state)
                observation, reward, done, info = env.step(actions[action])
                episode_reward += reward
            # print("Test Completion: %.2f%" % info["hitted_notes_count"]/env.n_notes)
            test_completion.append(info["hitted_notes_count"]/env.n_notes)
            test_scores.append(episode_reward)

        test_elapsed_time = time.time() - testing_time
        test_completion = np.array(test_completion)
        test_scores = np.array(test_scores)
        test_scores_list.append(test_scores.mean())
        print("Results: mean: %.1f±%.1f," % (test_scores.mean(), test_scores.std()),
              "min: %.1f" % test_scores.min(), "max: %.1f" % test_scores.max(), "Mean song accuracy: %.2f%." % test_completion.mean()*100)

        print("Total elapsed time: %.2f minutes" %
              ((time.time() - time_start) / 60.0))
    model.save(os.path.join("..", "agents",
                            "agente_final_{}".format(datetime.now().strftime("%d-%m-%Y-%H-%M"))))
    print("Train Scores: {}".format(train_scores_list))
    print("Test Scores: {}".format(test_scores_list))
    print("======================================")
    print("Training finished.")

    env.close()

    plt.plot(np.array(train_scores_list))
    plt.plot(np.array(test_scores_list))
    plt.show()
f.close()
