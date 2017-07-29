import csv
import sys

# loading data from csv

def share_url(search_input):

    with open('data.csv', 'rU') as f:
        csvReader = csv.DictReader(f)
        for episode in csvReader:
            if episode['ep_guest1'] == search_input:
                return episode
            if episode['ep_round_t'] == search_input:
                return episode
            if episode['ep_round_h'] == search_input:
                return episode

if __name__ == '__main__':
    episode_match = share_url(sys.argv[1])
    print('Here is {}. Is this the episode you were looking for? {}'.format(episode_match['ep_title'], episode_match['ep_url']))
