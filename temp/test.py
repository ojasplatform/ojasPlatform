from kairos import Timeseries
import pymongo

client = pymongo.MongoClient('localhost')
t = Timeseries(client, type='histogram', read_func=float, intervals={
  'minute':{
    'step':60,            # 60 seconds
    'steps':120,          # last 2 hours
  }
})

# t.insert('example', 3.14159)
# t.insert('example', 2.71828)
# t.insert('example', 2.71828)
# t.insert('example', 3.71828)
# t.insert('example', 4.71828)
# t.insert('example', 5.71828)
t.insert('example', 6.71828)
t.insert('example', 7.71828)
print t.get('example', 'minute')
