import random
import pygame
from pygame.locals import *
import sys

class Card:
    # this class contains all attributes of a playing card
    def __init__(self, suit, color, label, value):
        self.suit = suit
        self.color = color
        self.label = label
        self.value = value

    def __str__(self):
        return f"{self.label}  {self.suit}"

    def __repr__(self):
        return self.__str__()

# Attempt to import AI and CardCounter if available
try:
    from ai_algorithm_3 import AI
    from card_counter import CardCounter
except ImportError:
    # If these are not available, define placeholders
    class CardCounter:
        def update_count(self, card_id):
            pass

    class AI:
        def __init__(self, card_class):
            pass
        def set_card_counter(self, card_counter):
            pass
        def decide_action(self, player_hand, dealer_hand, remaining_cards):
            return "stand"
        def update_outcome_in_buffer(self, outcome):
            pass
        def flush_buffer_to_csv(self, filename):
            pass


# all of our imports are listed here
pygame.init()
pygame.font.init()

screenWidth, screenHeight = 1250, 750
halfWidth, halfHeight = screenWidth / 2, screenHeight / 2

black, blue, white, orange, red , green = (0, 0, 0), (51, 235, 255), (255, 255, 255), (255, 165, 0), (255, 0, 0), (34, 139, 34)
fontType = 'Poppins'
text_Title = pygame.font.SysFont(fontType, 80)
text_Heading = pygame.font.SysFont(fontType, 60)
text_SubHeading = pygame.font.SysFont(fontType, 45)
text_Bold = pygame.font.SysFont(fontType, 30)
text_Normal = pygame.font.SysFont(fontType, 20)
text_Small = pygame.font.SysFont(fontType, 10)

# function to add text to the game when needed
def add_text(text, font, surface, x, y, text_color):
    textObject = font.render(text, False, text_color)
    textWidth = textObject.get_rect().width
    textHeight = textObject.get_rect().height
    surface.blit(textObject, (x - (textWidth / 2), y - (textHeight / 2)))


class Deck:
    # this class contains an array that acts as our 52 card deck
    def __init__(self):
        self.cards = []

    # this method simply creates a deck using the Card class above
    def createDeck(self):
        suits = ["Clover", "Spade", "Heart", "Diamond"]
        for symbol in suits:
            number = 2
            while number < 15:
                if symbol == "Clover" or symbol == "Spade":
                    suitColor = "Black"
                else:
                    suitColor = "Red"
                value = number
                if number > 10:
                    value = 10
                if number == 14:
                    value = 1
                letter = number
                if number == 11:
                    letter = "J"
                elif number == 12:
                    letter = "Q"
                elif number == 13:
                    letter = "K"
                elif number == 14:
                    letter = "A"
                newCard = Card(symbol, suitColor, letter, value)
                self.cards.append(newCard)
                number += 1

    # this method allows us to shuffle our deck so that it is randomly arranged
    def shuffleDeck(self):
        return random.shuffle(self.cards)

    # this method basically gets the top card of the deck and returns it
    def getCard(self, card_counter=None):
        topCard = self.cards[0]
        self.cards.pop(0)
        if card_counter:
            # Update the card counter with the drawn card
            # We'll use label + suit's first letter as an ID, for example "A" + "H" for Ace of Hearts
            card_id = str(topCard.label) + topCard.suit[0]
            card_counter.update_count(card_id)
        return topCard


