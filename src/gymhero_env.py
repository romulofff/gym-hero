import time
import json
import gym

from game import *


class GymHeroEnv(gym.Env):

    def __init__(self):
        self.difficulty_dict = {
            "Easy": 3,
            "Medium": 4,
            "Hard": 5,
            "Expert": 5
        }
        self.args = arg_parser()
        self.action_space = gym.spaces.MultiBinary(
            self.difficulty_dict[self.args.difficulty])
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(
            SCREEN_WIDTH, SCREEN_HEIGHT, 3), dtype=np.uint8)
        with open(self.args.config) as f:
            self.config = json.load(f)
        self.done = False

    def step(self, action):
        """Run one timestep of the environment's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this environment's state.

        Accepts an action and returns a tuple (observation, reward, done, info).

        Args:
            action (object): an action provided by the agent

        Returns:
            observation (object): agent's observation of the current environment
            reward (float) : amount of reward returned after previous action
            done (bool): whether the episode has ended, in which case further step() calls will return undefined results
            info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning)
        """

        reward = 0
        # print("\n", action)
        if isinstance(action, list):
            action_vec = action
        elif isinstance(action, np.ndarray):
            action_vec = action
        else:
            action_vec = [False, False, False, False, False]
            action_vec[action] = True
        # print(action_vec)
        self.done, reward = update(self.score, 0, action_vec, self.song,
                                   self.visible_notes_list, self.all_notes_list, self.Buttons, self.clock, self.config['reward'])
        observation = get_obs(self.screen, self.score,
                              self.buttons_sprites_list, self.visible_notes_list)
        return observation, reward, self.done, {"hitted_notes_count": self.score.total_hits}

    def reset(self):
        """Resets the environment to an initial state and returns an initial
        observation.

        Note that this function should not reset the environment's random
        number generator(s); random variables in the environment's state should
        be sampled independently between multiple calls to `reset()`. In other
        words, each call of `reset()` should yield an environment suitable for
        a new episode, independent of previous episodes.

        Returns:
            observation (object): the initial observation.
        """

        self.done = False
        pygame.init()
        pygame.display.set_caption('Gym Hero')
        if self.args.screen:
            self.screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT))
        else:
            self.screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.HIDDEN)
        imgs, img_button = load_imgs()

        self.song, notes = load_chart(self.args.chart_file, imgs, difficulty=self.args.difficulty)
        self.n_notes = len(notes)
        self.all_notes_list = pygame.sprite.Group()
        self.buttons_sprites_list = pygame.sprite.Group()
        self.visible_notes_list = pygame.sprite.Group()

        self.Buttons = create_button_list(
            img_button, self.buttons_sprites_list, difficulty=self.difficulty_dict[self.args.difficulty])

        for note in notes:
            self.all_notes_list.add(note)
            # buttons_sprites_list.add(note)

        self.score = Score(
            decrease_mode=self.args.decrease_score, points=self.config['points'])
        self.clock = pygame.time.Clock()
        return get_obs(self.screen, self.score, self.buttons_sprites_list, self.visible_notes_list)

    def close(self):
        pygame.quit()


if __name__ == '__main__':
    print("Start")
    start_time = time.time()
    env = GymHeroEnv()
    env.reset()

    done = False
    total_reward = 0.0
    while not done:
        action = env.action_space.sample()
        print(action)
        state, reward, done, info = env.step(action)
        # print(reward, done, info)

        total_reward += reward

    print("Recompensa total do agente: {}.".format(total_reward))

    print("Tempo total: {} segundos.".format(time.time()-start_time))
