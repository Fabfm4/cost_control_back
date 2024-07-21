from app.core.infrastructure.db.conection_mixin import MixinConnection


class CardDB(MixinConnection):

    entity_name = "cards"