class Dealer:
    # this class contains everything that is within the control of the dealer
    def __init__(self, card_counter=None):
        self.deck = Deck()
        self.deck.createDeck()
        self.deck.shuffleDeck()
        self.hand = []
        self.count = 0
        self.card_counter = card_counter  # Store the card_counter
        self.x = halfWidth
        self.y = 100

    # this method creates the two-card hand that the dealer starts with
    def createDealerHand(self):
        for i in range(1, 3):
            self.addCard()

    # this method uses the getCard() to deal a card to a player
    def dealCard(self):
        return self.deck.getCard(self.card_counter)

    # this method allows the dealer to deal himself a card and also account for the dealer's count
    def addCard(self):
        dealerCard = self.dealCard()
        self.hand.append(dealerCard)
        self.count += dealerCard.value
        self.countAce()

    # this method prints the dealer's hand
    def printDealerHand(self):
        print("")
        print("Dealer's Hand: ")
        for dealerCard in self.hand:
            print("Suit: " + dealerCard.suit + "\nLabel: " + str(dealerCard.label))

    # this method prints the dealer's count
    def printDealerCount(self):
        print("")
        print("Dealer's Count: " + str(self.count))

    # this method considers all aces in a dealer's hand to give them the closest count under 21
    def countAce(self):
        if self.count <= 21:
            for card in self.hand:
                if card.label == "A":
                    self.count += 10
                    if self.count > 21:
                        self.count -= 10
                        break

    # this method will draw all the cards in a hand (13 : 20 Card Dimension Ratio)
    def drawHand(self, surface):
        cardWidth, cardHeight = 78, 120
        cardGap = 20
        playerBoxLength, playerBoxHeight = cardWidth + (cardGap * (len(self.hand) - 1)), cardHeight
        playerTopLeftX = self.x - (0.5 * playerBoxLength)
        playerTopLeftY = self.y - (0.5 * playerBoxHeight)
        for c in self.hand:
            if c == self.hand[1]:
                drawCard = pygame.image.load("Resources/Cards/Back/RedBack.png")
            else:
                drawCard = pygame.image.load("Resources/Cards/" + str(c.suit) + "/" + str(c.label) + ".png")
            resizedCard = pygame.transform.scale(drawCard, (cardWidth, cardHeight))
            surface.blit(resizedCard, (playerTopLeftX, playerTopLeftY))
            pygame.display.update()
            playerTopLeftX += cardGap
        nameX = self.x
        nameY = self.y + (0.75 * cardHeight)
        add_text("DEALER", text_Normal, surface, nameX, nameY, white)
        countString1 = ""
        countString1 +=  "Count: " + str(self.hand[0].value)
        add_text(countString1, text_Normal, surface, self.x + (0.20 * playerTopLeftX), self.y - 5, orange)
        deckX = 400 - (0.5 * cardWidth)
        deckY = 100 - (0.5 * cardHeight)
        for i in range(1, 7):
            deckCard = pygame.image.load("Resources/Cards/Back/RedBack.png")
            backCard = pygame.transform.scale(deckCard, (cardWidth, cardHeight))
            surface.blit(backCard, (deckX, deckY))
            deckX += cardGap


class Player:
    # this class contains everything that is within the control of the player
    def __init__(self, name, is_ai=False, ai_instance=None, card_counter=None):
        self.name = name
        self.hand = []
        self.count = 0
        self.blackjack = False
        self.bust = False
        self.roundsWon = 0
        self.x = 0
        self.y = 0
        self.currentTurn = False
        self.is_ai = is_ai  # Flag for AI-controlled player
        self.ai = ai_instance
        self.card_counter = card_counter

    # this method asks the player for their choice of action when it is their turn
    def askChoice(self):
        if self.is_ai and self.ai:
            dealer_hand_values = dealer.hand  # Pass the dealer's actual hand
            remaining_cards = dealer.deck.cards  # Pass remaining cards from the dealer's deck
            decision = self.ai.decide_action(self.hand, dealer_hand_values, remaining_cards)
            print(f"{self.name} (AI) chooses to {decision.upper()}")
            return 1 if decision == "hit" else 2
        else:
            inp = 0
            answered = False
            while not answered:
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN and event.key == K_h:
                        inp = 1
                        answered = True
                    if event.type == KEYDOWN and event.key == K_s:
                        inp = 2
                        answered = True
            return inp

    # this method adds a card provided by the dealer to the player's hand
    def addCard(self, card):
        self.hand.append(card)
        self.countCards()
        print(str(self.name) + "'s Count: " + str(self.count))

    # this method prints the player's hand
    def printHand(self):
        print("")
        print(str(self.name) + "'s Hand: ")
        for playerCard in self.hand:
            print("Suit - " + playerCard.suit + "\nLabel - " + str(playerCard.label))

    # this method prints the player's count
    def printCount(self):
        print("")
        print(str(self.name) + "'s Count: " + str(self.count))

    # this method resets the player's hand
    def resetHandAndCount(self):
        self.hand = []
        self.count = 0

    # this method considers all aces in a player's hand to give them the closest count under 21
    def countCards(self):
        self.count = 0
        aces = 0

        # First pass: treat all Aces as 1
        for card in self.hand:
            if card.label == 'A':
                aces += 1
                self.count += 1  # Ace as 1 initially
            else:
                self.count += card.value

        # Now try to "upgrade" some Aces from 1 to 11 by adding 10 each time
        for i in range(aces):
            if self.count + 10 <= 21:
                self.count += 10

    # this method will draw all the cards in a hand (13 : 20 Card Dimension Ratio)
    def drawHand(self, surface):
        cardWidth, cardHeight = 78, 120
        cardGap = 20
        playerBoxLength = cardWidth + (cardGap * (len(self.hand) - 1))
        playerBoxHeight = cardHeight
        playerTopLeftX = self.x - (0.5 * playerBoxLength)
        playerTopLeftY = self.y - (0.5 * playerBoxHeight)
        for c in self.hand:
            drawCard = pygame.image.load("Resources/Cards/" + str(c.suit) + "/" + str(c.label) + ".png")
            resizedCard = pygame.transform.scale(drawCard, (cardWidth, cardHeight))
            surface.blit(resizedCard, (playerTopLeftX, playerTopLeftY))
            pygame.display.update()
            playerTopLeftX += cardGap
        nameX = self.x
        nameY = self.y + (0.75 * cardHeight)
        nameColor = white
        if self.currentTurn:
            countString1 = ""
            countString1 += "Count: " + str(player.count)
            add_text(countString1, text_Normal, surface, self.x + (0.20 * playerTopLeftX), self.y - 5, orange)
            nameColor = blue
            add_text("Hit(H) or Stand(S)", text_Normal, surface, self.x, self.y - (0.75 * cardHeight), nameColor)
        if self.bust:
            bust = pygame.image.load("Resources/Icons/Bust.png")
            bustWidth = bust.get_width()
            bustHeight = bust.get_height()
            surface.blit(bust, (self.x - (0.5 * bustWidth), self.y - (0.5 * bustHeight)))
        if self.blackjack:
            blackjack = "Blackjack"
            add_text(blackjack, text_Title, surface, self.x - 5, self.y - 5, black)
        add_text(str(self.name), text_Normal, surface, nameX, nameY, nameColor)

    # function to reset everything for the next round
    def resetState(self):
        self.bust = False
        self.blackjack = False
        self.resetHandAndCount()


