# all of our imports are listed here
import math
import random
import pygame
from pygame.locals import *
import sys
from ai import AI
from shared import Card
from card_counter import CardCounter

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
            card_counter.update_count(topCard.label + topCard.suit[0])  # Example: "AH" for Ace of Hearts
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
            print(f"DEBUG: Remaining cards in deck: {[f'{card.label} of {card.suit}' for card in remaining_cards]}")  # Debug print
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
        for card in self.hand:
            self.count += card.value
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
            countString1 +=  "Count: " + str(player.count)
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




# below consists the py-game/graphics related code

pygame.init()
pygame.font.init()
screenWidth, screenHeight = 1250, 750
halfWidth, halfHeight = screenWidth / 2, screenHeight / 2

# Instantiate CardCounter
card_counter = CardCounter()

# Pass the card_counter to AI
ai_instance = AI(Card)  # Pass the Card class to the AI instance
ai_instance.set_card_counter(card_counter)

# Modify player creation to include card counting
player = Player("AI Agent Minimax", is_ai=True, ai_instance=ai_instance, card_counter=card_counter)

# Instantiate Dealer with card_counter
dealer = Dealer(card_counter=card_counter)

remaining_cards = [card.value for card in dealer.deck.cards]


black, blue, white, orange, red , green = (0, 0, 0), (51, 235, 255), (255, 255, 255), (255, 165, 0), (255, 0, 0), (34, 139, 34)
fontType = 'Poppins'
text_Title = pygame.font.SysFont(fontType, 80)
text_Heading = pygame.font.SysFont(fontType, 60)
text_SubHeading = pygame.font.SysFont(fontType, 45)
text_Bold = pygame.font.SysFont(fontType, 30)
text_Normal = pygame.font.SysFont(fontType, 20)
text_Small = pygame.font.SysFont(fontType, 10)

# global variables listed below

startY = 50
round = 0
# win, loss, draw/push
records = [0, 0, 0]
score_text = f'Wins: {records[0]}   Losses: {records[1]}   Draws: {records[2]}'


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

# function that sets the x and y coordinates of every player plus the dealer
def fixCoordinates():
    global player, dealer
    player.x = halfWidth
    player.y = 650

# function to restore all the cards to the deck for a new round
def newDeck():
    global dealer
    dealer = Dealer()

# function to create the hands of the dealer and all the players
def createHands():
    global dealer
    dealer.createDealerHand()
    for i in range(1, 3):
      card = dealer.dealCard()
      player.addCard(card)

# function to check for blackjacks (basically when the first two initial cards dealt to a player add up to 21)
# if there is one you automatically win one and a half times your bet, and you sit out for the round
def checkBlackJack():
  if player.count == 21:
    print("")
    print(player.name + ", you got a BLACKJACK !")
    player.blackjack = True

# function to run the turns of all players, basically allowing to hit and pass as normal
# this function also contains the code for changing the value of an ace when necessary
def playTurns():
    global player, round, score_text, last_decision  # Add last_decision here
    round += 1
    pygame.init()
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Play Round " + str(round))
    player.currentTurn = True
    player.printHand()
    drawTurn(screen)

    if player.blackjack:
        print(f"{player.name} has a blackjack!")
        last_decision = "stand"  # Automatically stand if blackjack
        return

    while not player.bust and not player.blackjack:
        choice = player.askChoice()  # AI logic makes the decision
        if choice == 1:  # AI decides to hit
            hitCard = dealer.dealCard()
            player.addCard(hitCard)
            drawTurn(screen)
            player.printHand()
            last_decision = "hit"  # Update the last decision
            if player.count > 21:
                player.bust = True
                print(f"{player.name} busted with a count of {player.count}.")
                break
        elif choice == 2:  # AI decides to stand
            print(f"{player.name} decides to stand with a count of {player.count}.")
            last_decision = "stand"  # Update the last decision
            break

    score_text = f'Wins: {records[0]}   Losses: {records[1]}   Draws: {records[2]}'
    drawTurn(screen)




# function to draw the screen every time an action is conducted in the playing of the game
def drawTurn(surface):
    global player, dealer, records, score_text
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    screen.fill(green)
    dealer.drawHand(surface)
    player.drawHand(surface)
    add_text("Round " + str(round), text_Normal, surface, 50, 20, white)
    add_text(score_text, text_SubHeading, surface, 240, 730, white)
    pygame.display.update()

# function to reveal the face down card of the dealer, and if the dealer has to force hit he will do so
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

# function to see how the bets are retrieved based on counts
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

# function to display a message about the results of the previous round
def showEndRoundScreen(surface, last_decision):
    global startY, gameOver, player, score_text
    pygame.init()
    pygame.display.set_caption("Round Over")
    add_text("Results:", text_SubHeading, surface, halfWidth, 300, orange)
    if revealDealerHand(surface) is False:
        compareCounts(surface)
    score_text = f'Wins: {records[0]}   Losses: {records[1]}   Draws: {records[2]}'
    add_text(score_text, text_SubHeading, surface, 240, 730, white)
    add_text("Dealer's Count: " + str(dealer.count), text_Normal, surface, halfWidth, 400, orange)
    countString1 = ""
    countString1 += str(player.name) + "'s Count: " + str(player.count)
    add_text(countString1, text_Normal, surface, halfWidth, 450, orange)

    # Add AI update
    ai_instance.update_outcome_in_csv(
        player.count,
        dealer.hand[0].value if dealer.hand else 0,
        last_decision,
        outcome="Win" if player.count > dealer.count else "Loss" if player.count < dealer.count else "Tie"
    )

    add_text("Press 'D' to DEAL or Press 'Q' to QUIT", text_SubHeading, surface, halfWidth, 500, orange)
    pygame.display.update()
    roundEnd = True
    while roundEnd:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
                score_text = f'Wins: {records[0]}   Losses: {records[1]}   Draws: {records[2]}'
                finalRecords()
            if event.type == KEYDOWN and event.key == K_d:
                roundEnd = False



# function to reset things such as the bets, and player hands for a new round (plus we need to reset the starting Y
# value for all the text shown in the end of the round
def resetStats():
    global player, startY
    player.resetState()
    startY = 100

# function displays the final scores of the game
def finalRecords():
    global records, score_text, round, player
    pygame.init()
    pygame.display.set_caption("Game Over")
    global players, dealer, records
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
        showEndRoundScreen(pygame.display.set_mode((screenWidth, screenHeight)), last_decision)
        resetStats()

