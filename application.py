
from flask import flash, redirect, request, render_template, Response, session
from flask_sqlalchemy import SQLAlchemy

import twilio.twiml
from twilio.rest import TwilioRestClient
import importlib

from csv_dict import find_episode, return_all_matches
import random

from rememberator import create_app
from rememberator import config
from rememberator.models import Episode
from rememberator.database import db

application = create_app()

@application.route("/")
def index():

    return render_template('index.html')

@application.route("/respond", methods=['GET', 'POST'])
def respond():
    """Respond to incoming texts"""

    resp = twilio.twiml.Response()

    incoming_msg = request.values.get('Body', '')

    txt = None

    if(incoming_msg=='clear'):
        # this clears all cookies
        session['seen_greeting'] = False
        session['seen_episode'] = False
        session['seen_retry'] = False
        session['seen_cc'] = False
        session['seen_cc_retry'] = False
        session['seen_jt'] = False
        session['seen_jt_retry'] = False
        session['coming_from_cc'] = False
        session['coming_from_jt'] = False
        session['coming_from_episode'] = False
        resp.sms("un-rememberating our conversation")
        return str(resp)

    elif session.get('seen_cc') == True and session.get('coming_from_jt') == False and session.get('coming_from_cc') == True and session.get ('coming_from_episode') == False and (incoming_msg=='Y' or incoming_msg=='N'):
        # someone is responding after seeing an SMI episode
        session['coming_from_cc'] = False
        episode_list = return_all_matches('Y')
        episode = random.choice(episode_list)

        if(incoming_msg=='Y' and episode['ep_smi_topic']=='n/a'):
            txt = 'OK, here ya go! {}'.format(episode['ep_url'])
            txt2 = 'If you want to search again, just type a guest name, \'joke time\', or \'career corner\'.'
        elif(incoming_msg=='Y'):
            txt = 'Here\'s one with advice on {}. {}'.format(episode['ep_smi_topic'], episode['ep_url'])
            txt2 = 'If you want to search again, just type a guest name, \'joke time\', or \'career corner\'.'
        else:
            txt = 'Cool cool. If you want to search again, just type a guest name, \'joke time\', or \'career corner\'.'
            txt2 = ':)'
            session['seen_episode'] = False
            session['seen_cc'] = False
            session['seen_jt'] = False

        resp.sms(txt)
        return str(resp)

    elif session.get('seen_jt') == True and session.get('coming_from_cc') == False and session.get('coming_from_jt') == True and session.get('coming_from_episode') == False and (incoming_msg=='Y' or incoming_msg=='N'):
        # someone is responding after seeing an joke
        session['coming_from_jt'] = False

        episode_list = return_all_matches('joke')
        episode = random.choice(episode_list)

        if(incoming_msg=='Y' and episode['ep_joke_topic']=='n/a'):
            txt = 'OK. Hittin\' ya on the buzz. {}'.format(episode['ep_url'])
        elif(incoming_msg=='Y'):
            txt = 'Please LOL on my behalf to this episode with a joke about {}. {}'.format(episode['ep_joke_topic'], episode['ep_url'])
        else:
            txt = 'OK, fine. If you want to search again, just type a guest name, \'joke time\', or \'career corner\'.'
            session['seen_episode'] = False
            session['seen_cc'] = False
            session['seen_jt'] = False

        resp.sms(txt)
        return str(resp)

    elif incoming_msg=='career corner':
        # someone is looking for an SMI episode -- this returns a random one
        session['seen_cc'] = True
        session['coming_from_cc'] = True
        episode_list = return_all_matches('Y')
        episode = random.choice(episode_list)

        if(episode['ep_smi_topic']=='n/a'):
            txt = 'Here\'s an episode where Stacy-Marie Ishmael gave us some career advice we desperately needed. {}'.format(episode['ep_url'])
            txt2 = 'Want me to find you another one? (Y/N)'
        else:
            txt = 'In this episode, Stacy-Marie dropped some knowledge about {}. {}'.format(episode['ep_smi_topic'], episode['ep_url'])
            txt2 = 'Want me to find you another Stacy\'s Career Corner? (Y/N)'

        resp.sms(txt)
        resp.sms(txt2)
        return str(resp)

    elif incoming_msg=='joke time':
        # someone is looking for a joke -- this returns a random one
        session['seen_jt'] = True
        session['coming_from_jt'] = True

        episode_list = return_all_matches('joke')
        episode = random.choice(episode_list)

        txt = 'Here\'s an episode where Tracy told a joke about {}. {}'.format(episode['ep_joke_topic'], episode['ep_url'])
        txt2 = 'Want another one? (Y/N)'

        resp.sms(txt)
        resp.sms(txt2)
        return str(resp)

    elif session.get('seen_episode') == True:
        # person is saying whether or not it was the right episode
        session['seen_retry'] = True
        session['seen_episode'] = False
        session['coming_from_episode'] = False

        if(incoming_msg=='Y'):
            txt = 'Glad I could help :) If you want to look for another episode, send me another search term!'
        elif(incoming_msg=='N'):
            txt = 'I\'m sorry... tbh I\'m not a very smart chatbot. You could always try searching for another interview guest...'
        elif find_episode(incoming_msg) == None:
            txt = 'I couldn\'t find that episode. Check your spelling and try again? Or, try searching for a different interview guest.'
        else:
            txt = 'If you want to search for another episode, I\'m listening...'

        resp.sms(txt)
        return str(resp)

    elif session.get('seen_greeting') == True or (session.get('seen_greeting') == True and session.get('seen_episode') == False):
        # person is responding with guest name
        session['seen_episode'] = True
        session['coming_from_episode'] = True
        episode = find_episode(incoming_msg) #TODO replace find_episode to use ORM and lookup in the database instead of using CSV

        if episode == None:
            txt = 'I couldn\'t find that episode. Check your spelling and try again? Or, try searching for a different interview guest.'
            session['seen_episode'] = False
        else:
            txt = 'Here\'s {}. Is this what you were looking for? (Y/N) {}'.format(episode['ep_title'],
            episode['ep_url'])
            existing_episode = Episode.query.filter_by(ep_num=episode['ep_num']).first()
            existing_episode.ep_searches+=1 #incrementing the search count for returned episode
            db.session.commit()

        resp.sms(txt)
        return str(resp)

    else:
        # this is the first time someone has texted
        session['seen_greeting'] = True
        resp.sms("Greetings, human, and welcome to the Another Round Rememberator. To find an episode, type the name of an interview guest. Or, try searching for \'career corner\' or \'joke time\'.")

    return str(resp)

if __name__ == "__main__":

    application.run(debug=debug, host='0.0.0.0')
