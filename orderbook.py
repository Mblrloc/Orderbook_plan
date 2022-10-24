import logging

import blockchain
import red_black_tree


class Orderbook:

    def __init__(self):
        self.blockchain = blockchain.Blockchain()
        self.sell = red_black_tree.RBTree()
        self.buy = red_black_tree.RBTree()

    def create_order(self, order):
        if order.direction == order.BUY:
            tree = self.buy
        else:
            tree = self.sell
        key = order.price
        if ~tree.is_in_tree(key):
            tree.insertNode(key)
        tree.get_node(key).add_order(order.client_id, order)

    def remove_order(self, order):
        if order.direction == order.BUY:
            tree = self.buy
        else:
            tree = self.sell
        key = order.price
        if tree.is_in_tree(key):
            tree.delete_node(key)
        else:
            logging.error("Trying to delete non existing node")
