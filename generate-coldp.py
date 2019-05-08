# -*- coding: utf-8 -*-

import csv, re
from openpyxl import Workbook, load_workbook
from collections import namedtuple

sheetName = 'CoLH Version 1.4'
firstRow  = 2
firstCol  = 'A'
ranks     = ['superkingdom','kingdom','subkingdom','infrakingdom', 'superphylum','phylum','subphylum','infraphylum', 'superclass','class','subclass','infraclass', 'cohort', 'superorder', 'order']


Taxon = namedtuple('Taxon', 'id col name')
synMatcher = re.compile('^(.+) *\[= *(.+) *] *')

parents = []    

def read(row):
    for col in range(1, len(ranks)+1):
        val = sheet[chr(ord(firstCol) + col - 1) + str(row+1)].value
        if val:
            return Taxon(str(row), col, val)
    return None

def writeName(out, t):
    out.write("%s,%s,\"%s\"\n" % (t.id, ranks[t.col-1], t.name.replace('"', '""')))

wb = load_workbook(filename = 'CoLH.xlsx')
with open('name.csv', 'w', newline='') as nout:
    with open('taxon.csv', 'w', newline='') as tout:
        with open('synonym.csv', 'w', newline='') as sout:
            nout.write("ID,rank,scientificName\n")
            tout.write("ID,parentID,nameID\n")
            sout.write("nameID,taxonID,status\n")
            sheet = wb[sheetName]
            row = 1 
            t = read(row)
            while (t):
                while(parents and parents[-1].col >= t.col):
                    parents.pop()
                pid = parents[-1].id if parents else None
                m = synMatcher.search(t.name)
                if m:
                    s = Taxon('s'+str(row), t.col, m.group(2))
                    t = Taxon(t.id, t.col, m.group(1))
                    writeName(nout, s)
                    sout.write("%s,%s,%s\n" % (s.id, t.id, 'synonym'))
                writeName(nout, t)
                tout.write("%s,%s,%s\n" % (t.id, pid or '', t.id))
                row = row + 1
                parents.append(t)
                t = read(row)
