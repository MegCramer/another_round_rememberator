import datetime

from .database import db


class Episode(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    ep_num = db.Column(db.String(255))
    ep_title = db.Column(db.String(255))
    ep_air_date = db.Column(db.String(255))
    ep_guest1 = db.Column(db.String(255))
    ep_guest2 = db.Column(db.String(255))
    ep_joke = db.Column(db.String(255))
    ep_joke_topic = db.Column(db.String(255))
    ep_smi = db.Column(db.String(255))
    ep_smi_topic = db.Column(db.String(255))
    ep_round_t = db.Column(db.String(255))
    ep_round_h = db.Column(db.String(255))
    ep_url = db.Column(db.String(255))

    ep_searches = db.Column(db.Integer)

    def __init__(self, episode_info):
        # I made ep_searches=None an option because there won't be anything in there when a new object gets added at first...I think?

        self.ep_update(episode_info)
        self.ep_searches = 0

    def ep_update(self, episode_info):

        self.ep_num = episode_info.get('ep_num', '')
        self.ep_title = episode_info.get('ep_title', '')
        self.ep_air_date = episode_info.get('ep_air_date', '')
        self.ep_guest1 = episode_info.get('ep_guest1', '')
        self.ep_guest2 = episode_info.get('ep_guest2', '')
        self.ep_joke = episode_info.get('ep_joke', '')
        self.ep_joke_topic = episode_info.get('ep_joke_topic', '')
        self.ep_smi = episode_info.get('ep_smi', '')
        self.ep_smi_topic = episode_info.get('ep_smi_topic', '')
        self.ep_round_t = episode_info.get('ep_round_t', '')
        self.ep_round_h = episode_info.get('ep_round_h', '')
        self.ep_url = episode_info.get('ep_url', '')

    # @classmethod
    # def find_episode(cls, search_input):
        #cls.objects ?
    #TODO Move everything from csv_dict into this class method


    def __repr__(self):
        return '<Episode %r>' % self.ep_searches
