import random

class JaipurCard:
    @property
    def is_camel(self):
        return isinstance(self, Camel)

    @property
    def is_goods(self):
        return isinstance(self, GoodsCard)

class JaipurGoods:
    def __init__(self, name, card_num, reward_list, minimum_sell_number=None):
        self.name = name
        self.card_num = card_num
        self.reward_list = reward_list
        self.minimum_sell_number = minimum_sell_number

JaipurGold = JaipurGoods("gold", 6, [7, 7, 5, 5, 5, 4], 2)
JaipurSilver = JaipurGoods("silver", 6, [6, 6, 5, 5, 4, 4], 2)
JaipurDiamonds = JaipurGoods("diamond", 6, [7, 6, 5, 5, 5, 4], 2)
JaipurSilk = JaipurGoods("silk", 8, [5, 4, 4, 4, 3, 3])
JaipurSpice = JaipurGoods("spice", 8, [5, 4, 4, 3, 3, 2])
JaipurLeather = JaipurGoods("leather", 10, [4, 3, 3, 3, 2, 2])

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

class TokenBonusType:
    pass

class Token:
    def __init__(self, token_type, token_value):
        self.token_type = token_type
        self.token_value = token_value

    def __str__(self):
        return "<{}>".format(self.token_value)
    def __repr__(self):
        return "<{}>".format(self.token_value)

class JaipurActionType:
    @property
    def is_take_all_camels(self):
        return False
    @property
    def is_take_one_goods(self):
        return False
    @property
    def is_exchange_goods(self):
        return False
    @property
    def is_sell_goods(self):
        return False

class TakeAllCamels(JaipurActionType):
    def __init__(self):
        pass
    @property
    def is_take_all_camels(self):
        return True
    def __repr__(self):
        return "(TakeAllCamels)"
    def __str__(self):
        return self.__repr__()

class SellGoods(JaipurActionType):
    def __init__(self, list_good_to_sell):
        self.list_good_to_sell = list_good_to_sell
    @property
    def is_sell_goods(self):
        return True
    def __repr__(self):
        return "(SellGoods:{}->)".format(self.list_good_to_sell)
    def __str__(self):
        return self.__repr__()

class ExchangeGoods(JaipurActionType):
    def __init__(self, player_exchg_goods, market_exchg_goods):
        self.player_exchg_goods = player_exchg_goods
        self.market_exchg_goods = market_exchg_goods
    @property
    def is_exchange_goods(self):
        return True
    def __repr__(self):
        return "(ExchangeGoods:{}<->{})".format(self.player_exchg_goods, self.market_exchg_goods)
    def __str__(self):
        return self.__repr__()

class TakeOneGoods(JaipurActionType):
    def __init__(self, market_goods):
        self.market_goods = market_goods
    @property
    def is_take_one_goods(self):
        return True
    def __repr__(self):
        return "(TakeOneGoods:{})".format(self.market_goods)
    def __str__(self):
        return self.__repr__()


class JaipurBoard:
    def __init__(self, goods_list, camel_num, init_market_camel=2):
        self.goods_list = goods_list
        self.camel_num = camel_num
        self.init_market_camel = init_market_camel

        self.tokens = {}
        self.bonus_tokens = {}
        self.stack = []

        # player hands
        self.player_hands = [], []
        self.player_camels = [], []

        self.player_tokens = set(), set()
        # market
        self.market = []

    def init_game(self):
        # initializing card stack and tokens
        self.stack = [Camel() for i in range(self.camel_num - self.init_market_camel)]
        for goods in self.goods_list:
            self.stack += [GoodsCard(goods) for i in range(goods.card_num)]
            self.tokens[goods] = [Token(goods, value) for value in goods.reward_list]

        # generating bonus tokens
        for goods_num in [3, 4, 5]:
            self.bonus_tokens[goods_num] = [Token(TokenBonusType, random.randrange(goods_num, goods_num * 2 + 1))]

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

    def game_end_state(self):
        return (len(gt for gt in tokens if not self.tokens[gt]) >= 3) or not len(self.stack)

    def display_state(self):
        print("{} card(s) in stack".format(len(self.stack)))
        print("Market: {}".format(self.market))
        print("Player0: {}".format(self.player_camels[0]))
        print("         {}".format(self.player_hands[0]))
        print("Player1: {}".format(self.player_camels[1]))
        print("         {}".format(self.player_hands[1]))
        for goods in self.goods_list:
            print("{:10}  {}".format("{}:".format(goods.name), self.tokens[goods]))

    def is_action_valid(self, player_id, action):
        """ Check if an action can be played by the given player """
        if action.is_take_all_camels:
            # check if there is at least one camel in the market
            return any(c.is_camel for c in self.market)

        elif action.is_take_one_goods:
            return action.market_goods in self.market

        elif action.is_sell_goods:
            goods_type = action.list_good_to_sell[0].goods_type
            same_goods_type = all(c.goods_type == goods_type for c in action.list_good_to_sell)
            goods_in_player_hands = all(c in self.player_hands[player_id] for c in action.list_good_to_sell)
            goods_sell_num = len(action.list_good_to_sell)
            goods_constraint = True if goods_type.minimum_sell_number is None else goods_sell_num >= goods_type.minimum_sell_number

            # FIXME: implement goods constraints (e.g. not able to sell less
            # than 2 rare goods)
            return same_goods_type and goods_in_player_hands and goods_constraint

        elif action.is_exchange_goods:
            goods_in_player_hands = all(c in self.player_hands[player_id] for c in action.player_exchg_goods if not c.is_camel)
            camel_in_player_possession = all(c in self.player_camels[player_id] for c in action.player_exchg_goods if c.is_camel)
            target_goods_in_market = all((c in self.market and not c.is_camel) for c in action.market_exchg_goods)
            return goods_in_player_hands and camel_in_player_possession and target_goods_in_market

        else:
            raise NotImplementedError

    def get_token_rewards(self, goods_type, goods_num):
        # preparing awarded goods token
        remaining_goods_token_num = len(self.tokens[goods_type])
        awarded_goods_token_num = min(remaining_goods_token_num, goods_num)
        goods_token = [self.tokens[goods_type].pop(0) for i in range(awarded_goods_token_num)]
        tokens = goods_token
        # preparing bonus token
        if goods_num in self.bonus_tokens and len(self.bonus_tokens[goods_num]):
            bonus_token = self.bonus_token[goods_num].pop(0)
            tokens.append(bonus_token)
        return tokens

    def execute_action(self, player_id, action):
        if action.is_take_all_camels:
            camel_cards = [c for c in self.market if c.is_camel]
            self.market = [c for c in self.market if not c.is_camel]
            self.player_camels[player_id].extend(camel_cards)
            # replacing camels by stack cards
            while len(self.market) < 5:
                self.market.append(self.stack.pop(0))

        elif action.is_take_one_goods:
            goods_card = action.market_goods
            self.market.remove(goods_card)
            self.player_hands[player_id].append(goods_card)
            # replacing good by stack card
            self.market.append(self.stack.pop(0))

        elif action.is_sell_goods:
            # removing sold goods from player hands
            for card in action.list_good_to_sell:
                self.player_hands[player_id].remove(card)

            goods_type = action.list_good_to_sell[0].goods_type
            goods_num = len(action.list_good_to_sell)

            # rewarding tokens
            self.player_tokens[player_id].update(self.get_token_rewards(goods_type, goods_num))

        elif action.is_exchange_goods:
            # removing exchanged goods from player hands
            for card in action.player_exchg_goods:
                if card.is_camel:
                    self.player_camels[player_id].remove(card)
                else:
                    self.player_hands[player_id].remove(card)
            # removing exchanged goods from market
            for card in action.market_exchg_goods:
                self.market.remove(card)

            self.market += action.player_exchg_goods
            self.player_hands[player_id].extend(action.market_exchg_goods)

        else:
            raise NotImplementedError

    def get_player_cards(self, player_id):
        return self.player_hands[player_id]
    def get_player_camels(self, player_id):
        return self.player_camels[player_id]


