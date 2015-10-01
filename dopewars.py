#!/usr/bin/env python

# TODO high score
# TODO bank
# TODO loan shark
# TODO fuzz
# TODO clear finished games

from operator import add, mul, div
import random

__all__ = ['start', 'is_finish', 'get_message', 'process']

locations = ['Bronx', 'Ghetto', 'Central Park', 'Manhattan', 'Coney Island', 'Brooklyn']

drugs = ['Acid', 'Cocaine', 'Ludes', 'PCP', 'Heroin', 'Weed', 'Shrooms', 'Speed']

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

games = {}

def randint():
    return random.randrange(0, 2 << 31)

def dice(n):
    return randint() % n == 0

def get_prices(leaveout=3):
    keys = random.sample(drugs, len(drugs) - random.randint(0, leaveout))
    return {k: random.randint(price_range[k]['low'], price_range[k]['high']) for k in keys}

def get_total(game):
    return sum(game['drugs'].values())

def select(items, input):
    try:
        return items[int(input) - 1]
    except:
        return None

def selector(items):
    return "1-%d" % len(items)

def goto_trade(game, append=False):
    if not append:
        game['messages'] = []
    game['options'] = [buy, sell, jet, quit]
    game['messages'] += trade_messages(game) + ['buy sell jet quit']
    return True

def gameover_messages(game):
    if game['cops'] == -1:
        return ["You're dead.", 'Congratulations.']
    elif game['cash'] < 0:
        return ["The Loan Shark's thugs broke your legs."]
    elif game['cash'] > 1000000:
        return ['You retired a millionaire in the Carribbean.']
    elif game['cash'] > 2000:
        return ['Congratulations!', "You didn't do half bad."]
    else:
        return ["You didn't make any money!", 'Better luck next time.']

def goto_finish(game):
    game['cash'] += game['bank'] - game['debt']
    game['prices'] = get_prices(0)
    for drug in drugs:
        game['cash'] += game['prices'][drug] * game['drugs'].get(drug, 0)
        game['drugs'][drug] = 0
    game['messages'] = [
        'Game Over',
        "Final Cash: $%d" % game['cash'],
    ] + gameover_messages(game) + [
        'High Scores', # XXX
        'Start New Game',
        'start'
    ]
    game['options'] = []
    game['finish'] = True
    return True

#action
def quit(game, input):
    if input == 'quit' or input == 'q':
        return goto_finish(game)

#action
def buy_amount(game, input):
    amount = int(input) if input.isdigit() else -1
    if amount >= 0:
        drug = game['drug']
        price = game['prices'][drug]
        max_amount = game['cash'] / price
        if amount > max_amount:
            game['messages'] = ['Buy Drugs', 'You cannot afford any of that drug.']
            return goto_trade(game, append=True)
        if get_total(game) + amount > game['coat']:
            game['messages'] = ['Sell Drugs', 'You do not have enough room in your trenchcoat.']
            return goto_trade(game, append=True)
        game['drugs'][drug] = game['drugs'].get(drug, 0) + amount
        game['cash'] -= price * amount
        return goto_trade(game)

#action
def buy_max(game, input):
    if input == 'max':
        amount = game['cash'] / game['prices'][game['drug']]
        return buy_amount(game, str(amount))

#action
def buy_drug(game, input):
    drug = select(drugs, input)
    if not drug:
        return
    if drug not in game['prices']:
        game['messages'] = ['Nobody is selling that drug here.']
        return goto_trade(game, append=True)
    price = game['prices'][drug]
    max_amount = min(game['coat'] - get_total(game), game['cash'] / price)
    amount = max_amount if max_amount < 1000 else 'a lot'
    game['drug'] = drug
    game['options'] = [buy_amount, buy_max, cancel, quit]
    game['messages'] = [
        "Buy %s" % drug,
        "At %d each, you can afford %s" % (price, amount),
        "How many do you want to buy?",
        cash_message(game),
        "0-%d max cancel quit" % max_amount
    ]
    return True

