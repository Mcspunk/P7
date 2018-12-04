import LeagueDrafter_RESTAPI.MCTS as MCTS
import LeagueDrafter_RESTAPI.db_connection as db
import LeagueDrafter_RESTAPI.initial_win_pred as NN
import random

champions_sorted_by_winpercent = sorted(db.retrieve_winpercent(), key=lambda tup: tup[1])


def pick_champ_enemy_team(available_champions, state):
    onemore = False
    available = list.copy(available_champions)
    if len(state.ally_team) == 0 or len(state.ally_team) == 5:
        for i in champions_sorted_by_winpercent:
            if i[0] in available_champions:
                state.enemy_team.append(i[0])
                break
    else:
        for i in champions_sorted_by_winpercent:
            if i[0] in available_champions:
                state.enemy_team.append(i[0])
                available.remove(i[0])
                if onemore is False:
                    onemore = True
                if onemore is True:
                    break


def evaluate_MCTS_UCT(number_of_eval):

    ally_wins = 0
    enemy_wins = 0

    ite = 0
    state = MCTS.State()
    state.ally_starting = True
    tree = None
    while ite < number_of_eval:
        banned_champs = set(random.sample(range(0, 141), 10))

        while len(state.enemy_team) < 5 or len(state.ally_team) < 5:
            tree = MCTS.recall_subtree(state, tree, banned_champs)
            allowed_champions = list.copy(tree.possible_actions)
            suggestions, reduced_root = MCTS.run_mcts(1000, tree, True, allowed_champions)

            if suggestions[0].champ2 is None:
                state.ally_team.append(suggestions[0].champ)
            else:
                state.ally_team.append(suggestions[0].champ)
                state.ally_team.append(suggestions[0].champ2)
            pick_champ_enemy_team(allowed_champions, state)
        input = list.copy(state.ally_team)
        input.extend(list.copy(state.enemy_team))
        result = NN.predictTeamComp(input)
        print("Home: ")
        print(result)
        if result > 0.5:
            ally_wins += 1
        elif result < 0.5:
            enemy_wins += 1
        else:
            ally_wins += 0
            enemy_wins += 0
        tree = None
        state = MCTS.State()
        ite += 1
    return ally_wins, enemy_wins


#ally, enemy = evaluate_MCTS_UCT(1000)