# global variables listed below
# Instantiate CardCounter and AI (from second snippet)
card_counter = CardCounter()
ai_instance = AI(Card)  # Pass the Card class to the AI instance
ai_instance.set_card_counter(card_counter)

player = Player("AI Agent Minimax", is_ai=True, ai_instance=ai_instance, card_counter=card_counter)
dealer = Dealer(card_counter=card_counter)

remaining_cards = [c.value for c in dealer.deck.cards]

startY = 50
round = 0
records = [0, 0, 0]  # wins, losses, draws
score_text = f'Wins: {records[0]}   Losses: {records[1]}   Draws: {records[2]}'
last_decision = None


def startGame():
    pygame.init()
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Welcome")
    screen.fill(green)
    add_text("Blackjack Minimax", text_Heading, screen, halfWidth, halfHeight, black)
    add_text("PRESS SPACE TO CONTINUE", text_SubHeading, screen, halfWidth, halfHeight + 100, white)
    pygame.display.update()
    beginning = True
    while beginning:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                beginning = False

def fixCoordinates():
    global player, dealer
    player.x = halfWidth
    player.y = 650

def newDeck():
    global dealer, card_counter
    dealer = Dealer(card_counter=card_counter)

def createHands():
    global dealer
    dealer.createDealerHand()
    for i in range(1, 3):
        card = dealer.dealCard()
        player.addCard(card)

def checkBlackJack():
    if player.count == 21:
        print("")
        print(player.name + ", you got a BLACKJACK !")
        player.blackjack = True

def drawTurn(surface):
    global player, dealer, records, score_text
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    screen.fill(green)
    dealer.drawHand(surface)
    player.drawHand(surface)
    add_text("Round " + str(round), text_Normal, surface, 50, 20, white)
    add_text(score_text, text_SubHeading, surface, 240, 730, white)
    pygame.display.update()

def revealDealerHand(surface):
    global dealer, startY, player
    dealerBust = False
    while dealer.count <= 16:
        dealer.addCard()
    if dealer.count > 21 and player.count <= 21:
        print("")
        print("The Dealer busted. YOU WON!")
        add_text("The Dealer busted. YOU WON!", text_Normal, surface, halfWidth, 350, white)
        records[0] += 1
        dealerBust = True
    dealer.printDealerHand()
    dealer.printDealerCount()
    if player.blackjack:
        add_text(str(player.name) + " got a blackjack!", text_Normal, surface, halfWidth, 370, white)
    return dealerBust

