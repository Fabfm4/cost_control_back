from src.core.infrastructure.db import MongoDBConection


class CardDB(MongoDBConection):

    collection_name = "cards"
