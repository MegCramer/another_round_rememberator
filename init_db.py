from rememberator.database import db
from rememberator.models import Episode
import requests
import csv

def init_db():

    db.create_all()

def grab_data():

    GDOC_ID = '1_Tc2CqyDMLswYKu0hFbXmb9Un1x-mrPJtTks2XKv5as'
    #TODO: Move this into config
    
    url = "https://docs.google.com/spreadsheets/d/{}/export?format=csv".format(GDOC_ID)
    r = requests.get(url)
    data = r.content

    if r.status_code==200:

        outfile = 'data.csv'
        with open(outfile, 'wb') as f:
            f.write(data)
            #Figure out a more elegant way to do this later
        with open(outfile) as f:
            reader = csv.DictReader(f)

            for episode_row in reader:
                ep_num_lookup = episode_row.get('ep_num')
                existing_episode = Episode.query.filter_by(ep_num=ep_num_lookup).first()
                if existing_episode:
                    existing_episode.ep_update(episode_row)
                else:
                    new_episode = Episode(episode_row)
                    db.session.add(new_episode)

        db.session.commit()

    else:
        print('could not get page')

if __name__ == "__main__":

    init_db()
    grab_data()
    print("done!")
