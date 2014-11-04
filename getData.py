import json
data = {}
metaData = json.load(open('saveWork.json'))
for val in metaData[0]:
	data[val] = json.load(open('data/' + val + '.json'))

