#!/usr/bin/env python

# TODO deposit
# TODO withdraw
# TODO payback
# TODO borrow
# TODO fuzz
# TODO buy clause
# TODO sell clause
# TODO jet clause
# TODO high score

import random

__all__ = ['play']

games = {}

locations = ['Bronx', 'Ghetto', 'Central Park', 'Manhattan', 'Coney Island', 'Brooklyn']

drugs = ['Acid', 'Cocaine', 'Ludes', 'PCP', 'Heroin', 'Weed', 'Shrooms', 'Speed']

price_range = {
    'Acid': (1000, 4500),
    'Cocaine': (15000, 30000),
    'Ludes': (10, 60),
    'PCP': (1000, 3500),
    'Heroin': (5000, 14000),
    'Weed': (300, 900),
    'Shrooms': (600, 1350),
    'Speed': (70, 250)
}

events = [
    {'freq': 13, 'mul': 4, 'drug': 'Weed', 'message': "The cops just did a big Weed bust! Prices are sky-high!"},
    {'freq': 20, 'mul': 4, 'drug': 'PCP', 'message': "The cops just did a big PCP bust! Prices are sky-high!"},
    {'freq': 25, 'mul': 4, 'drug': 'Heroin', 'message': "The cops just did a big Heroin bust! Prices are sky-high!"},
    {'freq': 13, 'mul': 4, 'drug': 'Ludes', 'message': "The cops just did a big Ludes bust! Prices are sky-high!"},
    {'freq': 35, 'mul': 4, 'drug': 'Cocaine', 'message': "The cops just did a big Cocaine bust! Prices are sky-high!"},
    {'freq': 15, 'mul': 4, 'drug': 'Speed', 'message': "The cops just did a big Speed bust! Prices are sky-high!"},
    {'freq': 25, 'mul': 8, 'drug': 'Heroin', 'message': "Addicts are buying Heroin at outrageous prices!"},
    {'freq': 20, 'mul': 8, 'drug': 'Speed', 'message': "Addicts are buying Speed at outrageous prices!"},
    {'freq': 20, 'mul': 8, 'drug': 'PCP', 'message': "Addicts are buying PCP at outrageous prices!"},
    {'freq': 17, 'mul': 8, 'drug': 'Shrooms', 'message': "Addicts are buying Shrooms at outrageous prices!"},
    {'freq': 35, 'mul': 8, 'drug': 'Cocaine', 'message': "Addicts are buying Cocaine at outrageous prices!"},
    {'freq': 17, 'div': 8, 'drug': 'Acid', 'message': "The market has been flooded with cheap home-made Acid!"},
    {'freq': 10, 'div': 4, 'drug': 'Weed', 'message': "A Columbian freighter dusted the Coast Guard! Weed prices have bottomed out!"},
    {'freq': 11, 'div': 8, 'drug': 'Ludes', 'message': "A gang raided a local pharmacy and are selling cheap Ludes!"},
    {'freq': 55, 'add': 3, 'drug': 'Cocaine', 'message': "You found some Cocaine on a dead dude in the subway!"},
    {'freq': 45, 'add': 6, 'drug': 'Acid', 'message': "You found some Acid on a dead dude in the subway!"},
    {'freq': 35, 'add': 4, 'drug': 'PCP', 'message': "You found some PCP on a dead dude in the subway!"}
]

def pick(items):
    def option(game):
        try:
            game['input'] = items[int(game['input']) - 1]
        except:
            pass
    return option

def price_messages(game):
    def price_message(i, drug):
        price = "$%d" % game['prices'][drug] if game['prices'][drug] else 'None'
        return "%d %s %s you have %d" % (i, drug, price, game['drugs'][drug])
    return [price_message(*item) for item in enumerate(drugs, 1)]

def cash_message(game):
    return "Cash: $%d" % game['cash']

def get_total(game):
    return sum(game['drugs'].values())

def get_prices(leaveout=3):
    prices = {drug: random.randint(*price_range[drug]) for drug in drugs}
    for i in range(leaveout):
        prices[random.choice(drugs)] = 0
    return prices

def current_location(game):
    return "Current Location: %s" % game['location']

def trade(game):
    game['options'] = [buy, sell, jet, quit]
    return [
        current_location(game)
    ] + price_messages(game) + [
        cash_message(game),
        "Debt: $%d" % game['debt'],
        "Savings: $%d" % game['bank'],
        "Coat: %d/%d" % (get_total(game), game['coat'])
    ] + (['Gun'] if game['guns'] else []) + [
        "Time remaining: %d day%s" %(game['days'], 's' if game['days'] > 1 else ''),
        'buy sell jet quit'
    ]

