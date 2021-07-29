import requests
import json

with open('settings.json', 'r') as f:
    SETTINGS = json.load(f)


def post_event(event_name, secret_key, val1=None, val2=None, val3=None):
    """Posts data to IFTTT via webhooks.
    IFTTT webhooks: https://ifttt.com/maker_webhooks

    event_name (str): the name of the IFTTT event
    secret_key (str): your IFTTT secret key.
    """
    report = {}

    if val1 is not None:
        report['value1'] = val1
    if val2 is not None:
        report['value2'] = val2
    if val3 is not None:
        report['value3'] = val3
    requests.post('https://maker.ifttt.com/trigger/{}/with/key/'
                  '{}'.format(event_name, secret_key), data=report)


def post_exam_changes(exam_changes):
    """Sends the new exam data to IFTTT

    exam_changes (list): a list of strings giving information of what was changed
    event_name (str): the name of the IFTTT event
    secret_key (str): your IFTTT secret key.
    """
    event_name = SETTINGS['ifttt_event']
    secret_key = SETTINGS['ifttt_secret_key']

    post_event(event_name, secret_key, '\n'.join(exam_changes))
