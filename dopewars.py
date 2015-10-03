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

def location_messages(game):
    return ['Where to, dude?'] + ["%d %s" % pair for pair in enumerate(locations, 1)]

def jet_messages(game):
    return location_messages(game) + [location_message(game), "%s cancel quit" % slider(locations)]

def start_messages(game):
    return location_messages(game) + ["%s quit" % slider(locations)]

def trade_messages(game):
    return [
        location_message(game)
    ] + price_messages(game) + [
        cash_message(game),
        "Debt: $%d" % game['debt'],
        "Savings: $%d" % game['bank'],
        "Coat: %d/%d" % (get_total(game), game['coat'])
    ] + (['Gun'] if game['guns'] else []) + [
        "Time remaining: %d day%s" %(game['days'], 's' if game['days'] > 1 else ''),
        'buy sell jet quit'
    ]

def buy_drug_messages(game):
    return [
        "Buy %s" % game['drug'],
        "At %d each, you can afford %s" % (game['prices'][game['drug']], get_display_max(game)),
        "How many do you want to buy?",
        cash_message(game),
        "0-%d max cancel quit" % get_max_amount(game)
    ]

def buy_messages(game):
    return ['Buy Drugs'] + price_messages(game) + [
        cash_message(game),
        "%s cancel quit" % slider(drugs)
    ]

def sell_drug_messages(game):
    return [
        "Sell %s" % game['drug'],
        "You can sell up to %d at %d each." % (game['drugs'][game['drug']], game['prices'][game['drug']]),
        "How many do you want to sell?",
        cash_message(game),
        "0-%d max cancel quit" % game['drugs'][game['drug']]
    ]

def location_message(game):
    return "Current Location: %s" % game['location']

def cash_message(game):
    return "Cash: $%d" % game['cash']

def price_messages(game):
    def price_message(i, drug):
        price = "$%d" % game['prices'][drug] if game['prices'][drug] else 'None'
        return "%d %s %s you have %d" % (i, drug, price, game['drugs'][drug])
    return [price_message(*item) for item in enumerate(drugs, 1)]

def sell_messages(game):
    return ['Sell Drugs'] + price_messages(game) + [
        cash_message(game),
        "%s cancel quit" % slider(drugs)
    ]

def coat_event_messages(game):
    return [
        'Buy a Bigger Coat',
        'Would you like to buy a trenchcoat with more pockets for $200?',
        'no yes quit'
    ]

def gun_messages(game):
    return ['Buy a Gun', 'Would you like to buy a gun for $400?', 'no yes quit']

def lack_money_messages(game):
    return ["Money", "You do not have that much money.", "ok quit"]

def no_cach_messages(game):
    return ['Buy Drugs', 'You cannot afford any of that drug.', 'ok quit']

def no_room_messages(game):
    return ['Buy Drugs', 'You do not have enough room in your trenchcoat.', 'ok quit']

def no_sellers_messages(game):
    return ['Nobody is selling that drug here.', 'ok quit']

def over_sell_messages(game):
    return ['Sell Drugs', "You don't have that much of that drug to sell.", 'ok quit']

def no_buyers_messages(game):
    return ['Nobody wants to buy that drug here.', 'ok quit']

def no_drugs_messages(game):
    return ['You do not have any of that drug to sell.', 'ok quit']

def loan_shark_event_messages(game):
    return ['Loan Shark', 'Would you like to visit the Loan Shark?', 'no yes quit']

def loan_shark_messages(game):
    return ['Loan Shark Options', 'What would you like to do?', 'done repay borrow quit']

def bank_event_messages(game):
    return ['Bank', 'Would you like to visit the Bank?', 'no yes quit']

def bank_messages(game):
    return ['Bank Options', 'What would you like to do at the Bank?', 'done withdraw deposit quit']

def gameover_messages(game):
    return (["You're dead.", 'Congratulations.'] if game['cops'] == -1 else
            ["The Loan Shark's thugs broke your legs."] if game['cash'] < 0 else
            ['You retired a millionaire in the Carribbean.'] if game['cash'] > 1000000 else
            ['Congratulations!', "You didn't do half bad."] if game['cash'] > 2000 else
            ["You didn't make any money!", 'Better luck next time.'])

def highscore_messages(game):
    return [] #XXX

def finish_messages(game):
    return [
        'Game Over',
        "Final Cash: %s$%d" % ('-' if game['cash'] < 0 else '', abs(game['cash'])),
    ] + gameover_messages(game) + highscore_messages(game) + ['start']

def pick(input, items):
    try:
        return items[int(input) - 1]
    except:
        pass

def get_prices(leaveout=3):
    prices = {drug: random.randint(*price_range[drug]) for drug in drugs}
    for i in range(leaveout):
        prices[random.choice(drugs)] = 0
    return prices

def dice(n):
    return random.getrandbits(32) % n == 0

def slider(items):
    return "1-%d" % len(items)

def get_total(game):
    return sum(game['drugs'].values())

def get_room(game):
    return game['coat'] - get_total(game)

def get_display_max(game):
    max_amount = get_max_amount(game)
    return max_amount if max_amount < 1000 else 'a lot'

def get_max_amount(game):
    return min(game['coat'] - get_total(game), game['cash'] / game['prices'][game['drug']])

def make_options(**kw):
    return [lambda game: kw.get(game['input'], lambda game: None)(game)] if kw else []

def reply(game, messages, options=[], **kw):
    game['options'] = options + make_options(**kw)
    return messages

def trade(game):
    return reply(game, trade_messages(game), buy=buy, sell=sell, jet=jet)

