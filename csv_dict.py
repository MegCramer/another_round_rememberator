import csv
import sys

# loading data from csv

def find_episode(search_input):
    with open('data.csv', 'rU') as f:
        csvReader = csv.DictReader(f)
        for episode in csvReader:
            if episode['ep_guest1'] == search_input:
                return episode
            elif episode['ep_round_t'] == search_input:
                return episode
            elif episode['ep_round_h'] == search_input:
                return episode

        return None


if __name__ == '__main__':
    episode_match = find_episode(sys.argv[1])
    if episode_match == None:
        print('I couldn\'t find that episode. Did you check your spelling?')
    else:
        print('Here is {}. Is this the episode you were looking for? (Y/N) {}'.format(episode_match['ep_title'], episode_match['ep_url']))