def compareCounts(surface):
    global player, dealer, startY, records
    noCounts = True
    highestCount = 0
    if 21 >= player.count > highestCount:
        highestCount = player.count
        noCounts = False
    if noCounts is False:
        if player.count == highestCount and highestCount > dealer.count:
            print("")
            print(str(player.name) + ", YOU WON!")
            add_text(str(player.name) + ", YOU WON!", text_Normal, surface, halfWidth, 350, white)
            records[0] += 1
            if player.blackjack:
                add_text(str(player.name) + " got a blackjack!", text_Normal, surface, halfWidth, 370, white)
        elif player.count == dealer.count:
            print("")
            print("YOU TIED.")
            add_text("YOU TIED.", text_Normal, surface, halfWidth, 350, white)
            records[2] += 1
            if player.blackjack:
                add_text(str(player.name) + " got a blackjack!", text_Normal, surface, halfWidth, 370, white)
        elif player.count < dealer.count and player.blackjack is False:
            print("")
            print("The Dealer won. YOU LOSE.")
            add_text("The Dealer won. YOU LOSE.", text_Normal, surface, halfWidth, 350, white)
            records[1] += 1
    elif player.bust:
        add_text(str(player.name) + " busted. YOU LOSE.", text_Normal, surface, halfWidth, 350, white)
        records[1] += 1

def finalRecords():
    global records, score_text, round, player
    pygame.init()
    pygame.display.set_caption("Game Over")
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    screen.fill(green)
    add_text(player.name + " Game Stats:", text_Title, screen, 600, 200, black)
    add_text("Rounds Completed: " + str(round), text_SubHeading, screen, 600, 350, white)
    add_text(score_text, text_SubHeading, screen, 600, 430, white)
    add_text("Press 'L' to LEAVE the game", text_SubHeading, screen, 600, 550, orange)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_l):
                pygame.quit()
                sys.exit()

def playTurns():
    global player, round, score_text, last_decision
    round += 1
    pygame.init()
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Play Round " + str(round))
    player.currentTurn = True
    player.printHand()
    drawTurn(screen)

    if player.blackjack:
        print(f"{player.name} has a blackjack!")
        last_decision = "stand"
        return

    while not player.bust and not player.blackjack:
        choice = player.askChoice()
        if choice == 1:  # hit
            hitCard = dealer.dealCard()
            player.addCard(hitCard)
            drawTurn(screen)
            player.printHand()
            last_decision = "hit"
            if player.count > 21:
                player.bust = True
                print(f"{player.name} busted with a count of {player.count}.")
                break
        elif choice == 2:  # stand
            print(f"{player.name} decides to stand with a count of {player.count}.")
            last_decision = "stand"
            break

    score_text = f'Wins: {records[0]}   Losses: {records[1]}   Draws: {records[2]}'
    drawTurn(screen)


def showEndRoundScreen(surface, last_decision):
    global player, dealer, ai_instance, score_text, records

    pygame.init()
    pygame.display.set_caption("Round Over")
    surface.fill(green)

    # Reveal dealer hand first
    dealerBust = revealDealerHand(surface)

    # If dealer didn't bust, we must compare counts to update records
    if not dealerBust:
        compareCounts(surface)

    # Now records should be updated by this point
    score_text = f'Wins: {records[0]}   Losses: {records[1]}   Draws: {records[2]}'

    # Determine the outcome string just for display (records are already updated)
    if player.bust:
        outcome = "Loss"
    elif dealerBust:
        outcome = "Win"
    else:
        # Deduce outcome from counts
        if player.count > 21:
            outcome = "Loss"
        elif dealer.count > 21:
            outcome = "Win"
        elif player.count > dealer.count:
            outcome = "Win"
        elif player.count == dealer.count:
            outcome = "Tie"
        else:
            outcome = "Loss"

    # Update AI’s history buffer with final outcome
    ai_instance.update_outcome_in_buffer(outcome)
    ai_instance.flush_buffer_to_csv(ai_instance.history_file if hasattr(ai_instance, 'history_file') else "history.csv")

    # Starting Y position
    y_start = 300
    line_spacing = 50  # Adjust spacing between lines

    add_text("Results:", text_SubHeading, surface, halfWidth, y_start, orange)
    add_text(score_text, text_SubHeading, surface, halfWidth, y_start + 2 * line_spacing, white)
    add_text("Press 'D' to DEAL or Press 'Q' to QUIT", text_SubHeading, surface, halfWidth, y_start + 3 * line_spacing, orange)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
                ai_instance.flush_buffer_to_csv("history.csv")
                finalRecords()
            if event.type == KEYDOWN and event.key == K_d:
                return  # Continue to next round


def resetStats():
    global player, startY
    player.resetState()
    startY = 100


# main game loop starts here
gameOver = False
while not gameOver:
    startGame()
    fixCoordinates()
    while True:  # Loop for each round
        newDeck()
        createHands()
        checkBlackJack()
        playTurns()
        screen = pygame.display.set_mode((screenWidth, screenHeight))
        showEndRoundScreen(screen, last_decision)
        resetStats()
