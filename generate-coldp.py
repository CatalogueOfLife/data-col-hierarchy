# -*- coding: utf-8 -*-

import csv, re
from openpyxl import Workbook, load_workbook
from collections import namedtuple

sheetName = 'CoLH Version 1.4'
firstRow  = 2
firstCol  = 'A'
notesCol  = 'P'
ranks     = ['superkingdom','kingdom','subkingdom','infrakingdom', 'superphylum','phylum','subphylum','infraphylum', 'superclass','class','subclass','infraclass', 'cohort', 'superorder', 'order']


Taxon = namedtuple('Taxon', 'id col name notes')
synMatcher = re.compile('^(.+) *\[= *(.+) *] *')

parents = []    

def read(row):
    for col in range(1, len(ranks)+1):
        val = sheet[chr(ord(firstCol) + col - 1) + str(row+1)].value
        note = sheet[notesCol + str(row+1)].value
        if val:
            return Taxon(str(row), col, val, note)
    return None

def writeUsage(out, t, parentID, status):
    out.write("%s,%s,%s,%s,\"%s\",\"%s\"\n" % (t.id, parentID, status, ranks[t.col-1], t.name.replace('"', '""'), (t.notes or "").replace('"', '""')))

wb = load_workbook(filename = 'CoLH.xlsx')
with open('NameUsage.csv', 'w', newline='') as out:
            out.write("ID,parentID,status,rank,scientificName,remarks\n")
            sheet = wb[sheetName]
            row = 1 
            t = read(row)
            while (t):
                while(parents and parents[-1].col >= t.col):
                    parents.pop()
                pid = parents[-1].id if parents else None
                m = synMatcher.search(t.name)
                if m:
                    s = Taxon('s'+str(row), t.col, m.group(2), None)
                    t = Taxon(t.id, t.col, m.group(1), t.notes)
                    writeUsage(out, s, t.id, 'synonym')
                writeUsage(out, t, pid or '', 'accepted')
                row = row + 1
                parents.append(t)
                t = read(row)
