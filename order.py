class Order:
    # direction types
    BUY = 0
    SELL = 1
    # tif(time in force) types
    GTC = 0  # good till cancel
    GTD = 1  # good till day
    # order types
    LIMIT = 0
    MARKET = 1

    def __init__(self, u_id, client_id, parr_A, parr_B, direction, tif, o_type, qty, price, timestamp):
        self.u_id = u_id
        self.client_id = client_id
        self.parr_A = parr_A
        self.parr_B = parr_B
        self.direction = direction
        self.tif = tif
        self.o_type = o_type
        self.qty = qty
        self.price = price
        self.timestamp = timestamp
