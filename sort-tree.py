# -*- coding: utf-8 -*-

import sys, re
from collections import namedtuple

indentMatcher = re.compile('^( *)[^ ]')
Node = namedtuple('Node', 'indent line children')

fn = sys.argv[1]
print("Sorting " + fn)
tree    = []
parents = []

# read
with open(fn, 'r') as file:
    lastIndent=0
    for line in file:
        m = indentMatcher.match(line)
        n = Node(len(m.group(1)), line, [])
        while(parents and parents[-1].indent >= n.indent):
            parents.pop()
        if parents:
            parents[-1].children.append(n)
        else:
            tree.append(n)
        parents.append(n)

# sort

# print
def printRecursively(n):
    sys.stdout.write(n.line)
    for c in sorted(n.children, key=lambda n: n.line):
        printRecursively(c)



for n in sorted(tree, key=lambda n: n.line):
    printRecursively(n)
