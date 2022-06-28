import numpy as np
import matplotlib.pyplot as plt
import time

class plotter:
    def __init__(self, window_size = 100, figsize= (20, 20)):
        self.points = []
        self.times = []
        self.started_from = 0
        self.window_size = window_size
        plt.close('all')
        plt.figure(figsize=figsize)
        plt.ion()
        plt.show()

    def refresh_plot(self):
        plt.cla()
        plt.plot(self.times, self.points)
        plt.pause(0.01)
        plt.xlabel('Time')
        plt.ylabel('Signal')
        plt.ylim(500, 700)
    
    def get_time(self):
        if len(self.points) < 1:
            self.started_from = time.time()
            return 0
        else:
            return time.time() - self.started_from

    def check_window_size(self):
        if len(self.points) > self.window_size:
            self.points.pop()
            self.times.pop() 

    def add_point(self, y):
        time_added = self.get_time()
        self.points.append(y)
        self.times.append(time_added)
        self.check_window_size()
        self.refresh_plot()
        
        

         