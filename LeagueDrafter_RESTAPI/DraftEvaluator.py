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


def pick_random_champ_enemy(available_champions, state):
    if len(state.ally_team) == 0 or len(state.ally_team) == 5:
        random_choice = random.choice(available_champions)
        state.enemy_team.append(random_choice)
        available_champions.remove(random_choice)
    else:
        #pick 1
        random_choice = random.choice(available_champions)
        state.enemy_team.append(random_choice)
        #pick 2
        available_champions.remove(random_choice)
        random_choice = random.choice(available_champions)
        state.enemy_team.append(random_choice)

        available_champions.remove(random_choice)


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


def evaluate_MCTS_against_real_matches(matches):
    ally_wins = 0
    enemy_wins = 0
    total_win_pct = 0
    ally_starting = matches[1]
    for match in matches[0]:
        enemy_team = match[1]
        banned_champs = match[2]
        state = MCTS.State()
        state.ally_starting = ally_starting
        tree = None
        while len(state.enemy_team) < 5 or len(state.ally_team) < 5:
            if not ally_starting:
                pick_for_enemy_team(enemy_team, state, ally_starting)
            tree = MCTS.recall_subtree(state, tree, set(banned_champs))
            allowed_champions = list.copy(tree.possible_actions)
            suggestions, reduced_root = MCTS.run_mcts(10, tree, True, allowed_champions)
            tree = reduced_root
            pick_for_ally_team(suggestions, enemy_team, state)
            if ally_starting:
                pick_for_enemy_team(enemy_team, state, ally_starting)
        input_vector = list.copy(state.ally_team)
        input_vector.extend(list.copy(state.enemy_team))
        result = NN.predictTeamComp(input_vector)
        total_win_pct += result

        if result > 0.5:
            ally_wins += 1
        else:
            enemy_wins += 1
    avg_pct = total_win_pct/len(matches)
    return ally_wins, enemy_wins, avg_pct


def evaluate_MCTS_against_random(data):

    number_of_eval = data[0]
    ally_wins = 0
    enemy_wins = 0
    total_win_pct = 0
    ally_starting = data[1]
    state = MCTS.State()
    state.ally_starting = ally_starting
    tree = None
    for iteration in range(0,number_of_eval):
        banned_champs = set(random.sample(range(0, 141), 10))
        allowed_champions = list(set(range(0,141)) - banned_champs)
        while len(state.enemy_team) < 5 or len(state.ally_team) < 5:
            if not ally_starting:
                pick_random_champ_enemy(allowed_champions, state)
            tree = MCTS.recall_subtree(state, tree, set(banned_champs))
            allowed_champions = list.copy(tree.possible_actions)
            suggestions, reduced_root = MCTS.run_mcts(10, tree, True, allowed_champions)

            if suggestions[0].champ2 is None:
                state.ally_team.append(suggestions[0].champ)
            else:
                state.ally_team.append(suggestions[0].champ)
                state.ally_team.append(suggestions[0].champ2)
            if ally_starting:
                pick_random_champ_enemy(allowed_champions, state)
        input_vector = list.copy(state.ally_team)
        input_vector.extend(list.copy(state.enemy_team))
        result = NN.predictTeamComp(input_vector)
        total_win_pct += result
        if result > 0.5:
            ally_wins += 1
        else:
            enemy_wins += 1
        tree = None
        state = MCTS.State()
        state.ally_starting = ally_starting
    avg_pct = total_win_pct / number_of_eval
    return ally_wins, enemy_wins, avg_pct


def evaluate_MCTS_against_winpct(data):
    number_of_eval = data[0]
    ally_wins = 0
    enemy_wins = 0
    total_win_pct = 0
    ally_starting = data[1]
    ite = 0
    state = MCTS.State()
    state.ally_starting = ally_starting

    tree = None
    for iteration in range(0,number_of_eval):
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
        total_win_pct += result
        if result > 0.5:
            ally_wins += 1
        elif result < 0.5:
            enemy_wins += 1
        tree = None
        state = MCTS.State()
        state.ally_starting = ally_starting
    avg_pct = total_win_pct / number_of_eval
    return ally_wins, enemy_wins, avg_pct


