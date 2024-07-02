from core.infrastructure.db import MongoDBConection


class TransactionSplitDB(MongoDBConection):

    collection_name = "transactions_split"