#action
def buy(game, input):
    if input == 'buy':
        game['options'] = [buy_drug, cancel, quit]
        game['messages'] = ['Buy Drugs'] + price_messages(game) + [
            cash_message(game),
            "%s cancel quit" % selector(drugs)
        ]
        return True
    args = input.split()
    if len(args) == 3 and args[0] == 'buy':
        r = buy_drug(game, args[1])
        if buy_amount in game['options']:
            return buy_amount(game, args[2]) or buy_max(game, args[2])
        return r

#action
def sell_amount(game, input):
    amount = int(input) if input.isdigit() else -1
    if amount >= 0:
        drug = game['drug']
        price = game['prices'][drug]
        max_amount = game['drugs'][drug]
        if amount > max_amount:
            game['messages'] = ['Sell Drugs', "You don't have that much of that drug to sell."]
            return goto_trade(game, append=True)
        game['drugs'][drug] = game['drugs'].get(drug, 0) - amount
        game['cash'] += price * amount
        return goto_trade(game)

#action
def sell_max(game, input):
    if input == 'max':
        amount = game['drugs'][game['drug']]
        return sell_amount(game, str(amount))

#action
def sell_drug(game, input):
    drug = select(drugs, input)
    if not drug:
        return
    if drug not in game['prices']:
        game['messages'] = ['Nobody wants to buy that drug here.']
        return goto_trade(game, append=True)
    if drug not in game['drugs']:
        game['messages'] = ['You do not have any of that drug to sell.']
        return goto_trade(game, append=True)
    price = game['prices'][drug]
    max_amount = game['drugs'][drug]
    game['drug'] = drug
    game['options'] = [sell_amount, sell_max, cancel, quit]
    game['messages'] = [
        "Sell %s" % drug,
        "You can sell up to %d at %d each." % (max_amount, price),
        "How many do you want to sell?",
        cash_message(game),
        "0-%d max cancel quit" % max_amount
    ]
    return True

#action
def sell(game, input):
    if input == 'sell':
        game['options'] = [sell_drug, cancel, quit]
        game['messages'] = ['Sell Drugs'] + price_messages(game) + [
            cash_message(game),
            "%s cancel quit" % selector(drugs)
        ]
        return True
    args = input.split()
    if len(args) == 3 and args[0] == 'sell':
        r = sell_drug(game, args[1])
        if sell_amount in game['options']:
            return sell_amount(game, args[2]) or sell_max(game, args[2])
        return r

def format_price(game, drug):
    amount = game['drugs'].get(drug, 0)
    price = game['prices'].get(drug)
    price = "$%d" % price if price else 'None'
    return "%s %s carry %d" % (drug, price, amount)

def price_messages(game):
    return ["%d %s" % (i, format_price(game, drug)) for i, drug in enumerate(drugs, 1)]

def cash_message(game):
    return "Cash: $%d" % game['cash']

def trade_messages(game):
    return [game['location']] + price_messages(game) + [
        cash_message(game),
        "Debt: $%d" % game['debt'],
        "Savings: $%d" % game['bank'],
        "Coat: %d/%d" % (get_total(game), game['coat'])
    ] + (['Gun'] if game['guns'] else []) + [
        "Time remaining: %d day%s" %(game['days'], 's' if game['days'] > 1 else ''),
    ]

#action
def jet_location(game, input):
    location = select(locations, input)
    if not location:
        return
    assert location != game['location'], 'same location'
    game['debt'] += game['debt'] >> 3 if game['days'] < 31 else 0
    game['bank'] += game['bank'] >> 4
    game['days'] -= 1
    game['prices'] = get_prices()
    game['location'] = location
    return fuzz_event(game)

#action
def cancel(game, input):
    if input == 'cancel':
        return goto_trade(game)

def jet_messages():
    return ['Where to, dude?'] + ["%d %s" % pair for pair in enumerate(locations, 1)]

#action
def jet(game, input):
    if input == 'jet':
        game['options'] = [jet_location, cancel, quit]
        game['messages'] = jet_messages() + ["%s cancel quit" % selector(locations)]
        return True
    args = input.split()
    if len(args) == 2 and args[0] == 'jet':
        return jet_location(game, args[1])

def start(name):
    id = randint()
    while id in games:
        id = randint()
    games[id] = {
        'id': id,
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
        'prices': {},
        'drug': '',
        'options': [jet_location, quit],
        'messages': jet_messages() + ["%s quit" % selector(locations)],
        'finish': False,
        'modal': {}
    }
    return id

