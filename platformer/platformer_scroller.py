# Simple 2D platformer example
# Writen by Gabriel Gillette
# License: Public Domain
# TODO: Some messy and rushed code!!

import math
import tkinter as tk
from tkinter import messagebox
import time
import os

#-------------------------------------------------------------------DELTA TIME

class DeltaTime():
    '''
    Keeps track of time elapsed between frames.
    '''
    def __init__(self) :
        '''
        Class init
        Parameters: None
        Returns: None
        '''
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


#----------------------------------------------------------------INPUT HANDLER

class InputHandler:
    '''
    Simple keyboard input interface to tkinter
    '''
    def __init__(self, root : tk.Tk, input_dict : dict):
        '''
        Class init
        Parameters:
            root : tk.Tk - tk root
            input_dict : dict - dictionary of the format key=keysym val=name
        Returns: None
        '''
        self.__input_status = dict() # status of each keysym
        self.__input_map = dict()    # map of keysyms to names

        # Bind generic keyboard events to their respective handlers
        root.bind(f'<KeyPress>', lambda e: self.__press_key_event(e.keysym))
        root.bind(f'<KeyRelease>', lambda e: self.__release_key_event(e.keysym))

        # Allows us to turn off keyboard repeat (causes havok)
        root.bind('<FocusIn>', lambda e: os.system("xset r off"))
        root.bind('<FocusOut>', lambda e: os.system("xset r on"))

        # Create our databases of keysyms
        # Keysyms have a many-to-one relationship to names 
        for key in input_dict.keys():
            self.__input_status[input_dict[key]] = 'up'
            self.__input_map[key] = input_dict[key]

    def __del__(self) -> None:
        '''
        Called on class deletion. 
        Turns back on keyboard repeat
        Parameters: None
        Returns: None
        '''
        os.system("xset r on")
        return None

    def __press_key_event(self, keysym : str) -> None:
        '''
        Generic event handler for a key press.
        Parameters:
            keysym : str - keysym passed in from event
        Returns: None
        '''
        # set the new status in our database
        if(keysym in self.__input_map):
            self.__input_status[self.__input_map[keysym]] = 'pressed'

        return None

    def __release_key_event(self, keysym : str) -> None:
        '''
        Generic event handler for a key release.
        Parameters:
            keysym : str - keysym passed in from event
        Returns: None
        '''
        # set the new status in our database        
        if(keysym in self.__input_map):
            self.__input_status[self.__input_map[keysym]] = 'released'

        return None
        

    def update(self) -> None:
        '''
        Updates key status so we know if a key was just pressed/released
            or is being held down
        Intended to be called in an update loop.
        Parameters: None
        Returns: None
        '''
        for key in self.__input_status.keys():
            # makes sure a key that was presed is set to down on next frame
            if(self.__input_status[key] == 'pressed'):
                self.__input_status[key] = 'down'
            
            # makes sure a key that was released is set to up on next frame
            if(self.__input_status[key] == 'released'):
                self.__input_status[key] = 'up'

        return None

    def key_is_up(self, name: str) -> bool:
        '''
        Checks if a key is up (not pressed down).
        Parameters:
            name : str - name of input to check.
        Returns: bool - result of check.
        '''
        if (name in self.__input_status and 
            (self.__input_status[name] == 'up' or 
             self.__input_status[name] == 'released')):
            # key is up
            return True
        
        # key is down
        return False

    def key_is_down(self, name: str) -> bool:
        '''
        Checks if a key is pressed down.
        Parameters:
            name : str - name of input to check.
        Returns: bool - result of check.
        '''
        if (name in self.__input_status.keys() and 
            (self.__input_status[name] == 'down' or 
             self.__input_status[name] == 'pressed')):
            
            # key is pressed down
            return True
        
        # key is not pressed down
        return False

    def key_is_pressed(self, name: str) -> bool:
        '''
        Checks if a key has just been pressed down (not held).
        Parameters:
            name : str - name of input to check.
        Returns: bool - result of check.
        '''
        if (name in self.__input_status.keys() and 
            (self.__input_status[name] == 'pressed')):

            # key has just been pressed down
            return True
        
        # Key has not just been pressed down
        return False

    def key_is_released(self, name: str) -> bool:
        '''
        Checks if a key has just been released this frame.
        Parameters:
            name : str - name of input to check.
        Returns: bool - result of check.
        '''
        if (name in self.__input_status.keys() and 
            (self.__input_status[name] == 'released')):

            # Key has just been released
            return True
        
        # key was not just released
        return False
        

