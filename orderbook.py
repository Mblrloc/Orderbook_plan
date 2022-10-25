import logging

import blockchain
import red_black_tree


class Orderbook:

    def __init__(self):
        self.blockchain = blockchain.Blockchain()
        self.sell = red_black_tree.RBTree()
        self.buy = red_black_tree.RBTree()
        self.order_id = 0

    def create_order(self, order):
        if order.direction == order.BUY:
            self.create_buy_order(order)
        elif order.direction == order.SELL:
            self.create_sell_order(order)
        else:
            logging.error("orderbook: wrong syntax's")
        self.order_id += 1
        return self.order_id

    def create_buy_order(self, order):
        key = order.price
        if key not in self.buy.levels:
            self.buy.insertNode(key)
        self.buy.add_order(key, order.client_id, order)
        if len(self.sell.levels) != 0:
            min_sell = self.sell.all_min()
            if min_sell >= key:
                self.match_order(order)

    def create_sell_order(self, order):
        key = order.price
        if key not in self.sell.levels:
            self.sell.insertNode(key)
        self.sell.get_node(key).add_order(order.client_id, order)
        if len(self.buy.levels) != 0:
            max_buy = self.buy.all_max()
            if max_buy <= key:
                self.match_order(order)

    def match_order(self, order):
        if order.direction == order.SELL:
            self.match_sell_order(order)
        if order.direction == order.BUY:
            self.match_buy_order(order)

    def remove_order(self, order):
        if order.direction == order.BUY:
            tree = self.buy
        else:
            tree = self.sell
        key = order.price
        if tree.is_in_tree(key):
            tree.remove_order_from_node(order.price, order.u_id)
        else:
            logging.error("Trying to delete non existing node")

    def match_buy_order(self, order):
        print("Starting matching")
        if order.o_type == order.MARKET:
            qnt = order.qty
            sum_qnt = 0
            keys = self.sell.levels
            order_arr = []
            partial_exec = None
            for i1 in keys:
                orders_i1 = self.sell.get_node(i1).ordered_dict
                for i2 in orders_i1:
                    it_order = orders_i1[i2]
                    if qnt - sum_qnt >= it_order.qty:
                        sum_qnt += it_order.qty
                        it_order.pending = True
                        order_arr.append(it_order)
                    else:
                        partial_exec = it_order
                        partial_exec.pending = True
            for i1 in order_arr:
                i1.execute(order.client_id)
                self.sell.remove_order_from_node(i1.price, i1)
                print("BuyCtrExe prc: " + str(i1.price) + " qnt:" + str(i1.qty))
            if partial_exec is not None:
                partial_exec.execute(order.client_id, qty=qnt - sum_qnt)
                print("PartBuyCtrExe prc: " + str(partial_exec.price) + " qnt: " + str(qnt - sum_qnt))
        else:
            pass

    def match_sell_order(self, order):
        pass
