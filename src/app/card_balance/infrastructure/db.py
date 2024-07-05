from app.core.infrastructure.db import MongoDBConection


class CardBalanceDB(MongoDBConection):

    collection_name = "card_balances"
