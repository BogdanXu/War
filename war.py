import random
import pygame
suits = ['hearts', 'diamonds', 'spades', 'clubs']
face_names = ['jack', 'queen', 'king', 'ace']


class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit


def build_deck(deck):
    deck = [Card(value, suit) for value in range(2, 11) for suit in suits]
    deck += [Card(face, suit) for face in face_names for suit in suits]
    return deck


def compare_cards(card_one, card_two):
    if card_one.value != card_two.value:
        if card_one.value > card_two.value:
            return "One wins"
        else:
            return "Two wins"
    else:
        return "War"


def shuffle_deck(deck):
    random.shuffle(deck)


def split_deck(deck, player_cards, cpu_cards):
    for i in range(0, len(deck), 2):
        player_cards.append(deck[i])
        cpu_cards.append(deck[i + 1])



if __name__ == "__main__":
    deck = list()
    deck = build_deck(deck)
    shuffle_deck(deck)
    player_cards = []
    cpu_cards = []
    split_deck(deck, player_cards, cpu_cards)
    for card in player_cards:
        print("Player deck:", card.value, card.suit)
    for card in cpu_cards:
        print("CPU card:", card.value, card.suit)
    #print(len(player_cards), len(cpu_cards))

    # WINDOW SIZE
    WIDTH = 1920
    HEIGHT = 1000
    MARGIN_LEFT = 230
    MARGIN_TOP = 150

    # Setting up the screen and background
    GRAY = (110, 110, 110)
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    screen.fill(GRAY)

    large_font = pygame.font.Font(None, 50)
    deal_button = large_font.render("HIGH", True, (0,0,0))

    card_one = pygame.image.load(r'./cards/back.png')
    card_one = pygame.transform.scale(card_one,(500,726))

    card_two = pygame.image.load(r'./cards/back.png')
    card_two = pygame.transform.scale(card_one,(500,726))
    
    while True:
        mouse = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            # Qutting event
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.blit(card_one, (MARGIN_LEFT,MARGIN_TOP))
        screen.blit(card_two, (MARGIN_LEFT + 950,MARGIN_TOP))
        pygame.display.update()

