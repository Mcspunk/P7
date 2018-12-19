import LeagueDrafter_RESTAPI.MCTS as MCTS
import LeagueDrafter_RESTAPI.db_connection as db
import LeagueDrafter_RESTAPI.initial_win_pred as NN
import random
import datetime
from joblib import Parallel, delayed
from multiprocessing.dummy import Pool as ThreadPool

champions_sorted_by_winpercent = sorted(db.retrieve_winpercent(), key=lambda tup: tup[1])


def pick_champ_enemy_team_winpct(available_champions, state):

    if len(state.ally_team) == 0 or len(state.ally_team) == 5:
        for i in champions_sorted_by_winpercent:
            if i[0] in available_champions and i[0] not in state.ally_team:
                state.enemy_team.append(i[0])
                available_champions.remove(i[0])
                break
    else:
        champions_selected = 0
        for champion in champions_sorted_by_winpercent:
            if champion[0] in available_champions and champions_selected < 2 and champion[0] not in state.ally_team:
                state.enemy_team.append(champion[0])
                available_champions.remove(champion[0])
                champions_selected += 1


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
    allysize = len(state.ally_team)
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
    if (allysize == len(state.ally_team)):
        print("shit")


def evaluate_MCTS_against_real_matches(data):
    ally_wins = 0
    enemy_wins = 0
    total_win_pct = 0
    enemy_team = data[0][0]
    ally_starting = data[1]
    banned_champs = data[0][1]
    exploration_term = data[2]
    state = MCTS.State()
    state.ally_starting = ally_starting
    tree = None
    while len(state.enemy_team) < 5 or len(state.ally_team) < 5:
        if not ally_starting:
            pick_for_enemy_team(enemy_team, state, ally_starting)
        tree = MCTS.recall_subtree(state, tree, set(banned_champs))
        allowed_champions = list.copy(tree.possible_actions)
        suggestions, tree = MCTS.run_mcts(10, tree, True, allowed_champions, exploration_term=exploration_term)
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
    return ally_wins, enemy_wins, result


def evaluate_MCTS_against_random(data):

    ally_wins = 0
    enemy_wins = 0
    total_win_pct = 0
    ally_starting = data[0]
    exploration_term = data[1]
    state = MCTS.State()
    state.ally_starting = ally_starting
    tree = None

    banned_champs = set(random.sample(range(0, 141), 10))
    allowed_champions = MCTS.get_allowed_champions(banned_champs=banned_champs)
    while len(state.enemy_team) < 5 or len(state.ally_team) < 5:
        if not ally_starting:
            pick_random_champ_enemy(allowed_champions, state)
        tree = MCTS.recall_subtree(state, tree, set(banned_champs))
        allowed_champions = list.copy(tree.possible_actions)
        suggestions, tree = MCTS.run_mcts(10, tree, True, allowed_champions, exploration_term=exploration_term)

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
    return ally_wins, enemy_wins, result


def MCTS_against_MCTS(data):
    exploration_one = data[0]
    exploration_two = data[1]
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

    banned_champs = set(random.sample(range(0, 141), 10))
    while len(ally_state.enemy_team) < 5 or len(ally_state.ally_team) < 5:

        # Ally Turn
        ally_tree = MCTS.recall_subtree(ally_state, ally_tree, set(banned_champs))
        allowed_champions = list.copy(ally_tree.possible_actions)
        suggestions, reduced_root = MCTS.run_mcts(10, ally_tree, True, allowed_champions, 10, exploration_one)
        ally_tree = reduced_root

        if suggestions[0].champ2 is None:
            ally_state.ally_team.append(suggestions[0].champ)
            enemy_state.enemy_team.append(suggestions[0].champ)
        else:
            ally_state.ally_team.append(suggestions[0].champ)
            ally_state.ally_team.append(suggestions[0].champ2)
            enemy_state.enemy_team.append(suggestions[0].champ)
            enemy_state.enemy_team.append(suggestions[0].champ2)

        # Enemy Team
        enemy_tree = MCTS.recall_subtree(enemy_state, enemy_tree, set(banned_champs))
        allowed_champions = list.copy(enemy_tree.possible_actions)
        suggestions, reduced_root = MCTS.run_mcts(10, enemy_tree, True, allowed_champions, 10, exploration_two)
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

    return ally_wins,enemy_wins,result_from_nn


