import random
import pygame
from enum import Enum
suits = ['hearts', 'diamonds', 'spades', 'clubs']
face_names = ['jack', 'queen', 'king', 'ace']
import time

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

def game_logic(get_value_of_card, compare_cards, player_cards, cpu_cards, war_list, war_check, large_font):

    #Place the cards down
    war_list.extend([cpu_cards.pop(0), player_cards.pop(0)])
    card_one = pygame.image.load(r'./cards/' + str(war_list[len(war_list)-2].value) + '_of_' + str(war_list[len(war_list)-2].suit) + '.png')
    card_two = pygame.image.load(r'./cards/' + str(war_list[len(war_list)-1].value) + '_of_' + str(war_list[len(war_list)-1].suit) + '.png')

    if war_check == 0:
        result = compare_cards(str(war_list[0].value), str(war_list[1].value))
        if result is 1:
            card_matchup = large_font.render("Cpu won", True, "Black", "White")
            cpu_cards.extend(war_list)
            war_list.clear()
        elif result is 2:
            card_matchup = large_font.render("Player won", True, "Black", "White")
            player_cards.extend(war_list)
            war_list.clear()
        else:
            card_matchup = large_font.render("War", True, "Black", "White")
            war_check = get_value_of_card(war_list[0].value) + 2

    #If the war is ongoing, continue here
    if war_check > 1:
        card_matchup = large_font.render("War ongoing", True, "Black", "White") 

        #If someone has placed his final card before ending the war, end the war early
        if len(player_cards) == 0 or len(cpu_cards) == 0:
            result = compare_cards(str(war_list[-2].value), str(war_list[-1].value))
            if result == 1:
                card_matchup = large_font.render("Cpu won war", True, "Black", "White")
                cpu_cards.extend(war_list)
            elif result == 2:
                card_matchup = large_font.render("Player won war", True, "Black", "White")
                player_cards.extend(war_list)
            war_list.clear()
            war_check = 0
        #Otherwise just continue adding cards to the war_list with each click
        else:
            war_check -= 1

    #Compare the final cards at the end of the war and append the cards to the winner
    if war_check == 1:
        result = compare_cards(str(war_list[-2].value), str(war_list[-1].value))
        if result == 1:
            card_matchup = large_font.render("Cpu won war", True, "Black", "White")
            cpu_cards.extend(war_list)
            war_list.clear()
            war_check -= 1
        elif result == 2:
            card_matchup = large_font.render("Player won war", True, "Black", "White")
            player_cards.extend(war_list)
            war_list.clear()
            war_check -= 1
                            #Special case, if the last cards placed at the end of the war have the same value, continue war from there
        else: 
            card_matchup = large_font.render("War", True, "Black", "White")
            war_check = get_value_of_card(player_cards[0].value)
    
    return card_matchup,card_one,card_two,war_check


