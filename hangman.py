import pygame
import random
import sys
import os
from pygame import mixer

# Try to import custom words
try:
    from custom_words import get_custom_categories
    has_custom_words = True
except ImportError:
    has_custom_words = False

# Initialize pygame
pygame.init()
mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
DARK_BLUE = (0, 0, 150)
AWS_ORANGE = (255, 153, 0)
AWS_BLUE = (35, 47, 62)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AWS Cloud Services Hangman Game")

# Load background images
background_images = {}
background_images["main"] = None
try:
    # Load background image from local file
    images_dir = os.path.join(os.path.dirname(__file__), "images")
    bg_path = os.path.join(images_dir, "aws_bg.jpg")
    if os.path.exists(bg_path):
        background_images["main"] = pygame.image.load(bg_path)
        background_images["main"] = pygame.transform.scale(background_images["main"], (SCREEN_WIDTH, SCREEN_HEIGHT))
        print("Background image loaded successfully.")
    else:
        print("Background image not found. Place an image named 'aws_bg.jpg' in the 'images' folder.")
except Exception as e:
    print(f"Error loading background image: {e}")

# Create a semi-transparent overlay for better text readability
overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
overlay.fill((255, 255, 255, 180))  # White with 70% opacity

# Fonts
font = pygame.font.SysFont('Arial', 32)
small_font = pygame.font.SysFont('Arial', 24)
letter_font = pygame.font.SysFont('Arial', 40)
title_font = pygame.font.SysFont('Arial', 50)

# Word categories
word_categories = {
    # Default categories will be replaced by AWS categories from custom_words.py
}

# Add AWS categories
if has_custom_words:
    custom_categories = get_custom_categories()
    word_categories.update(custom_categories)
else:
    # Fallback categories if custom_words.py is not available
    word_categories = {
        "AWS Compute": ["EC2", "LAMBDA", "FARGATE", "LIGHTSAIL", "BEANSTALK"],
        "AWS Storage": ["S3", "EBS", "EFS", "GLACIER", "SNOWBALL"],
        "AWS Database": ["RDS", "DYNAMODB", "AURORA", "REDSHIFT", "NEPTUNE"]
    }

# Sound effects
try:
    correct_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds", "correct.mp3"))
    wrong_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds", "wrong.mp3"))
    win_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds", "win.mp3"))
    lose_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds", "lose.mp3"))
