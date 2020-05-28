#!/usr/bin/env python
# coding: utf-8

import numpy as np
from collections import defaultdict
import argparse


class CFG(object):
    def __init__(self):
        self.prod = defaultdict(list)

    def add_prod(self, grammar):
        for rule in grammar:
            lhs = rule.split('\t')[1]
            rhs = rule.split('\t')[2]
            self.prod[lhs].append(rhs)
        print()

    def gen_random(self, symbol):
        sentence = ''
        # randomly choose rhs of a certain lhs symbol
        rand_prod = np.random.choice(self.prod[symbol])
        #         print(rand_prod)
        for sym in rand_prod.split():
            if sym in self.prod:
                sentence += self.gen_random(sym)
            else:
                sentence += sym + ' '

        return sentence


# change probability
def getGrammar(grammar_dir):
    with open(grammar_dir, 'r') as mf:
        data = mf.readlines()
    result = []
    for line in data:
        index = line.find('#')
        line = line[:index].strip()
        if len(line):
            result.append(line)
    return result


def getSentence(grammar_dir, num):
    grammar = getGrammar(grammar_dir)
    print(grammar)
    print()

    cfg1 = CFG()
    cfg1.add_prod(grammar)

    for i in range(num):
        print(cfg1.gen_random('ROOT'))
        print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process filepath and integer.')
    parser.add_argument('filepath', type=str, help='a string of filepath')
    parser.add_argument('num', type=int, help='the number of sentence', default=1)
    args = parser.parse_args()
    assert args.num >= 0
    print(args)
    getSentence(args.filepath, args.num)
