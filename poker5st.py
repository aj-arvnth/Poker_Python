import pygame
import random
import os
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CARD_WIDTH = 80  # Increase card width
CARD_HEIGHT = 90  # Increase card height
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLACK = (0, 0, 0)

# Get the path to the directory containing the script
script_dir = "C:/Users/Admin/Desktop/"
cards_dir = os.path.join(script_dir, "Cards")

# Load card images
def load_cards():
    card_paths = []
    for i in range(1, 14):
        for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
            card_path = os.path.join(cards_dir, f"{i}_of_{suit}.png")
            card_paths.append(card_path)
    return card_paths

# Function to draw cards
def draw_card(screen, card, x, y):
    screen.blit(card, (x, y))

# Function to display text
def display_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

# Function to check for flush strategy
def is_flush(hand):
    suits = [os.path.basename(card_path).split('_')[2].split('.')[0] for card_path in hand]
    return len(set(suits)) == 1

# Function to check for three of a kind strategy
def is_three_of_a_kind(hand):
    ranks = [int(os.path.basename(card_path).split('_')[0]) for card_path in hand]
    for rank in ranks:
        if ranks.count(rank) == 3:
            return True
    return False

# Function to check for straight strategy
def is_straight(hand):
    all_ranks = sorted([int(os.path.basename(card_path).split('_')[0]) for card_path in hand])
    return all_ranks[-1] - all_ranks[0] == 4 and len(set(all_ranks)) == 5


# Function to check for 2 pair strategy
def is_two_pair(hand):
    ranks = [int(os.path.basename(card_path).split('_')[0]) for card_path in hand]
    rank_counts = {rank: ranks.count(rank) for rank in set(ranks)}
    pairs = 0
    for count in rank_counts.values():
        if count == 2:
            pairs += 1
    return pairs == 2

# Function to check for 1 pair strategy
def is_one_pair(hand):
    ranks = [int(os.path.basename(card_path).split('_')[0]) for card_path in hand]
    rank_counts = {rank: ranks.count(rank) for rank in set(ranks)}
    pairs = 0
    for count in rank_counts.values():
        if count == 2:
            pairs += 1
    return pairs == 1