def evaluate_MCTS_against_winpct(data):
    ally_wins = 0
    enemy_wins = 0
    total_win_pct = 0
    ally_starting = data[0]
    exploration_term = data[1]
    state = MCTS.State()
    state.ally_starting = ally_starting

    tree = None

    banned_champs = set(random.sample(range(0, 141), 10))
    allowed_champions = MCTS.get_allowed_champions(banned_champs)
    while len(state.enemy_team) < 5 or len(state.ally_team) < 5:
        if ally_starting is not True:
            pick_champ_enemy_team_winpct(allowed_champions, state)
        tree = MCTS.recall_subtree(state, tree, set(banned_champs))
        allowed_champions = list.copy(tree.possible_actions)
        suggestions, tree = MCTS.run_mcts(10, tree, True, allowed_champions, exploration_term=exploration_term)

        if suggestions[0].champ2 is None:
            state.ally_team.append(suggestions[0].champ)
            allowed_champions.remove(suggestions[0].champ)
        else:
            state.ally_team.append(suggestions[0].champ)
            allowed_champions.remove(suggestions[0].champ)
            state.ally_team.append(suggestions[0].champ2)
            allowed_champions.remove(suggestions[0].champ2)
        if ally_starting is True:
            pick_champ_enemy_team_winpct(allowed_champions, state)
    input_vector = list.copy(state.ally_team)
    input_vector.extend(list.copy(state.enemy_team))
    result = NN.predictTeamComp(input_vector)
    total_win_pct += result
    if result > 0.5:
        ally_wins += 1
    elif result < 0.5:
        enemy_wins += 1

    return ally_wins, enemy_wins, result


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
        #print("match: " + str(iteration))
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


def multi_thread_test_realmatches(number_of_matches, ally_starting, exploration_term):

    matches = db.get_matches(number_of_matches)
    datamap = []

    for match in matches:
        datamap.append((match,ally_starting,exploration_term))

    results = Parallel(n_jobs=-1, verbose=1)(map(delayed(evaluate_MCTS_against_real_matches), datamap))

    test_results = [0, 0, 0]
    for result in results:
        test_results[0] += result[0]
        test_results[1] += result[1]
        test_results[2] += result[2]
    test_results[2] = test_results[2]/len(results)
    test = "MCTS-ALLY_exploration_" + str(exploration_term) + " against Real_matches_RM"
    result_string = test.center(80, '*') + "\n"
    result_string += "Ally team wins: " + str(test_results[0]) + "\nEnemy team wins: " + str(test_results[1]) \
                     + "\nAverage winpercent: " + str(test_results[2]) + "\nAlly starting: " + str(ally_starting) + "\n"
    return result_string



def multi_thread_test_random(number_of_matches, ally_starting, exploration_term):
    datamap = []
    for i in range(0, number_of_matches):
        datamap.append((ally_starting,exploration_term))

    results = Parallel(n_jobs=-1, verbose=1)(map(delayed(evaluate_MCTS_against_random), datamap))

    test_results = [0, 0, 0]
    for result in results:
        test_results[0] += result[0]
        test_results[1] += result[1]
        test_results[2] += result[2]
    test_results[2] = test_results[2]/len(results)
    test = "MCTS-ALLY_exploration_" + str(exploration_term) + " against Random_RT"
    result_string = test.center(80, '*') + "\n"
    result_string += "Ally team wins: " + str(test_results[0]) + "\nEnemy team wins: " + str(test_results[1]) \
                     + "\nAverage winpercent: " + str(test_results[2]) + "\nAlly starting: " + str(ally_starting) + "\n"
    return result_string



def multi_thread_test_highest_winpercent(number_of_matches, ally_starting, exploration_term):
    datamap = []

    for i in range(0, number_of_matches):
        datamap.append((ally_starting,exploration_term))

    results = Parallel(n_jobs=-1, verbose=1)(map(delayed(evaluate_MCTS_against_winpct), datamap))

    test_results = [0, 0, 0]
    for result in results:
        test_results[0] += result[0]
        test_results[1] += result[1]
        test_results[2] += result[2]
    test_results[2] = test_results[2]/len(results)
    test = "MCTS-ALLY_exploration_" + str(exploration_term) + " against Highest_winpercent_HW"
    result_string = test.center(80, '*') + "\n"
    result_string += "Ally team wins: " + str(test_results[0]) + "\nEnemy team wins: " + str(test_results[1])\
                     + "\nAverage winpercent: " + str(test_results[2]) + "\nAlly starting: " + str(ally_starting) + "\n"
    return result_string


def multi_thread_test_MCTS_VS_MCTS(number_of_matches, exploration_term_one, exploration_term_two, ally_starting):

    term_one = 0
    term_two = 0
    datamap = []
    if  ally_starting:
        term_one = exploration_term_one
        term_two = exploration_term_two
    else:
        term_one = exploration_term_two
        term_two = exploration_term_one

    for i in range(0, number_of_matches):
        datamap.append((term_one, term_two))

    results = Parallel(n_jobs=-1, verbose=1)(map(delayed(MCTS_against_MCTS), datamap))

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
                         + str(1-test_results[2]) + "\nAlly starting: " + str(ally_starting) + "\n"
    print(datetime.datetime.now().time())
    return result_string


expterm = 0.25
matches_to_evaluate = 500

#0.25 vs 3


result = multi_thread_test_MCTS_VS_MCTS(matches_to_evaluate,1,0.25,True)
print(result)
file = open("testoutput.txt", "a")
file.write(result)
file.close()

result = multi_thread_test_MCTS_VS_MCTS(matches_to_evaluate,1,0.25,False)
print(result)
file = open("testoutput.txt", "a")
file.write(result)
file.close()
