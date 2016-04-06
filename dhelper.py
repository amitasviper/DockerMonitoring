from pymongo import MongoClient

class MConnection():
	def __init__(self):
		self.connection = MongoClient('localhost', 27017)

	def fetch_all(self):
		local_db = self.connection['gcmkeys']
		local_collection = local_db['OldNonVegJokesv2']
		gcmKeyList = []

		cursor = local_collection.find({})

		for document in cursor:
			print document

def main():
	connection = MConnection()
	connection.fetch_all()

if __name__ == "__main__":
	main()