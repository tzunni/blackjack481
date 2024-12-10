# all of our imports are listed here
import math
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

class Deck:

    # this class contains an array that acts as our 52 card deck
    def __init__(self):
        self.cards = []
        self.shuffle = False

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
        self.shuffle = True
        return random.shuffle(self.cards)

    # this method basically gets the top card of the deck and returns it
    def getCard(self):
        topCard = self.cards[0]
        self.cards.pop(0)
        return topCard

    # Method to display all cards in the deck
    def showDeck(self):
        return "[" + ", ".join(str(card) for card in self.cards) + "]"

class Dealer:

    # this class contains everything that is within the control of the dealer
    def __init__(self):
        self.deck = Deck()
        self.deck.createDeck()
        self.deck.shuffleDeck()
        self.hand = []
        self.count = 0
        self.x = halfWidth
        self.y = 100

    # this method creates the two-card hand that the dealer starts with
    def createDealerHand(self):
        for i in range(1, 3):
            self.addCard()

    # this method uses the getCard() to deal a card to a player
    def dealCard(self):
        return self.deck.getCard()

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
        for card in self.hand:
            if card == self.hand[1]:
                drawCard = pygame.image.load("Resources/Cards/Back/RedBack.png")
            else:
                drawCard = pygame.image.load("Resources/Cards/" + str(card.suit) + "/" + str(card.label) + ".png")
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
        for card in range(1, 7):
            deckCard = pygame.image.load("Resources/Cards/Back/RedBack.png")
            backCard = pygame.transform.scale(deckCard, (cardWidth, cardHeight))
            surface.blit(backCard, (deckX, deckY))
            deckX += cardGap


class Player:

    # this class contains everything that is within the control of the player
    def __init__(self, name):
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

    # this method asks the player for their choice of action when it is their turn
    def askChoice(self):
        inp = 0
        answered = False
        while answered is False:
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
        for card in self.hand:
            self.count += card.value
        for card in self.hand:
            if card.label == "A":
                self.count += 10
                if self.count > 21:
                    self.count -= 10
                    break

    # New method to update player's score
    def updateScore(self, result):
        # result = 'win', 'loss', 'draw'
        if result == 'win':
            self.wins += 1
        elif result == 'loss':
            self.losses += 1
        elif result == 'draw':
            self.draws += 1

    # New method to display the player's score
    def displayScore(self):
        return f"{self.name}: Wins: {self.wins}, Losses: {self.losses}, Draws: {self.draws}"

    # this method will draw all the cards in a hand (13 : 20 Card Dimension Ratio)
    def drawHand(self, surface):
        cardWidth, cardHeight = 78, 120
        cardGap = 20
        playerBoxLength, playerBoxHeight = cardWidth + (cardGap * (len(self.hand) - 1)), cardHeight
        playerTopLeftX = self.x - (0.5 * playerBoxLength)
        playerTopLeftY = self.y - (0.5 * playerBoxHeight)
        for card in self.hand:
            drawCard = pygame.image.load("Resources/Cards/" + str(card.suit) + "/" + str(card.label) + ".png")
            resizedCard = pygame.transform.scale(drawCard, (cardWidth, cardHeight))
            surface.blit(resizedCard, (playerTopLeftX, playerTopLeftY))
            pygame.display.update()
            playerTopLeftX += cardGap
        nameX = self.x
        nameY = self.y + (0.75 * cardHeight)
        nameColor = white
        if self.currentTurn:
            countString1 = ""
            countString1 +=  "Count: " + str(self.count)
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


# officially the end of all our class initializations and methods


# below consists the py-game/graphics related code

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

# global variables listed below
players = []
numPlayers = 2
startY = 50
startX = 50
round = 0

# function to add text to the game when needed
def add_text(text, font, surface, x, y, text_color):
    textObject = font.render(text, False, text_color)
    textWidth = textObject.get_rect().width
    textHeight = textObject.get_rect().height
    surface.blit(textObject, (x - (textWidth / 2), y - (textHeight / 2)))

# function to create the start screen for the game
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

# function to receive the names of all the players
def getPlayerNames():
    global players, numPlayers
    players.append(Player("Human"))
    players.append(Player("AI Agent Minimax"))

# function that sets the x and y coordinates of every player plus the dealer
def fixCoordinates():
    global players, dealer, numPlayers
    if numPlayers == 1:
        players[0].x = halfWidth
        players[0].y = 650
    elif numPlayers == 2:
        players[0].x = 850
        players[0].y = halfHeight + 150
        players[1].x = 400
        players[1].y = halfHeight + 150

# function to restore all the cards to the deck for a new round
def newDeck():
    global dealer
    dealer = Dealer()

# function to create the hands of the dealer and all the players
def createHands():
    global dealer
    dealer.createDealerHand()
    for i in range(1, 3):
        for player in players:
            card = dealer.dealCard()
            player.addCard(card)

# function to check for blackjacks (basically when the first two initial cards dealt to a player add up to 21)
# if there is one you automatically win one and a half times your bet, and you sit out for the round
def checkBlackJack():
    for player in players:
        if player.count == 21:
            print("")
            print(player.name + ", you got a BLACKJACK!")
            player.blackjack = True

