from pymongo import MongoClient
import datetime
import numpy
# Globals

db = None
client = None
reqTable = None
respTable = None

"""
    This is a script stub, with definitions for all events.
"""
def start(ctx, argv):
    """
        Called once on script startup, before any other events.
    """
    global client 
    global reqTable 
    global db 
    global respTable
    client = MongoClient()
    db = client.mydb
    reqTable = db.reqTable
    respTable = db.respTable
    ctx.log("start")

def clientconnect(ctx, client_connect):
    """
        Called when a client initiates a connection to the proxy. Note that a
        connection can correspond to multiple HTTP requests
    """
    ctx.log("clientconnect")

def serverconnect(ctx, server_connection):
    """
        Called when the proxy initiates a connection to the target server. Note that a
        connection can correspond to multiple HTTP requests
    """
    ctx.log("serverconnect")

def request(ctx, flow):
    """
    """
    global reqTable
    global getCounter
    entry = {
		    "host": 	flow.request.host, 
		    "path": 	flow.request.path,
		    "method":   flow.request.method,
		    "http-version": flow.request.httpversion,
		    "cookies":	flow.request.headers['cookie'],
		    "content":  flow.request.content,
		    "timestamp": datetime.datetime.now(),
		    "strTime": str(datetime.datetime.now().strftime("%m-%d %H:%M"))
	}
    # insert the entire transaction into the table for mining
    reqId = reqTable.insert(entry)
    retVal = reqTable.find({"host": flow.request.host})
    ctx.log("request found" + str(retVal))
    ctx.log("request" + str(reqId))

def response(ctx, flow):
    """
       Called when a server response has been received.
    """
    global respTable
    entry = {
		    "response-length": 		flow.response.headers['content-length'], 
		    "response-content-type":	flow.response.headers['content-type'],
		    "req-host": 	flow.request.host, 
		    "req-path": 	flow.request.path,
		    "req-method":   flow.request.method,
		    "req-http-version": flow.request.httpversion,
		    "req-cookies":	flow.request.headers['cookie'],
		    "req-content":  flow.request.content,
		    "timestamp": datetime.datetime.now(),
		    "strTime": str(datetime.datetime.now().strftime("%m-%d %H:%M"))
	}
    # insert entry into resp table only if content length is non-zero
    respLength = flow.response.headers['content-length']
    if (respLength):
	    respTable.insert(entry)
	    ctx.log("inserted into response table")

    # Get aggregates
    ret = db.respTable.aggregate([ 
		{"$group": {"_id":"$req-host", 'req-path':{"$push":"$req-path"}, 'req-length':{"$push":"$response-length"}}}
		])
    # Extracts the length summaries per path
    for item in range(0,len(ret['result'])):
    	    path = ret['result'][item]['req-path']
    	    lenList = ret['result'][item]['req-length']
    	    intLenList = []
    	    for item in lenList:
    	    	intLenList.append(int(item[0]))
    	    entry = {
    	    		"std": numpy.std(intLenList),
			"mean": numpy.mean(intLenList),
			"max": max(intLenList),
    	    		"path": path
    	    	}
    	    db.learningTable.update({'path': path}, entry ,upsert=True)
    ctx.log("Successfully added to learning table")
    ctx.log("response")

def error(ctx, flow):
    """
        Called when a flow error has occured, e.g. invalid server responses, or
        interrupted connections. This is distinct from a valid server HTTP error
        response, which is simply a response with an HTTP error code.
    """
    ctx.log("error")

def clientdisconnect(ctx, client_disconnect):
    """
        Called when a client disconnects from the proxy.
    """
    ctx.log("clientdisconnect")

def done(ctx):
    """
        Called once on script shutdown, after any other events.
    """
    ctx.log("done")
