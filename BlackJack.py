import random

# Card suits, ranks and values

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

playing = True

# Card class is defined here


class Card:

    def __init__(self, suit, rank):  # Setting the cards
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit


# Deck class is defined here

class Deck:

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))  # Adding cards to the deck

    def __str__(self):
        deck_string = ''
        for card in self.deck:
            deck_string += '\n '+card.__str__()  # Adding cards in string format
        return 'The deck has:' + deck_string

    def shuffle(self):          # shuffle function will shuffle the whole deck
        random.shuffle(self.deck)

    def deal(self):             # deal function will take one card from the deck
        single_card = self.deck.pop()
        return single_card


# Hand class is defined here

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0    # Aces can be 1 or 11, so we need to track them

# Adding cards

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]

# Ace can either be 1 or 11

    def adjust_for_ace(self):
        while self.value > 21 and self.aces: # If it's over 21 and there's an Ace
            self.value -= 10
            self.aces -= 1


# Chips for betting


class Chips:

    def __init__(self):
        self.total = 100  # This can be changed
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


# Betting is defined here
def bet(chips):

    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except ValueError:
            print('Sorry, a bet must be an integer!')
        else:
            if chips.bet > chips.total:
                print("Sorry, your bet can't exceed",chips.total)
            else:
                break

# Hit function


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

# Hit and Stand choice function


def hit_or_stand(deck, hand):
    global playing

    while True:
        x = input("Would you like to Hit or Stand? Enter 'h' or 's' ")
        # Hit and Stand choice
        if x.lower() == 'h':
            hit(deck, hand)

        elif x.lower() == 's':
            print("Player stands. Dealer is playing.")
            playing = False

        else:
            print("Sorry, please try again.")
            continue
        break


# functions to display cards

def show_cards(player, dealer):
    print("\nDealer's Hand:")
    print("<< Card hidden >>")
    print('',dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')


def show_all(player,dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)


# Game outcomes

def player_busts(player,dealer,chips):
    print("Player busts!")
    chips.lose_bet()


def player_wins(player,dealer,chips):
    print("Player wins!")
    chips.win_bet()


def dealer_busts(player,dealer,chips):
    print("Dealer busts!")
    chips.win_bet()


def dealer_wins(player,dealer,chips):
    print("Dealer wins!")
    chips.lose_bet()


def push(player,dealer):
    print("Dealer and Player tie! It's a push.")


while True:

    print("Welcome to BLACKJACK!")

    # Shuffle the deck
    deck = Deck()
    deck.shuffle()

    player_hand = Hand() # Two cards for the player
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand() # Two cards for the dealer
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Set up the Player's chips
    player_chips = Chips()

    # Prompt the user for bet
    bet(player_chips)

    # Cards will be shown but the dealer one is hidden
    show_cards(player_hand, dealer_hand)

    while playing:

        # Prompt for hit/stand
        hit_or_stand(deck, player_hand)

        show_cards(player_hand, dealer_hand)

        # Player will lose if it goes over 21
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

    # Dealer needs to be over 17
    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        # Show all cards including the hidden dealer card
        show_all(player_hand, dealer_hand)

        # Ending scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)

        else:
            push(player_hand,dealer_hand)
    # One scenario is missing. it's that if the player hits a blackjack (Ace and Jack)

    # Inform Player of their chips total
    print("\nPlayer's winnings stand at", player_chips.total)

    # Ask to play again
    new_game = input("Would you like to play another hand?(y/n) ")

    if new_game.lower()=='y':
        playing=True
        continue
    else:
        print("Thanks for playing!")
        break
