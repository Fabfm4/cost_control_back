from app.core.infrastructure.db.conection_mixin import MixinConnection


class BankDB(MixinConnection):

    entity_name = "banks"
