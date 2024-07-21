from app.core.infrastructure.db.conection_mixin import MixinConnection


class TransactionSplitDB(MixinConnection):

    entity_name = "transactions_split"
