"""
War Card Game
A simple two-player card game where players reveal cards and the highest card wins.
"""

import random
from collections import deque


class Card:
    """Represents a single playing card."""
    
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    RANK_VALUES = {rank: value for value, rank in enumerate(RANKS)}
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def value(self):
        """Return the numeric value of the card."""
        return self.RANK_VALUES[self.rank]
    
    def __repr__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    """Represents a deck of playing cards."""
    
    def __init__(self):
        self.cards = deque()
        self._create_deck()
    
    def _create_deck(self):
        """Create a standard 52-card deck."""
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                self.cards.append(Card(suit, rank))
    
    def shuffle(self):
        """Shuffle the deck."""
        cards_list = list(self.cards)
        random.shuffle(cards_list)
        self.cards = deque(cards_list)
    
    def draw(self):
        """Draw a card from the deck."""
        return self.cards.popleft() if self.cards else None
    
    def add_to_bottom(self, card):
        """Add a card to the bottom of the deck."""
        self.cards.append(card)
    
    def __len__(self):
        return len(self.cards)


class Player:
    """Represents a player in the War card game."""
    
    def __init__(self, name):
        self.name = name
        self.deck = Deck()
    
    def play_card(self):
        """Play the top card from the player's deck."""
        return self.deck.draw()
    
    def add_cards(self, cards):
        """Add cards to the bottom of the player's deck."""
        for card in cards:
            self.deck.add_to_bottom(card)
    
    def has_cards(self):
        """Check if the player has cards left."""
        return len(self.deck) > 0
    
    def card_count(self):
        """Return the number of cards in the player's deck."""
        return len(self.deck)


class WarGame:
    """Manages the War card game."""
    
    def __init__(self, player1_name="Player 1", player2_name="Player 2"):
        self.player1 = Player(player1_name)
        self.player2 = Player(player2_name)
        self.round_count = 0
        self.war_count = 0
        self.max_rounds = 1000  # Prevent infinite loops
    
    def deal_cards(self):
        """Deal all cards to both players."""
        main_deck = Deck()
        main_deck.shuffle()
        
        while len(main_deck) > 0:
            self.player1.add_cards([main_deck.draw()])
            self.player2.add_cards([main_deck.draw()])
    
    def play_round(self):
        """Play a single round of War."""
        if not self.player1.has_cards() or not self.player2.has_cards():
            return False
        
        self.round_count += 1
        table_cards_p1 = []
        table_cards_p2 = []
        
        # Keep playing until someone wins the round (handles multiple wars)
        while True:
            # Draw cards for the round
            card1 = self.player1.play_card()
            card2 = self.player2.play_card()
            
            if not card1 or not card2:
                # Someone ran out of cards during the round
                return False
            
            table_cards_p1.append(card1)
            table_cards_p2.append(card2)
            
            print(f"  Round {self.round_count}: {self.player1.name} plays {card1} | {self.player2.name} plays {card2}")
            
            # Compare card values
            if card1.value() > card2.value():
                print(f"  → {self.player1.name} wins the round!")
                self.player1.add_cards(table_cards_p1 + table_cards_p2)
                return True
            elif card2.value() > card1.value():
                print(f"  → {self.player2.name} wins the round!")
                self.player2.add_cards(table_cards_p1 + table_cards_p2)
                return True
            else:
                # It's a tie - "War!" Play 3 face-down cards and 1 face-up
                self.war_count += 1
                print(f"  → WAR! Cards are tied. Each player plays 3 face-down cards...\n")
                
                # Each player plays 3 face-down cards
                for i in range(1, 4):
                    card1 = self.player1.play_card()
                    card2 = self.player2.play_card()
                    
                    if not card1 or not card2:
                        # Someone ran out of cards during war
                        return False
                    
                    table_cards_p1.append(card1)
                    table_cards_p2.append(card2)
                    print(f"    Face-down card {i}: {self.player1.name} | {self.player2.name}")
                
                # Loop continues to draw and compare the next face-up cards
                print()  # Blank line for readability
    
    def play_game(self):
        """Play the entire game until someone wins."""
        print(f"\n{'='*60}")
        print(f"Welcome to War Card Game!")
        print(f"Players: {self.player1.name} vs {self.player2.name}")
        print(f"{'='*60}\n")
        
        self.deal_cards()
        print(f"Cards dealt: {self.player1.name} has {self.player1.card_count()} cards, "
              f"{self.player2.name} has {self.player2.card_count()} cards.\n")
        
        while self.round_count < self.max_rounds:
            if not self.player1.has_cards():
                print(f"\n{'='*60}")
                print(f"🎉 {self.player2.name} wins the game!")
                print(f"Game lasted {self.round_count} rounds with {self.war_count} wars")
                print(f"{'='*60}\n")
                return self.player2.name
            
            if not self.player2.has_cards():
                print(f"\n{'='*60}")
                print(f"🎉 {self.player1.name} wins the game!")
                print(f"Game lasted {self.round_count} rounds with {self.war_count} wars")
                print(f"{'='*60}\n")
                return self.player1.name
            
            self.play_round()
            
            # Print status every 10 rounds
            if self.round_count % 10 == 0:
                print(f"[After {self.round_count} rounds] "
                      f"{self.player1.name}: {self.player1.card_count()} cards | "
                      f"{self.player2.name}: {self.player2.card_count()} cards\n")
        
        print(f"\n{'='*60}")
        print(f"Game ended after {self.max_rounds} rounds (likely a draw)")
        print(f"Total wars that occurred: {self.war_count}")
        print(f"{'='*60}\n")
        return None


def main():
    """Main function to run the game."""
    print("\nWelcome to War Card Game!\n")
    
    p1_name = input("Enter Player 1 name (default: Player 1): ").strip() or "Player 1"
    p2_name = input("Enter Player 2 name (default: Player 2): ").strip() or "Player 2"
    
    game = WarGame(p1_name, p2_name)
    game.play_game()


if __name__ == "__main__":
    main()
