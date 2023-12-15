# Demonstration of why delta time is important
# Written by Gabriel Gillette
# License: Public Domain

import math
import tkinter as tk
import time

class DeltaTime():
    def __init__(self) :

        # set current time
        self.__current = time.perf_counter()

        # prime the past as the current
        self.__past = self.__current

    def get(self) -> float:
        '''
        Get the current delta time
        Parameters: None
        Returns: Delta time in fractional seconds
        '''

        # get current time
        self.__current = time.perf_counter()

        # calculate delta
        delta = self.__current - self.__past

        # set new past
        self.__past = self.__current

        # return delta
        return delta

class Canvas_1(tk.Canvas):
    __WIDTH = 1280 # width of canvas
    __HEIGHT = 720/2 # height of canvas
    __R_W = 150 # rectangle width
    __R_H = 150 # rectangle Height

    def __init__(self) -> None:
        '''
        Class init
        Parameters: None
        Returns: None
        '''
        # init base canvas
        super().__init__(width=self.__WIDTH, height=self.__HEIGHT)

        # init position of box
        self.r_x = 0 + 200
        self.r_y = (self.__HEIGHT/2)

        # movement direction
        self.dir = 'right'

        return None


    def draw_rectangle(self, x : float, y : float, width : float, height : float, color : str) -> None:
        '''
        Draws a circle at position of given radius filled with color 
        Parameters:
            x : float - x position
            y : float - y position
            width : float - rectangle width
            height : float - reantangle height
            color : str - name of color  
        Returns: None
        '''
        # handle stores an int refrence to the object
        # it's okay that it's local, because we only use it here
        handle = self.create_rectangle(0, 0, width, height, fill=color)

        # center the rectangle
        self.moveto(handle, x - (width/2), y - (height/2))

        return None

    def update(self, delta : float) -> None :
        '''
        Canvas widget update function.
        To be called in a loop.
        Parameters: 
            delta : float - delta time 
        Returns: None
        '''
        # clear the entire canvas
        self.delete('all')

        # calculate current fps from delta time
        # since delta is in fractional seconds, we just need to get the reciprocal
        # since delta could be 0, this is dangerious!
        try: 
            fps = 1 / delta
        except:
            fps = 0

        self.create_text(100, 20, text=f'{"FPS":<}: {fps:>.2f}', font=('Monotype', 25), anchor='w')
        self.create_text(100, 50, text=f'Press space to toggle FPS Limits!', font=('Monotype', 25), anchor='w')
        self.create_text(100, 80, text=f'Red square is moving based on delta time (consistent).', font=('Monotype', 25), anchor='w')

        v_x = 0 # velocity for x coord

        # change the dir once the rectangle hits a boundry
        if(self.r_x < 200):
            self.dir = 'right'
        elif(self.r_x > self.__WIDTH - 200):
            self.dir = 'left'

        # set the velocity based on the dir
        # calculated to take 2 seconds to hit bound
        dist = self.__WIDTH - 200 # distance to travel
        seconds = 2               # how long to travel distance
        if(self.dir == 'right'):
            v_x = (dist * delta) / seconds
        else:
            v_x = ((dist * delta) / seconds) * -1 # same but inversed

        # shift the rectangle by it's velocity
        self.r_x += v_x

        # draw a rectangle
        self.draw_rectangle(self.r_x, self.r_y, self.__R_W, self.__R_H, 'red')

        # update base class
        super().update()
        super().update_idletasks()


