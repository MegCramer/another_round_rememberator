import json
import os

DEFAULT_SETTINGS = {
    "ADMIN_USER" : "admin",
    "ADMIN_PASS" : "temporary123",
    "DB_USER" : "replace me",
    "DB_PW" : "replace me",
    "DB_HOST" : "localhost",
    "DB_NAME" : "rememberator_db",
    "TWILIO_ACCOUNT_SID" : "replace me",
    "TWILIO_AUTH_TOKEN" : "replace me",
    "TWILIO_PHONE_NO" : "replace me", # "+12223456789"
    "SECRET_KEY" : "replace me",
    "DEBUG": "True",
    "APP_URL": "replace me" # "https://my-hotline-url-here.com'"
}


config_filepath = os.path.dirname(__file__)+'/config_vars_secret.json'


# make a config file if it doesnt exist, based on default values & env vars
if not os.path.isfile(config_filepath):
    # TODO: a more elegant way of doing this?

    config_settings = {}
    for k, default_v in DEFAULT_SETTINGS.items():
        # if env var exists, use env var value - otherwise use default value
        config_settings[k] = os.getenv(k, default_v)

    with open(config_filepath, 'w') as f:
        json.dump(config_settings, f, indent=4)



def update_config(updates):

    # start with old config
    if os.path.isfile(config_filepath):
        with open(config_filepath) as f:
            config = json.load(f)
    else:
        config = {}

    # update config accordingly
    for k, v in updates.items():
        config[k] = v

    # write config file
    with open(config_filepath, 'w') as f:
        json.dump(config, f, indent=4)



# read settings from config file
with open(config_filepath) as f:
    json_config = json.load(f)

    CONFIG_VARS = {}
    for k, default_v in DEFAULT_SETTINGS.items():
        # TODO: clean this up
        # use env vars if they exist, otherwise config file, otherwise default
        CONFIG_VARS[k] = os.getenv(k, json_config.get(k, default_v))
