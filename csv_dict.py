import csv
import sys
import random
from collections import defaultdict, Counter

def find_episode(search_input):
    with open('data.csv', 'rU') as f:
        csvReader = csv.DictReader(f)

        for episode in csvReader:
            if episode['ep_guest1'] == search_input:
                return episode
            elif episode['ep_guest2'] == search_input:
                return episode
            elif episode['ep_round_t'] == search_input:
                return episode
            elif episode['ep_round_h'] == search_input:
                return episode
            elif episode['ep_smi'] == search_input:
                return episode

        return None

# def fuzzy_search(search_input):
#     with open('data.csv', 'rU') as f:
#         csvReader = csv.DictReader(f)
#         episodelist = []
#
#         for episode in csvReader:
#             print episodelist.append(csvReader)
#         # compare = process.extractOne(search_input, episodes)
#         # compare_score = compare.get[1]
#         # match = compare.get[0]
#         #
#         # if (search_input_compare_score >= 70) is True:
#         #     return find_episode(match)

def return_all_matches(search_input):
    with open('data.csv', 'rU') as f:
        csvReader = csv.DictReader(f)
        matches = []

        for episode in csvReader:
            if episode['ep_smi'] == search_input:
                matches.append(episode)
            if episode['ep_joke'] == search_input:
                matches.append(episode)

        return matches

# if __name__ == '__main__':

    # find_random_match = return_all_matches(sys.argv[1])
    # print random.choice(find_random_match)

    # episode_match = find_episode(sys.argv[1])
    # if episode_match == None:
    #     print('I couldn\'t find that episode. Did you check your spelling?')
    # else:
    #     print('Here is {}. Is this the episode you were looking for? (Y/N) {}'.format(episode_match['ep_title'], episode_match['ep_url']))
