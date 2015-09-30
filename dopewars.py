#!/usr/bin/env python

from copy import deepcopy
from operator import add, mul, div
import random

events = [
    {'freq': 13, 'op': mul, 'amount': 4, 'drug': 'Weed', 'message': "The cops just did a big Weed bust!  Prices are sky-high!"},
    {'freq': 20, 'op': mul, 'amount': 4, 'drug': 'PCP', 'message': "The cops just did a big PCP bust!  Prices are sky-high!"},
    {'freq': 25, 'op': mul, 'amount': 4, 'drug': 'Heroin', 'message': "The cops just did a big Heroin bust!  Prices are sky-high!"},
    {'freq': 13, 'op': mul, 'amount': 4, 'drug': 'Ludes', 'message': "The cops just did a big Ludes bust!  Prices are sky-high!"},
    {'freq': 35, 'op': mul, 'amount': 4, 'drug': 'Cocaine', 'message': "The cops just did a big Cocaine bust!  Prices are sky-high!"},
    {'freq': 15, 'op': mul, 'amount': 4, 'drug': 'Speed', 'message': "The cops just did a big Speed bust!  Prices are sky-high!"},
    {'freq': 25, 'op': mul, 'amount': 8, 'drug': 'Heroin', 'message': "Addicts are buying Heroin at outrageous prices!"},
    {'freq': 20, 'op': mul, 'amount': 8, 'drug': 'Speed', 'message': "Addicts are buying Speed at outrageous prices!"},
    {'freq': 20, 'op': mul, 'amount': 8, 'drug': 'PCP', 'message': "Addicts are buying PCP at outrageous prices!"},
    {'freq': 17, 'op': mul, 'amount': 8, 'drug': 'Shrooms', 'message': "Addicts are buying Shrooms at outrageous prices!"},
    {'freq': 35, 'op': mul, 'amount': 8, 'drug': 'Cocaine', 'message': "Addicts are buying Cocaine at outrageous prices!"},
    {'freq': 17, 'op': div, 'amount': 8, 'drug': 'Acid', 'message': "The market has been flooded with cheap home-made Acid!"},
    {'freq': 10, 'op': div, 'amount': 4, 'drug': 'Weed', 'message': "A Columbian freighter dusted the Coast Guard!  Weed prices have bottomed out!"},
    {'freq': 11, 'op': div, 'amount': 8, 'drug': 'Ludes', 'message': "A gang raided a local pharmacy and are selling cheap Ludes!"},
    {'freq': 55, 'op': add, 'amount': 3, 'drug': 'Cocaine', 'message': "You found some Cocaine on a dead dude in the subway!"},
    {'freq': 45, 'op': add, 'amount': 6, 'drug': 'Acid', 'message': "You found some Acid on a dead dude in the subway!"},
    {'freq': 35, 'op': add, 'amount': 4, 'drug': 'PCP', 'message': "You found some PCP on a dead dude in the subway!"}
]

drugs = ['Acid', 'Cocaine', 'Ludes', 'PCP', 'Heroin', 'Weed', 'Shrooms', 'Speed']
locations = ['Bronx', 'Ghetto', 'Central Park', 'Manhattan', 'Coney Island', 'Brooklyn']
price_range = {
    'Acid': {'low': 1000, 'high': 4500},
    'Cocaine': {'low': 15000, 'high': 30000},
    'Ludes': {'low': 10, 'high': 60},
    'PCP': {'low': 1000, 'high': 3500},
    'Heroin': {'low': 5000, 'high': 14000},
    'Weed': {'low': 300, 'high': 900},
    'Shrooms': {'low': 600, 'high': 1350},
    'Speed': {'low': 70, 'high': 250}
}

sessions = {}

def randint():
    return random.randrange(0, 2 << 31)

def dice(n):
    return randint() % n == 0

def public(func):
    def new_func(*args, **kw):
        game = func(*args, **kw)
        game['messages'] += get_messages(game)
        return deepcopy(game)
    return new_func

def get_prices(leaveout=3):
    keys = random.sample(drugs, len(drugs) - random.randint(0, leaveout))
    return {k: random.randint(price_range[k]['low'], price_range[k]['high']) for k in keys}