def process(id, input):
    assert id in games, 'invalid id'
    game = games[id]
    for option in game['options'][:]:
        if option(game, input):
            return True
    assert 0, 'invalid input'

def fuzz_event(game):
    if dice(7) and game['days'] > 0 and get_total(game) > 0:
        return goto_fuzz(game)
    return finish_event(game)

def goto_fuzz(game):
    print 'NotImplemented'
    return finish_event(game) # XXX

def finish_event(game):
    if game['days'] == 0:
        return goto_finish(game)
    return coat_event(game)

def coat_event(game):
    if dice(10):
        game['messages'] = [
            'Buy a Bigger Coat',
            'Would you like to buy a trenchcoat with more pockets for $200?',
            'no yes quit'
        ]
        return modal(game, yes=buy_coat, no=gun_event)
    return gun_event(game)

def buy_coat(game):
    if game['cash'] < 200:
        return lack_money(game, ok=gun_event)
    game['cash'] -= 200
    game['coat'] += 40
    return gun_event(game)

def gun_event(game):
    if game['guns'] == 0 and dice(10):
        game['messages'] = [
            'Buy a Gun',
            'Would you like to buy a gun for $400?',
            'no yes quit'
        ]
        return modal(game, yes=buy_gun, no=random_events)
    return random_events(game)

def buy_gun(game):
    if game['cash'] < 400:
        return lack_money(game, ok=random_events)
    game['cash'] -= 400
    game['guns'] = 1
    return random_events(game)

def random_events(game):
    messages = []
    for event in events:
        drug = event['drug']
        if dice(event['freq']) and drug in game['prices']:
            messages.append(event['message'])
            if event['op'] == add:
                game['drugs'][drug] = game['drugs'].get(drug, 0) + event['amount']
            else:
                price = event['op'](game['prices'][drug], event['amount'])
            game['prices'][drug] = price
    if messages:
        game['messages'] = ['News Flash'] + messages + ['ok quit']
        return modal(game, ok=loan_shark_event)
    return loan_shark_event(game)

def lack_money(game, **kw):
    game['messages'] = ["Money", "You do not have that much money.", "ok quit"]
    return modal(game, **kw)

def loan_shark_event(game):
    if game['location'] == 'Bronx':
        messages = ['Loan Shark', 'Would you like to visit the Loan Shark?', 'no yes quit']
        game['messages'] = messages
        return modal(game, yes=loan_shark, no=bank_event)
    return bank_event(game)

def loan_shark(game):
    game['messages'] = [
        'Loan Shark Options',
        'What would you like to do?',
        'done repay borrow quit'
    ]
    return modal(game, done=bank_event, repay=repay, borrow=borrow)

def repay(game):
    raise NotImplementedError

def borrow(game):
    raise NotImplementedError

def bank_event(game):
    if game['location'] == 'Bronx':
        game['messages'] = ['Bank', 'Would you like to visit the Bank?', 'no yes quit']
        return modal(game, yes=bank, no=goto_trade)
    return goto_trade(game)

def bank(game):
    game['messages'] = [
        'Bank Options',
        'What would you like to do at the Bank?',
        'done withdraw deposit quit'
    ]
    return modal(game, done=goto_trade, withdraw=withdraw, deposit=deposit)

def withdraw(game):
    raise NotImplementedError

def deposit(game):
    raise NotImplementedError

def modal(game, **kw):
    game['options'] = [answer, quit]
    game['modal'] = kw
    return True

def answer(game, input):
    if input in game['modal']:
        return game['modal'][input](game)

def is_finish(id):
    # XXX garbage collection
    assert id in games, 'invalid id'
    game = games[id]
    return game['finish']

def get_message(id):
    assert id in games, 'invalid id'
    game = games[id]
    return '\n'.join(game['messages'])

def main():
    name = raw_input('Enter your name: ')
    id = start(name)
    while not is_finish(id):
        try:
            print
            print get_message(id)
            input = raw_input('> ')
            process(id, input)
        except:
            import traceback
            traceback.print_exc()
    print
    print get_message(id)

if __name__ == '__main__':
    main()