#----------------------------------------------------------------------HIT BOX

class HitBox:
    '''
    Contains information of a rectangle.
    Can be used to to check intersection with another hitbox
    '''
    def __init__(self, x=0, y=0, w=0, h=0):
        '''
        Class init
        Parameters:
            x : float - x position (center aligned)
            y : float - y position (center aligned)
            w : float - width
            h : float - height
        Returns: None
        '''
        self.__x_pos = x
        self.__y_pos = y
        self.__w = w
        self.__h = h

        # Outline color for debug drawing
        self.__outline = 'red'

        return None

    def debug_draw(self, canvas : tk.Canvas) -> None:
        '''
        Draws outline of hitbox.
        Parameters:
            canvas : tk.Canvas - canvas objet to draw to.
        Returns: None
        '''
        # Draw the rectangle to (0,0) then move it to the correct spot.
        # Makes the math a little easier.
        handle = canvas.create_rectangle(0, 0, self.__w, self.__h, 
                                         fill='', outline=self.__outline)
        canvas.moveto(handle, self.__x_pos - (self.__w / 2), 
                      self.__y_pos - (self.__h / 2))
        return None
    
    def set_outline(self, outline : str) -> None:
        '''
        Sets outline color.
        Parameters:
            outline : str - outline color
        Returns: None
        '''
        self.__outline = outline
        return None
    
    def get_attribs(self) -> tuple[float, float, float, float]:
        '''
        Get the x, y, w, h attributes as a tuple.
        Parameters:
            None.
        Returns: tuple[float, float, float, float] - our attributes
        '''
        return self.__x_pos, self.__y_pos, self.__w, self.__h
    
    def move(self, x : float = None, y : float = None) -> None:
        '''
        Move the hitbox.
        Parameters:
            x : float - x position
            y : float - y position
        Returns: None
        '''
        self.__x_pos = x or self.__x_pos
        self.__y_pos = y or self.__y_pos
        return None

    def resize(self, w : float = None, h : float = None) -> None:
        '''
        Resize our hit box.
        Parameters:
            w : float - width
            h : float - height
        Returns: none
        '''
        self.__w = w or self.__w
        self.__h = h or self.__h
        return None
    
    def box_hit_test(self, hit_box : 'HitBox'):
        '''
        Checks for a colission with another HitBox object.
        Parameters:
            hit_box : HitBox - hit box to check against.
        '''

        # get the basic hit box data
        x1, y1, width1, height1 = self.get_attribs()
        x2, y2, width2, height2 = hit_box.get_attribs() 

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
    

#------------------------------------------------------------------IMAGE CACHE
class ImageCache:
    '''
    Loads and stores images.
    '''
    def __init__(self) -> None:
        '''
        Class init
        Parameters: None.
        Returns: None
        '''
        # create our database
        self.__Cache = dict()

        return None
        
    def load_image(self, name : str, path : str) -> None:
        '''
        Load and store an image
        Parameters: 
            name : str - name of image
            path : str - file path of image
        Returns: None
        '''
        # store into database with name as key
        self.__Cache[name] = tk.PhotoImage(file=path)

        return None

    def get(self, name : str) -> tk.PhotoImage:
        '''
        Gets an image from database.
        Parameters:
            name : str - name of image
        Returns: tk.Photoimage - image from databse.
                 None type is name was not found. 
        '''
        if(name in self.__Cache):
            return self.__Cache[name]
        
        return None
    

#------------------------------------------------------------------GAME OBJECT
    