def gameover_messages(game):
    return ["You're dead.", 'Congratulations.'] if game['cops'] == -1 else [
            "The Loan Shark's thugs broke your legs."] if game['cash'] < 0 else [
            'You retired a millionaire in the Carribbean.'] if game['cash'] > 1000000 else [
            'Congratulations!', "You didn't do half bad."] if game['cash'] > 2000 else [
            "You didn't make any money!", 'Better luck next time.']

def highscore_messages():
    return [] #XXX

def finish(game):
    game['cash'] += game['bank'] - game['debt']
    game['prices'] = get_prices(0)
    for drug in drugs:
        game['cash'] += game['prices'][drug] * game['drugs'].get(drug, 0)
        game['drugs'][drug] = 0
    game['options'] = [start]
    return [
        'Game Over',
        "Final Cash: %s$%d" % ('-' if game['cash'] < 0 else '', abs(game['cash'])),
    ] + gameover_messages(game) + highscore_messages() + ['start']

def modal(game, messages, **options):
    game['options'] = [lambda game: options.get(game['input'], lambda game: None)(game)]
    return messages

def random_events(game):
    messages = []
    for event in events:
        if dice(event['freq']) and game['prices'][event['drug']]:
            game['prices'][event['drug']] *= event.get('mul', 1)
            game['prices'][event['drug']] /= event.get('div', 1)
            game['drugs'][event['drug']] += min(event.get('add', 0), get_room(game))
            messages.append(event['message'])
    if messages:
        return modal(game, ['News Flash'] + messages + ['ok quit'], ok=loan_shark_event)
    return loan_shark_event(game)

def lack_money_messages():
    return ["Money", "You do not have that much money.", "ok quit"]

def gun_messages():
    return ['Buy a Gun', 'Would you like to buy a gun for $400?', 'no yes quit']

def buy_gun(game):
    if game['cash'] < 400:
        return modal(game, lack_money_messages(), ok=random_events)
    game['cash'] -= 400
    game['guns'] = 1
    return random_events(game)

def gun_event(game):
    if game['guns'] == 0 and dice(10):
        return modal(game, gun_messages(), yes=buy_gun, no=random_events)
    return random_events(game)

def buy_coat(game):
    if game['cash'] < 200:
        return modal(game, lack_money_messages(), ok=gun_event)
    game['cash'] -= 200
    game['coat'] += 40
    return gun_event(game)

def get_room(game):
    return game['coat'] - get_total(game)

def repay(game):
    raise NotImplementedError#XXX

def borrow(game):
    raise NotImplementedError#XXX

def loan_shark(game):
    return modal(game, [
        'Loan Shark Options',
        'What would you like to do?',
        'done repay borrow quit'
    ], done=bank_event, repay=repay, borrow=borrow)

def withdraw(game):
    raise NotImplementedError#XXX

def deposit(game):
    raise NotImplementedError#XXX

def bank(game):
    return modal(game, [
        'Bank Options',
        'What would you like to do at the Bank?',
        'done withdraw deposit quit'
    ], done=trade, withdraw=withdraw, deposit=deposit)

def bank_event(game):
    if game['location'] == 'Bronx':
        return modal(game, [
            'Bank',
            'Would you like to visit the Bank?',
            'no yes quit'
        ], yes=bank, no=trade)
    return trade(game)

def loan_shark_event(game):
    if game['location'] == 'Bronx':
        return modal(game, [
            'Loan Shark',
            'Would you like to visit the Loan Shark?',
            'no yes quit'
        ], yes=loan_shark, no=bank_event)
    return bank_event(game)

def coat_event(game):
    if dice(10):
        return modal(game, [
            'Buy a Bigger Coat',
            'Would you like to buy a trenchcoat with more pockets for $200?',
            'no yes quit'
        ], yes=buy_coat, no=gun_event)
    return gun_event(game)

def finish_event(game):
    if game['days'] == 0:
        return finish(game)
    return coat_event(game)

def dice(n):
    return random.getrandbits(32) % n == 0

def fuzz(game):
    raise NotImplementedError#XXX

def fuzz_event(game):
    if dice(7) and game['days'] > 0 and get_total(game):
        return fuzz(game)
    return finish_event(game)

def jet_location(game):
    if game['input'] == game['location']:
        return trade(game)
    if game['input'] in locations:
        game['debt'] += game['debt'] >> 3 if game['days'] < 31 else 0
        game['bank'] += game['bank'] >> 4
        game['days'] -= 1
        game['prices'] = get_prices()
        game['location'] = game['input']
        return fuzz_event(game)

def start(game):
    if game['input'] == 'start':
        game.update({
            'cash': 2000,
            'debt': 5500,
            'bank': 0,
            'coat': 100,
            'guns': 0,
            'cops': 3,
            'days': 31,
            'drug': None,
            'input': None,
            'drugs': {drug: 0 for drug in drugs},
            'prices': {drug: 0 for drug in drugs},
            'options': [pick(locations), jet_location],
            'location': None
        })
        return jet_messages() + ["%s quit" % slider(locations)]

