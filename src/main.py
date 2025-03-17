from constants import *
from robot import Robot
from game import Game
import pygame


# PyGame Initialization
pygame.init()
screen = pygame.display.set_mode((MAP_WIDTH, MAP_HEIGHT))
clock = pygame.time.Clock()

# Robot/Map Initialization
game = Game()
robot = Robot(game)

# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Clear the screen
    screen.fill(BACKGROUND_COLOR)
    
    # Draw the game (map)
    game.draw(screen)
    
    # Run the robot
    robot.run()
    
    # Draw the robot
    robot.draw(screen)
    
    # Update the screen
    pygame.display.flip()
    
    # Limit the frame rate
    clock.tick(FRAME_RATE)