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


# Attempting to import AI and CardCounter from external files provided in the second snippet
try:
    from ai import AI
    from card_counter import CardCounter
except ImportError:
    # If not available, define stubs
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
            # Update card counter with this card
            card_id = str(topCard.label) + topCard.suit[0]
            card_counter.update_count(card_id)
        return topCard

    # Method to display all cards in the deck
    def showDeck(self):
        return "[" + ", ".join(str(card) for card in self.cards) + "]"


class Dealer:
    # this class contains everything that is within the control of the dealer
    def __init__(self, card_counter=None):
        self.deck = Deck()
        self.deck.createDeck()
        self.deck.shuffleDeck()
        self.hand = []
        self.count = 0
        self.card_counter = card_counter
        self.x = 0
        self.y = 0

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
        countString1 = "Count: " + str(self.hand[0].value)
        add_text(countString1, text_Normal, surface, self.x + (0.20 * playerTopLeftX), self.y - 5, orange)
        deckX = 400 - (0.5 * cardWidth)
        deckY = 100 - (0.5 * cardHeight)
        for _ in range(1, 7):
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
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.x = 0
        self.y = 0
        self.currentTurn = False
        self.is_ai = is_ai
        self.ai = ai_instance
        self.card_counter = card_counter

    # this method asks the player for their choice of action when it is their turn
    def askChoice(self):
        if self.is_ai and self.ai:
            dealer_hand_values = dealer.hand
            remaining_cards = dealer.deck.cards
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
        for c in self.hand:
            self.count += c.value
        for c in self.hand:
            if c.label == "A":
                self.count += 10
                if self.count > 21:
                    self.count -= 10
                    break

    # method to update player's score
    def updateScore(self, result):
        if result == 'win':
            self.wins += 1
        elif result == 'loss':
            self.losses += 1
        elif result == 'draw':
            self.draws += 1

    # method to display the player's score
    def displayScore(self):
        return f"{self.name}: Wins: {self.wins}, Losses: {self.losses}, Draws: {self.draws}"

    # this method will draw all the cards in a hand
    def drawHand(self, surface):
        cardWidth, cardHeight = 78, 120
        cardGap = 20
        playerBoxLength, playerBoxHeight = cardWidth + (cardGap * (len(self.hand) - 1)), cardHeight
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
            countString1 = "Count: " + str(self.count)
            add_text(countString1, text_Normal, surface, self.x + 120, self.y - 5, orange)
            nameColor = blue
            add_text("Hit(H) or Stand(S)", text_Normal, surface, self.x, self.y - (0.75 * cardHeight), nameColor)
        if self.bust:
            bust = pygame.image.load("Resources/Icons/bust.png")
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

# CardCounter and AI from second snippet
card_counter = CardCounter()
ai_instance = AI(Card)  # Pass the Card class to the AI instance
ai_instance.set_card_counter(card_counter)

# Multiple players (from first snippet) + one AI player (from second snippet)
players = []
numPlayers = 2

# Create Dealer with card_counter
dealer = Dealer(card_counter=card_counter)

round = 0
startY = 50
startX = 50
records = [0, 0, 0]  # wins, losses, draws
score_text = f'Wins: {records[0]}   Losses: {records[1]}   Draws: {records[2]}'
last_decision = None

def add_text(text, font, surface, x, y, text_color):
    textObject = font.render(text, False, text_color)
    textWidth = textObject.get_rect().width
    textHeight = textObject.get_rect().height
    surface.blit(textObject, (x - (textWidth / 2), y - (textHeight / 2)))

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

def getPlayerNames():
    # One human, one AI
    players.append(Player("Human"))
    players.append(Player("AI Agent Minimax", is_ai=True, ai_instance=ai_instance, card_counter=card_counter))

def fixCoordinates():
    global players, dealer, numPlayers
    dealer.x = halfWidth
    dealer.y = 100
    if numPlayers == 1:
        players[0].x = halfWidth
        players[0].y = 650
    elif numPlayers == 2:
        players[0].x = 850
        players[0].y = halfHeight + 150
        players[1].x = 400
        players[1].y = halfHeight + 150

def newDeck():
    global dealer
    dealer = Dealer(card_counter=card_counter)

def createHands():
    dealer.createDealerHand()
    for i in range(1, 3):
        for p in players:
            c = dealer.dealCard()
            p.addCard(c)

def checkBlackJack():
    for p in players:
        if p.count == 21:
            print("")
            print(p.name + ", you got a BLACKJACK!")
            p.blackjack = True

def drawTurn(surface, empty):
    global players, dealer, startY, startX
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    screen.fill(green)
    dealer.drawHand(surface)
    sx = startX
    for p in players:
        p.drawHand(surface)
        if empty:
            s_text = ''
        else:
            s_text = p.displayScore()
        add_text(s_text, text_Bold, surface, sx + 800, 680, white)
        sx -= 500
    add_text("Round " + str(round), text_Normal, surface, 50, 20, white)
    sx = 50
    startY = 50
    pygame.display.update()

def revealDealerHand(surface):
    global dealer
    dealerBust = False
    while dealer.count <= 16:
        dealer.addCard()
    if dealer.count > 21:
        print("")
        print("The Dealer busted.")
        dealerBust = True
    dealer.printDealerHand()
    dealer.printDealerCount()
    return dealerBust

