import logging


class Blockchain:
    INCREASE = 0
    DECREASE = 1

    def __new__(cls):  # singleton init
        if not hasattr(cls, 'instance'):
            cls.instance = super(Blockchain, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.balance_base = {}

    def register_user(self, user):
        self.balance_base[user] = {}

    def change_balance(self, user, currency, qnt, mode):
        if user in self.balance_base:
            user_balance = self.balance_base[user]
            self.change_balance(user_balance, currency, qnt, mode)
        else:
            logging.info("blockchain: no such user")

    @staticmethod
    def change_value(user_balance, currency, qnt, mode):
        if mode == Blockchain.INCREASE:
            if currency in user_balance:
                user_balance[currency] += qnt
            else:
                user_balance[currency] = qnt
        elif mode == Blockchain.DECREASE:
            if currency in user_balance and user_balance[currency] >= qnt:
                user_balance[currency] -= qnt
            else:
                logging.info("blockchain", "not enough currency")

    def transfer(self, user_from, user_to, currency, qnt):
        self.change_balance(user_from, currency, qnt, mode=Blockchain.DECREASE)
        self.change_balance(user_to, currency, qnt, mode=Blockchain.INCREASE)
