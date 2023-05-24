import sqlite3
from openpyxl import load_workbook
import re

def slugify(text, lower=1):
	if lower == 1:
		text = text.strip().lower()
	text = re.sub(r'[^\w _-]+', '', text)
	text = re.sub(r'[- ]+', '_', text)
	return text

con = sqlite3.connect('countries.db')
filename="backupdb.xlsx"
wb = load_workbook(filename)

sheets = wb.get_sheet_names()

for sheet in sheets:
	ws = wb[sheet] 

	columns= []
	query = 'CREATE TABLE ' + str(slugify(sheet)) + '(ID INTEGER PRIMARY KEY AUTOINCREMENT'
	for row in next(ws.rows):
		if(row.value==None):
			continue
		key = "country"
		if key in slugify(row.value):    #do not use country as column name!!!!!1
			query += ', ' + slugify(row.value) + ' TEXT'
		else:
			query += ', ' + slugify(row.value) + ' INTEGER'
		columns.append(slugify(row.value))
	query += ');'

	con.execute(query)

	tup = []
	for i, rows in enumerate(ws):
		tuprow = []
		if i == 0:
			continue
		for row in rows:
			if str(row.value).strip() != 'None':
				tuprow.append(str(row.value).strip())
			else:
				continue
		tup.append(tuple(tuprow))
		
	tup = [tuprow for tuprow in tup if tuprow]
	insQuery1 = 'INSERT INTO ' + str(slugify(sheet)) + '('
	insQuery2 = ''
	for col in columns:
		insQuery1 += col + ', '
		insQuery2 += '?, '
	insQuery1 = insQuery1[:-2] + ') VALUES('
	insQuery2 = insQuery2[:-2] + ')'
	insQuery = insQuery1 + insQuery2

	con.executemany(insQuery, tup)
	con.commit()
	
con.close()