# Demonstration of box-box (AKA AABB) colissions
# Written by Gabriel Gillette
# License: Public Domain

import math
import tkinter as tk
import time

def box_colission(x1 : float, y1 : float, width1 : float, height1 : float, 
                  x2 : float, y2 : float, width2 : float, height2 : float) -> bool:
    '''
    Box-Box colission check.
    Also known as Axis Aligned Bounding Boxes (AABB).
    Parameters:
        x1 : float - box 1 x coord (center)
        y1 : float - box 1 y coord (center)
        width1 : float - box 1 width
        height1 : float - box 2 height
        x2 : float - box 2 x coord (center)
        y2 : float - box 2 y coord (center)
        width2 : float - box 2 width
        height2 : float - box 2 height
    Returns: Bool - result of check
    '''
    # This check is just a series of inequality checks.
    # This function assumes the center is our anchor
    #   So we need to adjust the values a bit.
    # 
    
    corner1_x = x1 - (width1/2)
    corner1_y = y1 - (height1/2)
    corner2_x = x2 - (width2/2)
    corner2_y = y2 - (height2/2)
    if(corner1_x < corner2_x + width2 and corner1_x + width1 > corner2_x and 
       corner1_y < corner2_y + height2 and corner1_y + height1 > corner2_y):
        return True # colission!
    
    # no colission!
    return False


class Canvas_Box(tk.Canvas):
    __WIDTH = 1280    # width of canvas
    __HEIGHT = 720    # height of canvas
    __RECT_1_H = 50   # width of first rect
    __RECT_1_W = 125  # height of second rect
    __RECT_2_H = 200  # width of first rect
    __RECT_2_W = 420  # height of second rect

    def __init__(self) -> None:
        '''
        Class init
        Parameters: None
        Returns: None
        '''
        # init base canvas
        super().__init__(width=self.__WIDTH, height=self.__HEIGHT)

        # init position of smaller rectangle
        self.r1_x = 0
        self.r1_y = 0

        # init position of larger rectangle (center screen)
        self.r2_x = (self.__WIDTH / 2)
        self.r2_y = (self.__HEIGHT / 2)

        # Bind the mouse motion to call set_coords handler
        self.bind('<Motion>', lambda e: self.set_coords(e.x, e.y))

        return None

    def set_coords(self, x : float, y : float) -> None:
        '''
        To be called by tk motion '<Motion>' event.
        Sets r1_x and r1_y to x and y respectivly.
        Parameters:
            x : float - x position
            y : float - y position
        Returns: None
        '''
        self.r1_x = x 
        self.r1_y = y

        return None
    
    def draw_rectangle(self, x : float, y : float, width : float, height : float, color : str) -> None:
        '''
        Draws a rectangle centered at x and y with the given height and width filled with color
        Parameters:
            x : float - x position
            y : float - y position
            width : float - rectangle width
            height : float - rectangle height
            color : str - name of color  
        Returns: None
        '''
        # handle stores an int refrence to the object
        # it's okay that it's local, because we only use it here
        handle = self.create_rectangle(0, 0, width, height, fill=color)

        # center the rectangle
        self.moveto(handle, x - (width/2), y - (height/2))

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
        colission = box_colission(self.r1_x, self.r1_y, self.__RECT_1_W, self.__RECT_1_H, 
                                  self.r2_x, self.r2_y, self.__RECT_2_W, self.__RECT_2_H)

        # change color if boxes collide
        if(colission):
            color = 'yellow'

        # draw a big red rectangle
        self.draw_rectangle(self.r2_x, self.r2_y, self.__RECT_2_W, self.__RECT_2_H, 'red')

        # draw smaller rectangle that follows mouse
        self.draw_rectangle(self.r1_x, self.r1_y, self.__RECT_1_W, self.__RECT_1_H, color)

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
        self.root.title('Box-Box Colission Demo')
        self.root.resizable(False, False)

        # program will run until this is False
        self.running = True

        # create and pack our canvas object
        self.canvas_box = Canvas_Box()
        self.canvas_box.pack()

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
        self.canvas_box.update()

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