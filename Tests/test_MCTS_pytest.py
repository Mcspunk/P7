import LeagueDrafter_RESTAPI.MCTS as mcts
import pytest
import json


@pytest.fixture
def some_state():
    test_state = mcts.State()
    test_state.ally_team = []
    test_state.enemy_team = [1]
    test_state.ally_starting = False
    return test_state


@pytest.fixture
def some_state2():
    test_state = mcts.State()
    test_state.ally_team = []
    test_state.enemy_team = []
    test_state.ally_starting = True
    return test_state


@pytest.fixture
def some_state3():
    test_state = mcts.State()
    test_state.ally_team = [4, 5, 6]
    test_state.enemy_team = [1, 2, 3, 7]
    test_state.ally_starting = True
    return test_state


@pytest.fixture
def tree():
    def _tree(simple_state, higher_than_three):
        root = mcts.Node([], simple_state)
        child1 = mcts.Node([], simple_state, root)
        child11 = mcts.Node([], simple_state, child1)
        child12 = mcts.Node([], simple_state, child1)
        child2 = mcts.Node([], simple_state, root)
        child21 = mcts.Node([], simple_state, child2)
        child22 = mcts.Node([], simple_state, child2)

        root.children.append(child1)
        root.children.append(child2)

        child1.children.append(child11)
        child1.children.append(child12)

        child2.children.append(child21)
        child2.children.append(child22)

        child1.value = 0
        child1.visited = 2

        child2.value = 0
        child2.visited = 2

        child11.value = 1
        child11.visited = 1

        child12.value = 2
        child12.visited = 1

        child21.value = 3
        child21.visited = 1

        child22.value = higher_than_three
        child22.visited = 1
        return root
    return _tree


# lazy fixtures: https://pypi.org/project/pytest-lazy-fixture/#
# @pytest.mark.parametrize("test_input,expected", [
#    (some_state, True),
#    (some_state2, False),
# ])


def test_is_dual_return(some_state):
    assert mcts.is_dual_return(some_state)


def test_is_dual_return2(some_state2):
    assert not mcts.is_dual_return(some_state2)


def test_is_dual_return3(some_state3):
    assert mcts.is_dual_return(some_state3)


def test_get_suggestions(tree):
    simple_state = mcts.State()
    simple_state.ally_team = []
    simple_state.enemy_team = [1]
    simple_state.ally_starting = False
    test_tree = tree(simple_state, 9)
    suggestion = mcts.get_suggestions(test_tree, True, 1)
    assert suggestion[0].score == 9


def test_get_suggestions2(tree):
    simple_state = mcts.State()
    simple_state.ally_team = []
    simple_state.enemy_team = [1]
    simple_state.ally_starting = False
    test_tree = tree(simple_state, 5)
    suggestion = mcts.get_suggestions(test_tree, True, 1)
    assert suggestion[0].score == 5


@pytest.mark.parametrize("test_input,expected", [
    (set(range(0, 140)), {140}),
    (set(range(0, 139)), {139, 140}),
    (set(range(10, 140)), {0,1,2,3,4,5,6,7,8,9,140}),
    (set(range(10, 130)), {0,1,2,3,4,5,6,7,8,9,130,131,132,133,134,135,136,137,138,139,140}),

])
def test_get_allowed_champions(test_input, expected):
    assert mcts.get_allowed_champions(test_input) == expected


@pytest.mark.parametrize("test_input, already_chosen, expected", [
    (set(range(0, 140)), {140}, set()),
    (set(range(0, 138)), {139}, {138, 140}),
    (set(range(0, 2)), {140}, set(range(2, 140))),
    (set(range(0, 2)), set(range(20, 30)), set(range(2, 20)).union(set(range(30, 141)))),

])
def test_get_allowed_champions2(test_input, already_chosen, expected):
    assert mcts.get_allowed_champions(test_input, already_chosen) == expected


def test_select(tree: mcts.Node):
    simple_state = mcts.State()
    simple_state.ally_team = []
    simple_state.enemy_team = [1]
    simple_state.ally_starting = False
    assert mcts.select(tree(simple_state, 5).children[0]).value == 2


def test_select2(tree: mcts.Node):
    simple_state = mcts.State()
    simple_state.ally_team = []
    simple_state.enemy_team = [1]
    simple_state.ally_starting = False
    assert mcts.select(tree(simple_state, 5).children[1]).value == 5


@pytest.fixture(scope="module")
def node():
    simple_state = mcts.State()
    simple_state.ally_team = []
    simple_state.enemy_team = [1]
    simple_state.ally_starting = False

    a_node = mcts.Node([2, 3], simple_state)
    a_node.tree_path = {1, 4}
    return a_node


def test_expand_treepath(node):
    fresh_node = mcts.expand(node, 130, {1, 2})

    assert fresh_node.tree_path == {1, 4, 130}


def test_expand_possible_actions(node):
    fresh_node = mcts.expand(node, 130, {1, 2})

    assert fresh_node.possible_actions == [2]


def test_expand_children(node):
    mcts.expand(node, 130, {1, 2})

    assert len(node.children) == 1


def test_expand_new_state(node):
    fresh_node = mcts.expand(node, 130, {1, 2})

    assert fresh_node.state.ally_team == [130]


def test_expand_parent(node):
    fresh_node = mcts.expand(node, 130, {1, 2})

    assert fresh_node.parent == node


def test_expand_children_champ(node):
    fresh_node = mcts.expand(node, 130, {1, 2})

    assert fresh_node.champ == 130