class GameObject:
    '''
    Abstract GameObject class.
    All GameObjects inherit this.
    '''
    def __init__(self, x : float, y : float, w : float, h : float) -> None:
        '''
        Class init
        Parameters:
            x : float - x position
            y : float - y position
            w : float - width
            h : float - height
        Returns: None
        '''
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h

        # messages sent to communicate with game object
        self.__signals = []

        # by default a GameObject will not have a sprite or hitbox 
        self.__sprite : tk.PhotoImage = None
        self.__hit_box : HitBox = None

        return None
    
    def pop_signal(self) -> str :
        '''
        Pops a signal off of signal stack
        Parameters: None
        Returns: str - signal or None if empty 
        '''
        if(len(self.__signals) > 0):
            return self.__signals.pop()
        return ''
    
    def push_signal(self, signal : str) -> None :
        '''
        Pushes a signal onto signal stack
        Parameters: 
            signal : str - signal we wanna push
        Returns: None
        '''
        self.__signals.append(signal)
        return None
    
    def get_attribs(self) -> tuple[float, float, float, float]:
        '''
        Returns The four main GameObject attributes as a tuple.
        Parameters: None
        Returns: tuple[float, float, float, float] - x, y, width, height
        '''
        return self.__x, self.__y, self.__w, self.__h

    def get_hit_box(self) -> HitBox :
        '''
        Getter for HitBox
        Parameters: None
        Returns GameObject HitBox
        '''
        return self.__hit_box
    
    def set_hit_box(self, hit_box : HitBox) -> None :
        '''
        Setter for HitBox
        Parameters: 
            hit_box : HitBox - HitBox were setting to. 
        Returns: None
        '''
        self.__hit_box = hit_box
        return None
    
    def draw_hitbox(self, canvas : tk.Canvas) -> None:
        '''
        Debug drawing feature for HitBox
        Parameters:
            canvas : tk.Canvase - Canvas objet to draw to.
        Returns None.
        '''
        if(self.__hit_box):
            self.__hit_box.debug_draw(canvas)
    
    def set_sprite(self, image : tk.PhotoImage) -> None :
        '''
        Setter for sprite
        Parameters: 
            image : tk.PhotoImage - image were setting to. 
        Returns: None
        '''
        self.__sprite = image

    def hit_test(self, game_object : 'GameObject') -> bool :
        '''
        Check colission against another GameObject
        Parameters: 
            game_object : GamrObject to check against.
        Returns: bool - the result
        '''
        hit_box = game_object.get_hit_box()

        # if both GameObjects have a hit box
        if(self.__hit_box and hit_box):
            # Check colission
            return self.__hit_box.box_hit_test(hit_box)
        
        # else returns False
        return False
    
    def move(self, x : float = None, y : float = None) -> None:
        '''
        Move GameObject tp specific loation.
        Parameters:
            x : float - x position
            y : float - y position
        Returns: None
        '''
        self.__x = x or self.__x
        self.__y = y or self.__y

        # move the hit box with it
        if(self.__hit_box):
            self.__hit_box.move(self.__x, self.__y)

        return None

    def move_relative(self, x : float = 0, y : float = 0) -> None:
        '''
        Move GameObject relative from wher it os.
        Parameters:
            x : float - x movement
            y : float - y movement
        Returns: None
        '''
        self.__x += x
        self.__y += y

        # move the hit box with it
        if(self.__hit_box):
            self.__hit_box.move(self.__x, self.__y)

        return None

    def draw(self, canvas : tk.Canvas) -> None:
        '''
        Draws game object to canvas.
        Parameters:
            canvas : tk.Canvas - canvas to draw to.
        Returns: None
        '''
        if(self.__sprite):
            canvas.create_image(self.__x, self.__y, anchor='c', image=self.__sprite)
        return None
    
    def update(self, delta : float) -> None : 
        '''
        'Virtual' update function.
        Parameters:
            delta - delta time in fraction seconds.
        Returns: None
        '''
        return None


#------------------------------------------------------GAME OBJECT DEFINITIONS
    
class GroundTile(GameObject):
    '''
    The game's floor/ground
    '''
    def __init__(self, x: float, y: float,  image_cache : ImageCache) -> None:
        '''
        Class init
        Parameters:
            x : float - x position
            y : float - y position
            image_cache : ImageCache - to obtain texture
        Returns: None
        '''
        WIDTH = HEIGHT = 40
        super().__init__(x, y, WIDTH, HEIGHT)

        self.set_sprite(image_cache.get('ground'))

        # lets make the hit box slightly smaller
        self.set_hit_box(HitBox(x, y, WIDTH, HEIGHT - 2))

        return None

class GrassTile(GameObject):
    '''
    Decerative grass
    '''
    def __init__(self, x: float, y: float,  image_cache : ImageCache) -> None:
        '''
        Class init
        Parameters:
            x : float - x position
            y : float - y position
            image_cache : ImageCache - to obtain texture
        Returns: None
        '''
        WIDTH = HEIGHT = 40
        super().__init__(x, y, WIDTH, HEIGHT)
        self.set_sprite(image_cache.get('grass'))

        return None

