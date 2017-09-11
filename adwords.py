import csv
import random
import math
import sys


def greedy(q, budget, neighbours, total):
    revenues = []
    for i in xrange(100):
        tempbudget = budget.copy()
        revenue = 0
        for line in q:
            for neighbour in sorted(neighbours[line[:-1]], key=lambda x: x[1], reverse=True):
                if tempbudget[neighbour[0]] >= neighbour[1]:
                    revenue += neighbour[1]
                    tempbudget[neighbour[0]] -= neighbour[1]
                    break
        revenues.append(revenue)
        random.shuffle(q)
    meanrevenue = sum(revenues) / len(revenues)
    print "revenue: ", format(revenues[0], ".2f")
    print "competitive ratio: ", round(meanrevenue / total, 2)


def psi(x):
    return 1 - math.exp(x - 1)


def msvv(q, budget, neighbours, total):
    revenues = []
    for i in xrange(100):
        tempbudget = budget.copy()
        revenue = 0
        for line in q:
            for neighbour in sorted(neighbours[line[:-1]],
                                    key=lambda x: x[1] * psi((budget[x[0]] - tempbudget[x[0]]) / budget[x[0]]),
                                    reverse=True):
                if tempbudget[neighbour[0]] >= neighbour[1]:
                    revenue += neighbour[1]
                    tempbudget[neighbour[0]] -= neighbour[1]
                    break
        revenues.append(revenue)
        random.shuffle(q)
    meanrevenue = sum(revenues) / len(revenues)
    print "revenue: ", format(revenues[0], ".2f")
    print "competitive ratio: ", round(meanrevenue / total, 2)


def balance(q, budget, neighbours, total):
    revenues = []
    for i in xrange(100):
        tempbudget = budget.copy()
        revenue = 0
        for line in q:
            for neighbour in sorted(neighbours[line[:-1]], key=lambda x: tempbudget[x[0]], reverse=True):
                if tempbudget[neighbour[0]] >= neighbour[1]:
                    revenue += neighbour[1]
                    tempbudget[neighbour[0]] -= neighbour[1]
                    break
        revenues.append(revenue)
        random.shuffle(q)
    meanrevenue = sum(revenues) / len(revenues)
    print "revenue: ", format(revenues[0], ".2f")
    print "competitive ratio: ", round(meanrevenue / total, 2)


def main():
    if len(sys.argv) != 2:
        print "usage: python adwords.py <greedy|msvv|balance>"
        exit(1)

    neighbours = {}
    budget = {}
    total = 0
    with open('bidder_dataset.csv', 'rb') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[3]:
                budget[row[0]] = float(row[3])
                total += float(row[3])
            if row[1] in neighbours:
                neighbours[row[1]].append((row[0], float(row[2])))
            else:
                neighbours[row[1]] = [(row[0], float(row[2]))]

    q = []
    with open("queries.txt") as f:
        for line in f:
            q.append(line)

    random.seed(0)

    if sys.argv[1] == "greedy":
        greedy(q, budget, neighbours, total)
    elif sys.argv[1] == "msvv" or sys.argv[1] == "mssv":
        msvv(q, budget, neighbours, total)
    elif sys.argv[1] == "balance":
        balance(q, budget, neighbours, total)
    else:
        print "usage: python adwords.py <greedy|msvv|balance>"
        exit(1)


if __name__ == "__main__":
    main()
