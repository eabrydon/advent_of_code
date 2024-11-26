#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 13:00:14 2024

@author: evanbrydon
"""

import pandas as pd
import numpy as np

def get_data():    
    data_loc = './data'
    fn = 'day7_data.txt'
    f = open(f'{data_loc}/{fn}')
    data = [line.strip().split(sep = ' ') for line in f]
    f.close()
    hands = [x[0] for x in data]
    bids = [int(x[1]) for x in data]
    return hands, bids

def make_hand_dict(hand):
    hand_dict = {}
    for card in list(hand):
        try:
            hand_dict[card] += 1
        except:
            hand_dict[card] = 1
    return hand_dict

def get_hand_type(hand):
    '''Note for hand type: lowest number is better hand
    1 is 5oak, 2 is 4oak, 3 is fh, 4 is 3oak, 5 is 2p, 6 is 1p, 7 is hc'''
    hand_dict = make_hand_dict(hand)
    cts = sorted(hand_dict.values())
    if len(cts) == 1:
        return 1
    elif len(cts) == 2:
        if cts[0] == 1:
            return 2
        elif cts[0] == 2:
            return 3
    elif len(cts) == 3:
        if cts[-1] == 3:
            return 4
        elif cts[-1] == 2:
            return 5
    elif len(cts) == 4:
        return 6
    else:
        return 7

def convert_hands(hands, cdict):
    '''Convert letters in hands to alpha order so we can use sorted fx'''
    all_hands = ''.join(hands)
    for k,v in cdict.items():
        all_hands = all_hands.replace(k,v)
    return [all_hands[i:i+5] for i in range(0, len(all_hands), 5)]

def prep_df(hands_converted,bids,hand_types):
    hand_df = pd.DataFrame(data = {'hand':hands_converted, 'bid':bids, 'htype':hand_types})
    
    hand_df['hand'] = [list(h) for h in hand_df.hand]
    
    colnames = ['h1','h2','h3','h4','h5']
    hand_df[colnames] = pd.DataFrame(hand_df.hand.tolist(), index = hand_df.index)
    return hand_df

def calc_winnings(hand_df):
    colnames = ['h1','h2','h3','h4','h5']
    hand_df = hand_df.sort_values(by = ['htype']+colnames, 
                                  ascending = [True, False, False, False, False, False])
    hand_df['bid_mult'] = [i for i in range(len(hand_df), 0, -1)]
    hand_df['winnings'] = hand_df.bid * hand_df.bid_mult
    return hand_df\

def run_p1():
    conversion_dict = {
        'A':'e',
        'K':'d',
        'Q':'c',
        'J':'b',
        'T':'a',
        }
    hands, bids = get_data()  
       
    hands_converted = convert_hands(hands, conversion_dict)
    hand_types = [get_hand_type(hand) for hand in hands_converted]           
            
    hand_df = prep_df(hands_converted,bids,hand_types)
    hand_df = calc_winnings(hand_df)
    
    print(f'Total winnings: {np.sum(hand_df.winnings)}')

# Part 2
    
def adjust_counts(hd):
    try:
        jokers = hd['0']
    except:
        return sorted(hd.values())
    cts = sorted(hd.values())
    cts.remove(jokers)
    if len(cts) > 0:
        cts[-1] += jokers
    else:
        cts = [5]
    return cts

def assign_hand_type(cts):
    '''Note for hand type: lowest number is better hand
    1 is 5oak, 2 is 4oak, 3 is fh, 4 is 3oak, 5 is 2p, 6 is 1p, 7 is hc'''
    if len(cts) == 1:
        return 1
    elif len(cts) == 2:
        if cts[0] == 1:
            return 2
        elif cts[0] == 2:
            return 3
    elif len(cts) == 3:
        if cts[-1] == 3:
            return 4
        elif cts[-1] == 2:
            return 5
    elif len(cts) == 4:
        return 6
    else:
        return 7


def run_p2():
    conversion_dict = {
        'A':'e',
        'K':'d',
        'Q':'c',
        'T':'b',
        'J':'0',
        }
    hands, bids = get_data()  
       
    hands_converted2 = convert_hands(hands, conversion_dict)
    
    hand_dicts2 = [make_hand_dict(hand) for hand in hands_converted2]
    adjusted_counts2 = [adjust_counts(hd) for hd in hand_dicts2]
    hand_types2 = [assign_hand_type(ct) for ct in adjusted_counts2]           
            
    hand_df2 = prep_df(hands_converted2,bids,hand_types2)
    hand_df2 = calc_winnings(hand_df2)

    print(f'Total winnings p2: {np.sum(hand_df2.winnings)}')
    
if __name__ == '__main__':
    run_p1()
    run_p2()
