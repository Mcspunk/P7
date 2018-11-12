import random
import math
from array import *

class Node:

    def __init__(self, possible_actions, state, parent=None, champ=None):
        self.visited = 0
        self.value = 0
        self.parent = parent

        if self.parent is not None:
            self.depth = parent.depth + 1
            set_copy = set.copy(parent.tree_path)
            set_copy.add(champ)
            self.tree_path = set_copy

        else:
            self.depth = 0
            self.tree_path = set()
        self.state = state
        self.possible_actions = list(possible_actions) #from parent
        self.children = []
        self.champ = champ


class State:

    def __init__(self, parent=None, ally_starting=None):
        if parent is None:
            self.ally_team = []
            self.enemy_team = []
            self.ally_starting = ally_starting
        else:
            self.ally_team = list.copy(parent.ally_team)
            self.enemy_team = list.copy(parent.enemy_team)
            self.ally_starting = parent.ally_starting

class Mcts:

    def __init__(self, banned, input_state, exploration_term, starts):
        self.allowed_champions = self.get_allowed_champions(banned)
        self.root_node = Node(self.allowed_champions, input_state)
        self.exploration_term = exploration_term
        self.user_team_starts = starts


    def run_mcts(self,iterations):
        x=0
        current_node = self.root_node
        while x < iterations:
            selected_action = self.select(current_node)
            if not isinstance(selected_action, Node):
                new_node = self.expand(current_node, selected_action)
                simulation_result = self.simulate(new_node)
                self.backprop(simulation_result, new_node)
                x += 1
                continue
            else:
                current_node = selected_action
        best_choice = None
        best_val = 0
        for i in self.root_node.children:
            if i.value/i.visited > best_val:
                best_val = i.value/i.visited
                best_choice = i
        return best_val

    def get_allowed_champions(self, banned_champs):
        champions = set(range(1, 142))
        return champions - banned_champs

    def select(self, node):
        if len(node.possible_actions) > 0:
            chosen_action = self.choose_action(node.possible_actions)
            node.possible_actions.remove(chosen_action)
            return chosen_action
        else:
            best_score = - float("inf")
            most_promising_child = None

            for child in node.children:
                score = (float(child.value) / float(child.visited)) + (float(self.exploration_term) * math.sqrt(math.log(float(child.parent.visited))/float(child.visited)))
                if best_score < score:
                    best_score = score
                    most_promising_child = child
        return most_promising_child


    def choose_action(self, possible_actions):
        chosen_one = random.choice(tuple(possible_actions))
        return chosen_one

    def expand(self, current_node, action):
        new_state = self.find_new_state(action, current_node)
        tree_path = set.copy(current_node.tree_path)
        tree_path.add(action)
        possible_actions = self.allowed_champions - tree_path
        new_node = Node(possible_actions, new_state, current_node, action)
        current_node.children.append(new_node)
        return new_node

    def find_new_state(self, action, parent):

        new_state = State(parent.state)

        if len(new_state.enemy_team) > len(new_state.ally_team):
            insert_ally = True
        elif len(new_state.enemy_team) < len(new_state.ally_team):
            insert_ally = False
        else:
            if parent.state.ally_starting:
                if len(new_state.ally_team) % 2 == 0:
                    insert_ally = True
                else:
                    insert_ally = False
            else:
                if len(new_state.ally_team) % 2 == 0:
                    insert_ally = False
                else:
                    insert_ally = True

        if insert_ally:
            new_state.ally_team.append(action)
        else:
            new_state.enemy_team.append(action)
        return new_state


    def simulate(self, node):
        result = 0;
        state = State(node.state)
        copied_node = Node(node.possible_actions, node.state, node.parent, node.champ)
        while len(copied_node.state.enemy_team) <5 or len(copied_node.state.ally_team) < 5:
            action = random.choice(tuple(copied_node.possible_actions))
            copied_node.possible_actions.remove(action)
            copied_node.state = self.find_new_state(action, copied_node)


        #kald til NN her!
        result = random.uniform(0.0, 1.0)
        return result

    def backprop(self, result, node):
        node_to_update = node
        while node_to_update.parent is not None:
            node_to_update.visited += 1
            node_to_update.value +=result
            node_to_update = node_to_update.parent
        #updates root node below
        node_to_update.visited += 1
        node_to_update.value += result
        return None


listemedbann = set(range(1, 130))
root_state = State(None, True)
MctsInstance = Mcts(listemedbann, root_state, 2, True)
print(MctsInstance.run_mcts(10000))


