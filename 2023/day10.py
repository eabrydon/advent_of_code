#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 10:17:55 2024

@author: evanbrydon
"""
import numpy as np

def get_data():
    data_loc = './data'
    fn = 'day10_data.txt'
    f = open(f'{data_loc}/{fn}')
    data = np.array([list(line.strip()) for line in f])
    f.close()
    return data

def make_starting_move(data):
    '''Make any valid starting move'''
    (sy, sx) = np.where(data == 'S')
    (sy, sx) = sy[0],sx[0]
    if data[sy-1, sx] in {'|','F','7'}:
        return (sx, sy-1, 2)
    elif data[sy, sx+1] in {'-','7','J'}:
        return (sx+1, sy, 3)
    elif data[sy+1, sx] in {'|','J','L'}:
        return (sx, sy+1, 0)
    else:
        raise ValueError('loop not possible')

def find_next_section(data, x, y, prior_dir):
    '''Move along the pipe for standard traversal'''
    # 0 North, 1 East, 2 South, 3 West
    dir_dict = {
        'L':[0,1],
        'F':[1,2],
        '7':[2,3],
        'J':[3,0],
        '|':[0,2],
        '-':[1,3],
        }
    move = dir_dict[data[y,x]]
    move.remove(prior_dir)
    move = move[0]
    if move == 0:
        return (x, y-1, 2)
    elif move == 1:
        return (x+1, y, 3)
    elif move == 2:
        return (x, y+1, 0)
    elif move == 3:
        return (x-1, y, 1)
    
def count_loop_steps(data):
    '''Move along the loop and count steps as we go, stop at the start'''
    (x, y, pdir) = make_starting_move(data)
    steps = 1
    while data[y,x] != 'S':
        x,y,pdir = find_next_section(data, x, y, pdir)
        steps += 1
    return steps

# part 2 functions
def isolate_loop(data):
    '''Isolate the loop in the map so we can tell interior from exterior'''
    (ylen, xlen) = data.shape
    loop = np.array([['.' for x in range(xlen)] for y in range(ylen)])
    (sy, sx) = np.where(data == 'S')
    loop[sy[0],sx[0]] = 'S'
    (x, y, pdir) = make_starting_move(data)
    while data[y,x] != 'S':
        loop[y,x] = data[y,x]
        x,y,pdir = find_next_section(data, x, y, pdir)
    return loop

def replace_S(loop):
    '''Replace the starting S in our loop with the appropriate value'''
    dir_dict = {
        '[0, 1]':'L',
        '[1, 2]':'F',
        '[2, 3]':'7',
        '[0, 3]':'J',
        '[0, 2]':'|',
        '[1, 3]':'-'
        }
    (sy, sx) = np.where(loop == 'S')
    (sy, sx) = sy[0],sx[0]
    dirs = []
    if loop[sy-1,sx] in {'F','|','7'}:
        dirs.append(0)
    if loop[sy,sx+1] in {'J','-','7'}:
        dirs.append(1)
    if loop[sy+1,sx] in {'J','|','L'}:
        dirs.append(2)
    if loop[sy,sx-1] in {'F','-','L'}:
        dirs.append(3)
    loop[sy,sx] = dir_dict[str(dirs)]
    return loop

def count_interior_row(row):
    '''Track whether we're on the interior as we move along the row'''
    interior_count = 0
    in_status = 0 
    for item in row:
        if item in {'F','J'}:
            in_status += 1
        elif item in {'L','7'}:
            in_status -= 1
        elif item == '|':
            in_status += 2
        elif item == '.':
            add = (in_status%4)/2
            if int(add) != add:
                raise ValueError('odd in status!')
            interior_count += add
    return interior_count

def count_all_interior(data):
    '''Driver function for part 2'''
    loop = isolate_loop(data)
    loop = replace_S(loop)
    interior_counts = [count_interior_row(row) for row in loop]
    return np.sum(interior_counts)
        
    

if __name__ == '__main__':
    data = get_data()
    steps = count_loop_steps(data)
    print(f"Farthest point is {np.floor(steps/2)} steps away")

    interior_tiles = count_all_interior(data)
    print(f"Interior area is {interior_tiles} tiles")
    
