#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 09:47:56 2024

@author: evanbrydon
"""

import pandas as pd
import re
import numpy as np

data_loc = \
    '/Users/evanbrydon/Documents/GitStuff/advent_of_code/2023/data'
fn = 'day1_data.txt'
df = pd.read_csv(f'{data_loc}/{fn}', names = ['value'])

# Part 1

df['numbers_only'] = [re.sub('[A-z]*', '', x) for x in df.value]
df['calibration_value'] = [int(x[0]+x[-1]) for x in df.numbers_only]

print(f'Part 1 sum: {np.sum(df.calibration_value)}')

# Part 2

sub_dict = {
    'one':'1e',
    'two': '2o',
    'three':'3e',
    'four':'4',
    'five':'5e',
    'six':'6',
    'seven':'7n',
    'eight':'8t',
    'nine':'9e'
    }

sub_ptrn = ''
for x in sub_dict.keys():
    sub_ptrn = sub_ptrn + x + '|'
sub_ptrn = sub_ptrn[:-1]

replacement = lambda y: sub_dict[y.group(0)]

df['numbers_subbed'] = [re.sub(sub_ptrn, replacement, x) for x in df.value]
# Lol stupid edge case workaround not mentioned in instructions
df['numbers_subbed_twice'] = [re.sub(sub_ptrn, replacement, x) for x in df.numbers_subbed]

df['numbers_only_p2'] = [re.sub('[A-z]*', '', x) for x in df.numbers_subbed_twice]
df['calibration_value_p2'] = [int(x[0]+x[-1]) for x in df.numbers_only_p2]

print(f'Part 2 sum: {np.sum(df.calibration_value_p2)}')

# testing df
# tdf = pd.DataFrame({'value': ['oneight21','threeightwo4','eightwo1','sevenineight4six']})

    

