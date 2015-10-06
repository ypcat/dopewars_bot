#!/usr/bin/env python

# TODO help
# TODO enter name for highscore

import json
import os
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

def get_messages(game):
    messages = {
        'start': [location_messages, slider(locations)],
        'trade': [location_message, price_messages, cash_message, debt_message, bank_message, coat_message, guns_messages, days_message, '/buy /sell /jet'],
        'jet': [location_messages, location_message, slider(locations) + ' /cancel'],
        'buy': ['Buy Drugs', price_messages, cash_message, slider(drugs) + ' /cancel'],
        'sell': ['Sell Drugs', price_messages, cash_message, slider(drugs) + ' /cancel'],
        'buy_drug': [buy_drug_messages],
        'sell_drug': [sell_drug_messages],
        'coat_event': ['Buy a Bigger Coat', 'Would you like to buy a trenchcoat with more pockets for $200?', '/no /yes'],
        'gun_event': ['Buy a Gun', 'Would you like to buy a gun for $400?', '/no /yes'],
        'lack_money': ["Money", "You do not have that much money.", "/ok"],
        'no_cash': ['Buy Drugs', 'You cannot afford any of that drug.', '/ok'],
        'no_room': ['Buy Drugs', 'You do not have enough room in your trenchcoat.', '/ok'],
        'no_sellers': ['Nobody is selling that drug here.', '/ok'],
        'over_sell': ['Sell Drugs', "You don't have that much of that drug to sell.", '/ok'],
        'no_buyers': ['Nobody wants to buy that drug here.', '/ok'],
        'no_drugs': ['You do not have any of that drug to sell.', '/ok'],
        'news': ['News Flash', news_messages, '/ok'],
        'bank': ['Bank Options', 'What would you like to do at the Bank?', cash_message, bank_message, '/done /withdraw /deposit'],
        'shark': ['Loan Shark Options', 'What would you like to do?', cash_message, debt_message, '/done /repay /borrow'],
        'bank_event': ['Bank', 'Would you like to visit the Bank?', cash_message, bank_message, '/no /yes'],
        'shark_event': ['Loan Shark', 'Would you like to visit the Loan Shark?', cash_message, debt_message, '/no /yes'],
        'withdraw': ['Bank', 'How much would you like to withdraw?', cash_message, bank_message, withdraw_option_message],
        'deposit': ['Bank', 'How much would you like to deposit?', cash_message, bank_message, deposit_option_message],
        'repay': ['Loan Shark', 'How much would you like to repay?', cash_message, debt_message, repay_option_message],
        'borrow': ['Loan Shark', 'How much would you like to borrow?', cash_message, debt_message, borrow_option_message],
        'lack_bank': ['Money', 'You do not have that much money in the bank.', '/ok'],
        'over_pay': ['Money', 'You should not overpay the Loan Shark.', '/ok'],
        'no_more_loans': ['Loan Shark', 'The Loan Shark will not loan you any more money today.', '/ok'],
        'borrow_limit': ['Credit Risk', 'The Loan Shark is unwilling to loan you that much money.', borrow_limit_message, '/ok'],
        'no_debt': ['Money', 'You do not have any debt.', '/ok'],
        'fuzz': ['Police', chase_message, 'What do you do?', '/run /fight'],
        'no_gun': ['Gun', 'You do not have a gun.', '/ok'],
        'ran': ['Police', 'You lost them in the alleys.', '/ok'],
        'miss': ['Police', 'You shot at the cops, but missed.', '/ok'],
        'hit': ['Police', 'You shot and killed one of the cops.', '/ok'],
        'kill': ['Police', 'The cops shot you.', 'You died.', '/ok'],
        'remain': ['Police', still_chase_message, 'What do you do?', '/run /fight'],
        'missed': ['Police', 'The cops shot at you, but missed.', '/ok'],
        'wounded': ['Police', 'The cops shot you, and you are wounded.', '/ok'],
        'seize': ['Busted!', 'The cops seized all your dope and half your cash.', '/ok'],
        'caught': ['Police', 'You ran into a dead end, and the cops found you.', '/ok'],
        'achive_highscore': ['New High Score', 'You have achieved a new high score!', '/ok'],
        'finish': ['Game Over', final_cash_message, gameover_messages, highscore_messages, '/start']
    }[game['state']]
    def flatten(a):
        return [j for i in a for j in (i if isinstance(i, list) else [i])]
    return flatten([m(game) if callable(m) else m for m in messages])

def buy_drug_messages(game):
    return [
        "Buy %s" % game['drug'],
        "At %d each, you can afford %s" % (game['prices'][game['drug']], get_display_max(game)),
        "How many do you want to buy?",
        cash_message(game),
        "0-%d /cancel /max" % get_max_buy(game)
    ]

