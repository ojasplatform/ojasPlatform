from pymongo import MongoClient
import json
import numpy

hostVal = "127.0.0.1"
pathVal = "\collecitons\&=test"
mClient = MongoClient()
db = mClient.mydb
reqTable = db.reqTable
entry={'hosts': hostVal, 'pathVal': pathVal}
retId = reqTable.insert(entry)

# Get aggregates
ret = db.respTable.aggregate([ 
	{"$group": {"_id":"$req-host", 'req-path':{"$push":"$req-path"}, 'req-length':{"$push":"$response-length"}}}
	])
parsed = ret
# Extracts the length summaries per path
for item in range(0,len(ret['result'])):
	path = ret['result'][item]['req-path']
	lenList = ret['result'][item]['req-length']
	intLenList = []
	for item in lenList:
		intLenList.append(int(item[0]))
	entry = {
			'std': numpy.std(intLenList),
			'max': max(intLenList),
			'mean': numpy.mean(intLenList),
			'path': path
		}
	db.learningTable.update({'path': path}, entry ,upsert=True)
	print db.learningTable.find_one({'path': '/users'},{'std':1, 'mean':1, 'max':1, '_id':0})['std']
	
	print 'Successfully added to learning table'


#print json.dumps(parsed, indent=4, sort_keys=True)
#print "successfully added entry" + str(retId)

