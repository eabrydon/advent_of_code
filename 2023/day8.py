#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 10:34:46 2024

@author: evanbrydon
"""
import numpy as np
import copy

def get_data():    
    data_loc = \
      '/Users/evanbrydon/Documents/GitStuff/advent_of_code/2023/data'
    fn = 'day8_data.txt'
    f = open(f'{data_loc}/{fn}')
    data = f.read().split('\n\n')
    f.close()
    dirs = data[0]
    dmap = data[1].strip().split('\n')
    return dirs, dmap


def make_mapdict(dmap):
    mapdict = {}
    for line in dmap:
        mapdict[line[:3]] = {'L':line[7:10], 'R':line[12:15]}
    return mapdict


def follow_map(dirs, mapdict, loc = 'AAA', end = 'ZZZ'):
    step_count = 0
    finished = False
    while finished == False:
        for d in dirs:
            if finished == True:
                continue
            loc = mapdict[loc][d]
            step_count += 1
            if loc == 'ZZZ':
                finished = True
    return step_count

# Part 2

def find_start_nodes(mapdict):
    return [x for x in list(mapdict.keys()) if x[2] == 'A']

def follow_map_p2(dirs, mapdict, nodes):
    '''Not working, too many steps, need way to avoid doing every step
    Did ~200M steps without a solution'''
    step_count = 0
    finished = False
    while finished == False:
        for d in dirs:
            if finished == True:
                continue
            nodes = [mapdict[n][d] for n in nodes]
            step_count += 1
            if step_count % 1000000 == 0:
                print(f'Still working, step count: {step_count}')
            if ''.join([n[2] for n in nodes]) == 'ZZZZZZ':
                finished = True
    return step_count

def follow_map_to_z(node, dirs, i, mapdict):
    finished = False
    dirs = ''.join([dirs[i:],dirs[:i]])
    step_count = 0
    while not finished:
        for d in dirs:
            node = mapdict[node][d]
            step_count += 1
            if node[2] == 'Z':
                finished = True
                break
            elif step_count >= 10E7:
                finished = True
                break
    return (step_count, node)

def find_z_to_z_steps(mapdict, dirs):
    znodes = [x for x in list(mapdict.keys()) if x[2] == 'Z']
    step_dists = {}
    for node in znodes:
        step_dists[node] = {}
        for i in range(len(dirs)):
            step_dists[node][i] = follow_map_to_z(node, dirs, i, mapdict)
    return step_dists

def find_a_to_z_steps(mapdict, dirs):
    anodes = [x for x in list(mapdict.keys()) if x[2] == 'A']
    step_dists = []
    for node in anodes:
        step_dists.append(follow_map_to_z(node, dirs, 0, mapdict))
    return step_dists

def query_zs_dm(node, step, zstep_distmap, dir_l):
    '''Input: node, step total, map, length of directions
        Output: tuple: (new step number, new node)'''
    (ns, nn) = zstep_distmap[node][step%dir_l]
    return (ns+step, nn)

def find_all_zs(sn_tups, zstep_distmap):
    '''start by having each a node run until they hit a z node
    then for each one that isn't the max steps of the list, 
        jump steps ahead until next z node
    when all steps counts align, we're done'''
    dir_l = len(zstep_distmap[list(zstep_distmap.keys())[0]].keys())
    fin = False
    c = 0
    while not fin:
        steps = [sn[0] for sn in sn_tups]
        l = len(set(steps))
        if l == 1:
            return steps[0]
        else:
            m = max(steps)
            sn_tups = [(s,n) if s==m else query_zs_dm(n,s, zstep_distmap, dir_l) for (s,n) in sn_tups]
            c += 1
            if c%10E6 == 0:
                print(f'Steps: {m}')
        if c > 10E8:
            return steps
    
def make_loop_map(zstep_distmap):
    loop_map = {}
    dir_l = len(zstep_distmap[list(zstep_distmap.keys())[0]].keys())    
    for node in zstep_distmap.keys():
        loop_map[node] = {}
        for dir_start in zstep_distmap[node].keys():
            n = copy.copy(node)
            step = copy.copy(dir_start)
            looped = False
            loop_steps = [step]
            c = 0
            while not looped:
                (step,n) = query_zs_dm(n,step, zstep_distmap, dir_l)
                loop_steps.append(step)
                c+=1
                if (n == node) and (loop_steps[-1]%dir_l == dir_start):
                    looped = True
                    loop_map[node][dir_start] = loop_steps
                if c > 10E4:
                    break
    return loop_map

# arg - loop map shows no deviations in loops. Just need to LCM all 6
# problem is trivial because its an edge case and I made a generalized solution :(

def make_loop_map_small(zstep_distmap):
    loop_map = {}
    dir_l = len(zstep_distmap[list(zstep_distmap.keys())[0]].keys())    
    for node in zstep_distmap.keys():
        loop_map[node] = {}
        for dir_start in range(1):
            n = copy.copy(node)
            step = copy.copy(dir_start)
            looped = False
            loop_steps = [step]
            c = 0
            while not looped:
                (step,n) = query_zs_dm(n,step, zstep_distmap, dir_l)
                loop_steps.append(step)
                c+=1
                if (n == node) and (loop_steps[-1]%dir_l == dir_start):
                    looped = True
                    loop_map[node][dir_start] = loop_steps
                if c > 10E4:
                    print(f'No loop or too large for node: {node}, position: {dir_start}')
                    loop_map[node][dir_start] = []
                    break
    return loop_map

if __name__ == '__main__':
    dirs, dmap = get_data()
    mapdict = make_mapdict(dmap)
    steps = follow_map(dirs, mapdict)
    print(f'Steps part 1: {steps}')
    
    start_nodes = find_start_nodes(mapdict)
    zstep_distmap = find_z_to_z_steps(mapdict, dirs)
    az_steps = find_a_to_z_steps(mapdict, dirs)

    loop_map_small = make_loop_map_small(zstep_distmap)
    steps2 = np.lcm.reduce([loop_map_small[node][0][1] for node in loop_map_small.keys()])
    print(f'Steps part 2: {steps2}')

