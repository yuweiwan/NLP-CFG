#!/usr/bin/env python3

import argparse
import random


def input_info():
    parser = argparse.ArgumentParser(description='random sentence generator')
    parser.add_argument('path', type=str, help='path to the grammar file')
    parser.add_argument('count', type=int, help='number of sentences', default=1, nargs='?')
    parser.add_argument("-t", "--tree", action="store_true", help="print tree")

    args = parser.parse_args()
    return args.path, args.count, args.tree


# global variable: maximal expanded non-terminals
left_expend = 0


# grammar: {LHS1: [odd, RHS1, RHS2, ...],
#           LHS2: [odd, RHS1, RHS2, ...],
#           LHS3: [odd, RHS1, RHS2, ...], ...}
# token: 'ROOT' or 'NP' or 'ate' or ...
def gen(grammar, token, print_tree):
    global left_expend
    if token not in grammar:
        return token
    elif left_expend > 0:
        left_expend -= 1
    else:
        return '...'
    odd = sum(list(zip(*grammar[token]))[0])  # accumulation of odd
    rand = random.uniform(0, odd)  # find random float in [0, odd]
    count = 0.0
    rule = None
    for candidate in grammar[token]:  # candidate: [odd, RHS1, RHS2, ...]
        count += candidate[0]
        if rand <= count:
            rule = candidate
            break
    if rule is None:
        raise Exception('empty rule!')
    parts = []
    for symbol in rule[1:]:
        if print_tree:
            if symbol in grammar:
                parts += ['({} {})'.format(symbol, gen(grammar, symbol, print_tree))]
            else:
                parts += ['{}'.format(symbol)]
        else:
            parts += [gen(grammar, symbol, print_tree)]
    return " ".join(parts)


def preprocess(lines):
    lines = list(map(lambda l: l.split('#', 1)[0], lines))  # remove comments
    lines = [l.split() for l in lines]  # split rules
    lines = list(filter(len, lines))  # remove whitespace
    return lines


def main():
    path, count, print_tree = input_info()
    with open(path, encoding='gbk') as reader:
        lines = reader.readlines()
    lines = preprocess(lines)
    # store all grammar into format {LHS1: [odd, RHS1, RHS2, ...], LHS2: [odd, RHS1, RHS2, ...]}
    grammar = {}
    for line in lines:
        # add rules into grammar
        grammar.setdefault(line[1], []).append([float(line[0])] + line[2:])
    sentences = []
    global left_expend
    for _ in range(count):
        # initiate total number of non-terminals to expand
        left_expend = 450
        if not print_tree:
            sentences += [gen(grammar, 'ROOT', print_tree)]
        else:
            sentences += ["(ROOT {})".format(gen(grammar, 'ROOT', print_tree))]
    print(*sentences, sep="\n")


if __name__ == "__main__":
    main()
