#!/usr/bin/env python3

import sys

def sequential():
    totalSales = {}
    for line in sys.stdin:
        data = line.strip().split(",")
        timestamp, city, item, cost = data

        if city not in totalSales:
            totalSales[city] = 0
        totalSales[city] += float(cost)

    for key, value in sorted(totalSales.items()):
        print(key + "," + str(value))

if __name__ == "__main__":
    # what function should run when python sequential.py is called?
    sequential()