class Canvas_2(tk.Canvas):
    __WIDTH = 1280 # width of canvas
    __HEIGHT = 720/2 # height of canvas
    __R_W = 150 # rectangle width
    __R_H = 150 # rectangle Height

    def __init__(self) -> None:
        '''
        Class init
        Parameters: None
        Returns: None
        '''
        # init base canvas
        super().__init__(width=self.__WIDTH, height=self.__HEIGHT)

        # init position of box
        self.r_x = 0 + 200
        self.r_y = (self.__HEIGHT/2)

        # movement direction
        self.dir = 'right'

        return None


    def draw_rectangle(self, x : float, y : float, width : float, height : float, color : str) -> None:
        '''
        Draws a rectangle centered at x and y with the given height and width filled with color
        Parameters:
            x : float - x position
            y : float - y position
            width : float - rectangle width
            height : float - reantangle height
            color : str - name of color  
        Returns: None
        '''
        # handle stores an int refrence to the object
        # it's okay that it's local, because we only use it here
        handle = self.create_rectangle(0, 0, width, height, fill=color)

        # center the rectangle
        self.moveto(handle, x - (width/2), y - (height/2))

        return None

    def update(self, frame_rate) -> None :
        '''
        Canvas widget update function.
        To be called in a loop.
        Parameters: 
            frame_rate : float - expected frame_rate
        Returns: None
        '''
        # clear the entire canvas
        self.delete('all')

        self.create_text(100, 20, text=f'Blue square is moving based on frame rate (eratic).', font=('Monotype', 25), anchor='w')

        v_x = 0 # velocity for x coord

        # change the dir once the rectangle hits a boundry
        if(self.r_x < 200):
            self.dir = 'right'
        elif(self.r_x > self.__WIDTH - 200):
            self.dir = 'left'

        # set the velocity based on the dir
        # calculated to take 2 seconds to hit bound
        dist = self.__WIDTH - 200 # distance to travel
        seconds = 2               # how long to travel distance
        if(self.dir == 'right'):
            v_x = (dist * (1/frame_rate)) / seconds
        else:
            v_x = ((dist * (1/frame_rate)) / seconds) * -1 # same but inversed

        # shift the rectangle by it's velocity
        self.r_x += v_x

        # draw a rectangle
        self.draw_rectangle(self.r_x, self.r_y, self.__R_W, self.__R_H, 'blue')

        # update base class
        super().update()
        super().update_idletasks()


class Program:
    def __init__(self) -> None:
        '''
        Class init
        Parameters: None
        Returns: None
        '''
        # create window and set some basic properties
        self.root = tk.Tk()
        self.root.geometry('1280x720')
        self.root.title('Delta Time Demo')
        self.root.resizable(False, False)

        # program will run until this is False
        self.running = True

        # frame rate limiter (0 = none)
        self.fps_limit = 0

        # program's delta time object
        self.delta_time = DeltaTime()

        # create and pack our canvas objects
        self.canvas_1 = Canvas_1()
        self.canvas_1.pack()
        self.canvas_2 = Canvas_2()
        self.canvas_2.pack()

        # bind window close button to close_program() method
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.close_program())

        # bind space key to frame_rate toggle
        self.root.bind('<space>', lambda e: self.toggle_framerate())

        return None
    
    def toggle_framerate(self):
        '''
        To be called by tk <space> event
        Sets self.limit_fps = to it's inverse
        Parameters: None
        Returns: None
        '''
        self.fps_limit += 15
        self.fps_limit %= 120
        return None

    def close_program(self):
        '''
        sets self.running to False
        Parmeters: None
        Returns: None
        '''
        self.running = False
        return None

    def update(self):
        '''
        Program update function, to be called in a loop.
        Parameters: None
        Returns: None
        '''
        # get delta time
        delta = self.delta_time.get()

        # update canvas object
        self.canvas_1.update(delta)
        self.canvas_2.update(60)

        # update root window
        self.root.update_idletasks()
        self.root.update()

        if(self.fps_limit):
            time.sleep(1/self.fps_limit)

        return None

    def main_loop(self) -> None:
        '''
        Main process loop.
        Prameters: None
        Returns: None
        '''
        # while running flag is True
        while (self.running):
            
            # Call program update 
            self.update()

        # destroy root window when program is done
        self.root.destroy()


# Conditional call to main program loop
if(__name__ == '__main__'):
    program = Program()
    program.main_loop()
