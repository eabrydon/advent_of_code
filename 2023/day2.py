#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 10:08:16 2024

@author: evanbrydon
"""

import pandas as pd
import numpy as np

data_loc = \
  '/Users/evanbrydon/Documents/GitStuff/advent_of_code/2023'
fn = 'day2_data.txt'

data = pd.read_csv(f'{data_loc}/{fn}', delimiter =':', names = ['game','cube_data'])


# Part 1
data['cube_data_list'] = data.cube_data.str.split(';')
data = data.explode(column = 'cube_data_list')
data = data.rename(columns = {'cube_data_list':'draw'})
data = data[['game','draw']]

data['game'] = data.game.str.split(' ', expand = True)[1].astype('int')

data['draw_list'] = data.draw.str.split(',')
data = data.explode(column = 'draw_list')
data = data.rename(columns = {'draw_list':'single_draw'})
data = data[['game','single_draw']]

data['single_draw'] = data.single_draw.str.strip()
data[['number','color']] = data.single_draw.str.split(' ', expand = True)
data['number'] = data.number.astype('int')

def find_illegal_games(data, color, maximum):
    d = data.loc[(data.color == color) & (data.number > maximum)]
    return set(d.game)

legal_limits = {'red':12,'green':13,'blue':14}

illegal_games = set()
for c in legal_limits.keys():
    illegal_games = illegal_games.union(find_illegal_games(data, c, legal_limits[c]))
    
legal_games = set(data.game) - illegal_games
print(f'Part1 sum: {sum(legal_games)}')

# Part 2
data_maxes = data.groupby(['game','color'], as_index = False).agg({'number':'max'})
# Lol one liner
p2 = np.sum([np.prod(data_maxes.loc[data_maxes.game == game].number) for game in set(data_maxes.game)])
# groupby doesn't have a 'product' agg so did it this hacky iterative way
print(f'Part2 sum: {p2}')

