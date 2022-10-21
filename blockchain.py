class Blockchain:
    INCREASE = 0
    DECREASE = 1

    def __init__(self):
        self.balance_base = {}

    def register_user(self, user):
        self.balance_base[user] = {}

    def change_balance(self, user, currency, qnt, mode):
        if user in self.balance_base:
            user_balance = self.balance_base[user]
            self.change_balance(user_balance, currency, qnt, mode)
        else:
            raise Exception("blockchain", "no user")

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
                raise Exception("blockchain", "not enough currency")
