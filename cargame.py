import pygame
from pygame.locals import *
import random
import time

class Window:
    """ application window object """
    def __init__(self):
        # set window parameters
        self.width = 800
        self.height = 800
        self.window = pygame.display.set_mode((self.width, self.height))
        self.window.fill((88, 169, 201))  # Updated background color
        
        # set road parameters
        self.road_width = int(self.width/1.6)
        self.roadmark_width = int(self.width/80)
        self.right_lane = self.width/2 + self.road_width/4
        self.left_lane = self.width/2 - self.road_width/4
        
    def draw_background(self):
        """
        a method that draws a road
        """
        # draw road
        pygame.draw.rect(
            self.window,
            (50, 50, 50),
            (self.width/2-self.road_width/2, 0, self.road_width, self.height))
        # draw centre line
        pygame.draw.rect(
            self.window,
            (255, 240, 60),
            (self.width/2 - self.roadmark_width/2, 0, self.roadmark_width, self.height))
        # draw left road marking
        pygame.draw.rect(
            self.window,
            (255, 255, 255),
            (self.width/2 - self.road_width/2 + self.roadmark_width*2, 0, self.roadmark_width, self.height))
        # draw right road marking
        pygame.draw.rect(
            self.window,
            (255, 255, 255),
            (self.width/2 + self.road_width/2 - self.roadmark_width*3, 0, self.roadmark_width, self.height))

class CarGame:
    """ game loop and logic """
    def __init__(self):
        self.player = Player()
        self.enemy_vehicle = EnemyVehicle()
        self.counter = 0
        self.running = False
        self.level = 0
        self.font = pygame.font.SysFont('Serif-sans', 45)  # Add font for stopwatch and messages
        self.start_time = time.time()  # Record the start time
        self.level_up_message = False
        self.level_up_time = 0
        self.clock = pygame.time.Clock()  # Clock to control frame rate
        
        self.start_game()
        self.start_gameloop()
        
    def create_enemy(self):
        """
        a method that generates an enemy object
        """
        # if enemy vehicle is lower than the window (left the scene)
        if self.enemy_vehicle.location[1] > window.height:
            # randomly select lane
            if random.randint(0, 1) == 0:
                self.enemy_vehicle.location.center = window.right_lane, -200
            else:
                self.enemy_vehicle.location.center = window.left_lane, -200  
            
    def level_up(self):
        """
        level and difficulty increase logic
        """
        # start counting
        self.counter += 1  

        # increase game speed as count increases
        if self.counter == 1000:  # Adjusted for more frequent level ups
            self.enemy_vehicle.speed += 1  # Increased speed increment
            self.level += 1
            # reset counter
            self.counter = 0
            self.draw_level_up()
            
    def key_controls(self):
        """
        a method that stores keyboard logic
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                # collapse the app
                self.running = False
            if event.type == KEYDOWN:
                # move user car to the left
                if event.key in [K_a, K_LEFT]:
                    self.player.location = self.player.location.move([-int(window.road_width/2), 0])
                # move user car to the right
                if event.key in [K_d, K_RIGHT]:
                    self.player.location = self.player.location.move([int(window.road_width/2), 0])
                
    def draw_stopwatch(self):
        """
        a method to draw the stopwatch on the screen
        """
        elapsed_time = time.time() - self.start_time
        elapsed_time_str = f"Time: {int(elapsed_time)}s"
        text_surface = self.font.render(elapsed_time_str, True, (0, 0, 0))
        
        # Clear the area where the text will be drawn
        text_background = pygame.Rect(10, 10, 130, 30)  # Adjust the size as needed
        window.window.fill((88, 169, 201), text_background)  # Updated background color
        
        # Draw the new text
        window.window.blit(text_surface, (10, 10))

    def draw_level_up(self):
        """
        a method to draw the level up message on the screen
        """
        self.level_up_message = True
        self.level_up_time = time.time()
        
    def display_level_up(self):
        """
        a method to display the level up message on the screen
        """
        if self.level_up_message:
            level_up_str = f"LEVEL UP! Level: {self.level}"
            level_up_surface = self.font.render(level_up_str, True, (0, 255, 0))
            
            # Calculate position for centering the text
            level_up_rect = level_up_surface.get_rect(center=(window.width/2, window.height/2))
            
            # Draw the level up message
            window.window.blit(level_up_surface, level_up_rect)
            
            # Remove the message after 2 seconds
            if time.time() - self.level_up_time > 2:
                self.level_up_message = False
            
    def draw_game_over(self):
        """
        a method to draw the game over message and replay prompt on the screen
        """
        game_over_str = "GAME OVER! YOU LOST!"
        replay_str = "Press R to Replay or Q to Quit"
        game_over_surface = self.font.render(game_over_str, True, (255, 0, 0))
        replay_surface = self.font.render(replay_str, True, (255, 255, 255))
        
        # Calculate positions for centering the text
        game_over_rect = game_over_surface.get_rect(center=(window.width/2, window.height/2 - 30))
        replay_rect = replay_surface.get_rect(center=(window.width/2, window.height/2 + 30))
        
        # Draw the game over message and replay prompt
        window.window.blit(game_over_surface, game_over_rect)
        window.window.blit(replay_surface, replay_rect)
        
        # Apply changes
        pygame.display.update()

        # Wait for the player to press R or Q
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        self.__init__()  # Restart the game
                    if event.key == K_q:
                        pygame.quit()
                        exit()

    def check_off_road(self):
        """
        Check if the player has moved off the road and trigger game over
        """
        if self.player.location.left < (window.width/2 - window.road_width/2) or self.player.location.right > (window.width/2 + window.road_width/2):
            self.running = False
            self.draw_game_over()

    def start_game(self):
        """
        a method that initializes a new game
        """
        # initialize pygame
        pygame.display.set_caption("Henry's car game")
        # initialize game loop parameters
        self.running = True
               
    def start_gameloop(self):
        """
        a method that initiallizes the game loop
        """
        # start game loop
        while self.running:   
            # generate the next enemy
            self.create_enemy()
            # add level up logic
            self.level_up()
            # animate enemy vehicle
            self.enemy_vehicle.location[1] += self.enemy_vehicle.speed
            
            # game over logic
            if self.player.location.colliderect(self.enemy_vehicle.location):
                self.running = False
                self.draw_game_over()
                break
            
            # check if player is off the road
            self.check_off_road()
            
            # initialize key controls
            self.key_controls()
            # draw road
            window.draw_background()
            # draw stopwatch
            self.draw_stopwatch()
            # display level up message if active
            self.display_level_up()
            # place player car
            window.window.blit(self.player.car, self.player.location)
            # place enemy car
            window.window.blit(self.enemy_vehicle.car, self.enemy_vehicle.location)
            # apply changes
            pygame.display.update()

            # Control frame rate
            self.clock.tick(60)

        # collapse application window if game over
        pygame.quit()   

class Player:
    """ player object """
    def __init__(self):
        self.car = pygame.image.load("car.png")
        self.location = self.car.get_rect()
        self.location.center = window.right_lane, window.height*0.8

class EnemyVehicle:
    """ enemy vehicle object """
    def __init__(self):
        self.speed = 7  # Increased initial speed
        self.length = 250
        self.img_path = "otherCar.png"
        self.draw_car()
        
    def draw_car(self):
        self.car = pygame.image.load(self.img_path)
        self.location = self.car.get_rect()
        self.location.center = window.left_lane, window.height*0.2
 
# start game and main loop
if __name__ == "__main__":
    pygame.init()
    window = Window()
    game = CarGame()
