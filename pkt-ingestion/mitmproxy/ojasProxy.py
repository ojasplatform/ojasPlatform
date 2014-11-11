import datetime
from kairos import Timeseries
import pymongo
from pymongo import MongoClient
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
    global timeSeries

    client = MongoClient()
    db = client.mydb
    reqTable = db.reqTable
    respTable = db.respTable
    timeSeries = Timeseries(client, type='histogram', read_func=float, intervals={
	'minute':{
		'step':60,
		'steps':120,
	}
    })
    timeSeries.insert('startup', 1)
    ctx.log("start"+t.get('startup')

def clientconnect(ctx, client_connect):
    """
        Called when a client initiates a connection to the proxy. Note that a
        connection can correspond to multiple HTTP requests
    """
    global timeSeries
    timeSeries.insert('session', 1)
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
    global timeSeries
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
    timeSeries.insert('request', 1)
    reqId = reqTable.insert(entry)
    retVal = reqTable.find({"host": flow.request.host})
    ctx.log("request found" + str(retVal))
    ctx.log("request" + str(reqId))

def response(ctx, flow):
    """
       Called when a server response has been received.
    """
    global respTable
    global timeSeries
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
    timeSeries.insert('response', 1)
    # test the flow against learning table
    # 1. Find the app path that matches the current request
    # 2. Compare the learned attributes of the path with the current req/resp
    # 3.a. If everything checks out do nothing.
    # 3.b. If everything doesnt check out - insert entry into alert table
    learnVal = db.learningTable.find_one({'path': flow.request.path},{'std':1, 'mean':1, 'max':1, '_id':0})
    if (learnVal and respLength): 
    	if (int(respLength[0]) > (learnVal['max'] + learnVal['std'])) :
		inputStr = "Unusual size "+ respLength +" (Valid range: "+str(learnVal['mean'])+" +/- "+str(learnVal['std'])+")"
		entry["alertType"] = inputStr
    	        db.alertTable.insert(entry)
    		timeSeries.insert('alert', 1)
    	        ctx.log("inserted into alert table")
    	else:
    	        if (respLength):
    	    	    respTable.insert(entry)
    	            ctx.log("inserted into response table")
    else:
	#something needs to be done here.
        print ""	

    # add summary stats to the stats db
	# 1. number of GETS, 200OK, POSTS etc.  
	# 2. top 10 URL hits
	# 3. group by source IPs
    if (flow.request.method == 'GET'):
		ctx.log("adding "+str(flow.request.method))
    else:
		ctx.log("adding "+str(flow.request.method))

    # look at the path 
	# 1. match the path
	# 2. match the params and insert into alert table
    
    ctx.log("response")

def error(ctx, flow):
    """
        Called when a flow error has occured, e.g. invalid server responses, or
        interrupted connections. This is distinct from a valid server HTTP error
        response, which is simply a response with an HTTP error code.
    """
	
    global timeSeries
    timeSeries.insert('error', 1)
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
