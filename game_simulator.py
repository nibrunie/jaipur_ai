import random

class JaipurCard:
    @property
    def is_camel(self):
        return isinstance(self, Camel)

class JaipurGoods:
    def __init__(self, name, card_num, reward_list):
        self.name = name
        self.card_num = card_num
        self.reward_list = reward_list

JaipurGold = JaipurGoods("gold", 5, [7, 7, 5, 5, 5, 4])
JaipurSilver = JaipurGoods("silver", 7, [6, 6, 5, 5, 4, 4])
JaipurJewelry = JaipurGoods("jewelery", 6, [7, 6, 5, 5, 5, 4])
JaipurSilk = JaipurGoods("silk", 9, [5, 4, 4, 4, 3, 3])
JaipurSpice = JaipurGoods("spice", 10, [5, 4, 4, 3, 3, 2])
JaipurLeather = JaipurGoods("leather", 12, [4, 3, 3, 3, 2, 2])

class Camel(JaipurCard):
    def __str__(self):
        return "[Camel]"
    def __repr__(self):
        return "[Camel]"
class GoodsCard(JaipurCard):
    def __init__(self, goods_type):
        self.goods_type = goods_type
    def __str__(self):
        return "[{}]".format(self.goods_type.name)
    def __repr__(self):
        return "[{}]".format(self.goods_type.name)
class Token:
    def __init__(self, token_type, token_value):
        self.token_type = token_type
        self.token_value = token_value

    def __str__(self):
        return "<{}>".format(self.token_value)
    def __repr__(self):
        return "<{}>".format(self.token_value)

class JaipurGame:
    def __init__(self, goods_list, camel_num, init_market_camel=2):
        self.goods_list = goods_list
        self.camel_num = camel_num
        self.init_market_camel = init_market_camel

        self.tokens = {}
        self.stack = []

        # player hands
        self.player_hands = [], []
        self.player_camels = [], []
        # market
        self.market = []

    def init_game(self):
        # initializing card stack and tokens
        self.stack = [Camel() for i in range(self.camel_num - self.init_market_camel)]
        for goods in self.goods_list:
            self.stack += [GoodsCard(goods) for i in range(goods.card_num)]
            self.tokens[goods] = [Token(goods, value) for value in goods.reward_list]

        # shuffle stack
        random.shuffle(self.stack)

        # market
        self.market = [Camel() for i in range(self.init_market_camel)]
        INIT_MARKET_SIZE = 5
        for i in range(INIT_MARKET_SIZE - self.init_market_camel):
            self.market.append(self.stack.pop(0))

        INIT_PLAYER_SIZE = 5
        # player hands
        for i in range(INIT_PLAYER_SIZE):
            self.draw_card_for_player(0)
            self.draw_card_for_player(1)

    def draw_card_for_player(self, player_id):
        assert player_id in [0, 1]
        new_card = self.stack.pop(0)
        if new_card.is_camel:
            self.player_camels[player_id].append(new_card)
        else:
            self.player_hands[player_id].append(new_card)

    def display_state(self):
        print("{} card(s) in stack".format(len(self.stack)))
        print("Market: {}".format(self.market))
        print("Player0: {}".format(self.player_camels[0]))
        print("         {}".format(self.player_hands[0]))
        print("Player1: {}".format(self.player_camels[1]))
        print("         {}".format(self.player_hands[1]))
        for goods in self.goods_list:
            print("{:10}  {}".format("{}:".format(goods.name), self.tokens[goods]))




if __name__ == "__main__":
    game = JaipurGame(
        [JaipurGold, JaipurSilver, JaipurJewelry, JaipurSilk, JaipurSpice, JaipurLeather],
        20
    )

    game.init_game()
    game.display_state()
