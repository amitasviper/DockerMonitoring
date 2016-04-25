from pymongo import MongoClient
import json
from utils import *

class MConnection():
	def __init__(self, debug=0):
		self.debug = debug
		self.connection = MongoClient('localhost', 27017)
		self.local_db = self.connection['docker_db']

	def fetch_all(self, container_id, limit=20):

		local_collection = local_db[container_id]

		cursor = local_collection.find({}, sort=('_id',1)).limit(limit);

		records = []

		for document in cursor:
			records.append(document)

		return records

	def save_data(self, container_id, json_data):
		try:
			#print json_data,"\n\n\n\n"
			py_json_data = json.loads(json_data)
			value = 0
			if py_json_data.has_key('memory_stats'):
				if py_json_data['memory_stats'].has_key('stats'):
					if py_json_data['memory_stats']['stats'].has_key('hierarchical_memory_limit'):
						value = py_json_data['memory_stats']['stats']['hierarchical_memory_limit']
						value = bytes2human(int(value))
						py_json_data['memory_stats']['stats']['hierarchical_memory_limit'] = value

			#print py_json_data
			local_collection = self.local_db[container_id]
			local_collection.insert_one(py_json_data)
			if self.debug > 5:
				print "Record inserted successfully"
		except Exception, err:

			if self.debug > 1:
				print "Unable to enter data into database for container_id : ",container_id
				print str(err)


if __name__ == "__main__":
	connection = MConnection()
	connection.fetch_all()