def test_find_new_state(node):
    new_state = mcts.find_new_state(130, node)
    assert new_state.ally_team == [130]

#"simulate" skal muligvis lige lade være med at køre netværket for at kunne teste ordentligt


def test_backprop_node11_value(tree: mcts.Node):
    state = mcts.State()
    root = tree(state, 5)
    mcts.backprop(5, root.children[0].children[0])
    assert root.children[0].children[0].value == 6


def test_backprop_node11_visited(tree: mcts.Node):
    state = mcts.State()
    root = tree(state, 5)
    mcts.backprop(5, root.children[0].children[0])
    assert root.children[0].children[0].visited == 2


def test_backprop_node1_value(tree: mcts.Node):
    state = mcts.State()
    root = tree(state, 5)
    mcts.backprop(5, root.children[0].children[0])
    assert root.children[0].value == 5


def test_backprop_node1_visited(tree: mcts.Node):
    state = mcts.State()
    root = tree(state, 5)
    mcts.backprop(5, root.children[0].children[0])
    assert root.children[0].visited == 3


def test_backprop_root_value(tree: mcts.Node):
    state = mcts.State()
    root = tree(state, 5)
    mcts.backprop(5, root.children[0].children[0])
    assert root.value == 5


def test_backprop_root_visited(tree: mcts.Node):
    state = mcts.State()
    root = tree(state, 5)
    mcts.backprop(5, root.children[0].children[0])
    assert root.visited == 1


@pytest.fixture()
def node_with_champ():
    def _node_with_champ(champ):
        node = mcts.Node([], mcts.State())
        node.champ = champ
        return node
    return _node_with_champ


def test_find_state_at_turn(node_with_champ, node):
    node.children.append(node_with_champ(1))
    node.children.append(node_with_champ(2))
    node.children.append(node_with_champ(3))
    node.children.append(node_with_champ(4))
    assert mcts.find_state_at_turn(node, 4).champ == 4


def test_find_state_at_turn2(node_with_champ, node):
    node.children.append(node_with_champ(1))
    node.children.append(node_with_champ(2))
    node.children.append(node_with_champ(3))
    node.children.append(node_with_champ(4))
    assert mcts.find_state_at_turn(node, 2).champ == 2


@pytest.fixture()
def json_state():
    data = '{"ally_starting": true, "ally_team": [1,2,3], "enemy_team": [4,5], "banned_champs": [6,7,8,9,0]}'
    json_data = json.loads(data)
    return json_data


def test_game_state_from_json_bans(json_state):
    state, bans = mcts.game_state_from_json(json_state)
    assert bans == {6, 7, 8, 9, 0}


def test_game_state_from_json_ally_team(json_state):
    state, bans = mcts.game_state_from_json(json_state)
    assert state.ally_team == [1, 2, 3]


def test_game_state_from_json_enemy_team(json_state):
    state, bans = mcts.game_state_from_json(json_state)
    assert state.enemy_team == [4, 5]


def test_game_state_from_json_ally_starting(json_state):
    state, bans = mcts.game_state_from_json(json_state)
    assert state.ally_starting


@pytest.fixture(scope="module")
def list_of_fixtures():
    list = []
    list.append(mcts.Suggestion(1, 2, 3))
    list.append(mcts.Suggestion(4, 5, 6))
    return list


def test_suggestions_to_json(list_of_fixtures):
    json_obj = mcts.suggestions_to_json(list_of_fixtures)
    json_data = json.loads(json_obj)
    assert json_data[0] == [1, 3, 2]


def test_suggestions_to_json2(list_of_fixtures):
    json_obj = mcts.suggestions_to_json(list_of_fixtures)
    json_data = json.loads(json_obj)
    assert json_data[1] == [4, 6, 5]


@pytest.fixture
def recall_tree():
    def _tree(target_state):
        simple_state = mcts.State()
        simple_state.ally_team = []
        simple_state.enemy_team = [1]
        simple_state.ally_starting = False

        root = mcts.Node([], simple_state)
        child1 = mcts.Node([], simple_state, root)
        child11 = mcts.Node([], simple_state, child1)
        child12 = mcts.Node([], simple_state, child1)
        child2 = mcts.Node([], simple_state, root)
        child21 = mcts.Node([], simple_state, child2)

        child22 = mcts.Node([], target_state, child2)

        root.children.append(child1)
        root.children.append(child2)

        child1.children.append(child11)
        child1.children.append(child12)

        child2.children.append(child21)
        child2.children.append(child22)

        child1.value = 0
        child1.visited = 2

        child2.value = 0
        child2.visited = 2
        child2.champ = 1

        child11.value = 1
        child11.visited = 1

        child12.value = 2
        child12.visited = 1

        child21.value = 3
        child21.visited = 1

        child22.value = 5
        child22.visited = 1
        child22.champ = 2

        root.depth = 0
        return root
    return _tree


def test_recall_subtree_found_tree(recall_tree):
    plant_state = mcts.State()
    plant_state.ally_starting = True
    plant_state.ally_team = [1]
    plant_state.enemy_team = [2]
    node = mcts.recall_subtree(plant_state, recall_tree(plant_state), {1})
    assert 5 == node.value


def test_recall_subtree_not_found(recall_tree, some_state3):
    plant_state = mcts.State()
    plant_state.ally_starting = True
    plant_state.ally_team = [1]
    plant_state.enemy_team = [2]
    node = mcts.recall_subtree(some_state3, recall_tree(plant_state), {1})
    assert 0 == node.value
