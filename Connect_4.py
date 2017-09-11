####################################
##
##Jerry Aska
##
##Connect 4
##
####################################

###########################################################################################################################
##                                                  Constants Declaration
###########################################################################################################################

import pygame, pygame.gfxdraw, sys, random, math
from pygame.locals import *

pygame.init()

# colours        R    G    B

WHITE          = (255, 255, 255)
GREY           = (125, 125, 125)
BLACK          = (  0,   0,   0)
RED            = (255,   0,   0)
ORANGE         = (255, 125,   0)
YELLOW         = (255, 255,   0)
GREEN          = (  0, 255,   0)
BLUE           = (  0,   0, 255)
PURPLE         = (255,   0, 255)

list_of_colors         = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, BLACK, WHITE]
list_of_colors_names   = ["RED", "ORANGE", "YELLOW", "GREEN", "BLUE", "PURPLE", "BLACK", "WHITE"]
scr_height             = 600
scr_width              = 700
DISPLAYSURF            = pygame.display.set_mode((scr_width, scr_height),pygame.RESIZABLE)
##SECONDSURF             = DISPLAYSURF.copy()
##pxarray                = pygame.PixelArray(SECONDSURF)

list_of_functions      = ["Player 1", "Player 2", "Background"]


SCREEN_COLOR     = GREEN
SCREEN_RATIO     = 7/6
GRID_FACTOR      = 6

TOOL_BAR_COLOR   = RED
BAR_HEIGHT       = 25

STRIKE_COLOR     = YELLOW

TEXT_COLOR                 = WHITE
TEXT_BG_COLOR              = PURPLE
HIGHLIGHTED_TEXT_COLOR     = YELLOW
HIGHLIGHTED_TEXT_BG_COLOR  = BLACK

FONT_STYLE                 = "calibri"
FONT_SIZE_PERCENT          = 5
MENU_HEIGHT_PERCENT        = 5
MENU_WIDTH_PERCENT         = 20

color = [[RED, BLUE],["Red", "Blue"]]
 
###########################################################################################################################
##                                                  Classes Definition
###########################################################################################################################

class nothing:
    """
    Place Holder Object

    This object is simply to be used as a default for relational operators for when there is no object to relate to.
    It contains all the attributes necessary for relational operators in this program set to 0 indicating to other objects
    that there is nothing there.
    """
    def __init__(self, pos_x = 0, pos_y = 0, height = 0, width = 0, space_above = 0, space_to_the_left = 0):
        self.pos_x              = pos_x
        self.pos_y              = pos_y
        self.height             = height
        self.width              = width
        self.space_above        = space_above
        self.space_to_the_left  = space_to_the_left
        self.is_nothing         = True

###########################################################################################################################

class screen:
    """
    Screen Object

    This object contains attributes to allow for a miniature screen within the display surface. This object can be given a
    specific ratio and will maintain this ratio even when the display surface is resized. It can also be given items to
    share the display surface with and can be resized to allow space for those objects while still maintaining the ratio.
    """
    def __init__(self, width = scr_width, height = scr_height, item_above = nothing(), item_to_the_left = nothing(), space_to_the_left = 0, space_above = 0, color = SCREEN_COLOR, ratio = SCREEN_RATIO, grid_factor = GRID_FACTOR):
        self.pos_x              = item_to_the_left.pos_x + item_to_the_left.width + item_to_the_left.space_to_the_left
        self.pos_y              = item_above.pos_y + item_above.height + item_above.space_above
        self.space_to_the_left  = space_to_the_left
        self.space_above        = space_above
        self.width              = width - item_to_the_left.width
        self.height             = height - item_above.height
        self.item_to_the_left   = item_to_the_left
        self.item_above         = item_above
        self.color              = color
        self.ratio              = ratio
        self.is_nothing         = False
        self.grid_size          = self.height / grid_factor


    def display(self):
        DISPLAYSURF.fill(self.color, ((self.pos_x + self.space_to_the_left, self.pos_y + self.space_above), (self.width, self.height)))


    def resize(self, new_width, new_height, item_above = nothing(), item_to_the_left = nothing()):
        if not item_to_the_left.is_nothing:
            self.item_to_the_left = item_to_the_left
        if not item_above.is_nothing:
            self.item_above = item_above
        new_width = new_width - (self.item_to_the_left.pos_x + self.item_to_the_left.width)
        new_height = new_height - (self.item_above.pos_y + self.item_above.height)
        ratio = new_width / new_height
        if ratio == self.ratio:
            self.width = new_width
            self.height = new_height
            self.space_above = 0
            self.space_to_the_left = 0
        if ratio > self.ratio:
            self.width = int(new_height * self.ratio)
            self.height = new_height
            self.space_to_the_left = (new_width - self.width) // 2
            self.space_above = 0
        if ratio < self.ratio:
            self.width = new_width
            self.height = int(new_width / self.ratio)
            self.space_to_the_left = 0
            self.space_above = (new_height - self.height) // 2
        self.grid_size          = self.height / 6

