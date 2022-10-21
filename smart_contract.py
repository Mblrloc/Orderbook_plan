class SmartContract:
    MAKER = 0
    TAKER = 1

    def __init__(self, blockchain, u_id, maker, taker, parr_A, parr_B, qnt_A, qnt_B):
        self.id = u_id
        self.maker = maker
        self.taker = taker
        self.parr_A = parr_A
        self.parr_B = parr_B
        self.qnt_A = qnt_A
        self.qnt_B = qnt_B
        self.balance = {}
        self.history = {}
        self.blockhain = blockchain

    def entry_point(self, user, currency, value):
        self.balance[currency] = self.balance.get(currency, 0) + value
        self.history[user][currency] = self.history.get(user, {currency: value}).get(currency, 0) + value

    def check_user(self, mode):
        if mode == SmartContract.MAKER:
            return self.history[self.maker][self.parr_A] >= self.qnt_A
        elif mode == SmartContract.TAKER:
            return self.history[self.taker][self.parr_B] >= self.qnt_B
        else:
            raise Exception("sc", "err")

    def execute(self):
        if ~(self.check_user(SmartContract.MAKER)):
            raise Exception("exe", "not enough currency for maker")
        if ~(self.check_user(SmartContract.TAKER)):
            raise Exception("exe", "not enough currency for taker")