def sell_drug_messages(game):
    return [
        "Sell %s" % game['drug'],
        "You can sell up to %d at %d each." % (game['drugs'][game['drug']], game['prices'][game['drug']]),
        "How many do you want to sell?",
        cash_message(game),
        "0-%d /cancel /max" % game['drugs'][game['drug']]
    ]

def news_messages(game):
    return game['news']

def final_cash_message(game):
    return "Final Cash: %s$%d" % ('-' if game['cash'] < 0 else '', abs(game['cash']))

def location_messages(game):
    return ['Where to, dude?'] + ["/%d %s" % pair for pair in enumerate(locations, 1)]

def price_messages(game):
    def price_message(i, drug):
        price = "$%d" % game['prices'][drug] if game['prices'][drug] else 'None'
        return "/%d %s %s you have %d" % (i, drug, price, game['drugs'][drug])
    return [price_message(*item) for item in enumerate(drugs, 1)]

def borrow_limit_message(game):
    return 'He will loan you a maximum of $%d' % get_max_loan(game)

def repay_option_message(game):
    return "0-%d /cancel /max" % get_max_repay(game)

def borrow_option_message(game):
    return "0-%d /cancel /max" % get_max_loan(game)

def withdraw_option_message(game):
    return "0-%d /cancel /max" % get_max_withdraw(game)

def deposit_option_message(game):
    return "0-%d /cancel /max" % get_max_deposit(game)

def chase_message(game):
    return "Officer Hardass %s chasing you!" % cops_message(game)

def still_chase_message(game):
    return "Officer Hardass %s still chasing you!" % cops_message(game)

def gameover_messages(game):
    return (["You're dead.", 'Congratulations.'] if game['cops'] == -1 else
            ["The Loan Shark's thugs broke your legs."] if game['cash'] < 0 else
            ['You retired a millionaire in the Carribbean.'] if game['cash'] > 1000000 else
            ['Congratulations!', "You didn't do half bad."] if game['cash'] > 2000 else
            ["You didn't make any money!", 'Better luck next time.'])

def highscore_messages(game):
    def highscore_message(i, d):
        return "%d %s %d" % (i, d['name'], d['score'])
    return ['High Scores'] + [highscore_message(i, d) for i, d in enumerate(get_highscores(), 1)]

def location_message(game):
    return "Current Location: %s" % game['location']

def cash_message(game):
    return "Cash: $%d" % game['cash']

def debt_message(game):
    return "Debt: $%d" % game['debt']

def bank_message(game):
    return "Savings: $%d" % game['bank']

def coat_message(game):
    return "Coat: %d/%d" % (get_total(game), game['coat'])

def guns_messages(game):
    return ['Gun'] if game['guns'] else []

def days_message(game):
    return "Time remaining: %d day%s" %(game['days'], 's' if game['days'] > 1 else '')

def cops_message(game):
    return ('and two of his deputies are' if game['cops'] == 3 else
            'and one of his deputies are' if game['cops'] == 2 else 'is')

def get_total(game):
    return sum(game['drugs'].values())

def get_room(game):
    return game['coat'] - get_total(game)

def get_display_max(game):
    max_amount = get_max_buy(game)
    return max_amount if max_amount < 1000 else 'a lot'

def get_max_buy(game):
    return min(game['coat'] - get_total(game), game['cash'] / game['prices'][game['drug']])

def get_max_sell(game):
    return game['drugs'][game['drug']]

def get_max_repay(game):
    return min(game['debt'], game['cash'])

def get_max_loan(game):
    return min(max(game['cash'] * 30, 5500), max(999999999 - game['cash'], 0))

def get_max_withdraw(game):
    return game['bank']

def get_max_deposit(game):
    return game['cash']

def get_prices(leaveout=3):
    prices = {drug: random.randint(*price_range[drug]) for drug in drugs}
    for i in range(leaveout):
        prices[random.choice(drugs)] = 0
    return prices

def empty():
    return {drug: 0 for drug in drugs}

def pick(i, items):
    try:
        return items[int(i) - 1]
    except:
        pass

def dice(n):
    return random.getrandbits(32) % n == 0

def slider(items):
    return "1-%d" % len(items)

def get_highscore_file():
    return os.path.join(os.path.dirname(__file__), 'highscore.json')

def get_highscores():
    try:
        return json.load(open(get_highscore_file()))
    except:
        return []

def update_highscore(game):
    if game['cash'] > 0:
        scores = get_highscores() + [{'name': game['name'], 'score': game['cash']}]
        with open(get_highscore_file(), 'w') as fp:
            json.dump(sorted(scores, key=lambda d: d['score'], reverse=1)[:10], fp, indent=4)

