import random
from itertools import combinations


class Card:
    """
    класс карты с параметрами номера и масти
    """

    def __init__(self, number=' ', suit=' '):
        self.number = number
        self.suit = suit
        ratings = {' ': 0, 'A': 14, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11,
                   'Q': 12, 'K': 13}
        self.intnum = ratings[number]
        self.ratings = ratings

    def __str__(self):
        return f'{self.number}{self.suit}'

    def __gt__(self, other):
        return self.intnum < other

    def __lt__(self, other):
        return self.intnum > other

    def __ge__(self, other):
        return self.intnum <= other

    def __le__(self, other):
        return self.intnum >= other

    def __eq__(self, other):
        return self.number == other.number and self.suit == other.suit

    def __ne__(self, other):
        return self.number != other.number or self.suit != other.suit


class Deck:
    """
    класс колоды, пока по сути список
    """
    numbers = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = ['♡', '♢', '♤', '♧']
    list = [Card()] * 52
    count = 0
    for suit in range(4):
        for num in range(13):
            list[count] = Card(numbers[num], suits[suit])
            count += 1

    def __getitem__(self, item):
        return self.list[item]

    def __setitem__(self, key, value):
        self.list[key] = value

    def mix(self):
        """
        перемешивает колоду
        """
        new_deck = list(self.list)
        new_deck.append('')
        for count in range(52):
            num = random.randint(0, 51 - count)
            self.list[count] = new_deck[num]
            new_deck.pop(num)


class Player:
    def __init__(self, chips: int, cards=Card(), bid=0):
        self.chips = chips
        self.cards = cards
        self.bid = bid

    def __str__(self):
        return f'{self.chips} {str(self.cards)} {self.bid}'

def correct_bid(bid: int, i: int, players: list):
    """
    проверяет ставку на корректность,
    ставка должна быть меньше баланса самого бедного игрока,
    в случае некорректной ставки просит сделать новую
    """
    min_chips = players[0].chips
    for j in range(len(players)):
        if min_chips > players[j].chips:
            min_chips = players[j].chips
    if bid == 'pass':
        return 'pass'
    if int(bid) <= min_chips:
        return bid
    bid = input('Не коррекстная ставка, введите новую: ')
    if bid != 'pass':
        bid = int(bid)
    return correct_bid(bid, i, players)


def same_rate(players: list):
    """
    проверяет, что ставки всех оставшихся игроков равны между собой
    """
    no_pass = []
    for i in range(len(players)):
        if players[i].bid != 'pass':
            no_pass.append(players[i].bid)
    for i in range(1, len(no_pass)):
        if no_pass[i] != no_pass[i - 1]:
            return False
    return True


def collecting_bids(bank: int, players_on_bids: list):
    """
    собирает ставки игроков на текущем кону
    """
    a = True
    while a:
        for i in range(len(players_on_bids)):
            if players_on_bids[i].bid == 'pass':
                continue
            bid = input(f'Игрок {i + 1} какова ваша ставка?  ')
            if bid != 'pass':
                bid = int(bid)
            bid = correct_bid(bid, i, players_on_bids)
            players_on_bids[i].bid = bid
        a = not (same_rate(players_on_bids))
    for i in range(len(players_on_bids)):
        if players_on_bids[i].bid != 'pass':
            bank += players_on_bids[i].bid
            players_on_bids[i].chips -= players_on_bids[i].bid
    return bank, players_on_bids


def inform(bank: int, players_on_info: list):
    """
    выводит информацию (банк и фишки каждого из игроков)
    """
    print('Банк:', bank)
    for i in range(len(players_on_info)):
        print(f'Игрок {i + 1} ваш баланс:', players_on_info[i].chips)


def game(deck: Deck, players: list):
    """
    запускает 1 кон игры
    """
    bank = count = 0
    deck.mix()
    inform(bank, players)
    table = [Card()] * 5
    print('-' * 57)
    for i in range(len(players)):
        print(f'Игрок {i + 1} ваши карты: {deck[count]} {deck[count+1]}')
        players[i].cards = deck[count], deck[count + 1]
        count += 2
    print('-' * 57)
    print('Префлоп:')
    bank, players = collecting_bids(bank, players)
    print('-' * 57)
    inform(bank, players)
    print('-' * 57)
    print('-' * 57)
    print('Флоп:', end=' ')
    for i in range(1, 4):
        print(deck[count], end=' ')
        table[count - len(players) * 2] = deck[count]
        count += 1
    print()
    bank, players = collecting_bids(bank, players)
    print('-' * 57)
    inform(bank, players)
    print('-' * 57)
    print('-' * 57)
    print(f'Тёрн: {deck[count]}')
    table[count - len(players) * 2] = deck[count]
    count += 1
    print()
    bank, players = collecting_bids(bank, players)
    print('-' * 57)
    inform(bank, players)
    print('-' * 57)
    print('-' * 57)
    print(f'Ривер: {deck[count]}')
    table[count - len(players) * 2] = deck[count]
    count += 1
    print()
    bank, players = collecting_bids(bank, players)
    print('-' * 57)
    inform(bank, players)
    print('-' * 57)
    print('-' * 57)
    winner = who_win(players, table)
    players[winner - 1].chips += bank
    return players


def do_combinations(table: list, player_cards:list):
    all_cards = table + player_cards
    combs = [['']*5]*21
    i = 0
    for comb in combinations(all_cards, 5):
        combs[i] = list(comb)
        i += 1
    return combs


def do_straight(card: Card):
    if card.intnum > 10:  # не может быть 5 тузов
        return False
    straight = []
    for num in range(card.intnum, card.intnum + 5):
        straight.append(num)
    return straight


def is_straight(cards: list):
    cards.sort()
    straight = do_straight(cards[0])
    low_straight = [2, 3, 4, 5, 14]
    if not (straight):
        return False
    flag = True
    print(straight)
    for i in range(5):
        print(cards[i], i)
        if cards[i].intnum != straight[i]:
            flag = False
            break
    if not (flag):
        flag = True
        for i in range(5):
            if cards[i].intnum != low_straight[i]:
                flag = False
    return flag


def is_four_kind(cards):
    cards.sort()
    pass


def high_card1(cards: list):
    return max(cards)


def who_win(players: list, table: list):
    winner = int(input('Кто выиграл? '))
    return winner


def main():
    deck = Deck()
    players = int(input('Количество игроков: '))
    chip = int(input('Количество фишек: '))
    players = [Player(chip) for i in range(players)]
    players = game(deck, players)
    stop = True
    while stop:
        stop = bool(input('Завершить игру? '))
        players = game(deck, players)


if __name__ == '__main__':
    main()