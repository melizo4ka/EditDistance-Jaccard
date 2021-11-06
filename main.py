import csv

import numpy as np
import math
from timeit import default_timer as timer

cost = {'copy': 0, 'replace': 1, 'delete': 1, 'insert': 1}


def editDistance(x, y):
    m = len(x)
    n = len(y)
    c = np.zeros((m+1, n+1))
    op = np.zeros((m+1, n+1), str)
    for i in range(m+1):
        c[i, 0] = i * cost['delete']
        op[i, 0] = 'd'
    for j in range(n+1):
        c[0, j] = j * cost['insert']
        op[0, j] = 'i'
    for i in range(1, m+1):
        for j in range(1, n+1):
            c[i, j] = math.inf
            if x[i-1] == y[j-1]:
                c[i, j] = c[i-1, j-1] + cost['copy']
                op[i, j] = 'c'
            if (x[i-1] != y[j-1]) & (c[i-1, j-1] + cost['replace'] < c[i, j]):
                c[i, j] = c[i-1, j-1] + cost['replace']
                op[i, j] = 'r'
            if c[i-1, j] + cost['delete'] < c[i, j]:
                c[i, j] = c[i-1, j] + cost['delete']
                op[i, j] = 'd'
            if c[i, j-1] + cost['insert'] < c[i, j]:
                c[i, j] = c[i, j-1] + cost['insert']
                op[i, j] = 'i'
    return c[m, n]


def nGram(x):
    lst = []
    for i in range(2, len(x)+2):
        n = i
        lst.extend([x[i:i + n - 1] for i in range(len(x) - n + 2)])
    return lst


def checkJC(query, lessico):
    lessicoNGram = nGram(lessico)
    intersection = [i for i in query if i in lessicoNGram]
    union = list({i: i for i in query + lessicoNGram}.values())
    JC = len(intersection) / len(union)
    return JC


def main():
    queryList = ['abito', 'puro', 'ecco', 'scienza', 'triste', 'adon', 'pres', 'edic', 'schimm', 'ussi']
    table = [['Word checked', 'Time Edit Distance', 'Time N-Gram']]
    with open('parole_italiane.txt') as f:
        for x in queryList:
            queryNGram = nGram(x)
            minCost = math.inf
            maxJC = 0

            # edit distance
            i = 0
            startED = timer()
            f.seek(0)
            lines = f.readlines()
            for line in lines:
                i = i + 1
                newMin = editDistance(x, line)
                if newMin < minCost:
                    minCost = newMin
            endED = timer()
            timerED = round(endED - startED, 3)

            # JC con ngram
            i = 0
            startJC = timer()
            f.seek(0)
            lines = f.readlines()
            for line in lines:
                i = i + 1
                newJC = checkJC(queryNGram, line)
                if newJC >= maxJC:
                    maxJC = newJC
            endJC = timer()
            timerJC = round(endJC - startJC, 3)
            table.append([x, timerED, timerJC])
    file = open('time.csv', 'w+', newline='')
    with file:
        write = csv.writer(file)
        write.writerows(table)


if __name__ == "__main__":
    main()