# Function to determine winner and return winning player's hand and score
def determine_winner(player_hand, player2_hand_hidden, player3_hand_hidden, dealer_hand):
    if is_straight(player_hand):
        return "You win with a Straight", player_hand
    elif is_straight(player2_hand_hidden + dealer_hand):
        return "Player 2 wins with a Straight", player2_hand_hidden
    elif is_straight(player3_hand_hidden + dealer_hand):
        return "Player 3 wins with a Straight", player3_hand_hidden
    elif is_two_pair(player_hand):
        return "You win with Two Pairs", player_hand
    elif is_two_pair(player2_hand_hidden + dealer_hand):
        return "Player 2 wins with Two Pairs", player2_hand_hidden
    elif is_two_pair(player3_hand_hidden + dealer_hand):
        return "Player 3 wins with Two Pairs", player3_hand_hidden
    elif is_one_pair(player_hand):
        return "You win with One Pair", player_hand
    elif is_one_pair(player2_hand_hidden + dealer_hand):
        return "Player 2 wins with One Pair", player2_hand_hidden
    elif is_one_pair(player3_hand_hidden + dealer_hand):
        return "Player 3 wins with One Pair", player3_hand_hidden
    elif is_flush(player_hand):
        return "You win with a Flush", player_hand
    elif is_flush(player2_hand_hidden + dealer_hand):
        return "Player 2 wins with a Flush", player2_hand_hidden
    elif is_flush(player3_hand_hidden + dealer_hand):
        return "Player 3 wins with a Flush", player3_hand_hidden
    elif is_three_of_a_kind(player_hand):
        return "You win with Three of a Kind", player_hand
    elif is_three_of_a_kind(player2_hand_hidden + dealer_hand):
        return "Player 2 wins with Three of a Kind", player2_hand_hidden
    elif is_three_of_a_kind(player3_hand_hidden + dealer_hand):
        return "Player 3 wins with Three of a Kind", player3_hand_hidden
    else:
        return "The match is a tie", []

    
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Poker Game")
    clock = pygame.time.Clock()

    # Load card images
    cards = load_cards()

    # Game variables
    player_hand = []
    dealer_hand = []

    # Font
    font = pygame.font.Font(None, 36)

    # Button variables
    yes_button_rect = pygame.Rect(250, 500, 100, 50)
    no_button_rect = pygame.Rect(450, 500, 100, 50)
    next_button_rect = pygame.Rect(650, 500, 100, 50)
    exit_button_rect = pygame.Rect(50, 500, 100, 50)
    yes_button_text = font.render("Yes", True, WHITE)
    no_button_text = font.render("No", True, WHITE)
    next_button_text = font.render("Next", True, WHITE)
    exit_button_text = font.render("Exit", True, WHITE)

    # Player heading variable
    player_heading = "Your Hand"

    # Game state variables
    game_over = False
    winner_message = ""
    tie_message = ""
    yes_button_visible = True
    no_button_visible = True
    next_button_visible = False

    # Initialize available cards
    available_cards = cards[:]

    # Initialize player's hand
    player_hand = random.sample(available_cards, 2)
    for card in player_hand:
        available_cards.remove(card)

    # Initialize dealer's hand
    dealer_hand = random.sample(available_cards, 3)
    for card in dealer_hand:
        available_cards.remove(card)

    # Initialize player 2's hidden cards
    player2_hand_hidden = random.sample(available_cards, 2)

    # Initialize player 3's hidden cards
    player3_hand_hidden = random.sample(available_cards, 2)

    # Game loop
    running = True
    while running:
        screen.fill(GREEN)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if yes_button_rect.collidepoint(event.pos) and len(dealer_hand) < 5:
                    new_card = random.choice(available_cards)
                    dealer_hand.append(new_card)
                    available_cards.remove(new_card)
                    if len(dealer_hand) == 5:
                        yes_button_visible = False
                        no_button_visible = False
                        next_button_visible = True
                elif next_button_rect.collidepoint(event.pos) and next_button_visible:
                    winner_message, winning_hand = determine_winner(player_hand, player2_hand_hidden, player3_hand_hidden, dealer_hand)
                    game_over = True
                elif no_button_rect.collidepoint(event.pos):
                    winner_message, winning_hand = determine_winner(player_hand, player2_hand_hidden, player3_hand_hidden, dealer_hand)
                    game_over = True
                    yes_button_visible = False
                    no_button_visible = False
                    next_button_visible = False
            elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
                if exit_button_rect.collidepoint(event.pos):
                    running = False

        # Display player's hand or player 2/3
        player_x = 50
        player_y = 150
        for card_path in player_hand:
            card_image = pygame.image.load(card_path).convert_alpha()
            card_image = pygame.transform.scale(card_image, (CARD_WIDTH, CARD_HEIGHT))  # Resize card image
            draw_card(screen, card_image, player_x, player_y)
            player_x += CARD_WIDTH + 10
        display_text(screen, player_heading, font, WHITE, 50, 100)

        # Display dealer's hand
        dealer_x = 50
        dealer_y = 350
        for card_path in dealer_hand:
            card_image = pygame.image.load(card_path).convert_alpha()
            card_image = pygame.transform.scale(card_image, (CARD_WIDTH, CARD_HEIGHT))  # Resize card image
            draw_card(screen, card_image, dealer_x, dealer_y)
            dealer_x += CARD_WIDTH + 10
        display_text(screen, "Deal", font, WHITE, 50, 300)

        # Draw buttons
        if yes_button_visible:
            pygame.draw.rect(screen, BLACK, yes_button_rect)
            screen.blit(yes_button_text, (yes_button_rect.centerx - yes_button_text.get_width() // 2, yes_button_rect.centery - yes_button_text.get_height() // 2))
        if no_button_visible:
            pygame.draw.rect(screen, BLACK, no_button_rect)
            screen.blit(no_button_text, (no_button_rect.centerx - no_button_text.get_width() // 2, no_button_rect.centery - no_button_text.get_height() // 2))
        if next_button_visible:
            pygame.draw.rect(screen, BLACK, next_button_rect)
            screen.blit(next_button_text, (next_button_rect.centerx - next_button_text.get_width() // 2, next_button_rect.centery - next_button_text.get_height() // 2))
        pygame.draw.rect(screen, BLACK, exit_button_rect)
        screen.blit(exit_button_text, (exit_button_rect.centerx - exit_button_text.get_width() // 2, exit_button_rect.centery - exit_button_text.get_height() // 2))

        # Display winner message if game is over
        if game_over:
            if winner_message == "The match is a tie":
                display_text(screen, winner_message, font, WHITE, 300, 500)

                # Display Player 2's hand
                player2_x = 50
                player2_y = 250
                for card_path in player2_hand_hidden:
                    card_image = pygame.image.load(card_path).convert_alpha()
                    card_image = pygame.transform.scale(card_image, (CARD_WIDTH, CARD_HEIGHT))  # Resize card image
                    draw_card(screen, card_image, player2_x, player2_y)
                    player2_x += CARD_WIDTH + 10
                display_text(screen, "Player 2's Hand", font, WHITE, 250, 50)

                # Display Player 3's hand
                player3_x = 50
                player3_y = 150
                for card_path in player3_hand_hidden:
                    card_image = pygame.image.load(card_path).convert_alpha()
                    card_image = pygame.transform.scale(card_image, (CARD_WIDTH, CARD_HEIGHT))  # Resize card image
                    draw_card(screen, card_image, player3_x, player3_y)
                    player3_x += CARD_WIDTH + 10
                display_text(screen, "Player 3's Hand", font, WHITE, 250, 50)

            else:
                display_text(screen, winner_message, font, WHITE, 300, 500)

                # Display the winning hand
                winning_x = 50
                winning_y = 50
                for card_path in winning_hand:
                    card_image = pygame.image.load(card_path).convert_alpha()
                    card_image = pygame.transform.scale(card_image, (CARD_WIDTH, CARD_HEIGHT))
                                        # Resize card image
                    draw_card(screen, card_image, winning_x, winning_y)
                    winning_x += CARD_WIDTH + 10
                display_text(screen, "Winning Hand", font, WHITE, 250, 50)

                # Display dealer's hand
                dealer_x = 50
                dealer_y = 350
                for card_path in dealer_hand:
                    card_image = pygame.image.load(card_path).convert_alpha()
                    card_image = pygame.transform.scale(card_image, (CARD_WIDTH, CARD_HEIGHT))  # Resize card image
                    draw_card(screen, card_image, dealer_x, dealer_y)
                    dealer_x += CARD_WIDTH + 10
                display_text(screen, "Deal", font, WHITE, 50, 300)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

                                                        

if __name__ == "__main__":
    main()

