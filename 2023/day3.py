#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 11:22:36 2024

@author: evanbrydon
"""

import numpy as np
import string

def get_data():    
    data_loc = \
      '/Users/evanbrydon/Documents/GitStuff/advent_of_code/2023'
    fn = 'day3_data.txt'
    f = open(f'{data_loc}/{fn}')
    data = [[c for c in line] for line in f]
    f.close()
    return np.array(data)

def get_neighborhood_p1(data,x,y,l, x_bound, y_bound):
    y_min = max(y-1, 0)
    y_max = min(y+2, y_bound)
    x_min = max(x-l, 0)
    x_max = min(x+2, x_bound)
    return data[y_min:y_max, x_min:x_max]

def check_neighborhood_p1(nb, symbols):
    for element in set(nb.flatten().tolist()):
        if element in symbols:
            return True
        else:
            pass
    return False

def get_part_numbers(data):
    y_bound = len(data)
    x_bound = len(data[0])
    max_number_len = 0
    part_numbers = []
    number = ''
    l = 0
    digits = set(string.digits)
    symbols = set(string.punctuation)
    symbols.remove('.')
    for y in range(len(data)):
        for x in range(len(data[y])):
            e = data[y,x]
            if e in digits:
                number = number + e
                l += 1
                if l > max_number_len:
                    max_number_len = l
                if (data[y,min(x+1, x_bound)] not in digits) or (x == x_bound):
                    nb = get_neighborhood_p1(data, x, y, l, x_bound, y_bound)
                    if check_neighborhood_p1(nb, symbols):
                        part_numbers.append(int(number))
                    number = ''
                    l = 0                    


# Part 2

# max number length = 3

def get_neighborhood_p2(data, x, y, x_bound, y_bound):
    y_min = max(y-1, 0)
    y_max = min(y+2, y_bound)
    x_min = max(x-3, 0)
    x_max = min(x+4, x_bound)
    ast_x = get_ast_x(x_min, x_max, x_bound)
    return data[y_min:y_max, x_min:x_max], ast_x

def get_ast_x(x_min, x_max, x_bound):
    l = x_max-x_min
    if (l == 7) or (x_max == x_bound):
        return 3
    elif x_min == 0:
        return l-4
    else:
        ValueError(f'''Get ast x function failed: 
              x_min = {x_min}
              x_max = {x_max}
              x_bound = {x_bound}''')

def check_neighborhood_p2(nb, ast_x, digits):
    numbers = []
    for row in nb:
        if row[ast_x] in digits:      
            numbers.append(get_num(row,ast_x,digits))
        else:
            if ast_x != 0:
                if row[ast_x-1] in digits:
                    numbers.append(get_num(row,ast_x-1,digits))
            if row[ast_x+1] in digits:
                numbers.append(get_num(row,ast_x+1,digits))
    if len(numbers) == 2:
        return int(numbers[0]) * int(numbers[1])
    else:
        return 0
        
def get_num(row, i, digits):
    start = i
    end = i
    l = len(row)
    if i != 0:
        if row[i-1] in digits:
            start -= 1
            if i != 1:
                if row[i-2] in digits:
                    start -= 1
    if i < l-1:
        if row[i+1] in digits:
            end += 1
            if i < l-2:
                if row[i+2] in digits:
                    end += 1

    num = row[start:end+1]
    return ''.join(num)

def get_gear_ratios(data):
    digits = set(string.digits)
    y_bound = len(data)
    x_bound = len(data[0])
    gear_ratios = []           
    for y in range(len(data)):
        for x in range(len(data[y])):
            e = data[y,x]
            if e == '*':
                nb, ast_x = get_neighborhood_p2(data, x, y, x_bound, y_bound)
                gear_ratio = check_neighborhood_p2(nb, ast_x, digits)
                gear_ratios.append(gear_ratio)
                print(f'row:{y}, col:{x}, product: {gear_ratio}')
    return gear_ratios

if __name__ == '__main__':
    data = get_data()
    part_numbers = get_part_numbers(data)
    print(f'Part 1 sum: {np.sum(part_numbers)}')
    gear_ratios = get_gear_ratios(data)
    print(f'Part 2 Sum: {np.sum(gear_ratios)}')
        




    