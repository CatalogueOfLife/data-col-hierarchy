# -*- coding: utf-8 -*-

import csv, re
from openpyxl import Workbook, load_workbook
from collections import namedtuple

sheetName = 'CoLH Version 1.4'
firstRow  = 2
firstCol  = 'A'
ranks 	  = ['superkingdom','kingdom','subkingdom','infrakingdom', 'superphylum','phylum','subphylum','infraphylum', 'superclass','class','subclass','infraclass', 'cohort', 'superorder', 'order']


Taxon = namedtuple('Taxon', 'row col name')

parents = []	

def read(row):
	for col in range(1, len(ranks)+1):
		val = sheet[chr(ord(firstCol) + col - 1) + str(row+1)].value
		if val:
			return Taxon(row, col, val)
	return None


wb = load_workbook(filename = 'CoLH.xlsx')
with open('name.csv', 'w', newline='') as nout:
	with open('taxon.csv', 'w', newline='') as tout:
		nout.write("ID,rank,scientificName\n")
		tout.write("ID,parentID,nameID\n")
		sheet = wb[sheetName]
		row = 1	
		t = read(row)
		while (t):
			while(parents and parents[-1].col >= t.col):
				parents.pop()
			prow = parents[-1].row if parents else None
			nout.write("%s,%s,\"%s\"\n" % (t.row, ranks[t.col-1], t.name.replace('"', '""')))
			tout.write("%s,%s,%s\n" % (t.row, prow or '', t.row))
			row = row + 1
			parents.append(t)
			t = read(row)
