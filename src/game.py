import pygame
from constants import *

from scipy.special import comb
import numpy as np


class Game:
    def __init__(self):
        self.lanes = []
        
        control_points = [(MAP_WIDTH / 2 - 50, MAP_HEIGHT), (MAP_WIDTH // 3, MAP_HEIGHT // 3), (MAP_WIDTH, MAP_HEIGHT // 4)]
        lane = self.bezier_curve(control_points, 100)
        for i in range(len(lane) - 1):
            self.lanes.append(lane[i])
            
        control_points = [(MAP_WIDTH / 2 + 50, MAP_HEIGHT), (MAP_WIDTH // 2, MAP_HEIGHT // 2), (MAP_WIDTH, MAP_HEIGHT // 2)]
        lane = self.bezier_curve(control_points, 100)
        for i in range(len(lane) - 1):
            self.lanes.append(lane[i])

    def bezier_curve(self, control_points, resolution):
        n = len(control_points) - 1
        t_values = np.linspace(0, 1, resolution)
        curve_points = []
        
        for t in t_values:
            x = sum(comb(n, i) * (t ** i) * ((1 - t) ** (n - i)) * control_points[i][0] for i in range(n + 1))
            y = sum(comb(n, i) * (t ** i) * ((1 - t) ** (n - i)) * control_points[i][1] for i in range(n + 1))
            curve_points.append((x, y))
        
        # Generate line segments
        line_segments = [(curve_points[i], curve_points[i + 1]) for i in range(len(curve_points) - 1)]
        
        return line_segments

    def draw(self, screen):
        for lane in self.lanes:
            pygame.draw.line(screen, LANE_COLOR, lane[0], lane[1])