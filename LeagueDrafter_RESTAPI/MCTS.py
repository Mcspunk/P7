import random
import math
from array import *

class Node:

    def __init__(self, possible_children, state, parent=None, champ=None):
        self.visited = 0
        self.value = 0
        self.parent = parent

        if self.parent is not None:
            self.depth = parent.depth + 1
        else:
            self.depth = 0

        self.state = state
        self.unvisited_children = possible_children #from parent



        self.champ = champ


class State:

    def __init__(self):
        self.ally1
        self.ally2
        self.ally3
        self.ally4
        self.ally5

        self.enemy1
        self.enemy2
        self.enemy3
        self.enemy4
        self.enemy5

        self.ally_starting


class Mcts:

    def __init__(self, banned, input_state, exploration_term, starts):
        self.root_node = Node(input_state, self.get_allowed_champions(banned))
        self.exploration_term = exploration_term
        self.user_team_starts = starts

    def get_allowed_champions(self, banned_champs):
        champions = set(range(1, 142))
        return champions - banned_champs

    def select(self, node):
        if len(node.possible_actions) > 0:
            remaining_actions, chosen_action = self.choose_action(node.possible_actions)
            return remaining_actions, chosen_action
        else:
            best_score = - float("inf")
            most_promising_child = None

            for child in node.children:
                score = (float(child.value) / float(child.visited)) + (float(self.exploration_term) * math.sqrt(math.log(float(child.parent.visit))/float(child.visit)))
                if best_score < score:
                    best_score = score
                    most_promising_child = child
        return None, most_promising_child


    def choose_action(self, possible_actions):
        chosen_one = random.choice(possible_actions)
        smaller_list = possible_actions.remove(chosen_one)
        return smaller_list, chosen_one

    def expand(self, parent, action, possible_actions,):
        new_state = find_new_state(action, parent)
        new_node = Node(state, possible_children, parent)

    def find_new_state(self, action, parent):
        new_state = parent.state


        return new_state

    # måske skulle vores expand bare lave siblings???
    def get_siblings(self):
        siblings = self.children
        siblings.remove(self)
        return siblings


    def simulate(self):
        random_choices = list()
        while next.depth <= 10:  #10 champions
            next = random.choice(self.children)
            random_choices.__add__(next)
        return

  #  def select(self):

listemedbann = set([1])
MctsInstance = Mcts(listemedbann, None, 2)

print(MctsInstance.allowed_champions)


