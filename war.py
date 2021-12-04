import random
import pygame
from enum import Enum
suits = ['hearts', 'diamonds', 'spades', 'clubs']
face_names = ['jack', 'queen', 'king', 'ace']


class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

def get_value_of_card(card_name):
    if card_name is "jack":
        return 11
    elif card_name is "queen":
        return 12
    elif card_name is "king":
        return 13
    elif card_name is "ace":
        return 14
    else: return int(card_name)

def build_deck(deck):
    deck = [Card(value, suit) for value in range(2, 11) for suit in suits]
    deck += [Card(face, suit) for face in face_names for suit in suits]
    return deck


def compare_cards(card_one, card_two):
    value_one = 0
    value_two = 0
    value_one = get_value_of_card(card_one)
    value_two = get_value_of_card(card_two)

    if value_one > value_two:
        return 1
    elif value_one < value_two:
        return 2
    else: return 0


def shuffle_deck(deck, clock):
    random.seed(clock)
    random.shuffle(deck)


def split_deck(deck, player_cards, cpu_cards):
    for i in range(0, len(deck), 2):
        player_cards.append(deck[i])
        cpu_cards.append(deck[i + 1])

if __name__ == "__main__":
    clock = pygame.time.Clock()
    deck = list()
    deck = build_deck(deck)
    shuffle_deck(deck, clock)
    player_cards = []
    cpu_cards = []
    cpu_score_value = 0
    player_score_value = 0
    split_deck(deck, player_cards, cpu_cards)
    war_list = []
    war_check = 0
    done = False
    # for card in player_cards:
    #     print("Player deck:", card.value, card.suit)
    # for card in cpu_cards:
    #     print("CPU card:", card.value, card.suit)
    #print(len(player_cards), len(cpu_cards))

    cpu_size = len(cpu_cards)
    player_size = len(player_cards)
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

    deal_button = large_font.render("DEAL", True, (0,0,0), (255,255,255))
    deal_button_rect = deal_button.get_rect()
    deal_button_rect.center = (970, 800)

    cpu_score = large_font.render("Cpu Score: " + str(cpu_score_value), True, (0,0,0), (255,255,255))
    cpu_score_rect = cpu_score.get_rect()
    cpu_score_rect.center = (400, 120)

    player_score = large_font.render("Player Score: " + str(player_score_value), True, (0,0,0), (255,255,255))
    player_score_rect = player_score.get_rect()
    player_score_rect.center = (1400, 120)

    card_matchup = large_font.render("", True, (0,0,0), (255,255,255))
    card_matchup_rect = card_matchup.get_rect()
    card_matchup_rect.center = (1000, 120)

    cpu_count = large_font.render("Cards left: " + str(cpu_size), True, (0,0,0), (255,255,255))
    cpu_count_rect = cpu_count.get_rect()
    cpu_count_rect.center = (500, 920)

    player_count = large_font.render("Cards left: " + str(player_size), True, (0,0,0), (255,255,255))
    player_count_rect = player_count.get_rect()
    player_count_rect.center = (1400, 920)


    card_one = pygame.image.load(r'./cards/back.png')
    card_one = pygame.transform.scale(card_one,(500,726))

    card_two = pygame.image.load(r'./cards/back.png')
    card_two = pygame.transform.scale(card_one,(500,726))

    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                    screen.fill(GRAY)
                    player_score = large_font.render("Player Score: " + str(player_score_value), True, (0,0,0), (255,255,255))
                    cpu_score = large_font.render("Cpu Score: " + str(cpu_score_value), True, (0,0,0), (255,255,255))
                    if 970 <= mouse[0] <= 970+125 and 800 <= mouse[1] <= 800+60:
                        card_one = pygame.image.load(r'./cards/' + str(cpu_cards[0].value) + '_of_' + str(cpu_cards[0].suit) + '.png')
                        card_two = pygame.image.load(r'./cards/' + str(player_cards[0].value) + '_of_' + str(player_cards[0].suit) + '.png')
                        if war_check == 0:
                            result = compare_cards(str(cpu_cards[0].value), str(player_cards[0].value))
                            if result is 1:
                                print(1)
                                card_matchup = large_font.render("Cpu won", True, (0,0,0), (255,255,255))
                                cpu_cards.append(cpu_cards.pop(0))
                                cpu_cards.append(player_cards.pop(0))

                            elif result is 2:
                                print(2)
                                card_matchup = large_font.render("Player won", True, (0,0,0), (255,255,255))
                                player_cards.append(player_cards.pop(0))
                                player_cards.append(cpu_cards.pop(0))
                            else:
                                print(3)
                                card_matchup = large_font.render("War", True, (0,0,0), (255,255,255))
                                war_check = get_value_of_card(player_cards[0].value)
                                
                        if war_check > 0:
                            card_matchup = large_font.render("War ongoing", True, (0,0,0), (255,255,255)) 
                            if len(player_cards) == 1 or len(cpu_cards) == 1:
                                result = compare_cards(str(cpu_cards[0].value), str(player_cards[0].value))
                                if result == 1:
                                    card_matchup = large_font.render("Cpu won war", True, (0,0,0), (255,255,255))
                                    cpu_cards.extend(war_list)
                                elif result == 2:
                                    card_matchup = large_font.render("Player won war", True, (0,0,0), (255,255,255))
                                    player_cards.extend(war_list)
                                war_list.clear()
                                war_check = 0
                            else:
                                war_list.extend([cpu_cards.pop(0), player_cards.pop(0)])
                                war_check -= 1
                        if war_check == 1:
                            result = compare_cards(str(cpu_cards[0].value), str(player_cards[0].value))
                            if result == 1:
                                card_matchup = large_font.render("Cpu won war", True, (0,0,0), (255,255,255))
                                cpu_cards.extend(war_list)
                            elif result == 2:
                                card_matchup = large_font.render("Player won war", True, (0,0,0), (255,255,255))
                                player_cards.extend(war_list)
                            war_list.clear()
                            war_check -= 1

                    cpu_count = large_font.render("Cards left: " + str(len(cpu_cards)), True, (0,0,0), (255,255,255))
                    player_count = large_font.render("Cards left: " + str(len(player_cards)), True, (0,0,0), (255,255,255))

                    if len(player_cards)==0:
                        cpu_score_value +=1
                        player_cards.clear()
                        cpu_cards.clear()
                        shuffle_deck(deck, clock)
                        split_deck(deck, player_cards, cpu_cards)
                    if len(cpu_cards)==0:
                        player_score_value +=1
                        player_cards.clear()
                        cpu_cards.clear()
                        shuffle_deck(deck, clock)
                        split_deck(deck, player_cards, cpu_cards)

        screen.blit(card_one, (MARGIN_LEFT,MARGIN_TOP))
        screen.blit(card_two, (MARGIN_LEFT + 950,MARGIN_TOP))
        screen.blit(deal_button, deal_button_rect)
        screen.blit(cpu_score, cpu_score_rect)
        screen.blit(player_score, player_score_rect)
        screen.blit(card_matchup, card_matchup_rect)
        screen.blit(player_count, player_count_rect)
        screen.blit(cpu_count, cpu_count_rect)
        pygame.display.update()

        clock.tick(30)

