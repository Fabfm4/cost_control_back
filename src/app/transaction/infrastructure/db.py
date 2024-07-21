from app.core.infrastructure.db.conection_mixin import MixinConnection


class TransactionDB(MixinConnection):

    entity_name = "transactions"