except:
    # If sounds can't be loaded, create dummy sounds
    correct_sound = pygame.mixer.Sound(buffer=bytearray(100))
    wrong_sound = pygame.mixer.Sound(buffer=bytearray(100))
    win_sound = pygame.mixer.Sound(buffer=bytearray(100))
    lose_sound = pygame.mixer.Sound(buffer=bytearray(100))
    print("Warning: Sound files not found. Creating game without sound effects.")

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=BLACK, font=font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.current_color = color
        self.font = font
        self.text_surface = self.font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        surface.blit(self.text_surface, self.text_rect)
        
    def check_hover(self, pos):
        if self.rect.collidepoint(pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.color
            
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pos):
                return True
        return False
        
    def update_text(self, new_text):
        """Update the button text and recalculate text position"""
        self.text = new_text
        self.text_surface = self.font.render(new_text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

class Hangman:
    def __init__(self):
        self.game_state = "menu"  # menu, category_select, playing, game_over
        self.word = ""
        self.category = ""
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.max_wrong_guesses = 6
        self.score = 0
        self.games_played = 0
        self.current_page = 0  # For category pagination
        self.categories_per_page = 3  # Reduced from 4 to 3 to accommodate larger buttons
        
        # Create buttons
        self.play_button = Button(300, 250, 200, 60, "Play Game", GREEN, (100, 255, 100))
        self.menu_button = Button(300, 450, 200, 60, "Main Menu", WHITE, (45, 57, 72))
        self.play_again_button = Button(300, 350, 200, 60, "Play Again", GREEN, (100, 255, 100))
        
        # Navigation buttons for categories
        self.prev_button = Button(200, 500, 100, 40, "Previous", AWS_ORANGE, (45, 57, 72), font=small_font)
        self.next_button = Button(500, 500, 100, 40, "Next", AWS_ORANGE, (45, 57, 72), font=small_font)
        
        # Create category buttons
        self.category_buttons = []
        self.create_category_buttons()
        
        # Create letter buttons
        self.letter_buttons = []
        self.create_letter_buttons()
        
    def create_category_buttons(self):
        self.category_buttons = []
        categories = list(word_categories.keys())
        start_idx = self.current_page * self.categories_per_page
        end_idx = min(start_idx + self.categories_per_page, len(categories))
        
        # Center the buttons vertically based on how many we have
        total_height = (end_idx - start_idx) * 80  # 80px per button with spacing
        start_y = (SCREEN_HEIGHT - total_height) // 2
        
        for i in range(start_idx, end_idx):
            y_pos = start_y + (i - start_idx) * 80
            category = categories[i]
            # Make category buttons wider and taller
            button = Button(SCREEN_WIDTH//2, y_pos, 350, 60, category, AWS_BLUE, (45, 57, 72), text_color=WHITE, font=font)
            
            # Center the button horizontally
            button.rect.centerx = SCREEN_WIDTH // 2
            button.text_rect.centerx = button.rect.centerx
            
            self.category_buttons.append(button)
        
    def create_letter_buttons(self):
        self.letter_buttons = []
        # First row (A-J)
        x_start = 150
        y_pos = 400
        for i, letter in enumerate("ABCDEFGHIJ"):
            self.letter_buttons.append(Button(x_start + i*50, y_pos, 40, 40, letter, GRAY, (220, 220, 220), font=small_font))
        
        # Second row (K-T)
        y_pos = 450
        for i, letter in enumerate("KLMNOPQRST"):
            self.letter_buttons.append(Button(x_start + i*50, y_pos, 40, 40, letter, GRAY, (220, 220, 220), font=small_font))
        
        # Third row (U-Z)
        y_pos = 500
        for i, letter in enumerate("UVWXYZ"):
            self.letter_buttons.append(Button(x_start + i*50 + 100, y_pos, 40, 40, letter, GRAY, (220, 220, 220), font=small_font))
    
    def select_word(self, category):
        self.category = category
        self.word = random.choice(word_categories[category])
        self.guessed_letters = set()
        self.wrong_guesses = 0
    
    def check_guess(self, letter):
        self.guessed_letters.add(letter)
        if letter in self.word:
            correct_sound.play()
            return True
        else:
            self.wrong_guesses += 1
            wrong_sound.play()
            return False
    
    def is_word_guessed(self):
        return all(letter in self.guessed_letters for letter in self.word)
    
    def draw_hangman(self):
        # Base
        pygame.draw.line(screen, BLACK, (150, 350), (250, 350), 5)
        
        # Pole
        if self.wrong_guesses >= 1:
            pygame.draw.line(screen, BLACK, (200, 350), (200, 100), 5)
        
        # Top beam
        if self.wrong_guesses >= 2:
            pygame.draw.line(screen, BLACK, (200, 100), (300, 100), 5)
        
        # Rope
        if self.wrong_guesses >= 3:
            pygame.draw.line(screen, BLACK, (300, 100), (300, 150), 5)
        
        # Head
        if self.wrong_guesses >= 4:
            pygame.draw.circle(screen, BLACK, (300, 170), 20, 3)
        
        # Body
        if self.wrong_guesses >= 5:
            pygame.draw.line(screen, BLACK, (300, 190), (300, 250), 3)
            # Arms
            pygame.draw.line(screen, BLACK, (300, 210), (270, 230), 3)
            pygame.draw.line(screen, BLACK, (300, 210), (330, 230), 3)
        
        # Legs
        if self.wrong_guesses >= 6:
            pygame.draw.line(screen, BLACK, (300, 250), (270, 300), 3)
            pygame.draw.line(screen, BLACK, (300, 250), (330, 300), 3)
    
    def draw_word(self):
        word_display = ""
        for letter in self.word:
            if letter in self.guessed_letters:
                word_display += letter + " "
            else:
                word_display += "_ "
        
        word_surface = letter_font.render(word_display, True, BLACK)
        word_rect = word_surface.get_rect(center=(SCREEN_WIDTH//2, 300))
        screen.blit(word_surface, word_rect)
    
    def draw_menu(self):
        # Draw background if available
        if background_images["main"]:
            screen.blit(background_images["main"], (0, 0))
            screen.blit(overlay, (0, 0))
        else:
            screen.fill(WHITE)
            
        title = title_font.render("AWS Cloud Services", True, AWS_BLUE)
        subtitle = font.render("Hangman Game", True, AWS_ORANGE)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 120))
        screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 180))
        self.play_button.draw(screen)
    
    def draw_category_select(self):
        # Draw background if available
        if background_images["main"]:
            screen.blit(background_images["main"], (0, 0))
            screen.blit(overlay, (0, 0))
        else:
            screen.fill(WHITE)
            
        title = font.render("Select an AWS Category", True, AWS_BLUE)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 80))
        
        # Draw AWS logo text
        aws_text = font.render("AWS Cloud Services Hangman", True, AWS_ORANGE)
        screen.blit(aws_text, (SCREEN_WIDTH//2 - aws_text.get_width()//2, 40))
        
        for button in self.category_buttons:
            button.draw(screen)
            
        # Draw pagination info
        total_pages = (len(word_categories) + self.categories_per_page - 1) // self.categories_per_page
        page_text = small_font.render(f"Page {self.current_page + 1}/{total_pages}", True, BLACK)
        screen.blit(page_text, (SCREEN_WIDTH//2 - page_text.get_width()//2, 520))
        
        # Draw navigation buttons if needed
        if self.current_page > 0:
            self.prev_button.draw(screen)
        if (self.current_page + 1) * self.categories_per_page < len(word_categories):
            self.next_button.draw(screen)
    
    def draw_game(self):
        # Draw background if available
        if background_images["main"]:
            screen.blit(background_images["main"], (0, 0))
            screen.blit(overlay, (0, 0))
        else:
            screen.fill(WHITE)
        
        # Draw category
        category_text = font.render(f"Category: {self.category}", True, AWS_BLUE)
        screen.blit(category_text, (20, 20))
        
        # Draw hangman
        self.draw_hangman()
        
        # Draw word
        self.draw_word()
        
        # Draw guesses left
        guesses_text = small_font.render(f"Guesses Left: {self.max_wrong_guesses - self.wrong_guesses}", True, BLACK)
        screen.blit(guesses_text, (SCREEN_WIDTH - guesses_text.get_width() - 20, 20))
        
        # Draw AWS logo text
        aws_text = small_font.render("AWS Cloud Services", True, AWS_ORANGE)
        screen.blit(aws_text, (SCREEN_WIDTH//2 - aws_text.get_width()//2, 50))
        
        # Draw letter buttons
        for button in self.letter_buttons:
            # If letter has been guessed, disable the button
            if button.text in self.guessed_letters:
                if button.text in self.word:
                    button.current_color = GREEN
                else:
                    button.current_color = RED
            button.draw(screen)
    
    def draw_game_over(self):
        # Draw background if available
        if background_images["main"]:
            screen.blit(background_images["main"], (0, 0))
            screen.blit(overlay, (0, 0))
        else:
            screen.fill(WHITE)
        
        if self.is_word_guessed():
            result_text = title_font.render("You Win!", True, GREEN)
        else:
            result_text = title_font.render("Game Over", True, RED)
        
        screen.blit(result_text, (SCREEN_WIDTH//2 - result_text.get_width()//2, 120))
        
        # Draw AWS logo text
        aws_text = font.render("AWS Cloud Services", True, AWS_ORANGE)
        screen.blit(aws_text, (SCREEN_WIDTH//2 - aws_text.get_width()//2, 80))
        
        word_text = font.render(f"The service was: {self.word}", True, AWS_BLUE)
        screen.blit(word_text, (SCREEN_WIDTH//2 - word_text.get_width()//2, 200))
        
        score_text = font.render(f"Score: {self.score}/{self.games_played}", True, BLACK)
        screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 250))
        
        # Update button positions for better spacing
        self.play_again_button.rect.centery = 350
        self.play_again_button.rect.centerx = SCREEN_WIDTH // 2
        self.play_again_button.text_rect = self.play_again_button.text_surface.get_rect(center=self.play_again_button.rect.center)
        
        self.menu_button.rect.centery = 450
        self.menu_button.rect.centerx = SCREEN_WIDTH // 2
        self.menu_button.text_rect = self.menu_button.text_surface.get_rect(center=self.menu_button.rect.center)
        
        self.play_again_button.draw(screen)
        self.menu_button.draw(screen)
    
    def reset_game(self):
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.create_letter_buttons()
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if self.game_state == "menu":
                    self.play_button.check_hover(mouse_pos)
                    if self.play_button.is_clicked(mouse_pos, event):
                        self.game_state = "category_select"
                
                elif self.game_state == "category_select":
                    for i, button in enumerate(self.category_buttons):
                        button.check_hover(mouse_pos)
                        if button.is_clicked(mouse_pos, event):
                            start_idx = self.current_page * self.categories_per_page
                            category = list(word_categories.keys())[start_idx + i]
                            self.select_word(category)
                            self.game_state = "playing"
                            self.games_played += 1
                    
                    # Check navigation buttons
                    if self.current_page > 0:
                        self.prev_button.check_hover(mouse_pos)
                        if self.prev_button.is_clicked(mouse_pos, event):
                            self.current_page -= 1
                            self.create_category_buttons()
                    
                    if (self.current_page + 1) * self.categories_per_page < len(word_categories):
                        self.next_button.check_hover(mouse_pos)
                        if self.next_button.is_clicked(mouse_pos, event):
                            self.current_page += 1
                            self.create_category_buttons()
                
                elif self.game_state == "playing":
                    for button in self.letter_buttons:
                        if button.text not in self.guessed_letters:
                            button.check_hover(mouse_pos)
                            if button.is_clicked(mouse_pos, event):
                                self.check_guess(button.text)
                                
                                # Check if game is over
                                if self.is_word_guessed():
                                    self.score += 1
                                    win_sound.play()
                                    self.game_state = "game_over"
                                elif self.wrong_guesses >= self.max_wrong_guesses:
                                    lose_sound.play()
                                    self.game_state = "game_over"
                
                elif self.game_state == "game_over":
                    self.play_again_button.check_hover(mouse_pos)
                    self.menu_button.check_hover(mouse_pos)
                    
                    if self.play_again_button.is_clicked(mouse_pos, event):
                        self.reset_game()
                        self.game_state = "category_select"
                    
                    if self.menu_button.is_clicked(mouse_pos, event):
                        self.reset_game()
                        self.game_state = "menu"
            
            # Draw the appropriate screen based on game state
            if self.game_state == "menu":
                self.draw_menu()
            elif self.game_state == "category_select":
                self.draw_category_select()
            elif self.game_state == "playing":
                self.draw_game()
            elif self.game_state == "game_over":
                self.draw_game_over()
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    # Create sounds directory if it doesn't exist
    os.makedirs(os.path.join(os.path.dirname(__file__), "sounds"), exist_ok=True)
    
    game = Hangman()
    game.run()