class CoinTile(GameObject):
    def __init__(self, x: float, y: float,  image_cache : ImageCache) -> None:
        '''
        Class init
        Parameters:
            x : float - x position
            y : float - y position
            image_cache : ImageCache - to obtain texture
        Returns: None
        '''
        WIDTH = HEIGHT = 40
        super().__init__(x, y, WIDTH, HEIGHT)

        self.set_sprite(image_cache.get('coin'))
        self.set_hit_box(HitBox(x, y, WIDTH, HEIGHT))

        # direction of animation
        self.__dir = 'up'
        # animation travel
        self.__y_travel = 0

        return None

    def update(self, delta: float) -> None:
        '''
        Update coin's animation.
        Parameters:
            delta : float - dealta time in fractional seconds
        Returns: None
        '''
        SPEED = 40
        UPPER_BOUND = -10
        LOWER_BOUND = 0
        if(self.__dir == 'down'):
            self.move_relative(0, SPEED * delta)
            self.__y_travel += SPEED * delta
        else:
            self.move_relative(0, -SPEED * delta)
            self.__y_travel += -SPEED * delta

        if(self.__y_travel < UPPER_BOUND):
            self.__dir = 'down'
        elif(self.__y_travel > LOWER_BOUND):
            self.__dir = 'up'

        return super().update(delta)
    
class CloudTile(GameObject):
    '''
    Decorative cloud
    '''
    def __init__(self, x: float, y: float,  image_cache : ImageCache) -> None:
        '''
        Class init
        Parameters:
            x : float - x position
            y : float - y position
            image_cache : ImageCache - to obtain texture
        Returns: None
        '''
        WIDTH = HEIGHT = 80
        super().__init__(x, y, WIDTH, HEIGHT)
        self.set_sprite(image_cache.get('cloud'))

        return None

class PalmTile(GameObject):
    '''
    Decorative palm tree
    '''
    def __init__(self, x: float, y: float,  image_cache : ImageCache) -> None:
        '''
        Class init
        Parameters:
            x : float - x position
            y : float - y position
            image_cache : ImageCache - to obtain texture
        Returns: None
        '''
        WIDTH = 80
        HEIGHT = 120
        super().__init__(x, y, WIDTH, HEIGHT)
        self.set_sprite(image_cache.get('palm'))

        return None

class ExitTile(GameObject):
    '''
    Reach this to win the level.
    '''
    def __init__(self, x: float, y: float,  image_cache : ImageCache) -> None:
        '''
        Class init
        Parameters:
            x : float - x position
            y : float - y position
            image_cache : ImageCache - to obtain texture
        Returns: None
        '''
        WIDTH = HEIGHT = 40
        super().__init__(x, y, WIDTH, HEIGHT)
        
        self.set_hit_box(HitBox(x, y, WIDTH, HEIGHT))
        self.set_sprite(image_cache.get('exit'))

        self.__dir = 'down'
        self.y_travel = 0

        return None

    def update(self, delta: float) -> None:
        '''
        Update signs's animation.
        Parameters:
            delta : float - dealta time in fractional seconds
        Returns: None
        '''
        SPEED = 40
        UPPERBOUND = -5
        LOWERBOUND = 5
        if(self.__dir == 'down'):
            self.move_relative(0, SPEED * delta)
            self.y_travel += SPEED * delta
        else:
            self.move_relative(0, -SPEED * delta)
            self.y_travel += -SPEED * delta

        if(self.y_travel < UPPERBOUND):
            self.__dir = 'down'
        elif(self.y_travel > LOWERBOUND):
            self.__dir = 'up'

        return super().update(delta)

class Jerk(GameObject):
    '''
    The game's "monster"
    '''
    def __init__(self, x: float, y: float,  image_cache : ImageCache) -> None:
        '''
        Class init
        Parameters:
            x : float - x position
            y : float - y position
            image_cache : ImageCache - to obtain texture
        Returns: None
        '''
        WIDTH = HEIGHT = 40
    
        super().__init__(x, y, WIDTH, HEIGHT)
        self.set_sprite(image_cache.get('jerk'))
        self.set_hit_box(HitBox(x, y, WIDTH, HEIGHT))

        self.__dir = 'left'
        self.__x_travel = 0
        
        return None
    
    def update(self, delta: float) -> None:
        '''
        Update jerk's animation.
        Parameters:
            delta : float - dealta time in fractional seconds
        Returns: None
        '''
        SPEED = 30
        RIGHTBOUND = 40
        LEFTBOUND = -40

        if(self.__dir == 'left'):
            if(self.__x_travel > LEFTBOUND):
                self.move_relative((-SPEED * delta))
                self.__x_travel += -SPEED * delta
            else:
                self.__dir = 'right'
        if(self.__dir == 'right'):
            if(self.__x_travel < RIGHTBOUND):
                self.move_relative((SPEED * delta))
                self.__x_travel += SPEED * delta
            else:
                self.__dir = 'left'
        return super().update(delta)

