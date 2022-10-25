import logging

from smart_contract import SmartContract
from blockchain import Blockchain


class Order:
    # direction types
    BUY = 0
    SELL = 1
    # tif types
    GTC = 0  # good till cancel
    GTD = 1  # good till day
    # order types
    LIMIT = 0
    MARKET = 1
    #
    PARR_A = "ETH"
    PARR_B = "USDT"
    FULL_EXECUTION = 0
    PARTIAL_EXECUTION = 1

    def __init__(self, client_id, parr_A, parr_B, direction, tif, o_type, qty, price, timestamp):
        # self.u_id = u_id  # order id
        self.client_id = client_id  # owner of order id
        self.parr_A = parr_A  # maker currency
        self.parr_B = parr_B  # taker currency
        self.direction = direction  # sell / buy
        self.tif = tif  # time in force
        self.o_type = o_type  # order type
        self.qty = qty  # quantity of maker currency
        self.price = price  # price for single maker currency
        self.timestamp = timestamp  # time of order creation
        self.pending = False
        self.blockchain = Blockchain()

    def execute(self, executer, qty=FULL_EXECUTION):
        if self.pending:
            if qty == Order.FULL_EXECUTION:
                sc = self.create_sc(executer, self.price * self.qty)
                sc.execute()
            else:
                sc = self.create_sc(executer, self.price * qty)
                sc.execute()
                self.pending = False
                self.qty = self.qty - qty
        else:
            logging.error("Sc is not pending!")

    def create_sc(self, executer, B_qty):
        u_id = self.blockchain.register_sc()
        sc = SmartContract(u_id, self.client_id, executer, self.parr_A, self.parr_B, self.qty,
                           B_qty)  # u_id, maker, taker, parr_A, parr_B, qnt_A, qnt_B, exp_date=0)
        return sc
