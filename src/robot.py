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
FEELER_COUNT = 24
FEELER_LENGTH = 80
FOV = 360
FORWARD_SPEED = 0.6  # Tunable speed variable
TURN_SPEED = 1.4  # Tunable turning speed

class Robot:
    position = (0, 0)
    heading = 0
    waypoint = (MAP_WIDTH / 2, MAP_HEIGHT / 8)  # Default waypoint at top middle
    
    def __init__(self, game: Game):
        self.game = game
        
        # Start at the bottom middle
        self.position = (MAP_WIDTH / 2, MAP_HEIGHT - (MAP_HEIGHT / 8))
        
        # Start facing east (right)
        self.heading = 270

        # Start with no velocity
        self.current_velocity = 0
        
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
        self.draw_feelers(screen)
        
    def run(self, do_recalc):
        MIN_DISTANCE = 20
        feeler_distances = self.get_feeler_distances()
        left_feelers = feeler_distances[:FEELER_COUNT // 3]
        front_feelers = feeler_distances[FEELER_COUNT // 3: 2 * (FEELER_COUNT // 3)]
        right_feelers = feeler_distances[2 * (FEELER_COUNT // 3):]

        min_front_distance = min(front_feelers)
        min_left_distance = min(left_feelers)
        min_right_distance = min(right_feelers)
        
        # Compute direction to waypoint
        target_angle = math.degrees(math.atan2(self.waypoint[1] - self.position[1], self.waypoint[0] - self.position[0]))
        heading_error = (target_angle - self.getHeading() + 360) % 360
        if heading_error > 180:
            heading_error -= 360
        
        if min_front_distance < MIN_DISTANCE:
            if min_right_distance > min_left_distance:
                self.heading -= TURN_SPEED
            else:
                self.heading += TURN_SPEED
            if min_left_distance < MIN_DISTANCE and min_right_distance < MIN_DISTANCE:
                self.current_velocity = -FORWARD_SPEED
            else:
                self.current_velocity = 0
        else:
            self.current_velocity = FORWARD_SPEED

            # get distance to waypoint
            distance_to_waypoint = math.sqrt((self.waypoint[0] - self.position[0]) ** 2 + (self.waypoint[1] - self.position[1]) ** 2)

            # expoentionally become more aggressive to waypoint as distance to it decreases
            # self.heading += (heading_error / 20) * (1 - (distance_to_waypoint / 450)) * 0.8
        
        self.position = (
            self.position[0] + self.current_velocity * math.cos(math.radians(self.getHeading())),
            self.position[1] - self.current_velocity * math.sin(math.radians(self.getHeading()))
        )
        
    def get_feeler_distances(self):
        distances = []
        angle_step = FOV / (FEELER_COUNT - 1)
        start_angle = self.getHeading() - (FOV / 2)
                
        for i in range(FEELER_COUNT):
            angle = start_angle + (angle_step * i)
            end_x = self.position[0] + FEELER_LENGTH * math.cos(math.radians(angle))
            end_y = self.position[1] - FEELER_LENGTH * math.sin(math.radians(angle))
            feeler = (self.position, (end_x, end_y))
            
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
            angle = start_angle + (angle_step * i)
            end_x = self.position[0] + FEELER_LENGTH * math.cos(math.radians(angle))
            end_y = self.position[1] - FEELER_LENGTH * math.sin(math.radians(angle))
            feeler = (self.position, (end_x, end_y))
            
            intersection_point = self.feeler_intersects(feeler)
            if intersection_point:
                pygame.draw.line(screen, (255, 0, 0), self.position, intersection_point)
            else:
                pygame.draw.line(screen, FEELER_COLOR, self.position, (end_x, end_y))
                
    def feeler_intersects(self, feeler):
        closest_intersection = None
        closest_distance = 99999
        for line in self.game.lanes:
            intersection = calculate_line_intersection(feeler, line)
            if intersection:
                distance = math.sqrt((intersection[0] - self.position[0]) ** 2 + (intersection[1] - self.position[1]) ** 2)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_intersection = intersection
                
        return closest_intersection