def finish(game):
    game['cash'] += game['bank'] - game['debt']
    game['prices'] = get_prices(0)
    for drug in drugs:
        game['cash'] += game['prices'][drug] * game['drugs'].get(drug, 0)
        game['drugs'][drug] = 0
    return reply(game, finish_messages(game))

def random_events(game):
    messages = []
    for event in events:
        if dice(event['freq']) and game['prices'][event['drug']]:
            game['prices'][event['drug']] *= event.get('mul', 1)
            game['prices'][event['drug']] /= event.get('div', 1)
            game['drugs'][event['drug']] += min(event.get('add', 0), get_room(game))
            messages.append(event['message'])
    if messages:
        return reply(game, ['News Flash'] + messages + ['ok quit'], ok=loan_shark_event)
    return loan_shark_event(game)

def buy_gun(game):
    if game['cash'] < 400:
        return reply(game, lack_money_messages(game), ok=random_events)
    game['cash'] -= 400
    game['guns'] = 1
    return random_events(game)

def gun_event(game):
    if game['guns'] == 0 and dice(10):
        return reply(game, gun_messages(game), yes=buy_gun, no=random_events)
    return random_events(game)

def buy_coat(game):
    if game['cash'] < 200:
        return reply(game, lack_money_messages(game), ok=gun_event)
    game['cash'] -= 200
    game['coat'] += 40
    return gun_event(game)

def repay(game):
    raise NotImplementedError#XXX

def borrow(game):
    raise NotImplementedError#XXX

def loan_shark(game):
    return reply(game, loan_shark_messages(game), done=bank_event, repay=repay, borrow=borrow)

def withdraw(game):
    raise NotImplementedError#XXX

def deposit(game):
    raise NotImplementedError#XXX

def bank(game):
    return reply(game, bank_messages(game), done=trade, withdraw=withdraw, deposit=deposit)

def bank_event(game):
    if game['location'] == 'Bronx':
        return reply(game, bank_event_messages(game), yes=bank, no=trade)
    return trade(game)

def loan_shark_event(game):
    if game['location'] == 'Bronx':
        return reply(game, loan_shark_event_messages(game), yes=loan_shark, no=bank_event)
    return bank_event(game)

def coat_event(game):
    if dice(10):
        return reply(game, coat_event_messages(game), yes=buy_coat, no=gun_event)
    return gun_event(game)

def finish_event(game):
    if game['days'] == 0:
        return finish(game)
    return coat_event(game)

def fuzz(game):
    raise NotImplementedError#XXX

def fuzz_event(game):
    if dice(7) and game['days'] > 0 and get_total(game):
        return fuzz(game)
    return finish_event(game)

def jet_location(game):
    location = pick(game['input'], locations)
    if location and location == game['location']:
        return trade(game)
    if location in locations:
        game['debt'] += game['debt'] >> 3 if game['days'] < 31 else 0
        game['bank'] += game['bank'] >> 4
        game['days'] -= 1
        game['prices'] = get_prices()
        game['location'] = location
        return fuzz_event(game)

def buy_amount(game):
    amount = (int(game['input']) if game['input'].isdigit() else
              get_max_amount(game) if game['input'] == 'max' else -1)
    if amount >= 0:
        if amount > game['cash']:
            return reply(game, no_cach_messages(game), ok=trade)
        if amount > get_room(game):
            return reply(game, no_room_messages(game), ok=trade)
        game['drugs'][game['drug']] += amount
        game['cash'] -= game['prices'][game['drug']] * amount
        return trade(game)

def buy_drug(game):
    drug = pick(game['input'], drugs)
    if drug in drugs:
        if game['prices'][drug] == 0:
            return reply(game, no_sellers_messages(game), ok=trade)
        game['drug'] = drug
        return reply(game, buy_drug_messages(game), [buy_amount], cancel=trade)

def sell_amount(game):
    amount = (int(game['input']) if game['input'].isdigit() else
              game['drugs'][game['drug']] if game['input'] == 'max' else -1)
    if amount >= 0:
        if amount > game['drugs'][game['drug']]:
            return reply(game, over_sell_messages(game), ok=trade)
        game['drugs'][game['drug']] -= amount
        game['cash'] += game['prices'][game['drug']] * amount
        return trade(game)

def sell_drug(game):
    drug = pick(game['input'], drugs)
    if drug in drugs:
        if not game['prices'][drug]:
            return reply(game, no_buyers_messages(game), ok=trade)
        if not game['drugs'][drug]:
            return reply(game, no_drugs_messages(game), ok=trade)
        game['drug'] = drug
        return reply(game, sell_drug_messages(game), [sell_amount], cancel=trade)

def buy(game):
    return reply(game, buy_messages(game), [buy_drug], cancel=trade)

def sell(game):
    return reply(game, sell_messages(game), [sell_drug], cancel=trade)

def jet(game):
    return reply(game, jet_messages(game), [jet_location], cancel=trade)

def start(game):
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
        'options': [],
        'location': None
    })
    return reply(game, start_messages(game), [jet_location])

def play(name, command):
    game = games.setdefault(name, {'options': make_options(start=start)})
    game['input'] = command
    for option in game['options'] + make_options(quit=finish):
        messages = option(game)
        if not game['options']:
            del games[name]
        if messages:
            return '\n'.join(messages)
    return ''

def main():
    name = 'test'
    message = play(name, 'start')
    print message
    while 'Game Over' not in message:
        message = play(name, raw_input('> '))
        print '\n', message

if __name__ == '__main__':
    main()
