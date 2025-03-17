import pygame
from constants import *
import math
from game import Game
from lines import calculate_line_intersection
import time


# Robot Constants
ROBOT_SIZE = 5
ROBOT_COLOR = (255, 0, 0)
FEELER_COLOR = (0, 255, 0)
FEELER_COUNT = 36
FEELER_LENGTH = 60
FOV = 120


class Robot:
    position = (0, 0)
    heading = 0
    
    def __init__(self, game: Game):
        self.game = game
        
        # Start at the bottom middle
        self.position = (MAP_WIDTH / 2, MAP_HEIGHT - (MAP_HEIGHT / 8))
        
        # Start facing east (right)
        self.heading = 270
        
    def getHeading(self):
        return self.heading + 90
    
    def draw(self, screen: pygame.Surface):        
        # Just draw a circle
        pygame.draw.circle(screen, ROBOT_COLOR, self.position, ROBOT_SIZE)
        
        # Draw a small arrow to indicate the heading
        end_x = self.position[0] + 10 * math.cos(math.radians(self.getHeading()))
        end_y = self.position[1] - 10 * math.sin(math.radians(self.getHeading()))
        pygame.draw.line(screen, ROBOT_COLOR, self.position, (end_x, end_y))
        
        # Draw the feelers
        feeler_start = time.time()
        self.draw_feelers(screen)
        feeler_end = time.time()
        
        # print elapsed time in ms
        print(f"Feeler time: {(feeler_end - feeler_start) * 1000}ms")
        
    def run(self):
        # get the feeler lines
        feeler_distances = self.get_feeler_distances()
        
        # get the feeler angles
        feeler_angles = []
        angle_step = FOV / (FEELER_COUNT - 1)
        start_angle = self.getHeading() - (FOV / 2)
        for i in range(FEELER_COUNT):
            feeler_angles.append(start_angle + (angle_step * i))
            
        # closer feelers represent obstacles
        # try and avoid them
        weights = [1 / d for d in feeler_distances]
        total_weight = sum(weights)
        if total_weight > 0:
            weights = [w / total_weight for w in weights]

        # calculate the new heading
        new_heading = 0
        for i in range(FEELER_COUNT):
            new_heading += weights[i] * feeler_angles[i]

        # update the heading
        self.heading = new_heading
        
    def get_feeler_distances(self):
        distances = []
        angle_step = FOV / (FEELER_COUNT - 1)
        start_angle = self.getHeading() - (FOV / 2)
                
        for i in range(FEELER_COUNT):
            # first calculate the feeler line
            angle = start_angle + (angle_step * i)
            end_x = self.position[0] + FEELER_LENGTH * math.cos(math.radians(angle))
            end_y = self.position[1] - FEELER_LENGTH * math.sin(math.radians(angle))
            feeler = (self.position, (end_x, end_y))
            
            # check if the feeler intersects with any of the lines
            intersection_point = self.feeler_intersects(feeler)
            if intersection_point:
                distances.append(math.sqrt((intersection_point[0] - self.position[0]) ** 2 + (intersection_point[1] - self.position[1]) ** 2))
            else:
                distances.append(99999)
                
        return distances
        
    def draw_feelers(self, screen: pygame.Surface):
        angle_step = FOV / (FEELER_COUNT - 1)
        start_angle = self.getHeading() - (FOV / 2)
                
        for i in range(FEELER_COUNT):
            # first calculate the feeler line
            angle = start_angle + (angle_step * i)
            end_x = self.position[0] + FEELER_LENGTH * math.cos(math.radians(angle))
            end_y = self.position[1] - FEELER_LENGTH * math.sin(math.radians(angle))
            feeler = (self.position, (end_x, end_y))
            
            # check if the feeler intersects with any of the lines
            intersection_point = self.feeler_intersects(feeler)
            if intersection_point:
                pygame.draw.line(screen, (255, 0, 0), self.position, intersection_point)
            else:
                pygame.draw.line(screen, FEELER_COLOR, self.position, (end_x, end_y))
                
    def feeler_intersects(self, feeler):
        for line in self.game.lanes:
            intersection = calculate_line_intersection(feeler, line)
            if intersection:
                return intersection
        return None