def get_messages(game):
    messages = []
    state = game['state']
    if state == 'jet':
        messages = ['Where to, dude?']
    elif state == 'buy_sell':
        for drug in drugs:
            count = game['drugs'].get(drug, 0)
            price = game['prices'].get(drug)
            dollar = '$' if price else ''
            messages.append("%s amount: %d price: %s%s" % (drug, count, dollar, str(price)))
        messages.append("Cash $%d" % game['cash'])
        messages.append("Debt $%d" % game['debt'])
        messages.append("Savings $%d" % game['bank'])
        messages.append("Coat %d/%d" % (get_total(game), game['coat']))
    elif state == 'buy_select':
        drug = game['select']
        price = game['prices'][drug]
        amount = game['cash'] / price
        amount = amount if amount < 1000 else 'a lot'
        messages = ["Buy %s at %d each, you can afford %s" % (drug, price, amount)]
    return messages

def get_total(game):
    return sum(game['drugs'].values())

@public
def start(name):
    session = randint()
    while session in sessions:
        session = randint()
    sessions[session] = {
        'session': session,
        'name': name,
        'drugs': {},
        'cash': 2000,
        'debt': 5500,
        'bank': 0,
        'coat': 100,
        'guns': 0,
        'location': '',
        'days': 31,
        'cops': 3,
        'prices': get_prices(),
        'select': '',
        'messages': [],
        'state': 'jet',
        'options': locations,
        'finish': False
    }
    return sessions[session]

def validate(arg, options):
    try:
        if isinstance(options, dict):
            return options['type'](arg)
        assert arg in options
        return arg
    except:
        assert 0, 'invalid input'

@public
def transition(session, arg):
    assert session in sessions, 'invalid session'
    game = sessions[session]
    state = game['state']
    game['messages'] = []
    print 'state', state, 'arg', arg, 'options', game['options']
    arg = validate(arg, game['options'])
    print 'arg', arg
    if arg == 'jet':
        game.update(state='jet', options=locations+['cancel'])
        return game
    elif arg == 'cancel':
        game['state'] = 'buy_sell'
        return game
    elif state == 'jet':
        return jet(game, arg)
    elif arg == 'buy':
        game.update(state='buy', options=drugs)
        return game
    elif arg == 'sell':
        game.update(state='sell', options=drugs)
        return game
    elif state == 'buy':
        game.update(state='buy_select', select=arg, options={'type': int})
        return game
    elif state == 'sell':
        game.update(state='sell_select', select=arg, options={'type': int})
        return game
    elif state == 'buy_select':
        return buy(game, game['select'], arg)
    elif state == 'sell_select':
        return sell(game, game['select'], arg)
    assert 0, 'invalid state'

def jet(game, location):
    print 'jet', 'location', location
    assert location in locations and location != game['location'], 'invalid location'
    game['debt'] += game['debt'] >> 3 if game['days'] < 31 else 0
    game['bank'] += game['bank'] >> 4
    game['days'] -= 1
    game['prices'] = get_prices()
    game['messages'] = []
    #dice_fuzz(state)
    game['state'] = 'buy_sell'
    game['options'] = ['buy', 'sell', 'jet']
    return game

def buy(game, drug, Amount):
    raise NotImplementedError

def sell(game, drug, Amount):
    raise NotImplementedError

@public
def fuzz_event(game):
    if dice(7) and game['days'] > 0 and get_total(game) > 0:
        return dict(game, options=['fight', 'escape'])
    return finish_event(game)

@public
def finish_event(game):
    if game['days'] == 0:
        pass # XXX finish
    return coat_event(game)

@public
def coat_event(game):
    if dice(10):
        return dict(game, options=['buycoat', 'notbuycoat'])
    return gun_event(game)

@public
def gun_event(game):
    if game['guns'] == 0 and dice(10):
        return dict(game, options=['buygun', 'notbuygun'])
    return random_events(game)

@public
def random_events(game):
    for event in events:
        if dice(event['freq']) and event['drug'] in game['prices']:
            game['messages'].append(event['message'])
            price = event['op'](game['prices'][event['drug']], event['amount'])
            game['prices'][event['drug']] = price
    return loan_shark_event(game)

@public
def loan_shark_event(game):
    if location == 'Bronx':
        return dict(game, options=['visit_loan_shark', 'not_visit_loan_shark'])
    return bank_event(game)

@public
def bank_event(game):
    if location == 'Bronx':
        return dict(game, options=['visit_bank', 'not_visit_bank'])
    return dict(game, options=['buy', 'sell', 'jet'])

def main():
    name = raw_input('Enter your name: ')
    game = start(name)
    while not game['finish']:
        try:
            print '\n'.join(game['messages'])
            options = game['options']
            if isinstance(options, list):
                print 'Options:'
                for i, option in enumerate(game['options']):
                    print i, option
            print 'q Quit'
            arg = raw_input('? ')
            if arg == 'q':
                break
            if isinstance(options, list):
                arg = options[int(arg)]
            game = transition(game['session'], arg)
        except:
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    main()

