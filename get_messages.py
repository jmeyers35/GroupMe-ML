import json
import os
import requests

from settings import GROUPME_TOKEN

base_url = "https://api.groupme.com/v3"
messages = 100 # Max


def get_messages_by_user(group_id, user_id):
    pass

"""
Returns all the messages of a group identified by parameter id.
"""

def get_messages(group_id):
    url = base_url + "/groups/" + group_id + "/messages"

"""
Returns a list of dicts containing the groups the user with the token is in.
"""
def get_groups():
    url = base_url + "/groups"
    url += "?token=" + GROUPME_TOKEN

    response = requests.get(url)

    return json.loads(response.text)['response']