class Player(GameObject):
    MAX_VELOCITY = 1.2

    def __init__(self, x: float, y: float,  image_cache : ImageCache) -> None:
        super().__init__(x, y, 40, 80)

        self.set_sprite(image_cache.get('dude'))

        self.on_ground = True
        self.x_vel = 0
        self.y_vel = 0
        self.__is_dead = False

        self.set_hit_box(HitBox(x, y, 40, 80))

    def is_dead(self):
        '''
        Returns true if player should be dead
        Parameter: None
        Return: bool
        '''
        return self.__is_dead
    
    def update(self, delta : float) -> None:
        '''
        Update on-screen player
        Parameters:
            delta : float
        Returns: None
        '''
        GRAVITY = 4
        WALKSPEED = 5
        JUMP_STRENGTH = -2.5

        signal = self.pop_signal()

        # consume all the signals sent from the game
        # and act accordenly 
        while signal:
            signal_tokens = signal.split(' ')

            if(signal == 'move_left'):
                if(self.x_vel > (self.MAX_VELOCITY * -1)):
                    self.x_vel -= WALKSPEED * delta
            elif(signal == 'move_right'):
                if(self.x_vel < self.MAX_VELOCITY):
                    self.x_vel += WALKSPEED * delta
            elif(signal == 'move_neutral'):
                if(self.x_vel < 0):
                    self.x_vel += 2 * delta
                elif(self.x_vel > 0):
                    self.x_vel -= 2 * delta

            if(signal == 'jump' and self.on_ground):
                self.y_vel = JUMP_STRENGTH
                self.on_ground = False

            self.on_ground = False
            if(signal_tokens[0] == 'hit_ground' and self.y_vel > 0):
                self.on_ground = True
                self.move(y=float(signal_tokens[1]))
                self.y_vel = 0

            if(self.on_ground == False):
                self.y_vel += GRAVITY * delta
                
            signal = self.pop_signal()
        
        self.move_relative(self.x_vel, self.y_vel)
        
        # check for falling death
        if(self.get_attribs()[1] > 800):
            self.__is_dead = True

        return super().update(delta)
    

#------------------------------------------------------------------GAME CANVAS