def evaluate_MCTS_VS_MCTS(data):
    number_of_matches = data[0]
    exploration_term_one = data[1]
    exploration_term_two = data[2]
    ally_starting = True
    ally_state = MCTS.State()
    ally_state.ally_starting = ally_starting
    enemy_state = MCTS.State()
    enemy_state.ally_starting = not ally_starting
    ally_tree = None
    enemy_tree = None
    total_win_pct = 0
    ally_wins = 0
    enemy_wins = 0

    for iteration in range(0, number_of_matches):
        banned_champs = set(random.sample(range(0, 141), 10))
        while len(ally_state.enemy_team) < 5 or len(ally_state.ally_team) < 5:

            #Ally Turn
            ally_tree = MCTS.recall_subtree(ally_state, ally_tree, set(banned_champs))
            allowed_champions = list.copy(ally_tree.possible_actions)
            suggestions, reduced_root = MCTS.run_mcts(10, ally_tree, True, allowed_champions,10, exploration_term_one)
            ally_tree = reduced_root

            if suggestions[0].champ2 is None:
                ally_state.ally_team.append(suggestions[0].champ)
                enemy_state.enemy_team.append(suggestions[0].champ)
            else:
                ally_state.ally_team.append(suggestions[0].champ)
                ally_state.ally_team.append(suggestions[0].champ2)
                enemy_state.enemy_team.append(suggestions[0].champ)
                enemy_state.enemy_team.append(suggestions[0].champ2)

            #Enemy Team
            enemy_tree = MCTS.recall_subtree(enemy_state, enemy_tree, set(banned_champs))
            allowed_champions = list.copy(enemy_tree.possible_actions)
            suggestions, reduced_root = MCTS.run_mcts(10, enemy_tree, True, allowed_champions,10, exploration_term_two)
            enemy_tree = reduced_root

            if suggestions[0].champ2 is None:
                enemy_state.ally_team.append(suggestions[0].champ)
                ally_state.enemy_team.append(suggestions[0].champ)
            else:
                enemy_state.ally_team.append(suggestions[0].champ)
                enemy_state.ally_team.append(suggestions[0].champ2)
                ally_state.enemy_team.append(suggestions[0].champ)
                ally_state.enemy_team.append(suggestions[0].champ2)

        input_vector = list.copy(ally_state.ally_team)
        input_vector.extend(list.copy(ally_state.enemy_team))
        result_from_nn = NN.predictTeamComp(input_vector)
        total_win_pct += result_from_nn

        if result_from_nn > 0.5:
            ally_wins += 1
        else:
            enemy_wins += 1

        ally_tree = None
        ally_state = MCTS.State()
        ally_state.ally_starting = ally_starting

        enemy_tree = None
        enemy_state = MCTS.State()
        enemy_state.ally_starting = not ally_starting

    avg_pct = total_win_pct / number_of_matches
    return ally_wins, enemy_wins, avg_pct


def multi_thread_test_realmatches(number_of_matches, threads, ally_starting):

    matches = db.get_matches(number_of_matches)
    interval = int(number_of_matches / threads)
    start = 0
    end = interval
    match_sets = []
    for index in range(0,threads):
        match_sets.append((matches[int(start):int(end)], ally_starting))
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
    test = "MCTS against REAL_MATCHES - Ally_starting:" + str(ally_starting)
    result_string = test.center(80, '*') + "\n"
    result_string += "Ally team wins: " + str(test_results[0]) + "\nEnemy team wins: " + str(test_results[1]) \
                     + "\nAverage winpercent: " + str(test_results[2]) + "\nAlly starting: " + str(ally_starting) + "\n"
    return result_string



def multi_thread_test_random(number_of_matches, threads, ally_starting):

    chunk_size = int(number_of_matches / threads)
    data = (chunk_size,ally_starting)
    datamap = []
    for i in range(0, threads):

        datamap.append(data)

    pool = ThreadPool(threads)
    results = pool.map(evaluate_MCTS_against_random, datamap)

    test_results = [0, 0, 0]
    for result in results:
        test_results[0] += result[0]
        test_results[1] += result[1]
        test_results[2] += result[2]
    test_results[2] = test_results[2]/len(results)
    test = "MCTS against RANDOM - Ally_starting:" + str(ally_starting)
    result_string = test.center(80, '*') + "\n"
    result_string += "Ally team wins: " + str(test_results[0]) + "\nEnemy team wins: " + str(test_results[1]) \
                     + "\nAverage winpercent: " + str(test_results[2]) + "\nAlly starting: " + str(ally_starting) + "\n"
    return result_string



