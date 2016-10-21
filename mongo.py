import os
from pymongo import MongoClient

class Collections:

	def __init__(self):
		mongo_host = os.environ["MONGO_PORT_27017_TCP_ADDR"]
		mongo_port = os.environ["MONGO_PORT_27017_TCP_PORT"]
		self.conn = "mongodb://{mongo_host}:{mongo_port}".format(mongo_host=mongo_host, mongo_port=mongo_port)
		self.client = MongoClient(self.conn)

		self.db = self.client['latinoware_db']

		self.speakers = self.db['speakers']
		self.keynotes = self.db['keynotes']