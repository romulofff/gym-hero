import pygame


class Action:

    def __init__(self):
        self.keys = 'asdfg'  # could be a list, tuple or dict instead
        self.actions = [False, False, False, False, False]

    def __call__(self):
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                for n, key in enumerate(self.keys):
                    if event.key == getattr(pygame, f"K_{key}"):
                        if self.actions[n]:
                            self.actions[n] = -1
                        else:
                            self.actions[n] = True

            if event.type == pygame.KEYUP:
                for n, key in enumerate(self.keys):
                    if event.key == getattr(pygame, f"K_{key}"):
                        self.actions[n] = False

        aux = []
        for action in self.actions:
            if action == -1:
                aux.append(False)
            else:
                aux.append(action)

        return aux
