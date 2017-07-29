
from flask import flash, redirect, request, render_template, Response, session
from csv_dict import find_episode
import twilio.twiml
from twilio.rest import TwilioRestClient

application = create_app()

@application.route("/")
def index():

    return render_template('index.html')

@application.route("/respond", methods=['GET', 'POST'])
def respond():
    """Respond to incoming texts"""

    resp = twilio.twiml.Response()

    incoming_msg = request.values.get('Body', '')

    if(incoming_msg=='clear'):
        # this clears all cookies
        session['seen_greeting'] = False
        session['seen_episode'] = False
        session['state'] = ''
        resp.sms("un-rememberating our conversation")
        return str(resp)

    elif session.get('seen_retry') == True
        # person is submitting another search term
        session['seen_episode'] == False

    elif session.get('seen_episode') == True
        # person is saying whether or not it was the right episode
        session['seen_retry'] = True

        if(incoming_msg=='Y'):
            txt = 'Glad I could help! If you want to look for another episode, type \'search again\''
        elif(incoming_msg=='N'):
            txt = 'I\'m sorry. tbh I\'m not a very smart chatbot. You could always try searching for another interview guest... or for something Tracy or Heben bought a round for!'

        resp.sms(txt)
        return str(resp)

    elif session.get('seen_greeting') == True:
        # person is responding with guest name
        session['seen_episode'] = True
        episode = find_episode(incoming_msg)

        if episode == None:
            txt = 'I couldn\'t find that episode. Check your spelling and try again, or try searching for a different interview guest.'
        else:
            txt = 'Here\'s {}. Is this what you were looking for? (Y/N) {}'.format(episode['ep_title'],
            episode['ep_url'])

        resp.sms(txt)
        return str(resp)


    else:
        # this is the first time someone has texted
        session['seen_greeting'] = True
        resp.sms("Greetings, human, and welcome to the Another Round Rememberator, a tool for finding that episode you KNOW you heard, even if you can't remember what it's called. To get started, try typing the name of an interview guest.")

    return str(resp)
