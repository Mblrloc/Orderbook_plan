class User:

    def __init__(self, u_id, balance, locked_balance=0):
        self.u_id = u_id
        self.balance = balance
        self.locked_balance = locked_balance

    # should know this straight from the blockchain
    def get_balance(self):
        return self.balance - self.locked_balance

    # blockchain should do this via executing SC
    def change_balance(self, balance):
        self.balance = balance

    # blockchain should do this via entering SC
    def lock_balance(self, locked_balance):
        self.locked_balance += locked_balance

    # SC should do this via cancelling
    def unlock_balance(self, locked_balance):
        self.locked_balance -= locked_balance

    def lock_possible(self, locked_balance):
        return self.balance - self.locked_balance > locked_balance
