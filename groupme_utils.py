import json
import os
import requests
from typing import Dict, List

from config.config import GROUPME_TOKEN

BASE_URL = "https://api.groupme.com/v3"
MAX_MESSAGE_BATCH = 100

def get_messages_by_user(group_id: int, user_id: int) -> List[Dict]:
    """Returns all messages sent by user identified by user_id in group identified by group_id."""
    msgs = get_messages_by_group(group_id)

    user_msgs =  list(filter(lambda x: x['sender_id'] == user_id, msgs))
    
    return user_msgs


def get_messages_by_group(group_id: int) -> List[Dict]:
    """Returns a list of all the messages of a group identified by group_id."""
    url = BASE_URL + "/groups/" + group_id + "/messages"
    url += "?token=" + GROUPME_TOKEN
    url += "&limit=" + str(MAX_MESSAGE_BATCH)
    response = requests.get(url)

    msgs = []

    # First batch of messages
    first_res = json.loads(response.text)['response']

    num_msgs = first_res['count']

    while (num_msgs > 0):
        num_msgs -= MAX_MESSAGE_BATCH
        messages = json.loads(response.text)['response']['messages']
        msgs.extend(messages)

        last_message = messages[-1]

        new_url = url + "&before_id=" + last_message['id']

        response = requests.get(new_url)

    return msgs

def get_all_groups() -> List[Dict]:
    """Returns all of the groups the user corresponding to the configured access token is in"""
    url = BASE_URL + "/groups"
    url += "?token=" + GROUPME_TOKEN

    response = requests.get(url)

    return json.loads(response.text)['response']


def get_all_group_ids() -> List[Tuple[str, int]]:
    """Returns a list of tuples containing the name and id of all the groups the user corresponding to the access token is in"""
    url = BASE_URL + "/groups"
    url += "?token=" + GROUPME_TOKEN

    tups = []

    response = requests.get(url)

    list_groups = json.loads(response.text)['response']

    for group_dict in list_groups:
        tups.append((group_dict['name'], group_dict['id']))

    return tups


def get_group_by_id(group_id: int) -> List[Dict]:
    """Returns a single group denoted by group_id, if it exists. Returns None otherwise."""
    groups = get_all_groups()
    try:
        return next(x for x in groups if x['id'] == group_id)
    except StopIteration:
        return None


def get_group_by_name(group_name: int) -> List[Dict]:
    """Returns the first group with name group_name, if it exists. Returns None otherwise."""
    groups = get_all_groups()
    try:
        return next(x for x in groups if x['name'] == group_name)
    except StopIteration:
        return None

def get_users_by_group(group_id: int) -> List[Tuple[str, int]]:
    """Returns a list of tuples of the form (name, id) containing group member info for group group_id"""
    group = get_group_by_id(group_id)
    members = []
    for member in group['members']:
        members.append((member['name'], member['user_id']))
    return members

def write_group_messages_to_file(group_id: int) -> None:
    """Given a group_id, writes all of the messages in that group to a text file"""
    msgs = get_messages_by_group(group_id)
    text_list = [x['text'] + '\n' for x in msgs if x['text'] is not None]
    with open('messages.txt', 'w') as file:
        file.writelines(text_list)

def write_user_messages_to_file(group_id: int, user_id: int) -> None:
    """Given a group_id and user_id, writes all of the messages by that user in that group to a text file"""
    msgs = get_messages_by_user(group_id, user_id)
    name = msgs[0]['name']
    name = name.replace(' ', '_')
    name = name.lower()
    text_list = [x['text'] + '\n' for x in msgs if x['text'] is not None]
    with open(name + '_messages.txt', 'w') as file:
        file.writelines(text_list)
    
def get_all_user_messages(group_id: int) -> List[Tuple[int, str, Dict]]:
    """Returns a list of triples containing User Names and IDs, with all messages sent by the corresponding user"""
    all_msgs=get_messages_by_group(group_id)
    msgs= []
    all_members=get_users_by_group(group_id)
    for i in range(len(all_members)):
        user_id=all_members[i][1]
        name= all_members[i][0]
        res =  list(filter(lambda x: x['sender_id'] == user_id, all_msgs))
        msgs_text = [x['text'] for x in res]

        msgs.append((user_id, name, msgs_text))
    return msgs
