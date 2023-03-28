import random
import time

class card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
    def __str__(self):
        return (self.value + " of " + self.suit)

class deck:
    def __init__(self):
        self.cards = []
        self.build()
    def build(self):
        for s in ["Spades", "Clubs", "Diamonds", "Hearts"]:
            for v in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]:
                self.cards.append(card(s, v))
    def show(self):
        for c in self.cards:
            print(c)
    def shuffle(self):
        for i in range(len(self.cards)-1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]
    def drawCard(self):
        return self.cards.pop()
    
class player:
    def __init__(self, name):
        self.name = name
        self.hand = []
    def draw(self, deck):
        self.hand.append(deck.drawCard())
        return self
    def showHand(self):
        print(self.name + "'s hand:")
        for card in self.hand:
            print(card)
    def discard(self):
        return self.hand.pop()
    def handValue(self):
        value = 0
        for card in self.hand:
            if card.value == "Ace":
                value += 11
            elif card.value in ["Jack", "Queen", "King"]:
                value += 10
            else:
                value += int(card.value)
        for card in self.hand:
            if value > 21 and card.value == "Ace":
                value -= 10
        return value

class dealer(player):
    def __init__(self, name):
        self.name = name
        self.hand = []
    def showFirstCard(self):
        print("Dealer's first card:")
        print(self.hand[0])

class bankAccount:
    def __init__(self, balance):
        self.balance = balance
    def roundToDollar(self):
        self.balance = round(self.balance)
        return self
    def deposit(self, amount):
        self.balance += amount
        self.roundToDollar()
        return self
    def withdraw(self, amount):
        if self.balance - amount < 0:
            print("Insufficient funds")
            return False
        else:
            self.balance -= amount
            self.roundToDollar()
            return True
        return self
    def displayAccountInfo(self):
        print("Balance: $" + str(self.balance))
    def yieldInterest(self):
        if self.balance > 0:
            self.balance *= 1.01
            self.roundToDollar()
        return self

    
    
class game:
    """Blackjack game"""
    def __init__(self):
        self.playerBalance = bankAccount(100)
        self.delay = 1
    def play(self):
        self.deck = deck()
        self.deck.shuffle()
        self.player = player("Player")
        self.dealer = dealer("Dealer")
        print("Welcome to Blackjack!")
        self.playerBalance.displayAccountInfo()
        bet = int(input("How much do you want to bet? "))
        if self.playerBalance.withdraw(bet):
            self.player.draw(self.deck).draw(self.deck)
            self.dealer.draw(self.deck).draw(self.deck)
            self.playerBalance.displayAccountInfo()
            time.sleep(self.delay)
            self.player.showHand()
            time.sleep(self.delay)
            self.dealer.showFirstCard()
            time.sleep(self.delay)
            while True:
                choice = input("Do you want to hit or stay? ")
                if choice == "hit":
                    self.player.draw(self.deck)
                    self.player.showHand()
                    time.sleep(self.delay)
                    if self.player.handValue() > 21:
                        print("You lose!")
                        time.sleep(self.delay)
                        break
                elif choice == "stay":
                    while self.dealer.handValue() < 17:
                        self.dealer.draw(self.deck)
                    self.dealer.showHand()
                    time.sleep(self.delay)
                    if self.dealer.handValue() > 21:
                        print("You win!")
                        time.sleep(self.delay)
                        self.playerBalance.deposit(bet * 2)
                        break
                    elif self.dealer.handValue() > self.player.handValue():
                        print("You lose!")
                        time.sleep(self.delay)
                        break
                    elif self.dealer.handValue() < self.player.handValue():
                        print("You win!")
                        time.sleep(self.delay)
                        self.playerBalance.deposit(bet * 2)
                        break
                    else:
                        print("It's a tie!")
                        time.sleep(self.delay)
                        self.playerBalance.deposit(bet)
                        break
                else:
                    print("Please enter hit or stay.")
            self.playerBalance.yieldInterest()
            self.playerBalance.displayAccountInfo()
            time.sleep(self.delay)
        else:
            print("You don't have enough money to bet that much.")
if __name__ == "__main__":
    game = game()
    while True:
        choice = input("Do you want to play again? ")
        if choice == "yes":
            game.play()
        elif choice == "no":
            print("Thanks for playing!")
            break
        else:
            print("Please enter yes or no.")