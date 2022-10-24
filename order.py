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

    def __init__(self, u_id, client_id, parr_A, parr_B, direction, tif, o_type, qty, price, timestamp):
        self.u_id = u_id  # order id
        self.client_id = client_id  # owner of order id
        self.parr_A = parr_A  # maker currency
        self.parr_B = parr_B  # taker currency
        self.direction = direction  # sell / buy
        self.tif = tif  # time in force
        self.o_type = o_type  # order type
        self.qty = qty  # quantity of maker currency
        self.price = price  # price for single maker currency
        self.timestamp = timestamp  # time of order creation

    def __lt__(self, other):
        return self.price < other.price

    def __le__(self, other):
        return self.price <= other.price

    def __gt__(self, other):
        return self.price > other.price

    def __ge__(self, other):
        return self.price >= other.price

    def __eq__(self, other):
        return  self.price == other.price

    def __ne__(self, other):
        return self.price == other.price

#    def create_simple_sc(self):
