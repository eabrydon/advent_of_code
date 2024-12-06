#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 10:18:43 2024

@author: evanbrydon
"""

import numpy as np
from functools import reduce

def get_data():    
    data_loc = './data'
    fn = 'day9_data.txt'
    f = open(f'{data_loc}/{fn}')
    data = [np.array([int(x) for x in line.strip().split(' ')]) for line in f]
    f.close()
    return data

def make_pattern_tree(l):
    '''Makes a tree object where each list after the first is the diffs
    between the numbers in the prior list
    Ends when a whole list is zero'''
    tree = [l]
    zeroed = False
    while zeroed == False:
        l = l[1:] - l[:-1]
        tree.append(l)
        if set(l) == {0}:
            zeroed = True
        elif len(l) == 1:
            raise ValueError('no pattern found')
    return tree
        
def get_history_value(tree, direction):
    '''Gets history value for a tree
    direction can be f for forwards in part 1 or b for backwards in part 2'''
    if direction == 'f':
        history_values = [level[-1] for level in tree]
        return np.sum(history_values)
    elif direction == 'b':
        history_values = list(reversed([level[0] for level in tree]))
        return reduce(lambda x,y: y-x, history_values)
    else:
        raise ValueError('direction must be f or b')

def get_all_history_values(data, direction = 'f'):
    trees = [make_pattern_tree(l) for l in data]
    return [get_history_value(tree, direction) for tree in trees]

if __name__ == '__main__':
    data = get_data()

    history_values = get_all_history_values(data)
    print(f'Part 1 sum: {np.sum(history_values)}')
        
    history_values_p2 = get_all_history_values(data, 'b')
    print(f'Part 2 sum: {np.sum(history_values_p2)}')
