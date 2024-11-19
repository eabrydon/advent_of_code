#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 13:48:05 2024

@author: evanbrydon
"""

import numpy as np
import pandas as pd

def get_data():    
    data_loc = \
      '/Users/evanbrydon/Documents/GitStuff/advent_of_code/2023'
    fn = 'day4_data.txt'
    f = open(f'{data_loc}/{fn}')
    data = [line[:-1].split(sep = ':') for line in f]
    f.close()
    return data

data = get_data()

def get_points(data):
    df = pd.DataFrame(data = data, columns = ['card','data'])
    df['data'] = df.data.str.replace('  ',' ')
    df['card'] = [x.split()[1] for x in df.card]
    df[['winners','haves']] = df.data.str.split('|', expand = True)
    df['winners'] = df.winners.str.strip().str.split(' ')
    df['haves'] = df.haves.str.strip().str.split(' ')
    
    df['ws'] = [set(x) for x in df.winners]
    df['hs'] = [set(x) for x in df.haves]
    
    df['ints'] = [list(w.intersection(h)) for (w,h) in zip(df.ws,df.hs)]
    df['points'] = [int(2**(len(x)-1)) for x in df.ints] 
    return df

df = get_points(data)
print(f'Part 1 point total: {np.sum(df.points)}')

# part 2 - seems like it has to be iterative, doesn't make sense to stay in df

df['matches'] = [len(x) for x in df.ints]
df['card'] = df.card.astype('int')

def get_card_count(df):
    card_max = df.card[len(df)-1]
    card_dict = {}
    for (card, matches) in zip(df.card, df.matches):
        card_dict[card] = {'matches':matches, 'copies':1}
    
    total_cards = 0
    for current_card in df.card:
        cd = card_dict[current_card]
        for future_card in range(current_card+1,current_card+cd['matches']+1):
            if future_card > card_max:
                continue
            card_dict[future_card]['copies'] += cd['copies']
        total_cards += cd['copies']
    return total_cards

total_cards = get_card_count(df)
    
print(f'Part 2 card total: {total_cards}')

