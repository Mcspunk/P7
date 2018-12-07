import LeagueDrafter_RESTAPI.MCTS as MCTS
import LeagueDrafter_RESTAPI.db_connection as db
import LeagueDrafter_RESTAPI.initial_win_pred as NN
import random
from multiprocessing.dummy import Pool as ThreadPool

champions_sorted_by_winpercent = sorted(db.retrieve_winpercent(), key=lambda tup: tup[1])


def pick_champ_enemy_team_winpct(available_champions, state):
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


def make_random_banns():
    return set(random.sample(range(0, 141), 10))


def pick_for_enemy(state, enemy_team):
    for champ in enemy_team:
        if champ not in state.enemy_team:
            state.enemy_team.append(champ)
            break

def pick_for_enemy_team(enemy_team, state, ally_starting):
    if ally_starting is True:
        if len(state.enemy_team) is not 4:
                pick_for_enemy(state, enemy_team)
                pick_for_enemy(state, enemy_team)
        else:
            pick_for_enemy(state, enemy_team)
    else:
        if len(state.enemy_team) < 1:
            pick_for_enemy(state, enemy_team)
        else:
                pick_for_enemy(state, enemy_team)
                pick_for_enemy(state, enemy_team)


def pick_for_ally_team(suggestions, enemy_team, state):
    for suggestion in suggestions:
        if suggestion.champ2 is None:
            if suggestion.champ in enemy_team:
                continue
            else:
                state.ally_team.append(suggestion.champ)
                break
        elif suggestion.champ not in enemy_team and suggestion.champ2 not in enemy_team:
            state.ally_team.append(suggestion.champ)
            state.ally_team.append(suggestion.champ2)
            break


def evaluate_MCTS_against_real_matches(matches, ally_team_starting=True):

    ally_wins = 0
    enemy_wins = 0
    total_win_pct = 0
    for match in matches:
        banned_champs = match[2]
        enemy_team = match[1]
        state = MCTS.State()
        state.ally_starting = ally_team_starting
        tree = None
        while len(state.enemy_team) < 5 or len(state.ally_team) < 5:
            tree = MCTS.recall_subtree(state, tree, set(banned_champs))
            allowed_champions = list.copy(tree.possible_actions)
            suggestions, reduced_root = MCTS.run_mcts(10, tree, True, allowed_champions)
            tree = reduced_root
            pick_for_ally_team(suggestions, enemy_team, state)
            pick_for_enemy_team(enemy_team, state, ally_team_starting)
        input_vector = list.copy(state.ally_team)
        input_vector.extend(list.copy(state.enemy_team))
        result = NN.predictTeamComp(input_vector)
        total_win_pct += result

        if result > 0.5:
            ally_wins += 1
        else:
            enemy_team += 1
    avg_pct = total_win_pct/len(matches)
    return ally_wins, enemy_wins, avg_pct

def pick_random_champ_enemy(available_champions, state):
    if len(state.ally_team) == 0 or len(state.ally_team) == 5:
        random_choice = random.choice(available_champions)
        state.enemy_team.append(random_choice)
    else:
        #pick 1
        random_choice = random.choice(available_champions)
        state.enemy_team.append(random_choice)
        #pick 2
        available_champions.remove(random_choice)
        random_choice = random.choice(available_champions)
        state.enemy_team.append(random_choice)

def evaluate_MCTS_against_random(number_of_eval):
    ally_wins = 0
    enemy_wins = 0

    ite = 0
    state = MCTS.State()
    state.ally_starting = True
    tree = None
    while ite < number_of_eval:
        banned_champs = set(random.sample(range(0, 141), 10))

        while len(state.enemy_team) < 5 or len(state.ally_team) < 5:
            tree = MCTS.recall_subtree(state, tree, set(banned_champs))
            allowed_champions = list.copy(tree.possible_actions)
            suggestions, reduced_root = MCTS.run_mcts(10, tree, True, allowed_champions)

            if suggestions[0].champ2 is None:
                state.ally_team.append(suggestions[0].champ)
            else:
                state.ally_team.append(suggestions[0].champ)
                state.ally_team.append(suggestions[0].champ2)
            pick_random_champ_enemy(allowed_champions, state)
        input_vector = list.copy(state.ally_team)
        input_vector.extend(list.copy(state.enemy_team))
        result = NN.predictTeamComp(input_vector)
        print("Home: ")
        print(result)
        if result > 0.5:
            ally_wins += 1
        else:
            enemy_wins += 1
        tree = None
        state = MCTS.State()
        ite += 1
    return ally_wins, enemy_wins

def evaluate_MCTS_against_winpct(number_of_eval):

    ally_wins = 0
    enemy_wins = 0
    ite = 0
    state = MCTS.State()
    state.ally_starting = True
    tree = None
    while ite < number_of_eval:
        banned_champs = set(random.sample(range(0, 141), 10))

        while len(state.enemy_team) < 5 or len(state.ally_team) < 5:
            tree = MCTS.recall_subtree(state, tree, set(banned_champs))
            allowed_champions = list.copy(tree.possible_actions)
            suggestions, reduced_root = MCTS.run_mcts(10, tree, True, allowed_champions)

            if suggestions[0].champ2 is None:
                state.ally_team.append(suggestions[0].champ)
            else:
                state.ally_team.append(suggestions[0].champ)
                state.ally_team.append(suggestions[0].champ2)
            pick_champ_enemy_team_winpct(allowed_champions, state)
        input_vector = list.copy(state.ally_team)
        input_vector.extend(list.copy(state.enemy_team))
        result = NN.predictTeamComp(input_vector)
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


def multi_thread_test(number_of_matches, threads):

    matches = db.get_matches(number_of_matches)
    interval = number_of_matches / threads
    start = 0
    end = interval
    match_sets = []
    for index in range(0,threads):
        match_sets.append(matches[int(start):int(end)])
        start += interval
        end += interval

    pool = ThreadPool(threads)
    results = pool.map(evaluate_MCTS_against_real_matches, match_sets)

    test_results = [0, 0, 0]
    for result in results:
        test_results[0] += result[0]
        test_results[1] += result[1]
        test_results[2] += result[2]
    test_results[2] = test_results[2]/len(results)
    return test_results


multi_thread_test(4, 4)

