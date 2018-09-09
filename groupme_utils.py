import json
import os
import requests

from settings import GROUPME_TOKEN

BASE_URL = "https://api.groupme.com/v3"
MAX_MESSAGE_BATCH = 100 # Max


"""
Returns all messages sent by user identified by user_id in group identified by group_id.
"""

def get_messages_by_user(group_id, user_id):
    msgs = get_messages(group_id)

    return filter(lambda x: x['sender_id'] == user_id)

"""
Returns a list of all the messages of a group identified by parameter id.

Returns: list<dict>
"""

def get_messages(group_id):
    url = BASE_URL + "/groups/" + group_id + "/messages"
    url += "?token=" + GROUPME_TOKEN
    url += "&limit=" + str(MAX_MESSAGE_BATCH)
    response = requests.get(url)

    msg_list = []

    # First batch of messages
    first_res = json.loads(response.text)['response']

    num_msgs = first_res['count']

    while (num_msgs > 0):
        num_msgs -= MAX_MESSAGE_BATCH
        messages = json.loads(response.text)['response']['messages']
        msg_list.extend(messages)

        last_message = messages[-1]

        new_url = url + "&before_id=" + last_message['id']

        response = requests.get(new_url)

    return msg_list




"""
Returns a list of dicts containing the groups the user corresponding to t   he access token is in.

Returns list<dict>
"""

def get_groups():
    url = BASE_URL + "/groups"
    url += "?token=" + GROUPME_TOKEN

    response = requests.get(url)

    return json.loads(response.text)['response']

"""
Returns a list of tuples containing the name and id of all the groups the user corresponding to the access
token is in.
"""
def get_group_names_ids():
    url = BASE_URL + "/groups"
    url += "?token=" + GROUPME_TOKEN

    tups = []

    response = requests.get(url)

    list_groups = json.loads(response.text)['response']

    for group_dict in list_groups:
        tups.append((group_dict['name'], group_dict['id']))

    return tups
    