import blockchain
import logging
import time


class SmartContract:
    MAKER = 0
    TAKER = 1

    def __init__(self, u_id, maker, taker, parr_A, parr_B, qnt_A, qnt_B, exp_date=0):
        self.u_id = u_id                           # contract id in blockchain
        self.maker = maker                         # maker id
        self.taker = taker                         # taker id
        self.parr_A = parr_A                       # maker currency
        self.parr_B = parr_B                       # taker currency
        self.qnt_A = qnt_A                         # quantity of parr_A
        self.qnt_B = qnt_B                         # quantity of parr_B
        self.history = {}                          # history of all entry point usages with non-zero number of tokens
        self.exp_date = exp_date                   # expiration date
        self.blockchain = blockchain.Blockchain()  # our "blockchain"
        self.active = True                         # activeness of contract

    def entry_point(self, user, currency, qnt):
        if qnt >= 0:
            self.blockchain.transfer(user, self.u_id, currency, qnt)
            self.history[user][currency] = self.history.get(user, {currency: qnt}).get(currency, 0) + qnt
        else:
            logging.info("ep: negative qnt of ep tokens")

    def check_user(self, mode):                    # check if maker/taker added enough currency for sc execution
        if mode == SmartContract.MAKER:
            return self.history[self.maker][self.parr_A] >= self.qnt_A
        elif mode == SmartContract.TAKER:
            return self.history[self.taker][self.parr_B] >= self.qnt_B
        else:
            raise Exception("sc", "syntax error")

    def check_time(self):                          # check if SC is expired
        return self.exp_date == 0 or time.time() < self.exp_date

    def check_all(self):                           # all conditions
        if ~self.active:
            logging.info("execution: sc is cancelled")
            return False
        if ~self.check_time():
            logging.info("execution: contract is expired")
            return False
        if ~(self.check_user(SmartContract.MAKER)):
            logging.info("execution: not enough currency for maker")
            return False
        if ~(self.check_user(SmartContract.TAKER)):
            logging.info("execution: not enough currency for taker")
            return False
        return True

    def execute(self):
        if self.check_all():
            self.blockchain.transfer(self.u_id, self.maker, self.parr_B, self.qnt_B)
            self.blockchain.transfer(self.u_id, self.taker, self.parr_A, self.qnt_A)

    def cancel(self):
        qnt_a = self.history[self.maker][self.parr_A]
        qnt_b = self.history[self.taker][self.parr_B]
        if qnt_a > 0:
            self.blockchain.transfer(self.u_id, self.maker, self.parr_A, qnt_a)
        if qnt_b > 0:
            self.blockchain.transfer(self.u_id, self.taker, self.parr_B, qnt_b)
        self.active = False  # may vary in actual realisation
