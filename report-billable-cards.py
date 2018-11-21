#!/usr/bin/env python2

from prettytable import PrettyTable
import json
import requests
import os
import sys

try:
    api_key = os.environ['trello_api_key']
    user_token = os.environ['trello_user_token']
    invoice_board = os.environ['trello_invoice_board']
    invoice_list = os.environ['trello_invoice_list']

except KeyError as e:
    print "Environment variable not set: %s" % e
    sys.exit(1)

invoice_board_id = None
invoice_list_id = None
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
    if board_list['name'] == invoice_list:
        invoice_list_id = board_list['id']
        
if not invoice_list_id:
    print 'could not find ID for list {} in board {}'.format(invoice_list, invoice_board)
    sys.exit(1)

my_list_cards_url = 'https://api.trello.com/1/lists/{}/cards'.format(invoice_list_id)
my_list_cards = get_objects(my_list_cards_url)

total_hrs = 0

table = PrettyTable(["Card Name", "Hours"])
if '--plain-output' in sys.argv:
    table.border = False

table.align["Card Name"] = 'l'

for card in my_list_cards:

    card_billable = False
    card_hrs = 0

    for label in card['labels']:
    
        if label['name'] == 'done':
            card_billable = True

        if 'hrs-' in label['name']:
            card_hrs += float(label['name'].replace('hrs-', ''))
            total_hrs += card_hrs

    if card_billable:
        print '-', card['name']
        table.add_row([card['name'], card_hrs])

#print table
print ""
print "total hrs:", total_hrs
print ""