def compareCounts(surface):
    global players, dealer, startY
    startY = 0
    startXcoord = halfWidth
    dealerBust = revealDealerHand(surface)
    allPlayersBusted = all(p.bust for p in players)

    if dealerBust and allPlayersBusted:
        for p in players:
            add_text(f"{p.name}, EVERYONE BUSTED. IT'S A DRAW.", text_Normal, surface, startXcoord + 230, 350, white)
            p.updateScore('draw')
            startXcoord -= 430
    elif dealerBust:
        for p in players:
            if p.bust:
                add_text(f"{p.name} busted. YOU LOSE.", text_Normal, surface, startXcoord + 230, 350, white)
                p.updateScore('loss')
            else:
                add_text(f"{p.name}, YOU WON! The dealer busted.", text_Normal, surface, startXcoord + 230, 350, white)
                p.updateScore('win')
            startXcoord -= 430
    else:
        for p in players:
            if p.bust:
                add_text(f"{p.name} busted. YOU LOSE.", text_Normal, surface, startXcoord + 230, 350, white)
                p.updateScore('loss')
            elif p.count > dealer.count:
                add_text(f"{p.name}, YOU WON!", text_Normal, surface, startXcoord + 230, 350, white)
                p.updateScore('win')
            elif p.count == dealer.count:
                add_text(f"{p.name}, YOU TIED.", text_Normal, surface, startXcoord + 230, 350, white)
                p.updateScore('draw')
            else:
                add_text(f"The Dealer won. {p.name}, YOU LOSE.", text_Normal, surface, startXcoord + 230, 350, white)
                p.updateScore('loss')
            startXcoord -= 430

def showEndRoundScreen(surface):
    global players, startY, startX
    pygame.init()
    pygame.display.set_caption("Round Over")
    add_text("Results:", text_SubHeading, surface, halfWidth, 250, orange)
    compareCounts(surface)
    startXcoord = 50
    for p in players:
        s_text = p.displayScore()
        add_text(s_text, text_Bold, surface, startXcoord + 800, 680, white)
        startXcoord -= 500
    startY = 0
    add_text("Dealer's Count: " + str(dealer.count), text_Normal, surface, halfWidth, 280, orange)
    startY += 50
    countString1 = ""
    # Display all player counts in a single line
    for i, p in enumerate(reversed(players)):
        countString1 += f"{p.name}'s Count: {p.count}    "

    add_text(countString1, text_Normal, surface, halfWidth, 320, orange)
    add_text("Press 'D' to DEAL or Press 'Q' to QUIT", text_SubHeading, surface, halfWidth, 400, orange)
    pygame.display.update()
    roundEnd = True
    while roundEnd:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
                finalRecords()
            if event.type == KEYDOWN and event.key == K_d:
                roundEnd = False

def resetStats():
    global players, startY
    for p in players:
        p.resetState()
    startY = 100

def finalRecords():
    global round, players
    pygame.init()
    pygame.display.set_caption("Game Over")
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    screen.fill(green)
    add_text("Rounds Completed: " + str(round), text_SubHeading, screen, 625, 200, white)
    startXcoord = 0
    startYcoord = 0
    for p in players:
        add_text(p.name + " Game Stats:", text_SubHeading, screen, startXcoord + 250, startYcoord + 350, black)
        add_text(p.displayScore(), text_Bold, screen, startXcoord + 260, startYcoord + 400, white)
        startXcoord += 700
    add_text("Press 'L' to LEAVE the game", text_SubHeading, screen, 625, 550, orange)
    pygame.display.update()
    while True:
      for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_l):
          pygame.quit()
          sys.exit()

def playTurns():
    global players, round
    round += 1
    pygame.init()
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Play Round " + str(round))
    drawTurn(screen, empty=False)
    turn = 0
    while turn < len(players):
        currentPlayer = players[turn]
        if currentPlayer.blackjack:
            turn += 1
            if turn >= len(players):
                break
            currentPlayer = players[turn]
        for p in players:
            p.currentTurn = False
        currentPlayer.currentTurn = True

        currentPlayer.printHand()
        drawTurn(screen, empty=False)

        if not currentPlayer.blackjack:
            choice = currentPlayer.askChoice()
            if choice == 1: # hit
                keepHitting = True
                while keepHitting is True:
                    hitCard = dealer.dealCard()
                    currentPlayer.addCard(hitCard)
                    drawTurn(screen, empty=False)
                    currentPlayer.printHand()

                    if currentPlayer.count == 21:
                        print("")
                        print(str(currentPlayer.name) + " got a blackjack!")
                        currentPlayer.blackjack = True
                        break
                    if currentPlayer.count > 21:
                        print("")
                        print(str(currentPlayer.name) + ", you busted.")
                        currentPlayer.bust = True
                        break
                    choice = currentPlayer.askChoice()
                    if choice != 1:
                        keepHitting = False

        turn += 1
    drawTurn(screen, empty=True)
    showEndRoundScreen(screen)


# main game loop starts here
gameOver = False
while not gameOver:
    startGame()
    getPlayerNames()
    fixCoordinates()
    roundOver = False
    while not roundOver:
        newDeck()
        createHands()
        checkBlackJack()
        playTurns()
        resetStats()
