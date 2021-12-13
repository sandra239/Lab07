#!/usr/bin/env python3

import sys

def mapper():
    for line in sys.stdin:
        data = line.strip().split(",")
        if len(data) == 4:
            timestamp, city, item, cost = data
            print(city + "," + cost)

if __name__ == "__main__":
    # what function should run when python mapper.py is called?
    mapper()
