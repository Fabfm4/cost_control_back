from app.core.infrastructure.db import MongoDBConection


class TransactionDB(MongoDBConection):

    collection_name = "transactions"
