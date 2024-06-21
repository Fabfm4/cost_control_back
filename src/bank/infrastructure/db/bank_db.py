from src.core.infrastructure.db import MongoDBConection


class BankDB(MongoDBConection):

    collection_name = "banks"