def quit(game):
    if game['input'] == 'quit' and start not in game['options']:
        return finish(game)

def cancel(game):
    if game['input'] == 'cancel':
        return trade(game)

def slider(items):
    return "1-%d" % len(items)

def enter_amount(game):
    if game['input'].isdigit():
        game['input'] = int(game['input'])

def no_cach_messages():
    return ['Buy Drugs', 'You cannot afford any of that drug.', 'ok quit']

def no_room_messages():
    return ['Buy Drugs', 'You do not have enough room in your trenchcoat.', 'ok quit']

def buy_amount(game):
    if isinstance(game['input'], int):
        if game['input'] > game['cash']:
            return modal(game, no_cach_messages(), ok=trade)
        if game['input'] > get_room(game):
            return modal(game, no_room_messages(), ok=trade)
        game['drugs'][game['drug']] += game['input']
        game['cash'] -= game['prices'][game['drug']] * game['input']
        return trade(game)

def get_max_buy_amount(game):
    return min(game['coat'] - get_total(game), game['cash'] / game['prices'][game['drug']])

def buy_max(game):
    if game['input'] == 'max':
        game['input'] = get_max_buy_amount(game)
        return buy_amount(game)

def no_sellers_messages():
    return ['Nobody is selling that drug here.', 'ok quit']

def buy_drug(game):
    if game['input'] in drugs:
        game['drug'] = game['input']
        if game['prices'][game['drug']] == 0:
            return modal(game, no_sellers_messages(), ok=trade)
        price = game['prices'][game['drug']]
        max_amount = get_max_buy_amount(game)
        amount = max_amount if max_amount < 1000 else 'a lot'
        game['options'] = [enter_amount, buy_amount, buy_max, cancel]
        return [
            "Buy %s" % game['drug'],
            "At %d each, you can afford %s" % (price, amount),
            "How many do you want to buy?",
            cash_message(game),
            "0-%d max cancel quit" % max_amount
        ]

def buy(game):
    if game['input'] == 'buy':
        game['options'] = [pick(drugs), buy_drug, cancel, quit]
        return ['Buy Drugs'] + price_messages(game) + [
            cash_message(game),
            "%s cancel quit" % slider(drugs)
        ]

def over_sell_messages():
    return ['Sell Drugs', "You don't have that much of that drug to sell.", 'ok quit']

def sell_amount(game):
    if isinstance(game['input'], int):
        if game['input'] > game['drugs'][game['drug']]:
            return modal(game, over_sell_messages(), ok=trade)
        game['drugs'][game['drug']] -= game['input']
        game['cash'] += game['prices'][game['drug']] * game['input']
        return trade(game)

def sell_max(game):
    if game['input'] == 'max':
        game['input'] = game['drugs'][game['drug']]
        return sell_amount(game)

def no_buyers_messages():
    return ['Nobody wants to buy that drug here.', 'ok quit']

def no_drugs_messages():
    return ['You do not have any of that drug to sell.', 'ok quit']

def sell_drug(game):
    if game['input'] in drugs:
        game['drug'] = game['input']
        if not game['prices'][game['drug']]:
            return modal(game, no_buyers_messages(), ok=trade)
        if not game['drugs'][game['drug']]:
            return modal(game, no_drugs_messages(), ok=trade)
        price = game['prices'][game['drug']]
        max_amount = game['drugs'][game['drug']]
        game['options'] = [enter_amount, sell_amount, sell_max, cancel]
        return [
            "Sell %s" % game['drug'],
            "You can sell up to %d at %d each." % (max_amount, price),
            "How many do you want to sell?",
            cash_message(game),
            "0-%d max cancel quit" % max_amount
        ]

def sell(game):
    if game['input'] == 'sell':
        game['options'] = [pick(drugs), sell_drug, cancel, quit]
        return ['Sell Drugs'] + price_messages(game) + [
            cash_message(game),
            "%s cancel quit" % slider(drugs)
        ]

def jet_messages():
    return ['Where to, dude?'] + ["%d %s" % pair for pair in enumerate(locations, 1)]

def jet(game):
    if game['input'] == 'jet':
        game['options'] = [pick(locations), jet_location, cancel, quit]
        return jet_messages() + [current_location(game), "%s cancel quit" % slider(locations)]

def option_name(option): #XXX
    return getattr(option, '__name__', str(option))

def play(name, text):
    game = games.setdefault(name, {'options': [start]})
    game['input'] = text
    for option in game['options'] + [quit]:
        messages = option(game)
        if messages:
            return '\n'.join(messages)
    return 'Invalid input', 'options', [option_name(option) for option in game['options']] #XXX

def main():
    name = 'test'
    message = play(name, 'start')
    print '\n', message
    while 'Game Over' not in message:
        text = raw_input('> ')
        message = play(name, text)
        print '\n', message

if __name__ == '__main__':
    main()
