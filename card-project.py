import random

# Card values and suits (using Unicode symbols for bonus point)
values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
suits = ["\u2665", "\u2660", "\u2663", "\u2666"]

# Card class represents a single playing card
class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        # Give each card a numeric value for easy comparison
        if value == "A":
            self.numeric_value = 14
        elif value == "K":
            self.numeric_value = 13
        elif value == "Q":
            self.numeric_value = 12
        elif value == "J":
            self.numeric_value = 11
        else:
            self.numeric_value = int(value)

    def __repr__(self):
        return f"{self.value}{self.suit}"

# Deck class creates and manages a full 52-card deck
class Deck:
    def __init__(self):
        # Create a list of all card combinations
        self.cards = [Card(v, s) for s in suits for v in values]

    def shuffle(self):
        # Shuffle the deck randomly
        random.shuffle(self.cards)

    def deal(self):
        # Deal (pop) one card from the top of the deck
        return self.cards.pop() if self.cards else None

# Hand class stores and manages a player's cards
class Hand:
    def __init__(self, owner):
        self.owner = owner
        self.cards = []

    def add_card(self, card):
        # Add single or multiple cards to player's hand
        if isinstance(card, list):
            self.cards.extend(card)
        else:
            self.cards.append(card)

    def play_card(self):
        # Play (remove) the top card from hand
        return self.cards.pop(0) if self.cards else None

    def size(self):
        # Return number of cards left in hand
        return len(self.cards)

# --- Game setup ---
print("Welcome to WAR!")
p1_name = input("Enter Player 1's name: ")
p2_name = input("Enter Player 2's name: ")

deck = Deck()
deck.shuffle()

# Create hands for both players
p1 = Hand(p1_name)
p2 = Hand(p2_name)

# Deal 26 cards to each player
for i in range(26):
    p1.add_card(deck.deal())
    p2.add_card(deck.deal())

round_num = 0

# --- Main Game Loop ---
while p1.size() > 0 and p2.size() > 0:
    round_num += 1
    input(f"\nPress Enter for Round {round_num}: ")
    
    # round limit so no infinite matches
    if round_num > 250:
        print("\nGame reached 250 rounds — it's a draw!")
        exit()

    # Each player flips one card
    c1 = p1.play_card()
    c2 = p2.play_card()

    print(f"{p1_name} plays {c1}  |  {p2_name} plays {c2}")

    # Cards go into a pile for the winner
    pile = [c1, c2]

    # Compare card values
    if c1.numeric_value > c2.numeric_value:
        p1.add_card(pile)
        print(f"{p1_name} wins the round!")
    elif c2.numeric_value > c1.numeric_value:
        p2.add_card(pile)
        print(f"{p2_name} wins the round!")
    else:
        # Handle WAR (tie)
        print("WAR!")
        while True:
            # Check if players have enough cards to continue
            if p1.size() < 4:
                print(f"{p1_name} doesn't have enough cards. {p2_name} wins the game!")
                exit()
            elif p2.size() < 4:
                print(f"{p2_name} doesn't have enough cards. {p1_name} wins the game!")
                exit()
            
            # Each player puts down 3 face-down and 1 face-up card
            pile += [p1.play_card() for _ in range(3)]
            pile += [p2.play_card() for _ in range(3)]

            c1 = p1.play_card()
            c2 = p2.play_card()
            pile += [c1, c2]
            print(f"War cards: {p1_name} plays {c1} | {p2_name} plays {c2}")

            # Compare new cards
            if c1.numeric_value > c2.numeric_value:
                p1.add_card(pile)
                print(f"{p1_name} wins the war!")
                break
            elif c2.numeric_value > c1.numeric_value:
                p2.add_card(pile)
                print(f"{p2_name} wins the war!")
                break
            else:
                print("Another WAR!")  # If tie again, repeat
                continue
# --- Game Over ---

if p1.size() > p2.size():
    print(f"\n{p1_name} wins the game!")
elif p2.size() > p1.size():
    print(f"\n{p2_name} wins the game!")
else:
    print("\nIt's a tie!")
