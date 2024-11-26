#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 11:19:05 2024

@author: evanbrydon
"""

#  maps are: destination range start, souce range start, range length
# maps are in order to don't need to worry about their names
import numpy as np
import copy


def get_data():    
    data_loc = './data'
    fn = 'day5_data.txt'
    f = open(f'{data_loc}/{fn}')
    data = f.read()
    f.close()
    return data

data = get_data()

def prep_data(data):
    
    data = data.split('\n\n')
    
    seeds = data[0].split(':')[1]
    seed_list = [int(x) for x in seeds.replace('\n',' ').strip().split(' ')]
    
    maps = data[1:]
    names = [m.split(':')[0] for m in maps]
    map_data_str = [m.split(':')[1].strip() for m in maps]
    map_data = [np.array([[int(x) for x in row.strip().split(' ')] for row in m.split('\n')]) for m in map_data_str]
    return seed_list, names, map_data

seeds, names, maps = prep_data(data)

def put_num_through_map(num, m):
    for row in m:
        if (num >= row[1]) and (num <= row[1] + row[2]): 
            return row[0] + num - row[1]
    else:
        return num

def put_seeds_through_maps(seeds, maps):
    results = []
    for seed in seeds:
        num = seed
        for m in maps:
            num = put_num_through_map(num, m)
        results.append(num)
    return results

result_locations = put_seeds_through_maps(seeds, maps)
print(f'Result locations:\n{result_locations}')
print(f'\nLowest location number: {np.min(result_locations)}')

# part 2

def get_seed_range_tuples(seeds):
    seed_ranges = np.reshape(np.array(seeds),shape = [-1,2])
    return [(x[0],x[1]) for x in seed_ranges]

seed_range_tuples = get_seed_range_tuples(seeds)
# only needs lowest location number
# idea: need to put whole blocks of numbers through maps, do 1 calculation for each blocks
#   if block splits then do calcs for both blocks

def put_numranges_through_map(input_ranges, m, name):
    destination_ranges = [] # list of tuples: (num, range_len)
    remaining_ranges = copy.copy(input_ranges)
    while_counter = 0
    print(f'Starting {name}')
    while len(remaining_ranges) > 0:
        if while_counter > 100:
            raise ValueError('infinite loop')
        for (in_st, in_r) in remaining_ranges:
            row_hit = False
            for row in m:
                # check if any part of input range will map
                if (in_st + in_r-1 >= row[1]) and (in_st <= row[1] + row[2]-1):
                    row_hit = True
                    # print('row hit')
                    # print(f'in_st: {in_st}, in_r: {in_r}, row: {row}')
                    # case 1: full input range mapped
                    if (in_st >= row[1]) and (in_st + in_r <= row[1]+ row[2]):
                        # print('1')
                        destination_ranges.append((row[0] - row[1] + in_st, in_r))
                    # case 2: input range spans map
                    elif (in_st < row[1]) and (in_st + in_r > row[1]+ row[2]):
                        destination_ranges.append((row[0], row[2]))
                        input_ranges.append((in_st, row[1] - in_st))
                        input_ranges.append((row[1]+row[2]+1, in_st+in_r-row[1]-row[2]))
                        # print('2')
                    # case 3: input range scissors low
                    elif (in_st < row[1]) and (in_st + in_r-1 >= row[1]):
                        destination_ranges.append((row[0], in_st + in_r - row[1]))
                        input_ranges.append((in_st, row[1] - in_st))
                        # print('3')
                    # case 4: input range scissors high
                    elif (in_st >= row[1]) and (in_st + in_r > row[1]+ row[2]):
                        destination_ranges.append((row[0]+in_st-row[1], row[1]+row[2]-in_st))
                        input_ranges.append((row[1]+row[2]+1, in_st+in_r-row[1]-row[2]))
                        # print('4')
                    else:
                        raise ValueError(f'row hit but logic broken for in: ({in_st},{in_r}), row = {row}')
            if not row_hit:
                destination_ranges.append((in_st,in_r))
            input_ranges = input_ranges[1:]

        remaining_ranges = copy.copy(input_ranges)
        while_counter += 1
        print(f'loop {while_counter} complete')
        print(f'tuple count: {len(remaining_ranges)} ')
    print(f'finished {name}')
    print(f'outgoing tuple count: {len(destination_ranges)}\n')

    return destination_ranges

def put_numranges_through_map2(input_ranges, m, name):
    # tried to simplify logic and naming in this version
    destination_ranges = [] # list of tuples: (num, range_len)
    remaining_ranges = copy.copy(input_ranges)
    while_counter = 0
    print(f'Starting {name}')
    while len(remaining_ranges) > 0:
        if while_counter > 100:
            raise ValueError('infinite loop')
        for (in_st, in_r) in remaining_ranges:
            row_hit = False
            in_e = in_st + in_r
            for row in m:
                row_e = row[1] + row[2]
                # check if any part of input range will map
                if (in_e-1 >= row[1]) and (in_st <= row_e-1):
                    row_hit = True
                    # input range lower bound >= map range lower bound
                    if in_st >= row[1]:
                        # case 1 - input range contained in map range
                        if in_e <= row_e:
                            destination_ranges.append((row[0] - row[1] + in_st, in_r))
                        # case 2 - input range ub scissors map range from above
                        elif in_e > row_e:
                            destination_ranges.append((row[0]+in_st-row[1], row_e-in_st))
                            input_ranges.append((row_e+1, in_e-row_e))
                    # input range lower bound < map range lower bound
                    elif in_st < row[1]:
                        # case 3 - input range envelops map range
                        input_ranges.append((in_st, row[1] - in_st))
                        if in_e > row_e:
                            destination_ranges.append((row[0], row[2]))
                            input_ranges.append((row_e+1, in_e-row_e))
                        # case 4 - input range ub scissors map range from below
                        elif in_e-1 >= row[1]:
                            destination_ranges.append((row[0], in_e - row[1]))
            if not row_hit:
                destination_ranges.append((in_st,in_r))
            input_ranges = input_ranges[1:]
        remaining_ranges = copy.copy(input_ranges)
        while_counter += 1
        print(f'loop {while_counter} complete')
        print(f'tuple count: {len(remaining_ranges)} ')
    print(f'finished {name}')
    print(f'outgoing tuple count: {len(destination_ranges)}\n')
    return destination_ranges


def put_seedranges_through_maps(seedranges, maps, names):

    for (m,n) in zip(maps, names):
        seedranges = put_numranges_through_map(seedranges, m, n)
    return seedranges


locations = put_seedranges_through_maps(seed_range_tuples, maps, names)
low_locations = [l[0] for l in locations]

print(f'\nLowest location number: {np.min(low_locations)}')

# troubleshooting
# test_seeds = [(int(2),int(3)),(int(8),int(4))]

# test_maps = [
#     np.array([[1,3,3],[6,7,4]]),
# #    np.array([[5,2,2],[4,7,5]])
#     ]

# test_names = ['map1','map2']      

# locations = put_seedranges_through_maps(test_seeds, test_maps, test_names)
# low_locations = [l[0] for l in locations]

# print(f'\nLowest location number: {np.min(low_locations)}')