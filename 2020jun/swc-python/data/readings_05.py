#!/usr/bin/env python3

import sys
import numpy


def process(filename, action):
    data = numpy.loadtxt(filename, delimiter=',')

    if action == '--min':
        values = numpy.min(data, axis=1)
    elif action == '--mean':
        values = numpy.mean(data, axis=1)
    elif action == '--max':
        values = numpy.max(data, axis=1)

    for val in values:
        print(val)


def main():
    script = sys.argv[0]
    if len(sys.argv) < 2:
        print('You must provide an action and a filename.')
        sys.exit(1)
    action = sys.argv[1]
    filenames = sys.argv[2:]
    if action not in ['--min', '--mean', '--max']:
        print('Action is not one of --min, --mean, or --max: ', action)
        sys.exit(2)
    for filename in filenames:
        process(filename, action)


if __name__ == '__main__':
   main()