def achive_highscore(game):
    highscores = get_highscores()
    if len(highscores) < 10 or game['cash'] > highscores[-1]['score']:
        return True

def skip(game):
    pass

def make_options(options=[], **kw):
    return options + [lambda game: kw.get(game['input'], skip)(game)]

def reply(game, state, options=[], **kw):
    return dict(game, options=make_options(options, **kw), state=state, choices=kw)

def get_amount(game, **kw):
    return (int(game['input']) if game['input'].isdigit() else
            kw.get(game['input'], lambda game: -1)(game))

def trade(game):
    return reply(game, 'trade', [buy_clause, sell_clause, jet_clause], buy=buy, sell=sell, jet=jet)

def confirm_highscore(game):
    return reply(game, 'finish')

def finish(game):
    game['cash'] += game['bank'] - game['debt']
    game['prices'] = get_prices(0)
    for drug in drugs:
        game['cash'] += game['prices'][drug] * game['drugs'].get(drug, 0)
        game['drugs'][drug] = 0
    if achive_highscore(game):
        update_highscore(game)
        return reply(game, 'achive_highscore', ok=confirm_highscore)
    return reply(game, 'finish')

def news(game):
    game['news'] = []
    for event in events:
        if dice(event['freq']) and game['prices'][event['drug']]:
            game['prices'][event['drug']] *= event.get('mul', 1)
            game['prices'][event['drug']] /= event.get('div', 1)
            game['drugs'][event['drug']] += min(event.get('add', 0), get_room(game))
            game['news'].append(event['message'])
    if game['news']:
        return reply(game, 'news', ok=shark_event)
    return shark_event(game)

def buy_gun(game):
    if game['cash'] < 400:
        return reply(game, 'lack_money', ok=news)
    game['cash'] -= 400
    game['guns'] = 1
    return news(game)

def gun_event(game):
    if game['guns'] == 0 and dice(10):
        return reply(game, 'gun_event', yes=buy_gun, no=news)
    return news(game)

def buy_coat(game):
    if game['cash'] < 200:
        return reply(game, 'lack_money', ok=gun_event)
    game['cash'] -= 200
    game['coat'] += 40
    return gun_event(game)

def repay_amount(game):
    amount = get_amount(game, max=get_max_repay)
    if amount >= 0:
        if amount > game['cash']:
            return reply(game, 'lack_money', ok=shark)
        if amount > game['debt']:
            return reply(game, 'over_pay', ok=shark)
        game['cash'] -= amount
        game['debt'] -= amount
        return shark(game)

def borrow_amount(game):
    amount = get_amount(game, max=get_max_loan)
    if amount >= 0:
        if amount > get_max_loan(game):
            return reply(game, 'borrow_limit', ok=shark)
        game['cash'] += amount
        game['debt'] += amount
        game['loan'] = 1 if amount else game['loan']
        return shark(game)

def withdraw_amount(game):
    amount = get_amount(game, max=get_max_withdraw)
    if amount >= 0:
        if amount > game['bank']:
            return reply(game, 'lack_bank', ok=bank)
        game['cash'] += amount
        game['bank'] -= amount
        return bank(game)

def deposit_amount(game):
    amount = get_amount(game, max=get_max_deposit)
    if amount >= 0:
        if amount > game['cash']:
            return reply(game, 'lack_money', ok=bank)
        game['cash'] -= amount
        game['bank'] += amount
        return bank(game)

def withdraw(game):
    return reply(game, 'withdraw', [withdraw_amount], cancel=bank)

def deposit(game):
    return reply(game, 'deposit', [deposit_amount], cancel=bank)

def repay(game):
    if game['debt'] == 0:
        return reply(game, 'no_debt', ok=shark)
    return reply(game, 'repay', [repay_amount], cancel=shark)

def borrow(game):
    if game['loan']:
        return reply(game, 'no_more_loans', ok=shark)
    return reply(game, 'borrow', [borrow_amount], cancel=shark)

def withdraw_clause(game):
    return clause(game, 'withdraw', [None, withdraw_amount])

def deposit_clause(game):
    return clause(game, 'deposit', [None, deposit_amount])

def repay_clause(game):
    return clause(game, 'repay', [repay, repay_amount])

def borrow_clause(game):
    return clause(game, 'borrow', [borrow, borrow_amount])

def bank(game):
    return reply(game, 'bank', [withdraw_clause, deposit_clause], done=trade, withdraw=withdraw, deposit=deposit)

def shark(game):
    return reply(game, 'shark', [repay_clause, borrow_clause], done=bank_event, repay=repay, borrow=borrow)

def bank_event(game):
    if game['location'] == 'Bronx':
        return reply(game, 'bank_event', yes=bank, no=trade)
    return trade(game)

