import math
import random
import json
import time
import LeagueDrafter_RESTAPI.initial_win_pred as NN
import LeagueDrafter_RESTAPI.db_connection as db
EXPLORATION_TERM = 2


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


def post_draft_turn(json, session_id):

    state, banned_champs = game_state_from_json(json)
    tree = db.loadTree(session_id)
    root_node = recall_subtree(state, tree, banned_champs)
    allowed_champions = list.copy(root_node.possible_actions)
    suggestions, reduced_root = run_mcts(15, root_node, True, allowed_champions)
    db.saveTree(reduced_root, session_id) #Venter sådan set på at træ er gemt til databasen før vi returnerer suggestions
    json_suggestions = suggestions_to_json(suggestions)
    return json_suggestions


def run_mcts(running_time, root, pair_of_champions, allowed_champions, suggested_amount=10):

    now = time.time()
    run_till = now.__add__(running_time)
    current_node = root
    while run_till > time.time():
        selected_action = select(current_node)
        if not isinstance(selected_action, Node):
            new_node = expand(current_node, selected_action, allowed_champions)
            match_vector = simulate(new_node)
            simulation_result = NN.predictTeamComp(match_vector)
            backprop(simulation_result, new_node)
        else:
            current_node = selected_action
            if current_node.depth == 10:
                match_vector = simulate(current_node)
                simulation_result = NN.predictTeamComp(match_vector)
                backprop(simulation_result, current_node)
                current_node = root

    suggestions = get_suggestions(root, pair_of_champions, suggested_amount)
    reduced_root = reduce_root_to_suggestions(root,suggestions)

    return suggestions, reduced_root


def reduce_root_to_suggestions(root, suggestions):
    good_children = list()
    for i in root.children:
        for j in suggestions:
            if i.champ == j.champ or i.champ == j.champ2:
                good_children.append(i)
    root.children = good_children
    return root

def get_suggestions(root, pair_of_champions, suggested_amount):
    if pair_of_champions and is_dual_return(root.state):
        suggestions = []
        for i in root.children:
            for j in i.children:
                suggestions.append(Suggestion(j.champ, j.mcts_score(), i.champ))
        suggestions.sort(key=lambda x: x.score, reverse=True)
        return suggestions[:suggested_amount]

    else:
        suggestions = []
        result = list.copy(root.children)
        result.sort(key=lambda x: x.mcts_score(), reverse=True)
        for child in result:
            suggestions.append(Suggestion(child.champ, child.mcts_score()))
        return suggestions[:suggested_amount]


def is_dual_return(state: State):
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


def get_allowed_champions(banned_champs=None, already_chosen=None):
    champions = set(range(0, 141))
    if banned_champs is None:
        if already_chosen is None:
            return champions
        else:
            return champions - set(already_chosen)
    else:
        if already_chosen is None:
            return champions - banned_champs
        else:
            return champions - banned_champs - set(already_chosen)


def select(node):
    if len(node.possible_actions) > 0:
        chosen_action = choose_action(node.possible_actions)
        node.possible_actions.remove(chosen_action)
        return chosen_action
    else:
        best_score = - float("inf")
        most_promising_child = None

        for child in node.children:
            score = UCT(child)
            if best_score < score:
                best_score = score
                most_promising_child = child
    return most_promising_child


def UCT(node):
    return (float(node.value) / float(node.visited)) + (
                float(EXPLORATION_TERM) * math.sqrt(math.log(float(node.parent.visited)) / float(node.visited)))


def choose_action(possible_actions):
    chosen_one = random.choice(tuple(possible_actions))
    return chosen_one


def expand(current_node, action, allowed_champions):
    new_state = find_new_state(action, current_node)
    tree_path = set.copy(current_node.tree_path)
    tree_path.add(action)
    possible_actions = set(allowed_champions) - tree_path
    new_node = Node(possible_actions, new_state, current_node, action)
    current_node.children.append(new_node)
    return new_node


def find_new_state(action, parent):
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


def simulate(node):
    copied_node = Node(node.possible_actions, node.state, node.parent, node.champ)
    while len(copied_node.state.enemy_team) < 5 or len(copied_node.state.ally_team) < 5:
        action = random.choice(tuple(copied_node.possible_actions))
        copied_node.possible_actions.remove(action)
        copied_node.state = find_new_state(action, copied_node)
    match_vector = list(copied_node.state.ally_team)
    match_vector.extend(list(copied_node.state.enemy_team))
    return match_vector


def backprop(result, node):
    node_to_update = node
    while node_to_update.parent is not None:
        node_to_update.visited += 1
        node_to_update.value += result
        node_to_update = node_to_update.parent
    # updates root node below
    node_to_update.visited += 1
    node_to_update.value += result
    return None


def find_state_at_turn(node, champ):
    for child in node.children:
        if child.champ == champ:
            return child


def recall_subtree(state: State, tree, bans):
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
            else:
                choices.append(first_pick_team.pop(0))
        else:
            if alternate:
                choices.append(last_pick_team.pop(0))
                alternate = False
            else:
                choices.append(first_pick_team.pop(0))
                alternate = True

    if tree is None:
        return Node(get_allowed_champions(bans, choices), state)
    else:
        current_turn = tree.depth
        node = tree
        for turn in range(current_turn, search_depth):
            node = find_state_at_turn(node, choices[turn])
            if node is None:
                node = Node(get_allowed_champions(bans, choices), state)
                break
        node.parent = None
    return node


def suggestions_to_json(suggestions):

    suggestions_string = []
    for sug in suggestions:
        suggest = (sug.champ,sug.champ2, sug.score)
        suggestions_string.append(suggest)

    json_suggestions = json.dumps(suggestions_string)
    return json_suggestions


def game_state_from_json(json_object):
    obj = json_object

    ally_starting = obj['ally_starting']
    ally_team = obj['ally_team']
    enemy_team = obj['enemy_team']
    banned_champs = obj['banned_champs']

    state = State(None, ally_starting)
    state.ally_team = ally_team
    state.enemy_team = enemy_team

    return state, set(banned_champs)