from app.core.infrastructure.db.conection_mixin import MixinConnection


class CardBalanceDB(MixinConnection):

    entity_name = "card_balances"
