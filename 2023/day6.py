#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 15:59:41 2024

@author: evanbrydon
"""
import numpy as np 
from functools import reduce
def get_data():    
    data_loc = \
      '/Users/evanbrydon/Documents/Documents/random_projects/advent_of_code/2023'
    fn = 'day6_data.txt'
    f = open(f'{data_loc}/{fn}')
    data = f.read().split('\n')
    f.close()
    times = data[0].split(':')[1].strip().split()
    distances = data[1].split(':')[1].strip().split()
    return [int(x) for x in times], [int(x) for x in distances]

times, distances = get_data()

def get_race_distances(race_time):
    charge_t = np.array(range(race_time+1))
    move_t = charge_t[::-1]
    return charge_t * move_t

def get_winning_product(times, distances):
    wins = []
    for (t,d) in zip(times, distances):
        dists = get_race_distances(t)
        wins.append(np.sum(dists > d))
    return reduce((lambda x,y: x*y), wins)

def get_winning_product_lol(times, distances):
    return reduce((lambda x,y: x*y), [np.sum(get_race_distances(t) > d) for (t,d) in zip(times, distances)])

winning_prod = get_winning_product(times, distances)
print(f'Product of winning options: {winning_prod}')
winning_prod_lol = get_winning_product_lol(times, distances)