def shark_event(game):
    if game['location'] == 'Bronx':
        return reply(game, 'shark_event', yes=shark, no=bank_event)
    return bank_event(game)

def coat_event(game):
    if dice(10):
        return reply(game, 'coat_event', yes=buy_coat, no=gun_event)
    return gun_event(game)

def finish_event(game):
    if game['days'] == 0:
        return finish(game)
    return coat_event(game)

def seize(game):
    game['drugs'] = empty()
    game['cash'] /= 2
    return reply(game, 'seize', ok=finish_event)

def run(game):
    if dice(3):
        if dice(5):
            return reply(game, 'caught', ok=seize)
        return remain(game)
    return reply(game, 'ran', ok=finish_event)

def shot(game):
    if dice(5):
        if dice(5):
            game['cops'] = -1
            return reply(game, 'kill', ok=finish)
        return reply(game, 'wounded', ok=seize)
    return reply(game, 'missed', ok=remain)

def fight(game):
    if game['guns'] == 0:
        return reply(game, 'no_gun', ok=remain)
    if dice(4):
        game['cops'] -= 1
        return reply(game, 'hit', ok=shot if game['cops'] else finish_event)
    return reply(game, 'miss', ok=shot)

def remain(game):
    return reply(game, 'remain', run=run, fight=fight)

def fuzz(game):
    return reply(game, 'fuzz', run=run, fight=fight)

def fuzz_event(game):
    if dice(7) and game['days'] and game['cops'] and get_total(game):
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
        game['loan'] = 0
        game['prices'] = get_prices()
        game['location'] = location
        return fuzz_event(game)

def buy_amount(game):
    amount = get_amount(game, max=get_max_buy)
    if amount >= 0:
        if amount > game['cash']:
            return reply(game, 'no_cash', ok=trade)
        if amount > get_room(game):
            return reply(game, 'no_room', ok=trade)
        game['drugs'][game['drug']] += amount
        game['cash'] -= game['prices'][game['drug']] * amount
        return trade(game)

def buy_drug(game):
    drug = pick(game['input'], drugs)
    if drug in drugs:
        if game['prices'][drug] == 0:
            return reply(game, 'no_sellers', ok=trade)
        game['drug'] = drug
        return reply(game, 'buy_drug', [buy_amount], cancel=trade)

def sell_amount(game):
    amount = get_amount(game, max=get_max_sell)
    if amount >= 0:
        if amount > get_max_sell(game):
            return reply(game, 'over_sell', ok=trade)
        game['drugs'][game['drug']] -= amount
        game['cash'] += game['prices'][game['drug']] * amount
        return trade(game)

def sell_drug(game):
    drug = pick(game['input'], drugs)
    if drug in drugs:
        if not game['prices'][drug]:
            return reply(game, 'no_buyers', ok=trade)
        if not game['drugs'][drug]:
            return reply(game, 'no_drugs', ok=trade)
        game['drug'] = drug
        return reply(game, 'sell_drug', [sell_amount], cancel=trade)

def buy(game):
    return reply(game, 'buy', [buy_drug], cancel=trade)

def sell(game):
    return reply(game, 'sell', [sell_drug], cancel=trade)

def jet(game):
    return reply(game, 'jet', [jet_location], cancel=trade)

def buy_clause(game):
    return clause(game, 'buy', [None, buy_drug, buy_amount])

def sell_clause(game):
    return clause(game, 'sell', [None, sell_drug, sell_amount])

def clause(game, arg0, options):
    args = game['input'].split()
    if len(args) > 1 and args[0] == arg0:
        for arg, option in map(None, args, options): # zip
            if arg and callable(option):
                game = option(dict(game, input=arg))
                if not game or 'ok' in game['choices']:
                    return game
        return game

def jet_clause(game):
    return clause(game, 'jet', [None, jet_location])

def start(game):
    game.update({
        'news': [],
        'cash': 2000,
        'debt': 5500,
        'bank': 0,
        'coat': 100,
        'guns': 0,
        'cops': 3,
        'days': 31,
        'loan': 0,
        'drug': '',
        'input': '',
        'state': '',
        'drugs': empty(),
        'prices': empty(),
        'options': [],
        'location': ''
    })
    return reply(game, 'start', [jet_location])

def play(name, command):
    game = dict(games.setdefault(name, {'name': name, 'options': []}), input=command.lstrip('/'))
    for option in make_options(game['options'], start=start):
        temp = option(game)
        if temp:
            game = games[name] = temp
            if game['state'] == 'finish':
                del games[name]
            return get_messages(game)
    return []

def main():
    command = 'start'
    while command not in ('q', 'quit'):
        print '\n'.join(play('test', command)) or 'invalid input'
        command = raw_input('> ')

if __name__ == '__main__':
    main()