# function to run the turns of all players, basically allowing to hit and pass as normal
# this function also contains the code for changing the value of an ace when necessary
def playTurns():
    global players, round, score_text
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
        for player in players:
            player.currentTurn = False
            if player == currentPlayer:
                player.currentTurn = True

        currentPlayer.printHand()
        drawTurn(screen, empty = False)

        choice = currentPlayer.askChoice()
        if choice == 1:
            keepHitting = True
            while keepHitting is True:
                hitCard = dealer.dealCard()
                currentPlayer.addCard(hitCard)

                drawTurn(screen, empty = False)
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
    drawTurn(screen, empty = True)
    showEndRoundScreen(screen)

# function to draw the screen every time an action is conducted in the playing of the game
def drawTurn(surface, empty):
    global player, dealer, records, startY, startX
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    screen.fill(green)
    dealer.drawHand(surface)
    for player in players:
        player.drawHand(surface)
        if empty:
            score_text = ''
        else:
          score_text = player.displayScore()
        add_text(score_text, text_Bold, surface, startX + 800, startY + 680, white)
        startX -= 500
    add_text("Round " + str(round), text_Normal, surface, 50, 20, white)
    startX = 50
    startY = 50
    pygame.display.update()

# function to reveal the face down card of the dealer, and if the dealer has to force hit he will do so
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

# function to see how the bets are retrieved based on counts
def compareCounts(surface):
    global players, dealer, startY
    startY = 0
    startX = halfWidth
    dealerBust = revealDealerHand(surface)
    # Check if all players busted
    allPlayersBusted = all(player.bust for player in players)

    if dealerBust and allPlayersBusted:
        # If everyone busts, it's a draw
        for player in players:
            add_text(f"{player.name}, EVERYONE BUSTED. IT'S A DRAW.", text_Normal, surface, startX + 230, startY + 350, white)
            player.updateScore('draw')
            startX -= 430
    elif dealerBust:
        # Dealer busts: all non-busting players win
        for player in players:
            if player.bust:
                add_text(f"{player.name} busted. YOU LOSE.", text_Normal, surface, startX + 230, startY + 350, white)
                player.updateScore('loss')
            else:
                add_text(f"{player.name}, YOU WON! The dealer busted.", text_Normal, surface, startX + 230, startY + 350, white)
                player.updateScore('win')
            startX -= 430
    else:
        # Dealer did not bust: compare scores with each player
        for player in players:
            if player.bust:
                add_text(f"{player.name} busted. YOU LOSE.", text_Normal, surface, startX + 230, startY + 350, white)
                player.updateScore('loss')
            elif player.count > dealer.count:
                add_text(f"{player.name}, YOU WON!", text_Normal, surface, startX + 230, startY + 350, white)
                player.updateScore('win')
            elif player.count == dealer.count:
                add_text(f"{player.name}, YOU TIED.", text_Normal, surface, startX + 230, startY + 350, white)
                player.updateScore('draw')
            else:
                add_text(f"The Dealer won. {player.name}, YOU LOSE.", text_Normal, surface, startX + 230, startY + 350, white)
                player.updateScore('loss')
            startX -= 430

# function to display a message about the results of the previous round
def showEndRoundScreen(surface):
    global startY, gameOver, players, startX
    pygame.init()
    pygame.display.set_caption("Round Over")
    add_text("Results:", text_SubHeading, surface, halfWidth, 250, orange)
    compareCounts(surface)
    startX = 50
    startY = 50
    for player in players:
      score_text = player.displayScore()
      add_text(score_text, text_Bold, surface, startX + 800, startY + 680, white)
      startX -= 500
    startY = 0
    add_text("Dealer's Count: " + str(dealer.count), text_Normal, surface, halfWidth, startY + 280, orange)
    startY += 50
    countString1 = ""
    for i in range(numPlayers - 1, -1, -1):
        player = players[i]
        if (numPlayers > 3 and player == players[2]) or player == players[0]:
            countString1 += str(player.name) + "'s Count: " + str(player.count)
        else:
            countString1 += str(player.name) + "'s Count: " + str(player.count) + "                                                                   "
        if i == numPlayers - 2 and numPlayers == 2:
            break
    add_text(countString1, text_Normal, surface, halfWidth, startY + 260, orange)

    add_text("Press 'D' to DEAL or Press 'Q' to QUIT", text_SubHeading, surface, halfWidth, 400, orange)
    pygame.display.update()
    roundEnd = True
    while roundEnd:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
                finalRecords()
            if event.type == KEYDOWN and event.key == K_d:
                roundEnd = False

# function to reset things such as the bets, and player hands for a new round (plus we need to reset the starting Y
# value for all the text shown in the end of the round
def resetStats():
    global players, startY
    for player in players:
        player.resetState()
    startY = 100

# function displays the final scores of the game
def finalRecords():
    global records, score_text, round, players, dealer
    pygame.init()
    pygame.display.set_caption("Game Over")
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    screen.fill(green)
    startX = 0
    startY = 0
    add_text("Rounds Completed: " + str(round), text_SubHeading, screen, 625, 200, white)
    for player in players:
      add_text(player.name + " Game Stats:", text_SubHeading, screen, startX + 250, startY + 350, black)
      add_text(player.displayScore(), text_Bold, screen, startX + 260, startY + 400, white)
      startX += 700
    add_text("Press 'L' to LEAVE the game", text_SubHeading, screen, 625, 550, orange)
    pygame.display.update()
    while True:
      for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_l):
          pygame.quit()
          sys.exit()

# main game loop starts here

gameOver = False
while gameOver is False:
    startGame()
    getPlayerNames()
    fixCoordinates()
    roundOver = False
    while roundOver is False:
        newDeck()
        createHands()
        checkBlackJack()
        playTurns()
        resetStats()
