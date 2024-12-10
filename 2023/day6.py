#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 15:59:41 2024

@author: evanbrydon
"""
import numpy as np 
from functools import reduce

def get_data():    
    data_loc = './data'
    fn = 'day6_data.txt'
    f = open(f'{data_loc}/{fn}')
    data = [line for line in f]
    f.close()
    times = data[0].split(':')[1].strip().split()
    distances = data[1].split(':')[1].strip().split()
    return [int(x) for x in times], [int(x) for x in distances]

def get_race_distances(race_time):
    '''Gets movement distance for each possible charge/move split
    Used np array for easy flip and comparison'''
    charge_t = np.array(range(race_time+1))
    move_t = charge_t[::-1]
    return charge_t * move_t

def get_winning_product(times, distances):
    '''Gets winning times for each race and returns product'''
    wins = []
    for (t,d) in zip(times, distances):
        dists = get_race_distances(t)
        wins.append(np.sum(dists > d))
    return reduce((lambda x,y: x*y), wins)

def get_winning_product_alt(times, distances):
    reduce((lambda x,y: x*y), [get_winner_count(t,d) for t,d in zip(times, distances)])
    
    
# Part 2

def get_data_p2():    
    data_loc = './data'
    fn = 'day6_data.txt'
    f = open(f'{data_loc}/{fn}')
    data = [line for line in f]
    f.close()
    time = data[0].split(':')[1].strip().replace(' ','')
    distance = data[1].split(':')[1].strip().replace(' ','')
    return int(time), int(distance)

def get_winner_count(race_time, distance):
    '''Count winning options, stopping when we get first d > D
    Better for long races'''
    for i in range(np.ceil((race_time+1)/2)):
        if i * (race_time - i) > distance:
            return race_time + 1 - (2*i)
    return 0

def get_winner_count_eff(race_time, distance):
    '''Binary search to get close to first winning charge time
    Saves tons of time on longer races'''
    start = 0
    end = int(np.ceil((race_time)/2))
    while end-start > 1:
        i = int((start+end)/2)
        if i * (race_time - i) > distance:
            end = i
        else:
            start = i
    return race_time + 1 - (2*end)
 
if __name__ == '__main__':
    times, distances = get_data()
    winning_prod = get_winning_product(times, distances)
    print(f'Product of winning times: {winning_prod}')

    time, distance = get_data_p2()
#    winning_ways = np.sum(get_race_distances(time) > distance) SLOW: ~5 seconds
#    winning_ways = get_winner_count(time,distance) FASTER: ~.8 seconds
    winning_ways = get_winner_count_eff(time,distance) # FAST 8 μs 
    print(f'Winning options count: {winning_ways}')


