import logging

import blockchain
import red_black_tree
import numpy as np
from order import Order


class Orderbook:

    def __init__(self):
        self.blockchain = blockchain.Blockchain()
        self.sell = red_black_tree.RBTree()
        self.buy = red_black_tree.RBTree()
        self.order_id = 0

    def create_order(self, order):
            self.match_order(order)
            return self.order_id

    def add_order(self, key, order):
        if order.direction == order.SELL:
            if key not in self.sell.levels:
                self.sell.insertNode(key)
            self.sell.get_node(key).add_order(order.client_id, order)
        elif order.direction == order.BUY:
            if key not in self.buy.levels:
                self.buy.insertNode(key)
            self.buy.get_node(key).add_order(order.client_id, order)
        else:
            logging.error("Syntaxis error")

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

    def match_order(self, order):
        qnt = order.qty
        sum_qnt = 0

        if order.direction == order.SELL:
            keys = self.buy.levels.copy()
            keys.reverse()
            tree = "BUY"
        else:
            keys = self.sell.levels
            tree = "SELL"
        keys = np.array(keys)
        if order.o_type == order.LIMIT:
            if order.direction == order.SELL:
                filter_arr = keys >= order.price
            else:
                filter_arr = keys <= order.price
            keys = keys[filter_arr]
        order_arr = []
        partial_exec = None
        for i1 in keys:
            if order.direction == order.SELL:
                orders_i1 = self.buy.get_node(i1).ordered_dict
            else:
                orders_i1 = self.sell.get_node(i1).ordered_dict
            for i2 in orders_i1:
                it_order = orders_i1[i2]
                if qnt - sum_qnt > it_order.qty:
                    sum_qnt += it_order.qty
                    it_order.pending = True
                    order_arr.append(it_order)
                else:
                    partial_exec = it_order
                    partial_exec.pending = True
        for i1 in order_arr:
            i1.execute(order.client_id)
            if order.direction == order.SELL:
                self.buy.remove_order_from_node(i1.price, i1)
            else:
                self.sell.remove_order_from_node(i1.price, i1)
            print(tree + " CtrExe prc: " + str(i1.price) + " qnt: " + str(i1.qty))
        if partial_exec is not None:
            partial_exec.execute(order.client_id, qty=qnt - sum_qnt)
            print("Part " + tree + " CtrExe prc: " + str(partial_exec.price) + " qnt: " + str(qnt - sum_qnt))
        elif order.o_type == order.LIMIT:
            order_ost = Order(order.client_id, order.parr_A, order.parr_B, order.direction, order.tif, order.o_type,
                          qnt - sum_qnt, order.price, order.timestamp)
            if sum_qnt != 0:
                print("NewOrder: " + tree + " pr:" + str(order_ost.price) + " qnt:" + str(order_ost.qty))
            self.add_order(order_ost.price, order_ost)
            self.order_id += 1
