import json
from bson import json_util
import bottle
from bottle import route, run, request, abort, response
from pymongo import Connection
import pymongo 
 
connection = Connection('localhost', 27017)
db = connection.mydb
kdb = connection.kairos
 
# the decorator
def enable_cors(fn):
	def _enable_cors(*args, **kwargs):
		# set CORS headers
		response.headers['Access-Control-Allow-Origin'] = '*'
		response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
		response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
		if bottle.request.method != 'OPTIONS':
			# actual request; reply with the actual response
			return fn(*args, **kwargs)
        return _enable_cors

@route('/resp', method='PUT')
def put_document():
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    entity = json.loads(data)
    if not entity.has_key('_id'):
        abort(400, 'No _id specified')
    try:
        db['documents'].save(entity)
    except ValidationError as ve:
        abort(400, str(ve))
     
@route('/respFull/:id', method='GET')
def get_document(id):
	entity = db.respTable.find_one({'req-host':id}, {'_id':0})
    	if not entity:
        	abort(404, 'No document with id %s' % id)
   	return entity

@route('/respLength/:id', method='GET')
def get_document(id):
	entity = db.respTable.find_one({'req-host':id}, {'response-length':1, '_id':0})
    	if not entity:
        	abort(404, 'No document with id %s' % id)
   	return entity

@route('/reset/:id', method='GET')
def get_document(id):
	if (id == 'resp'):
		entity = db.respTable.drop()
	if (id == 'req'):
		entity = db.reqTable.drop()
	if (id == 'all'):
		entity = db.respTable.drop()
		entity = db.reqTable.drop()
		entity = db.learningTable.drop()
		entity = db.alertTable.drop()
		entity = True
    	
	if not entity:
        	abort(404, 'System already reset %s' % id)
   	return entity

@route('/getStats', method='GET')
def get_document():
	entity = None
	#entity = db.respTable.find({'
	return entity

@route('/getAlerts', method='GET')
@enable_cors
def get_document():
	json_docs = []
	entity = db.alertTable.find({},{'strTime':1, 'alertType':1, 'req-path':1, '_id':0}).sort('_id', pymongo.DESCENDING).limit(10)
	for doc in entity: 
		#json_doc = json.dumps(doc, default=json_util.default)
		json_docs.append(doc)
	response.content_type = 'application/json'
	if not entity:
        	abort(404, 'System already reset %s' % id)
	return json.dumps(json_docs)


@route('/getEvents', method='GET')
@enable_cors
def get_document():
	json_docs = []
	entity = db.respTable.find({},{'strTime':1, 'req-method':1, 'response-length':1, 'req-host':1, 'req-path':1, '_id':0}).sort('_id', pymongo.DESCENDING).limit(10)
	for doc in entity: 
		#json_doc = json.dumps(doc, default=json_util.default)
		json_docs.append(doc)
	response.content_type = 'application/json'
	if not entity:
        	abort(404, 'System already reset %s' % id)
	return json.dumps(json_docs)

@route('/getTimeSeries', method='GET')
@enable_cors
def get_document():
	json_docs = []
	entity = kdb.minute.find({},{'name':1, 'value':1, '_id':0}).limit(10)
	for doc in entity: 
		#json_doc = json.dumps(doc, default=json_util.default)
		json_docs.append(doc)
	response.content_type = 'application/json'
	if not entity:
        	abort(404, 'System already reset %s' % id)
	return json.dumps(json_docs)

@route('/setLearn', method='GET')
@enable_cors
def get_document():
	json_docs = []
	entity = db.alertTable.find({},{'strTime':1, 'alertType':1, 'req-path':1, '_id':0}).limit(3)
	for doc in entity: 
		#json_doc = json.dumps(doc, default=json_util.default)
		json_docs.append(doc)
	response.content_type = 'application/json'
	if not entity:
        	abort(404, 'System already reset %s' % id)
	return json.dumps(json_docs)
 
run(host='0.0.0.0', port=5000)
