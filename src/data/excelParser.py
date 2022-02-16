import pandas as pd
import os, json

def save(data, file):
	with open(file, 'w+', encoding="utf8") as fs:
		fs.write(json.dumps(data, indent=2, ensure_ascii=False))
		fs.close()

def load(open_file):
	df = pd.read_excel(open_file)
	r1 = {}
	r2 = {}
	r3 = {}
	keys = df.columns.tolist()
	companys = keys[3:7]
	strategies = keys[7:11]
	tactics = keys[11:]
	data = []
	for row in df.itertuples():
		item = {
			'id': row.Index,
			'class': row[1],
			'prototype_name': row[2],
			'subtype': row[3] if pd.notnull(row[3]) else None
		}
		for x in range(4,8):
			if pd.notnull(row[x]):
				item['company'] = companys[x-4]
				break

		item['strategy'] = []
		for x in range(8,12):
			if pd.notnull(row[x]):
				item['strategy'].append(strategies[x-8]) 
		
		item['tactic'] = []
		for x in range(12,14):
			if pd.notnull(row[x]):
				item['tactic'].append(tactics[x-14])
		data.append(item)
	return data

if __name__ == '__main__':
	data = load('data.xlsx')
	save(data, 'data.json')