###########################################################################################################################
        
class bar:
    """
    Bar Object
    
    This object contains attributes for creating a bar, for example a task or tool bar.
    It can also be given an objevt to follow and will allign itself width-wise to this
    object.
    """
    def __init__(self, width = scr_width, height = BAR_HEIGHT, item_above = nothing(), item_to_the_left = nothing(), space_to_the_left = 0, space_above = 0, color = WHITE, something = nothing()):
        self.pos_x              = item_to_the_left.pos_x + item_to_the_left.width + item_to_the_left.space_to_the_left
        self.pos_y              = item_above.pos_y + item_above.height  + item_above.space_above
        self.space_to_the_left  = space_to_the_left
        self.space_above        = space_above
        self.width              = width
        self.height             = height
        self.item_to_the_left   = item_to_the_left
        self.item_above         = item_above
        self.color              = color
        self.ratio              = width / (height * 25)
        self.is_nothing         = False

        
    def display(self):
        DISPLAYSURF.fill(self.color, ((self.pos_x + self.space_to_the_left, self.pos_y + self.space_above), (self.width, self.height)))


    def resize(self, item_to_follow = nothing()):
        self.width              = item_to_follow.width
        self.space_to_the_left  = item_to_follow.space_to_the_left
        self.space_above        = item_to_follow.space_above

###########################################################################################################################

