
from copy import deepcopy


class Board(object):
    def __init__(self, state):
        self.state = deepcopy(state)

    def update_state(self, new_state):
        self.state = new_state

