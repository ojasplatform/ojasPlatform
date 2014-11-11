from pymongo import MongoClient
import datetime
import json
from kafka import KafkaClient, SimpleProducer, SimpleConsumer

#globals
db = None
client = None
reqTable = None
respTable = None

# To send messages synchronously
kafka = KafkaClient("localhost:9093")
producer = SimpleProducer(kafka)

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
		    "reqHost": 	flow.request.host, 
		    "reqPath": 	flow.request.path,
		    "reqMethod":   flow.request.method,
		    "httpVersion": flow.request.httpversion,
		    "cookies":	flow.request.headers['cookie'],
		    "content":  flow.request.content,
		    "strTime": str(datetime.datetime.now().strftime("%m-%d %H:%M"))
	}
    # insert the entire transaction into the table for mining
    #producer.send_messages("mytopic", json.dumps(entry))
    
    # reqId = reqTable.insert(entry)
    # retVal = reqTable.find({"host": flow.request.host})
    # ctx.log("request found" + str(retVal))
    # ctx.log("request" + str(reqId))

def response(ctx, flow):
    """
       Called when a server response has been received.
    """
    global respTable
    entry = {
		    "responseLength": 		flow.response.headers['content-length'], 
		    "responseContentType":	flow.response.headers['content-type'],
		    "reqHost": 	flow.request.host, 
		    "reqPath": 	flow.request.path,
		    "reqMethod":   flow.request.method,
		    "reqHttpVersion": flow.request.httpversion,
		    "reqCookies":	flow.request.headers['cookie'],
		    "reqContent":  flow.request.content,
		    "strTime": str(datetime.datetime.now().strftime("%m-%d %H:%M"))
	}

    respLength = flow.response.headers['content-length']
    if (respLength):
    	ctx.log("length" + str(flow.response.headers['content-length']))
    producer.send_messages("mytopic", json.dumps(entry))
    # insert entry into resp table only if content length is non-zero
    # respLength = flow.response.headers['content-length']
    # test the flow against learning table
    # 1. Find the app path that matches the current request
    # 2. Compare the learned attributes of the path with the current req/resp
    # 3.a. If everything checks out do nothing.
    # 3.b. If everything doesnt check out - insert entry into alert table
    # learnVal = db.learningTable.find_one({'path': flow.request.path},{'std':1, 'mean':1, 'max':1, '_id':0})
    # if (learnVal and respLength): 
    # 	if (int(respLength[0]) > (learnVal['max'] + learnVal['std'])) :
    #     	inputStr = "Unusual size "+ respLength +" (Valid range: "+str(learnVal['mean'])+" +/- "+str(learnVal['std'])+")"
    #     	entry["alertType"] = inputStr
    # 	        db.alertTable.insert(entry)
    # 	        ctx.log("inserted into alert table")
    # 	else:
    # 	        if (respLength):
    # 	    	    respTable.insert(entry)
    # 	            ctx.log("inserted into response table")
    # else:
    #     #something needs to be done here.
    #     print ""	
    #ctx.log("response")

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
    kafka.close()