class Game(tk.Canvas):
    __WIDTH = 1280  # width of canvas
    __HEIGHT = 720  # height of canvas
    __X_RES = 32    # num of horz tiles
    __Y_RES = 18    # num of vert tiles
    __LEVEL_PATH = 'level2.txt' # data file to load from
    __GRAVITY = 4

    def __init__(self, root : tk.Tk) -> None:
        '''
        Class init
        Parameters: None
        Returns: None
        '''
        # init base canvas
        super().__init__(width=self.__WIDTH, height=self.__HEIGHT)

        
        input_defs = {'a' : 'move_left', 'Left' : 'move_left', 'd' : 'move_right', 
                  'Right' : 'move_right', 'w' : 'jump', 'space' : 'jump', 'Up' : 'jump',
                  'h': 'hitbox'}

        self.input_handler = InputHandler(root, input_defs)

        self.delta_time = DeltaTime()

        self.level_data = self.__load_level(self.__LEVEL_PATH)
        self.image_cache = ImageCache()

        self.image_cache.load_image('ground', 'assets/ground.png')
        self.image_cache.load_image('coin', 'assets/coin.png')
        self.image_cache.load_image('cloud', 'assets/cloud.png')
        self.image_cache.load_image('jerk', 'assets/jerk.png')
        self.image_cache.load_image('palm', 'assets/palm.png')
        self.image_cache.load_image('exit', 'assets/exit.png')
        self.image_cache.load_image('grass', 'assets/grass.png')
        self.image_cache.load_image('dude', 'assets/dude.png')

        self.__score = 0

        self.__player : Player 
        self.__ground = []

        self.alive = True

        self.game_objects = []

        self.__draw_hitbox = False

        self.__spawn_tiles(self.level_data, self.image_cache)

        return None

    def __load_level(self, path : str) -> list[list[str]] :
        '''
        Parse level file into list of list contaning level data
        Parameters:
            path : str - path to file
        Returns: list[list[str]] - level data
        '''

        EOF = ''
        buffer = ''
        data = []
        row = 0

        try:
            with open(path, 'r') as in_file:
                buffer = in_file.readline()
                while buffer != EOF:
                    data.append([])
                    for char in buffer:
                        data[row].append(char)
                    row += 1
                    buffer = in_file.readline()

        except IOError as e:
            print(f"Had trouble reading {path}!")

        return data
    
    def __spawn_tiles(self, level_data : list[list[str]], image_cache : ImageCache ) -> None :
        for i, row in enumerate(level_data):
            for j, val in enumerate(row):
                if(val == 'g'):
                    self.game_objects.append(GroundTile((40 * j) + 20, (40 * i) + 20, image_cache))
                    self.__ground.append(self.game_objects[-1])
                if(val == 'b'):
                    self.game_objects.append(GrassTile((40 * j) + 20, (40 * i) + 20, image_cache))
                if(val == 'c'):
                    self.game_objects.append(CoinTile((40 * j) + 20, (40 * i) + 20, image_cache))
                if(val == 't'):
                    self.game_objects.append(PalmTile((40 * j) + 40, (40 * i) - 20, image_cache))
                if(val == 'e'):
                    self.game_objects.append(ExitTile((40 * j) + 20, (40 * i) + 20, image_cache))
                if(val == 'j'):
                    self.game_objects.append(Jerk((40 * j) + 20, (40 * i) + 20, image_cache))
                if(val == 'l'):
                    self.game_objects.append(CloudTile((40 * j) + 40, (40 * i) + 40, image_cache))
                if(val == 'p'):
                    self.game_objects.append(Player((40 * j) + 20, (40 * i), image_cache))
                    self.__player = self.game_objects[-1]

    def __draw_game_objects(self) -> None:
        self.create_text(1000, 24, text=f"score: {self.__score:<8.2f}", font=('Arial', 24))
        for i, go in enumerate(self.game_objects):
            go.draw(self)
            if(self.__draw_hitbox):
                go.draw_hitbox(self)
        return None

    def __update_game_objects(self, delta : float) -> None:

        hit_ground = False

        # lets get the player attribs first
        p_x, p_y, P_w, p_h = self.__player.get_attribs()

        
        if(self.input_handler.key_is_down('move_left')):
            self.__player.push_signal('move_left')

        elif(self.input_handler.key_is_down('move_right')):
            self.__player.push_signal('move_right')
        else:
            self.__player.push_signal('move_neutral')
            
        if(self.input_handler.key_is_pressed('jump')):
            self.__player.push_signal('jump')

        for gr in self.__ground:
            if(self.__player.hit_test(gr)):
                ground_y = gr.get_attribs()[1] - 56
                self.__player.push_signal(f"hit_ground {ground_y}")
                hit_ground = True
                break

        for go in self.game_objects:
            if(isinstance(go, CoinTile)):
                if(self.__player.hit_test(go)):
                    self.game_objects.remove(go)
                    self.__score += 3.14

            if(isinstance(go, Jerk)):

                if(self.__player.hit_test(go)):
                    if(hit_ground):
                        self.die()
                    else:
                        self.game_objects.remove(go)
                    
            if(isinstance(go, ExitTile)):
                if(self.__player.hit_test(go)):
                    self.win()
                    return None

        for i, go in enumerate(self.game_objects):
            go.update(delta)

        if(self.__player.is_dead()):
            self.die()

        # the scrolling magic starts here
        if(p_x > 800):
            for go in self.game_objects:
                go.move_relative(-400 * delta, 0)

        self.input_handler.update()
        
        return None
        
    def despawn_all(self):
        self.game_objects = []            

    def die(self):
        messagebox.showinfo(title="oops", message="You've died horribly \n :/")
        self.alive = False

    def win(self):
        messagebox.showinfo(title="oops", message="You've won horribly \n :/")
        self.alive = False

    def update(self) -> None :
        '''
        Canvas widget update function.
        To be called in a loop.
        Parameters: None
        Returns: None
        '''
        delta = self.delta_time.get()

        # clear the entire screen
        self.delete('all')

        if(self.input_handler.key_is_released('hitbox')):
            self.__draw_hitbox = not self.__draw_hitbox

        self.__update_game_objects(delta)
        self.__draw_game_objects()

        # update base class
        super().update()
        super().update_idletasks()


#-----------------------------------------------------------------MAIN PROGRAM

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
        self.root.title('Simple Platformer')
        self.root.resizable(False, False)

        # program will run until this is False
        self.running = True

        # create and pack our canvas object
        self.game = Game(self.root)
        self.game.pack()

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

        self.game.update()

        if(self.game.alive == False):
            self.game.despawn_all()
            self.game.destroy()
            self.game = Game(self.root)
            self.game.pack()

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