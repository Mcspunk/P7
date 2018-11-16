import random
import math
import LeagueDrafter_RESTAPI.initial_win_pred as NN


class Suggestion:
    def __init__(self, champ, score, champ2=None):
        self.champ = champ
        self.score = score
        self.champ2 = champ2


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

    def mcts_score(self):
        return self.value/self.visited


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

    def get_turn(self):
        return len(self.ally_team) + len(self.enemy_team)


class Mcts:

    def __init__(self, banned, input_state, exploration_term):
        self.banned_champs = banned
        self.allowed_champions = self.get_allowed_champions(self.banned_champs)
        self.root_node = Node(self.allowed_champions, input_state)
        self.exploration_term = exploration_term


    def run_mcts(self,iterations, node, pair_of_champions, suggested_amount=10):
        x = 0
        current_node = node
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
                if current_node.depth == 10:
                    simulation_result = self.simulate(current_node)
                    self.backprop(simulation_result, current_node)
                    current_node = node
                    x += 1
        return self.get_suggestions(node, pair_of_champions, suggested_amount)

    def get_suggestions(self, node, pair_of_champions, suggested_amount):
        if pair_of_champions and self.is_dual_return(node.state):
            suggestions = []
            for i in self.root_node.children:
                for j in i.children:
                    suggestions.append(Suggestion(j.champ, j.mcts_score(), i.champ))
            suggestions.sort(key=lambda x: x.score, reverse=True)
            return suggestions[:suggested_amount]

        else:
            suggestions = []
            result = list.copy(self.root_node.children)
            result.sort(key=lambda x: x.mcts_score(), reverse=True)
            for child in result:
                suggestions.append(Suggestion(child.champ, child.mcts_score()))
            return suggestions[:suggested_amount]

    def post_draft_turn(self, state:State, pair_of_champs, banned_champs, iterations):
        self.banned_champs = banned_champs
        self.root_node = self.recall_subtree(state, self.root_node)
        suggestions = self.run_mcts(iterations, self.root_node, pair_of_champs)
        return suggestions

    def is_dual_return(self, state:State):
        if state.ally_starting:
            if state.get_turn() == 3 or state.get_turn() == 7:
                return True
            else:
                return False
        else:
            if state.get_turn() == 1 or state.get_turn() == 5:
                return True
            else:
                return False

    def get_allowed_champions(self, banned_champs, already_chosen = None):
        champions = set(range(0, 141))
        if already_chosen is None:
            return champions - banned_champs
        else:
            return champions - banned_champs - set(already_chosen)

    def select(self, node):
        if len(node.possible_actions) > 0:
            chosen_action = self.choose_action(node.possible_actions)
            node.possible_actions.remove(chosen_action)
            return chosen_action
        else:
            best_score = - float("inf")
            most_promising_child = None

            for child in node.children:
                score = self.UCT(child)
                if best_score < score:
                    best_score = score
                    most_promising_child = child
        return most_promising_child

    def UCT(self, node):
        return (float(node.value) / float(node.visited)) + (float(self.exploration_term) * math.sqrt(math.log(float(node.parent.visited))/float(node.visited)))


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
        copied_node = Node(node.possible_actions, node.state, node.parent, node.champ)
        while len(copied_node.state.enemy_team) <5 or len(copied_node.state.ally_team) < 5:
            action = random.choice(tuple(copied_node.possible_actions))
            copied_node.possible_actions.remove(action)
            copied_node.state = self.find_new_state(action, copied_node)
        input_list = list(copied_node.state.ally_team)
        input_list.extend(list(copied_node.state.enemy_team))
        return NN.predictTeamComp(input_list)

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

    def find_state_at_turn(self, node, champ):
        for child in node.children:
            if child.champ == champ:
                return child

    def recall_subtree(self, state:State, root=None):
        search_depth = state.get_turn()
        choices = []
        if state.ally_starting:
            first_pick_team = list(state.ally_team)
            last_pick_team = list(state.enemy_team)
        else:
            first_pick_team = list(state.enemy_team)
            last_pick_team = list(state.ally_team)

        alternate = True
        for i in range(0, search_depth):
            if i == 0:
                choices.append(first_pick_team.pop(0))
                alternate = True
            elif i == 9:
                choices.append(last_pick_team.pop(0))
            elif i % 2 == 1:
                if alternate:
                    choices.append(last_pick_team.pop(0))
                else:  choices.append(first_pick_team.pop(0))
            else:
                if alternate:
                    choices.append(last_pick_team.pop(0))
                    alternate = False
                else:
                    choices.append(first_pick_team.pop(0))
                    alternate = True

        current_turn = root.depth
        node = root
        for turn in range(current_turn, search_depth):
            node = self.find_state_at_turn(node, choices[turn])
            if node is None:
                node = Node(self.get_allowed_champions(self.banned_champs, choices), state)
                break
        node.parent = None
        return node


listemedbann = set(range(1, 10))
root_state = State(None, True)
MctsInstance = Mcts(listemedbann, root_state, 2)
test_state = State()
test_state.ally_team = [11,14,16,17]
test_state.enemy_team = [12, 13, 22, 23, 24]
test_state.ally_starting = False
result = MctsInstance.post_draft_turn(test_state, True, listemedbann, 5000)

print(result)


