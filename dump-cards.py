#!/usr/bin/env python

from prettytable import PrettyTable
import json
import requests
import os
import sys

try:
    api_key = os.environ['trello_api_key']
    user_token = os.environ['trello_user_token']
    invoice_board = os.environ['trello_invoice_board']

except KeyError as e:
    print "Environment variable not set: %s" % e
    sys.exit(1)

invoice_board_id = None
s = requests.Session()
s.headers = {
	'content-type':'application/json'
}
params = {
	'key' : api_key,
	'token' : user_token
}

def get_objects(url):
    try:
        result = s.get(url, params=params)
        result.raise_for_status()
        return result.json()
    except:
        print 'could not fetch objects from {}; exiting'.format(url)
        sys.exit(1)

trello_api_url = 'https://api.trello.com/1'
my_boards_url = '{}/members/me/boards'.format(trello_api_url)

for board in get_objects(my_boards_url):
    if board['name'] == invoice_board:
        invoice_board_id = board['id']

if not invoice_board_id:
    print 'could not find ID for board {}'.format(invoice_board)
    sys.exit(1)
    
my_board_lists_url = '{}/boards/{}/lists'.format(trello_api_url, invoice_board_id)

for board_list in get_objects(my_board_lists_url):
    invoice_list_id = board_list['id']
    print board_list['name']
        
    my_list_cards_url = 'https://api.trello.com/1/lists/{}/cards'.format(invoice_list_id)
    my_list_cards = get_objects(my_list_cards_url)

    for card in my_list_cards:
        print '-', card['name']
    print ''
