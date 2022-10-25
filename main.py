import random
import matplotlib.pyplot as plt
import numpy as np
from order import Order
from blockchain import Blockchain
from orderbook import Orderbook

blockchain = Blockchain()


def print_market():
    ask_tree = orderbook.buy
    bid_tree = orderbook.sell
    # ask_tree.print_tree()
    ask = ask_tree.levels
    bid = bid_tree.levels

    # print(ask)
    # print(bid)
    ask_graph = []
    bid_graph = []

    for i1 in ask:
        ask_graph.append(ask_tree.get_node(i1).order_num)

    for i1 in bid:
        bid_graph.append(bid_tree.get_node(i1).order_num)
    # print(ask_graph)
    # print(bid_graph)
    ask_graph = np.flip(np.cumsum(np.flip(ask_graph)))
    bid_graph = np.cumsum(bid_graph)
    # print(ask_graph)
    # print(bid_graph)
    fig, axs = plt.subplots(2)
    fig.suptitle('Биржевой стакан')
    plt.subplot(2, 1, 2)
    axs[1].barh(ask, ask_graph, color="green")
    # plt.gca().invert_yaxis()
    plt.subplot(2, 1, 1)
    axs[0].barh(bid, bid_graph, color="red")
    plt.show()


def create_user(name, currency1, qnt1, currency2, qnt2):
    blockchain.register_user(name)
    blockchain.change_balance(name, currency1, qnt1, mode=blockchain.INCREASE)
    blockchain.change_balance(name, currency2, qnt2, mode=blockchain.INCREASE)


orderbook = Orderbook()
for i1 in range(100):
    create_user(str(i1), "ETH", 1000, "USDT", 1000)

for i1 in range(50):
    order = Order(str(i1), parr_A="ETH", parr_B="USDT", direction=Order.BUY,
                  tif=Order.GTC, o_type=Order.MARKET, qty=int(random.uniform(10, 100)),
                  price=int(random.uniform(57, 70)), timestamp=0)
    orderbook.create_order(order)

for i1 in range(50):
    order = Order(str(i1 + 50), parr_A="ETH", parr_B="USDT", direction=Order.SELL,
                  tif=Order.GTC, o_type=Order.MARKET, qty=int(random.uniform(10, 100)),
                  price=int(random.uniform(70, 83)), timestamp=0)
    orderbook.create_order(order)

print_market()

order = Order("Test1", parr_A="ETH", parr_B="USDT", direction=Order.BUY,
              tif=Order.GTC, o_type=Order.MARKET, qty=1000,
              price=65, timestamp=0)
orderbook.create_order(order)

print_market()
