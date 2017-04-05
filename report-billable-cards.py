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

except KeyError as e:
    print "Environment variable not set: %s" % e
    sys.exit(1)

invoice_board_id = None

params = {
	'key' : api_key,
	'token' : user_token
}

headers = {
	'content-type':'application/json'
}

my_boards_url = 'https://api.trello.com/1/members/me/boards'

result = requests.get(my_boards_url, params=params, headers=headers)

if result.status_code == requests.codes.ok:
    my_boards = json.loads(result.text)
else:
    print "error: %s" % result.status_code
    sys.exit(1)

for board in my_boards:
    if board['name'] == invoice_board:
        invoice_board_id = board['id']

if not invoice_board_id:
    print "couldn't find ID for board: %s" % invoice_board
    sys.exit(1)

#print "looking for billable cards in board: %s (id = %s)" % (invoice_board, invoice_board_id)
my_board_cards_url = "https://api.trello.com/1/boards/%s/cards" % invoice_board_id

result = requests.get(my_board_cards_url, params=params, headers=headers)

my_board_cards = json.loads(result.text)

total_hrs = 0

table = PrettyTable(["Card Name", "Hours"])
table.align["Card Name"] = 'l'

for card in my_board_cards:

    card_billable = False
    card_hrs = 0

    for label in card['labels']:
    
        if label['name'] == 'done':
            card_billable = True

        if 'hrs-' in label['name']:
            card_hrs += float(label['name'].replace('hrs-', ''))
            total_hrs += card_hrs

    if card_billable:
        #print card['name'], card_hrs
        table.add_row([card['name'], card_hrs])

print table
print ""
print "total hrs:", total_hrs
print ""
