""" 

Adapted from Atsushi Sakai's Python Robotics
Simulator

"""

import numpy as np
import matplotlib.pyplot as plt
import math
import random
from bresenham import bresenham

MAX_RANGE = 1000

class Robot():
    def __init__(self):
        self.x = 25
        self.y = 0
    
    def visualize_robot(self):
        plt.plot(self.x, self.y, "*r")

    def move(self):
        self.y += 1

class Map():
    def __init__(self, src_path_map):
        self.map = np.genfromtxt(src_path_map)
        self.width = self.map.shape[1] #TODO: check
        self.height = self.map.shape[0]
        self.max_dist = math.sqrt(self.width**2 + self.height**2)
        print("Finished reading map of width " + 
            str(self.width) + "and height " + str(self.height))

    def visualize_map(self):
        # fig = plt.figure()
        # plt.switch_backend('TkAgg')
        # mng = plt.get_current_fig_manager()
        # mng.resize(*mng.window.maxsize())
        # plt.ion()
        plt.imshow(self.map, cmap='Greys')
        plt.axis([0, self.width, 0, self.height])
        # plt.draw()
        # plt.pause(1.0)


class LidarSim():
    def __init__(self, angles, map1):
        self.range_noise = 0.0
        self.angles = angles * np.pi/180. # list in deg
        # self.frame_pairs  = frame_pairs # coordinates of corners
        self.map = map1
        self.sensed_obs = None 
        self.ranges = None

    def get_bresenham_points(self, p1, p2):
        """Get list of coordinates of line (in tuples) from p1 and p2. 
        Input: points (tuple) ex. (x,y)"""

        return list(bresenham(p1[0], p1[1], p2[0], p2[1]))

    def update_reading(self, pos):
        """Update sensed obstacle locations and ranges."""
        closest_obs = [self.get_closest_obstacle(
            pos, angle) for angle in self.angles]
        self.sensed_obs = np.array(closest_obs)

        self.ranges = self.get_ranges(pos)

    def get_ranges(self, pos):
        """Get ranges given sensed obstacles"""

        ranges = []
        for obstacle in self.sensed_obs:
            if obstacle is None:
                ranges.append(10000)
            else:
                ranges.append(calc_dist((pos[0], pos[1]), obstacle))
        return np.array(ranges)

        
    def get_closest_obstacle(self, pos, angle):
        """"Get closest obs position given angle."""
        end_point_x = int(round(self.map.max_dist * np.cos(angle) + pos[0]))
        end_point_y = int(round(self.map.max_dist * np.sin(angle) + pos[1]))
        end_point = (end_point_x, end_point_y)
        along_line_pts = self.get_bresenham_points(pos, end_point)
        # make sure pts are within index
        along_line_pts = [pt for pt in along_line_pts if (pt[0] >= 0 and pt[0] < self.map.width)]
        along_line_pts = [pt for pt in along_line_pts if (
            pt[1] >= 0 and pt[1] < self.map.height)]
        along_line_pts = np.array(along_line_pts)
        # plt.plot(along_line_pts[:,0], along_line_pts[:,1], '.')
        along_line_occ = self.map.map[along_line_pts[:,1], along_line_pts[:,0]]
        # TODO: change to binary
        closest_obs_coord = along_line_pts[np.where(along_line_occ > 0.99)]
        if len(closest_obs_coord) == 0: # no obstacles
            # TODO: make into constant
            return [MAX_RANGE * np.cos(angle), MAX_RANGE * np.sin(angle)]
        else:
            return closest_obs_coord[0]
            

    def visualize_lidar(self, pos):
        plt.plot(self.sensed_obs[:, 0], self.sensed_obs[:, 1], "o")
        plt.plot(np.vstack((self.sensed_obs[:, 0], np.ones(len(self.angles)) * pos[0])),
                 np.vstack((self.sensed_obs[:, 1], np.ones(len(self.angles)) * pos[1])), 'k', linewidth=0.1)


def calc_dist(p1, p2):
    return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)




def main():
    print("start!!")

    print("done!!")
    # src_path_map = "map.dat"
    # map1 = Map(src_path_map)
    # map1.visualize_map()

    # lidar_sim = LidarSim()
    # pts = lidar_sim.get_bresenham_points((0,0), (0,4))
    # print(pts)

if __name__ == '__main__':
    main()
