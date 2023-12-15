# Demonstration of circle-circle colissions
# Written by Gabriel Gillette
# License: Public Domain

import math
import tkinter as tk
import time


def circle_colission(x1 : float, y1 : float, radius1 : float, x2 : float, y2 : float, radius2 : float) -> bool:
    '''
    Circle-Circle colission check
    Parameters:
        x1 : float - x pos of first circle
        y2 : float - y pos of first circle
        radius1 : float - radius of first circle
        x2 : float - x pos of second circle
        y2 : float - y pos of second circle
        radious2 : float - radious of second circle
    Returns: Bool - collision check result
    '''
    # This is just pythagorean theorem! 
    # (A*A) + (B*B) = (C*C)

    dx = x2 - x1 # length of one leg
    dy = y2 - y1 # length of another

    # Find the length of the third
    dist = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))

    # determine if the length is the size of the sum of the radii
    if dist < (radius1 + radius2):
        return True # colission! 
    
    # no colission!
    return False


class Canvas_Circle(tk.Canvas):
    __WIDTH = 1280 # width of canvas
    __HEIGHT = 720 # height of canvas
    __RAD_1 = 50   # radius of one circle
    __RAD_2 = 125  # radius of another

    def __init__(self) -> None:
        '''
        Class init
        Parameters: None
        Returns: None
        '''
        # init base canvas
        super().__init__(width=self.__WIDTH, height=self.__HEIGHT)

        # init position of smaller circle
        self.c1_x = 0
        self.c1_y = 0

        # init position of larger circle (center screen)
        self.c2_x = (self.__WIDTH / 2)
        self.c2_y = (self.__HEIGHT / 2)

        # Bind the mouse motion to call set_coords handler
        self.bind('<Motion>', lambda e: self.set_coords(e.x, e.y))

        return None

    def set_coords(self, x : float, y : float) -> None:
        '''
        To be called by tk motion '<Motion>' event.
        Sets c1_x and c1_y to x and y respectivly.
        Parameters:
            x : float - x position
            y : float - y position
        Returns: None
        '''
        self.c1_x = x 
        self.c1_y = y

        return None

    def draw_circle(self, x : float, y : float, radius : float, color : str) -> None:
        '''
        Draws a circle at position of given radius filled with color 
        Parameters:
            x : float - x position
            y : float - y position
            radius : float - circle radius
            color : str - name of color  
        Returns: None
        '''
        # handle stores an int refrence to the object
        # it's okay that it's local, because we only use it here
        handle = self.create_oval(0, 0, radius * 2, radius * 2, fill=color)

        # center the circle
        self.moveto(handle, x - radius, y - radius)

        return None

    def update(self) -> None :
        '''
        Canvas widget update function.
        To be called in a loop.
        Parameters: None
        Returns: None
        '''
        # clear the entire screen
        # this is necessary to be able to change the colors
        self.delete('all')

        color = 'blue' # initial default color of smaller circle

        # check hit
        colission = circle_colission(self.c1_x, self.c1_y, self.__RAD_1, self.c2_x, self.c2_y, self.__RAD_2)

        # change color if circles collide
        if(colission):
            color = 'yellow'

        # draw a big red circle
        self.draw_circle(self.c2_x, self.c2_y, self.__RAD_2, 'red')

        # draw smaller circle that follows mouse
        self.draw_circle(self.c1_x, self.c1_y, self.__RAD_1, color)

        # update base class
        super().update()
        super().update_idletasks()

        return None


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
        self.root.title('Circle-Circle Colission Demo')
        self.root.resizable(False, False)

        # program will run until this is False
        self.running = True

        # create and pack our canvas object
        self.canvas_circle = Canvas_Circle()
        self.canvas_circle.pack()

        # bind window close button to close_program() method
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.close_program())

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
        # update canvas object
        self.canvas_circle.update()

        # update root window
        self.root.update_idletasks()
        self.root.update()

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