def multi_thread_test_highest_winpercent(number_of_matches, threads, ally_starting):
    chunk_size = int(number_of_matches / threads)
    data = (chunk_size,ally_starting)
    datamap = []

    for i in range(0, threads):
        datamap.append(data)

    pool = ThreadPool(threads)
    results = pool.map(evaluate_MCTS_against_winpct, datamap)

    test_results = [0, 0, 0]
    for result in results:
        test_results[0] += result[0]
        test_results[1] += result[1]
        test_results[2] += result[2]
    test_results[2] = test_results[2]/len(results)
    test = "MCTS against HIGHEST_WINPERCENT - Ally_starting:" + str(ally_starting)
    result_string = test.center(80, '*') + "\n"
    result_string += "Ally team wins: " + str(test_results[0]) + "\nEnemy team wins: " + str(test_results[1])\
                     + "\nAverage winpercent: " + str(test_results[2]) + "\nAlly starting: " + str(ally_starting) + "\n"
    return result_string


def multi_thread_test_MCTS_VS_MCTS(number_of_matches, threads, exploration_term_one, exploration_term_two, ally_starting):
    chunk_size = int(number_of_matches/threads)
    if ally_starting is True:
        data = (chunk_size,exploration_term_one,exploration_term_two)
    else:
        data = (chunk_size, exploration_term_two, exploration_term_one)

    pool = ThreadPool(threads)
    datamap = []
    for i in range(0, threads):
        datamap.append(data)
    results = pool.map(evaluate_MCTS_VS_MCTS, datamap)

    test_results = [0, 0, 0]
    for result in results:
        test_results[0] += result[0]
        test_results[1] += result[1]
        test_results[2] += result[2]
    test_results[2] = test_results[2] / len(results)
    test = "MCTS-ALLY_exploration_" + str(exploration_term_one) + " against MCTS-ENEMY_exploration_" + str(exploration_term_two)
    result_string = test.center(80, '*') + "\n"
    if ally_starting:
        result_string += "Ally team wins: " + str(test_results[0]) + "\nEnemy team wins: " + str(test_results[1]) + "\nAverage winpercent: " \
                         + str(test_results[2]) + "\nAlly starting: " + str(ally_starting) + "\n"
    else:
        result_string += "Ally team wins: " + str(test_results[1]) + "\nEnemy team wins: " + str(test_results[0]) + "\nAverage winpercent: " \
                         + str(test_results[2]) + "\nAlly starting: " + str(ally_starting) + "\n"

    return result_string


file = open("testoutput.txt", "a")
threads_amount = 4
matches_to_evaluate = 12
exploration_term_one = 1.5
exploration_term_two = 2.5
# First parameter number of matches, second is number of threads, third if ally has starting turn
'''
test1 = multi_thread_test_random(matches_to_evaluate, 4, True)
file.write(test1)
print(test1)

test2 = multi_thread_test_highest_winpercent(matches_to_evaluate, 4, True)
file.write(test2)
print(test2)

test3 = multi_thread_test_realmatches(matches_to_evaluate, 4, True)
file.write(test3)
print(test3)
'''
test4 = multi_thread_test_MCTS_VS_MCTS(matches_to_evaluate, 4,exploration_term_one,exploration_term_two, True)
file.write(test4)
print(test4)

test5 = multi_thread_test_random(matches_to_evaluate, 4, False)
file.write(test5)
print(test5)

test6 = multi_thread_test_highest_winpercent(matches_to_evaluate, 4, False)
file.write(test6)
print(test6)

test7 = multi_thread_test_realmatches(matches_to_evaluate, 4, False)
file.write(test7)
print(test7)

test8 = multi_thread_test_MCTS_VS_MCTS(matches_to_evaluate, 4,exploration_term_one,exploration_term_two, False)
file.write(test8)
print(test8)
