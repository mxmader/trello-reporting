#!/usr/bin/env python3

import json
import requests
import os
import sys


def delete_object(url, params):
    result = s.delete(url, params=params)
    result.raise_for_status()
    return result.json()

def get_objects(url, params):
    result = s.get(url, params=params)
    result.raise_for_status()
    return result.json()

# expect KeyErrors if not set
api_key = os.environ['trello_api_key']
user_token = os.environ['trello_user_token']

debug = os.environ.get('debug', False)
s = requests.Session()
s.headers = {'content-type':'application/json'}
global_params = {'key' : api_key, 'token' : user_token}

trello_api_url = 'https://api.trello.com/1'
my_boards_url = f'{trello_api_url}/members/me/boards'
my_boards_params = global_params.copy()
my_boards_params['filter'] = 'all'

if debug:
    print('getting all boards')

for board in get_objects(my_boards_url, my_boards_params):
    
    print('[', board['name'], ']')
    my_board_lists_url = f"{trello_api_url}/boards/{board['id']}/lists"
    board_params = global_params.copy()
    board_params['cards'] = 'closed'
    board_params['card_fields'] = ['closed', 'name', 'dateLastActivity']
    board_params['filter'] = 'all'
    
    if debug:
        print(' getting all lists in board')

    for board_list in get_objects(my_board_lists_url, board_params):
        print(' [', board_list['name'], ']')
        board_list_cards_url = f"{trello_api_url}/lists/{board_list['id']}/cards"
        board_list_card_params = global_params.copy()
        board_list_card_params['filter'] = 'all'

        print('  getting cards')

        for card in get_objects(board_list_cards_url, board_list_card_params):
            
            if card['closed']:

                # TODO: add check for the age of the card
                card_is_old = True
                if card_is_old:
                    if debug:
                        print('  I would delete card:', card['name'])
                        continue
                    
                    delete_card_url = f"{trello_api_url}/cards/{card['id']}"
                    print('   Deleting card:', card['name'])
                    delete_object(delete_card_url, global_params)