class sector:
    """
    
    """
    def __init__(self, sector_pos, screen, color = WHITE):
        self.sector_pos  = sector_pos
        self.pos_x       = (sector_pos % 7) * screen.grid_size + screen.space_to_the_left + screen.pos_x
        self.pos_y       = (sector_pos // 7) * screen.grid_size + screen.space_above + screen.pos_y
        self.width       = screen.width // 7
        self.height      = screen.height // 6
        self.mid_x       = self.pos_x + self.width // 2
        self.mid_y       = self.pos_y + self.height // 2
        self.radius      = min(self.width,self.height) // 2
        self.state       = False
        self.color       = color
        self.points      = 0
        self.screen      = screen
        self.type        = "None"
        self.is_nothing  = False

        
    def reset(self, color = WHITE):
        self.state  = False
        self.type   = "None"
        self.color  = color

        
    def resize(self, screen = nothing()):  
        if not screen.is_nothing:
            self.screen = screen      
        self.pos_x   = (self.sector_pos % 7) * self.screen.grid_size + self.screen.space_to_the_left + self.screen.pos_x
        self.pos_y   = (self.sector_pos // 7) * self.screen.grid_size + self.screen.space_above + self.screen.pos_y
        self.len_x   = self.screen.width // 7
        self.len_y   = self.screen.height // 6
        self.mid_x   = self.pos_x + self.len_x // 2
        self.mid_y   = self.pos_y + self.len_y // 2
        self.radius  = min(self.len_x,self.len_y) // 2

        
    def set_state(self, player, color = WHITE):
        if not self.state:
            self.type  = str(player)
            self.state = True
            self.color = color

            
    def is_clicked(self, mouse_pos_x, mouse_pos_y):
        if mouse_pos_x > self.pos_x and mouse_pos_x < self.pos_x + self.len_x:
            if mouse_pos_y > self.pos_y and mouse_pos_y < self.pos_y + self.len_y:
                return True
        return False


    def recolor(self, player, new_color):
        if self.type == str(player):
            self.color = new_color

    
    def do_function(self, sector_list, player):
        column_list = []
        for y in range(self.sector_pos % 7, len(sector_list.list), 7):
            column_list.append(y)
        for y in column_list[-1::-1]:
            if not sector_list.list[y].state:
                drop_animation(self.screen, sector_list.list[y % 7], sector_list.list[column_list[-1]], sector_list.list[y], color = color[0][player])
                sector_list.list[y].set_state(player, color = color[0][player])
                return (player + 1) % 2

                    
    def display(self):
        pygame.gfxdraw.filled_circle(DISPLAYSURF, int(self.mid_x), int(self.mid_y), int(self.radius), self.color)

###########################################################################################################################


class menu_item:
    """
    
    """
    def __init__(self, item_pos, screen, text = "Menu Item", screen_width_percentage = 0, font_style = FONT_STYLE, font_size_percent = FONT_SIZE_PERCENT,
                 height_percent = MENU_HEIGHT_PERCENT, width_percent = MENU_WIDTH_PERCENT, text_color = TEXT_COLOR, highlighted_text_color = HIGHLIGHTED_TEXT_COLOR,
                 bg_color = TEXT_BG_COLOR, highlighted_bg_color = HIGHLIGHTED_TEXT_BG_COLOR, is_drop_down = False, item_to_the_left = nothing()):
        self.pos_x                    = int(screen.space_to_the_left + screen.pos_x + screen.width * screen_width_percentage / 100) + item_to_the_left.width + item_to_the_left.pos_x
        self.pos_y                    = screen.space_above + screen.pos_y + int(screen.height * height_percent / 100) * item_pos
        self.is_drop_down             = is_drop_down
        self.item_to_the_left         = item_to_the_left        
        self.item_pos                 = item_pos
        self.screen_width_percentage  = screen_width_percentage
        self.text                     = text
        self.text_color               = text_color
        self.bg_color                 = bg_color
        self.highlighted_text_color   = highlighted_text_color
        self.highlighted_bg_color     = highlighted_bg_color
        self.height_percent           = height_percent
        self.width_percent            = width_percent
        self.height                   = int(screen.height * height_percent / 100)
        self.width                    = int(screen.width * width_percent / 100)
        self.style                    = font_style
        self.size                     = font_size_percent / 100
        self.font                     = pygame.font.SysFont(self.style, int(screen.height * self.size))
        self.screen                   = screen
        self.highlight                = False
        self.is_nothing               = False

        
    def resize(self, item_to_the_left = nothing(), screen = nothing()):  
        if not screen.is_nothing:
            self.screen = screen
        if not item_to_the_left.is_nothing:
            self.item_to_the_left = item_to_the_left
        self.height = int(self.screen.height * self.height_percent / 100)
        self.width  = int(self.screen.width * self.width_percent / 100)  
        self.pos_x  = int(self.screen.space_to_the_left + self.screen.pos_x + self.screen.width * self.screen_width_percentage / 100)
        self.pos_y  = self.item_to_the_left.pos_y - self.item_to_the_left.height+ self.screen.space_above + self.screen.pos_y + self.height * self.item_pos
        self.font   = pygame.font.SysFont(self.style, int(self.screen.height * self.size))

            
    def is_clicked(self, mouse_pos_x, mouse_pos_y):
        if mouse_pos_x > self.pos_x and mouse_pos_x < self.pos_x + self.width:
            if mouse_pos_y > self.pos_y and mouse_pos_y < self.pos_y + self.height:
                return True
        return False


    def is_highlighted(self, mouse_pos_x, mouse_pos_y):
        if mouse_pos_x > self.pos_x and mouse_pos_x < self.pos_x + self.width:
            if mouse_pos_y > self.pos_y and mouse_pos_y < self.pos_y + self.height:
                self.highlight = True
            else:
                self.highlight = False
        else:
            self.highlight = False
    

    def do_function(self, ignore, ignore_still):
        print(self.text)
        if self.text in list_of_colors_names:
            return list_of_colors[list_of_colors_names.index(self.text)]
        if self.text == "Player 1":
            new_color = menu_loop(colors, drop_from = self)
            if not new_color == None:
                for y in range(len(sectors.list)):
                    sectors.list[y].recolor(0, new_color)
                    color[0][0] = new_color
        if self.text == "Player 2":
            new_color = menu_loop(colors, drop_from = self)
            if not new_color == None:
                for y in range(len(sectors.list)):
                    sectors.list[y].recolor(1, new_color)
                    color[0][1] = new_color
        if self.text == "Background":
            new_color = menu_loop(colors, drop_from = self)
            if not new_color == None:
                self.screen.color = new_color
        return None
        

        
    def display(self):
        if not self.highlight:
            bg_color = self.bg_color
            TEXT = pygame.font.Font.render(self.font, self.text, True, self.text_color)
        elif self.highlight:
            bg_color = self.highlighted_bg_color
            TEXT = pygame.font.Font.render(self.font, self.text, True, self.highlighted_text_color)
                                           
        pygame.draw.rect(DISPLAYSURF, bg_color, (self.pos_x, self.pos_y, self.width, self.height))
        DISPLAYSURF.blit(TEXT, (self.pos_x, self.pos_y))

            
###########################################################################################################################
      
class object_list:
    """
    
    """
    def __init__(self):
        self.list       = []
        self.is_nothing = False

        
    def append(self, item):
        self.list.append(item)

        
    def resize(self, item_to_follow = nothing()):
        for y in range (len(self.list)):
            self.list[y].resize(item_to_follow)

            
    def reset(self, color = WHITE):
        for x in range(len(self.list)):
            self.list[x].reset(color = color)


    def check_if_highlighted(self, mouse_pos_x, mouse_pos_y):
        for x in range(len(self.list)):
            self.list[x].is_highlighted(mouse_pos_x, mouse_pos_y)

            
##    def check_if_clicked_2(self, mouse_pos_x, mouse_pos_y, player):
##        for x in range(len(self.list)):
##            if self.list[x].is_clicked(mouse_pos_x, mouse_pos_y):
##                column_list = []
##                for y in range(x%7, len(self.list), 7):
##                    column_list.append(y)
##                for y in column_list[-1::-1]:
##                    if not self.list[y].state:
##                        self.list[y].set_state(color = color[0][player])
##                        return (player + 1) % 2
##        return player

    
    def check_if_clicked(self, mouse_pos_x, mouse_pos_y, player):
        for x in range(len(self.list)):
            if self.list[x].is_clicked(mouse_pos_x, mouse_pos_y):
                check = self.list[x].do_function(self, player)
                if check == None:
                    break
                else:
                    return check
        return player

    
    def display(self):
        for y in range (len(self.list)):
            self.list[y].display()

###########################################################################################################################
##                                                  Functions Definition
###########################################################################################################################

def com_play(screen, sectors, player):
    """
    Computer Artificial Intellegence

    Allows the computer to play interactively with a user.
    At current the computer simply selects a play randomly.
    """
    pygame.time.delay(500)
    column_list = []
    x = random.randrange(0, len(sectors.list))
    for y in range(x%7, len(sectors.list), 7):
        column_list.append(y)
    for y in column_list[-1::-1]:
        if not sectors.list[y].state:
            drop_animation(screen, sectors.list[y % 7], sectors.list[column_list[-1]], sectors.list[y], color = color[0][player])
            sectors.list[y].set_state(player, color = color[0][player])
            return (player + 1) % 2

###########################################################################################################################
        
def draw_strike(screen, win_sector_1, win_sector_2, y):
    """
    Draws a Strike

    Draws a strike between two sectors to display the winning
    combination to the user(s).
    """
    FPS = 60
    fpsClock = pygame.time.Clock()
    sleep_time = 50
    strike_vect_x = int((win_sector_2.mid_x - win_sector_1.mid_x)/99)
    strike_vect_y = int((win_sector_2.mid_y - win_sector_1.mid_y)/99)
    strike_pos_x = win_sector_1.mid_x
    strike_pos_y = win_sector_1.mid_y
    
    while True:
        for event in pygame.event.get():
            if (event.type == MOUSEBUTTONDOWN) or (event.type == KEYDOWN):
                FPS = 500
                sleep_time = 0 
        pygame.draw.circle(DISPLAYSURF, STRIKE_COLOR, (int(strike_pos_x), int(strike_pos_y)), screen.width//60)
        strike_pos_x += strike_vect_x
        strike_pos_y += strike_vect_y
        fpsClock.tick(FPS)
        pygame.display.update()
        if not y == 6:
            if strike_pos_x > win_sector_2.mid_x:
                break
            if strike_pos_y > win_sector_2.mid_y:
                break
        else:
            if strike_pos_y > win_sector_2.mid_y:
                break
    pygame.time.delay(sleep_time)

###########################################################################################################################
    
def display_results(winning_color, x, y, z):
    """
    
    """
    draw_strike(game_screen, sectors.list[x], sectors.list[x+y*z], y)
    winner_name = color[1][color[0].index(winning_color)]
    print(winner_name,"Wins")
    start_time = pygame.time.get_ticks()
    sectors.reset()
    results_screen = True
    while results_screen:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
                results_screen = False
        current_time = pygame.time.get_ticks()
        if current_time - start_time > 2000:
            results_screen = False

###########################################################################################################################
            
def check_for_winner(sectors):
    """
    
    """
    count = 0
    for x in range(len(sectors.list)):
        if sectors.list[x].state:
            for y in [1,6,7,8]:
                count = 0
                for z in range(4):
                    if x + y * z < len(sectors.list):
                        if (not (x + y * z) % 7 == 0) or z == 0:
                            if sectors.list[x+y*z].state:
                                if sectors.list[x+y*z].color == sectors.list[x].color:
                                    count +=1
                if count == 4:
                    break
        if count == 4:
            break
    if count == 4:
        display_results(sectors.list[x].color, x, y, z)        
        return True
    return False

###########################################################################################################################

##def draw_circle_outline(mid_x, mid_y, radius, color):
##    for x in range(-radius, radius):
##        for y in range(-radius, radius):
##            if ((radius-x)*(radius+x) > 0) and ((radius-y)*(radius+y) > 0):
##                if ((- math.sqrt((radius-x)*(radius+x)) < y) or (math.sqrt((radius-x)*(radius+x)) > y)) and ((- math.sqrt((radius-y)*(radius+y)) < x) or (math.sqrt((radius-y)*(radius+y)) > x)):
##                    if not ((- math.sqrt((radius-x)*(radius+x)) < y) and (math.sqrt((radius-x)*(radius+x)) > y)):
##                        pxarray[x + mid_x,y + mid_y] = color
##
##def draw_grid_2(screen, top_sector, color):
##    print("attempting to draw grid")
##    x = top_sector.sector_pos % 7
##    for y in range(6):
##        draw_circle_outline(top_sector.mid_x, top_sector.pos_y + top_sector.height * y, top_sector.radius, color)
##    DISPLAYSURF.blit(SECONDSURF.unlock(),(0,0))

###########################################################################################################################

def drop_animation(screen, start_sector, bottom_sector, end_sector, color):
    FPS = 60
    fpsClock = pygame.time.Clock()
    sleep_time = 50
    drop_vect_y = int((bottom_sector.mid_y - start_sector.mid_y)/99)
    drop_pos_x = start_sector.mid_x
    drop_pos_y = start_sector.mid_y
    while True:
        for event in pygame.event.get():
            if (event.type == MOUSEBUTTONDOWN) or (event.type == KEYDOWN):
                FPS = 500
                sleep_time = 0
        objects.display()
        pygame.draw.circle(DISPLAYSURF, color, (int(drop_pos_x), int(drop_pos_y)), start_sector.radius)
        drop_pos_y += drop_vect_y
        fpsClock.tick(FPS)
        draw_grid()
##        draw_grid_2(screen, start_sector, YELLOW)
        pygame.display.update()
        if drop_pos_y > end_sector.mid_y:
            break
    pygame.time.delay(sleep_time)

###########################################################################################################################  

def draw_grid():
    
    for x in range(round(game_screen.width/game_screen.grid_size) + 1):
        pygame.draw.line(DISPLAYSURF,WHITE,(x * game_screen.grid_size + game_screen.space_to_the_left + game_screen.pos_x, game_screen.space_above + game_screen.pos_y),(x * game_screen.grid_size + game_screen.space_to_the_left + game_screen.pos_x, game_screen.space_above + game_screen.height + game_screen.pos_y))
    for y in range(round(game_screen.height/game_screen.grid_size) + 1):
        pygame.draw.line(DISPLAYSURF,WHITE,(game_screen.space_to_the_left + game_screen.pos_x, y * game_screen.grid_size + game_screen.space_above + game_screen.pos_y), (game_screen.space_to_the_left + game_screen.width + game_screen.pos_x, y * game_screen.grid_size + game_screen.space_above + game_screen.pos_y))

###########################################################################################################################
        
def menu_loop(items, drop_from = nothing()):
    pygame.event.clear()
    if not drop_from.is_nothing:
        items.resize(item_to_follow = drop_from)
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                for x in range(len(items.list)):
                    items.list[x].highlight = False
                return None
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
                value = items.check_if_clicked(mouse_pos_x, mouse_pos_y, None)
                for x in range(len(items.list)):
                    items.list[x].highlight = False
                return value
            if event.type == MOUSEMOTION:
                mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
                items.check_if_highlighted(mouse_pos_x, mouse_pos_y)
            if event.type == VIDEORESIZE:
                DISPLAYSURF = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)            
                game_screen.resize(event.w, event.h)
                tool_bar.resize(item_to_follow = game_screen)
                sectors.resize()
                items.resize()
                objects.display()
        items.display()
        pygame.display.update()
        
###########################################################################################################################
##                                                  Instance Creation
###########################################################################################################################

tool_bar    = bar(color = TOOL_BAR_COLOR)

game_screen = screen(item_above = tool_bar)
game_screen.resize(scr_width, scr_height)

sectors     = object_list()
for y in range(42):
    sectors.append(sector(y, game_screen))
    
menu_items  = object_list()
for y in range(len(list_of_functions)):
    menu_items.append(menu_item(y, game_screen, list_of_functions[y]))
    
colors  = object_list()
for x in range(len(list_of_colors_names)):
    colors.append(menu_item(x, game_screen, list_of_colors_names[x], screen_width_percentage = 20))
                    
objects     = object_list()
objects.append(tool_bar)
objects.append(game_screen)
objects.append(sectors)

player = 0
com = True

###########################################################################################################################
##                                                  Main Game Loop
###########################################################################################################################

while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_c:
                com = not com
            if event.key == K_m:              
                menu_loop(menu_items)
        if event.type == MOUSEBUTTONDOWN:
            mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
            player = sectors.check_if_clicked(mouse_pos_x, mouse_pos_y, player)
        if event.type == VIDEORESIZE:
            DISPLAYSURF = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)            
            game_screen.resize(event.w, event.h)
            tool_bar.resize(item_to_follow = game_screen)
            sectors.resize()
            menu_items.resize()
            colors.resize()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    DISPLAYSURF.fill(GREY)
    objects.display()
    draw_grid()
    pygame.display.update()
    if check_for_winner(sectors):
        player = 0
    if player == 1 and com:
        player = com_play(game_screen, sectors, player)

###########################################################################################################################
##                                                  End of Program
###########################################################################################################################