class JaipurPlayer:
    def __init__(self, player_id):
        self.player_id = player_id

    def select_action(self, game_object):
        raise NotImplementedError

class RandomPlayer(JaipurPlayer):
    def select_action(self, game_object):
        return self.random_action(game_object)

    def random_action(self, game_object):
        possible_list = []
        player_cards = game_object.get_player_cards(self.player_id)
        player_camels = game_object.get_player_camels(self.player_id)
        # taking all camels
        if any(c.is_camel for c in game_object.market):
            possible_list.append(TakeAllCamels())
        # selling goods
        if any(c.is_goods for c in player_cards): 
            goods_type = list(c.goods_type for c in player_cards if c.is_goods)
            random_goods = random.choice(goods_type)
            goods_list = [c for c in player_cards if (c.is_goods and c.goods_type == random_goods)]
            goods_num = random.randrange(1, len(goods_list)+1)
            goods_to_sell_list = goods_list[:goods_num]
            possible_list.append(SellGoods(goods_to_sell_list))
        # taking one goods
        if any(c.is_goods for c in game_object.market):
            random_good = random.choice(list(c for c in game_object.market if c.is_goods))
            possible_list.append(TakeOneGoods(random_good))
        # exchanging goods
        if any(c.is_goods for c in game_object.market):
            market_goods = [c for c in game_object.market if c.is_goods]
            max_exchange_num = min(len(player_cards) + len(player_camels), len(market_goods))
            if max_exchange_num > 0:
                exchange_size = random.randrange(1, max_exchange_num + 1)
                min_required_camel_num = max(0, exchange_size - len(player_cards))
                camel_num = random.randrange(min_required_camel_num, len(player_camels) + 1)
                goods_num = exchange_size - camel_num
                player_exchg_list = player_camels[:camel_num] + player_cards[:goods_num] 
                market_exchg_list = market_goods[:exchange_size] 
                possible_list.append(ExchangeGoods(player_exchg_list, market_exchg_list))

        return random.choice(possible_list)
        

class JaipurGame:
    def __init__(self, player0, player1):
        INIT_CAMEL_NUM = 11
        self.game_object = JaipurBoard(
            [JaipurGold, JaipurSilver, JaipurDiamonds, JaipurSilk, JaipurSpice, JaipurLeather],
            INIT_CAMEL_NUM
        )
        self.players = player0, player1
        self.game_object.init_game()

    def play_one_turn(self):
        print("player0's action")
        player0_action = self.players[0].select_action(self.game_object)
        print("  action is {}".format(player0_action))
        if not self.game_object.is_action_valid(0, player0_action):
            print("player0 attempted an invalid action: {}".format(player0_action))
            raise Exception()
        self.game_object.execute_action(0, player0_action)
        self.game_object.display_state()

        print("player1's action")
        player1_action = self.players[1].select_action(self.game_object)
        print("  action is {}".format(player1_action))
        if not self.game_object.is_action_valid(1, player1_action):
            print("player1 attempted an invalid action: {}".format(player1_action))
            raise Exception()
        self.game_object.execute_action(1, player1_action)
        self.game_object.display_state()
        
            

if __name__ == "__main__":
    game = JaipurGame(RandomPlayer(0), RandomPlayer(1))
    game.game_object.display_state()
    for i in range(5):
        print("playing one turn")
        game.play_one_turn()
        print("\n")
