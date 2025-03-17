import pygame
from constants import *

from scipy.special import comb
import numpy as np


class Game:
    def __init__(self):
        self.lanes = []
        
        # Outer Lane
        lines = self.rounded_rectangle(MAP_WIDTH // 2, MAP_HEIGHT // 2, MAP_WIDTH - 100, MAP_HEIGHT - 100, 50)
        for line in lines:
            self.lanes.append(line)

        # Inner Lane
        lines = self.rounded_rectangle(MAP_WIDTH // 2, MAP_HEIGHT // 2, MAP_WIDTH - (100 + LANE_WIDTH), MAP_HEIGHT - (100 + LANE_WIDTH), 50)
        for line in lines:
            self.lanes.append(line)

        # draw a small rounded rectangle as a "barrel" on the right side that touches the inner lane (inside the lanes for reference)
        lines = self.rounded_rectangle(MAP_WIDTH - 60, MAP_HEIGHT // 2 - 70, 16, 16, 25)
        for line in lines:
            self.lanes.append(line)

        # draw a small rounded rectangle as a "barrel" on the right side that touches the inner lane (inside the lanes for reference)
        lines = self.rounded_rectangle(MAP_WIDTH - 76, MAP_HEIGHT // 2 - 70, 16, 16, 25)
        for line in lines:
            self.lanes.append(line)

        # draw one above it by 60 pxels
        lines = self.rounded_rectangle(MAP_WIDTH - 116, MAP_HEIGHT // 2, 16, 16, 25)
        for line in lines:
            self.lanes.append(line)

        # draw one above it by 60 pxels
        lines = self.rounded_rectangle(MAP_WIDTH - 100, MAP_HEIGHT // 2, 16, 16, 25)
        for line in lines:
            self.lanes.append(line)

        # draw a small rounded rectangle as a "barrel" on the right side that touches the inner lane (inside the lanes for reference)
        lines = self.rounded_rectangle(MAP_WIDTH - (MAP_WIDTH // 4.3), MAP_HEIGHT // 2 + 182, 16, 16, 25)
        for line in lines:
            self.lanes.append(line)

        # draw a small rounded rectangle as a "barrel" on the right side that touches the inner lane (inside the lanes for reference)
        lines = self.rounded_rectangle(MAP_WIDTH - (MAP_WIDTH // 4.3), MAP_HEIGHT // 2 + 244, 16, 16, 25)
        for line in lines:
            self.lanes.append(line)

        # draw one above it by 60 pxels
        lines = self.rounded_rectangle(MAP_WIDTH - 80, MAP_HEIGHT // 4, 16, 16, 25)
        for line in lines:
            self.lanes.append(line)

                # draw one above it by 60 pxels
        lines = self.rounded_rectangle(MAP_WIDTH - 70, MAP_HEIGHT - (MAP_HEIGHT // 4), 16, 16, 25)
        for line in lines:
            self.lanes.append(line)

                # draw one above it by 60 pxels
        lines = self.rounded_rectangle(MAP_WIDTH - 95, MAP_HEIGHT - (MAP_HEIGHT // 3), 16, 16, 25)
        for line in lines:
            self.lanes.append(line)

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

    def bezier_curve(self, control_points, resolution=8):
        n = len(control_points) - 1
        t_values = np.linspace(0, 1, resolution)
        curve_points = []
        
        for t in t_values:
            x = sum(comb(n, i) * (t ** i) * ((1 - t) ** (n - i)) * control_points[i][0] for i in range(n + 1))
            y = sum(comb(n, i) * (t ** i) * ((1 - t) ** (n - i)) * control_points[i][1] for i in range(n + 1))
            curve_points.append((x, y))
        
        return curve_points

    def rounded_rectangle(self, x, y, width, height, radius, resolution=8):
        if radius > min(width, height) / 2:
            radius = min(width, height) / 2
        
        # Define the corner control points for Bézier curves
        corners = {
            'top_left': [(x - width/2, y + height/2 - radius), (x - width/2, y + height/2), (x - width/2 + radius, y + height/2)],
            'top_right': [(x + width/2 - radius, y + height/2), (x + width/2, y + height/2), (x + width/2, y + height/2 - radius)],
            'bottom_right': [(x + width/2, y - height/2 + radius), (x + width/2, y - height/2), (x + width/2 - radius, y - height/2)],
            'bottom_left': [(x - width/2 + radius, y - height/2), (x - width/2, y - height/2), (x - width/2, y - height/2 + radius)]
        }
        
        # Generate line segments
        line_segments = []
        
        # Top edge
        line_segments.append(((x - width/2 + radius, y + height/2), (x + width/2 - radius, y + height/2)))
        # Right edge
        line_segments.append(((x + width/2, y + height/2 - radius), (x + width/2, y - height/2 + radius)))
        # Bottom edge
        line_segments.append(((x + width/2 - radius, y - height/2), (x - width/2 + radius, y - height/2)))
        # Left edge
        line_segments.append(((x - width/2, y - height/2 + radius), (x - width/2, y + height/2 - radius)))
        
        # Add rounded corners
        for key in corners:
            bezier_points = self.bezier_curve(corners[key], resolution)
            line_segments.extend([(bezier_points[i], bezier_points[i + 1]) for i in range(len(bezier_points) - 1)])
        
        # Ensure flat list of tuples
        return [segment for segment in line_segments]

    def draw(self, screen):
        for lane in self.lanes:
            pygame.draw.line(screen, LANE_COLOR, lane[0], lane[1])