def save_and_reset(shuffle_deck, split_deck, clock, deck, player_cards, cpu_cards, cpu_score_value, player_score_value, f):
    if len(player_cards) == 0:
        cpu_score_value += 1
    else: 
        player_score_value += 1
    player_cards.clear()
    cpu_cards.clear()
    shuffle_deck(deck, clock)
    split_deck(deck, player_cards, cpu_cards)
    f.seek(0)
    f.truncate(0)
    f.write(str(cpu_score_value))
    f.write('\n')
    f.write(str(player_score_value))
    return cpu_score_value, player_score_value, player_cards, cpu_cards, deck


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
    color = "White"
    autoplay = False
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
    GRAY = (4, 110, 38)
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    screen.fill(GRAY)
    pygame.display.set_caption('War')
    large_font = pygame.font.Font(None, 50)

    deal_button = large_font.render("Place Cards", True, "Black", "GRAY")
    deal_button_rect = deal_button.get_rect()
    deal_button_rect.center = (WIDTH/2, HEIGHT/2)

    cpu_score = large_font.render("Cpu Score: " + str(cpu_score_value), True, "Black", "White")
    cpu_score_rect = cpu_score.get_rect()
    cpu_score_rect.center = (WIDTH/4, HEIGHT/10)

    player_score = large_font.render("Player Score: " + str(player_score_value), True, "Black", "White")
    player_score_rect = player_score.get_rect()
    player_score_rect.center = (WIDTH - WIDTH/4, HEIGHT/10)

    card_matchup = large_font.render("", True, "Black", "White")
    card_matchup_rect = card_matchup.get_rect()
    card_matchup_rect.center = (WIDTH/2 - 100, HEIGHT/10)

    cpu_count = large_font.render("Cards left: " + str(cpu_size), True, "Black", "White")
    cpu_count_rect = cpu_count.get_rect()
    cpu_count_rect.center = (WIDTH/4, HEIGHT - HEIGHT/10)

    player_count = large_font.render("Cards left: " + str(player_size), True, "Black", "White")
    player_count_rect = player_count.get_rect()
    player_count_rect.center = (WIDTH - WIDTH/4, HEIGHT - HEIGHT/10)

    autoplay_button = large_font.render("Autoplay", True, "Black", "GRAY")
    autoplay_button_rect = autoplay_button.get_rect()
    autoplay_button_rect.center = (WIDTH/2, HEIGHT/2 + 100)

    card_one = pygame.image.load(r'./cards/back.png')
    card_one = pygame.transform.scale(card_one,(500,726))

    card_two = pygame.image.load(r'./cards/back.png')
    card_two = pygame.transform.scale(card_one,(500,726))

    f = open("scores.txt", "r+")
    cpu_score_value = int(f.readline())
    player_score_value = int(f.readline())
    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                f.close()
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                    screen.fill(GRAY)
                    if autoplay_button_rect.collidepoint(pygame.mouse.get_pos()):
                        autoplay = True
                    if deal_button_rect.collidepoint(pygame.mouse.get_pos()):
                        autoplay = False
                    player_score = large_font.render("Player Score: " + str(player_score_value), True, "Black", "White")
                    cpu_score = large_font.render("Cpu Score: " + str(cpu_score_value), True, "Black", "White")
                    cpu_count = large_font.render("Cards left: " + str(len(cpu_cards)), True, "Black", "White")
                    player_count = large_font.render("Cards left: " + str(len(player_cards)), True, "Black", "White")

                    current_time = pygame.time.get_ticks()

                    print(current_time)
                    if autoplay is False:
                        card_matchup, card_one, card_two, war_check = game_logic(get_value_of_card, compare_cards, player_cards, cpu_cards, war_list, war_check, large_font)      

                    #If someone is left with no cards, increase the other party's score, reshuffle and split deck
                    if len(player_cards) == 0 or len(cpu_cards) == 0:
                            cpu_score_value, player_score_value, player_cards, cpu_cards, deck = save_and_reset(shuffle_deck, split_deck, clock, deck, player_cards, cpu_cards, cpu_score_value, player_score_value, f)
        if autoplay is True:
            screen.fill(GRAY)
            player_score = large_font.render("Player Score: " + str(player_score_value), True, "Black", "White")
            cpu_score = large_font.render("Cpu Score: " + str(cpu_score_value), True, "Black", "White")
            cpu_count = large_font.render("Cards left: " + str(len(cpu_cards)), True, "Black", "White")
            player_count = large_font.render("Cards left: " + str(len(player_cards)), True, "Black", "White")
            now = pygame.time.get_ticks()
            if now - current_time > 100:
                card_matchup, card_one, card_two, war_check = game_logic(get_value_of_card, compare_cards, player_cards, cpu_cards, war_list, war_check, large_font)
                current_time = now
                if len(player_cards) == 0 or len(cpu_cards) == 0:
                    cpu_score_value, player_score_value, player_cards, cpu_cards, deck = save_and_reset(shuffle_deck, split_deck, clock, deck, player_cards, cpu_cards, cpu_score_value, player_score_value, f)     

        
        screen.blit(card_one, (MARGIN_LEFT,MARGIN_TOP))
        screen.blit(card_two, (MARGIN_LEFT + 950,MARGIN_TOP))
        screen.blit(deal_button, deal_button_rect)
        screen.blit(cpu_score, cpu_score_rect)
        screen.blit(player_score, player_score_rect)
        screen.blit(card_matchup, card_matchup_rect)
        screen.blit(player_count, player_count_rect)
        screen.blit(cpu_count, cpu_count_rect)
        screen.blit(autoplay_button, autoplay_button_rect)
        pygame.display.update()

        clock.tick(300)

