import pygame,sys,time
from pygame.locals import *



##  Defines the Class for each cell  ##

class cell(object) :
    def __init__ (s):
        s.cs = 0
        s.ns = 0
        s.fs = 0

    def calcNS(s,i,j):
        s.ns =  o[(i+26)%27][j].cs + \
                o[(i+1)%27][j].cs + \
                o[(i+26)%27][(j+1)%47].cs + \
                o[(i+26)%27][(j+46)%47].cs + \
                o[(i+1)%27][(j+1)%47].cs + \
                o[(i+1)%27][(j+46)%47].cs + \
                o[i][(j+1)%47].cs +  \
                o[i][(j+46)%47].cs\

    def calcFS(s):
        if s.cs == 0 :
            if s.ns == 3 :
                s.fs=1            
            else :
                s.fs=0
        elif s.cs==1 :
            if (s.ns==2) or (s.ns==3) :
                s.fs=1
            else:
                s.fs=0

    def switchToFS(s):
        s.cs = s.fs


##  Defines some of the Global Variables used  ##


pygame.init()


o = [[cell() for j in range(47)] for i in range(27)]

mouse_click = False
##click = pygame.mouse.get_pressed()
##cur = pygame.mouse.get_pos()


white = (255,255,255)
black = (0,0,0)
d_grey = (169,169,169)

screen = pygame.display.set_mode((1200,580))
pygame.display.set_caption("Conway\'s Game of Life")

icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)


clock = pygame.time.Clock()


##  Some Functions that are used in the main Program  ##


def message_to_screen(msg,color,(posx,posy), f_size = 25, f_type = "comicsansms"):
    font = pygame.font.SysFont(f_type,f_size)
    screen_text = font.render(msg,True, color)
    text_box = screen_text.get_rect()
    screen.blit(screen_text, [posx - text_box.center[0], posy - text_box.center[1]])


def button(msg, (posx, posy), width, height,
           inactive_colour, active_colour, 
           function):
    
    click = pygame.mouse.get_pressed()
    cur = pygame.mouse.get_pos()
    
    if posx + width > cur[0] > posx and posy + height > cur[1] > posy:
        pygame.draw.rect(screen, active_colour, [posx,posy,width,height])
        if click[0] == 1:
            time.sleep(0.1)
            function()
    else:
        pygame.draw.rect(screen, inactive_colour, [posx,posy,width,height])
    message_to_screen(msg, black, (posx+width/2,posy+height/2))


def draw_grid():
    for a in range(20,960,20):
        for b in range(20,560,20):
            i = b/20-1
            j = a/20-1
            if o[i][j].cs == 0:
                pygame.draw.rect(screen, black, [a,b,19,19],1)
            else:
                pygame.draw.rect(screen, black, [a,b,19,19])
                

def set_state(c):
    j = (c[0] -((c[0]-20)%20))
    i = (c[1] -((c[1]-20)%20))
    i = i/20-1
    j = j/20-1
    
    if  i<27 and j<47:
        if o[i][j].cs == 1 and mouse_click == False:
            o[i][j].cs = 0
            draw_grid()

            button("Start", (1025,40) , 100, 50, white, d_grey, game_play)                   
            button("Step", (1025,140), 100, 50, white, d_grey, runStep)
            button("Clear", (1025,240), 100, 50, white, d_grey, game_clear)
            button("Quit", (1025,340), 100, 50, white, d_grey, game_exit)
            
            pygame.display.update()     
            time.sleep(0.1)
        else:
            o[i][j].cs = 1


def runStep():
    for i in range(27):
        for j in range(47):
            o[i][j].calcNS(i,j)
            o[i][j].calcFS()
            
    for i in range(27):
        for j in range(47):
            o[i][j].switchToFS()
    

##  Contains the Main Loops and Different states of the Game  ##


def start_screen():    
    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
 
        screen.fill(white)
        
        message_to_screen("Conway's", black, (120,40), 25)
        message_to_screen("GAME", black, (200,100), 100)
        message_to_screen("OF", black, (200,200), 100)
        message_to_screen("LIFE", black, (200,300), 100)
        button("Begin", (100,400), 100, 50, white, d_grey, game_start)
        button("Quit", (200,400), 100, 50, white, d_grey, game_exit)
        button("Read More", (750,400), 150, 50, white, d_grey, game_help)
        
        message_to_screen("The project consists of a computer based version of the mathematical game \"Life\"   ", black, (800,100), 18)
        message_to_screen("designed by John Horton Conway.                                                      ", black, (720,120), 18)
        message_to_screen("It is a zero player game that requires the user to only enter the initial states.    ", black, (785,150), 18)
        message_to_screen("The game starts with the user chossing some of the cells to be alive.                ", black, (770,180), 18)
        message_to_screen("Every generation cells are born and die according to the following two rules :       ", black, (780,210), 18)
        message_to_screen("1.  A live cell with two or three live neighbours survives into the next generation, ", black, (800,240), 18)
        message_to_screen("otherwise it dies of starvation or overcrowding.                                     ", black, (770,260), 18)
        message_to_screen("2.  A dead cell with exactly three live neighbours is born in the next generation.   ", black, (800,280), 18)
        message_to_screen("Note: Neighbours means the eight cells adjacent to any cell.                         ", black, (800,310), 18)
        message_to_screen("Normally it is done in an infinite plane but in this it is done on a torus.          ", black, (775,340), 18)
        
        pygame.display.update()
        clock.tick(30)


def game_start():

    time.sleep(0.4)
    
    global mouse_click
    
    while True:
        for event in pygame.event.get():        
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(white)
        click = pygame.mouse.get_pressed()
        cur = pygame.mouse.get_pos()
        
        if click[0] == 1:
            set_state(cur)
            draw_grid()        
            mouse_click = True                         
        else:
            mouse_click = False

        button("Start", (1025,40) , 100, 50, white, d_grey, game_play)                   
        button("Step", (1025,140), 100, 50, white, d_grey, runStep)
        button("Clear", (1025,240), 100, 50, white, d_grey, game_clear)
        button("Quit", (1025,340), 100, 50, white, d_grey, game_exit)

        clock.tick(30)
        draw_grid()
        
        pygame.display.update()


def game_play():
    while True:
        for event in pygame.event.get():        
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(white)

        button("Stop", (1025,40) , 100, 50, white, d_grey, game_start)                   
        button("Step", (1025,140), 100, 50, white, d_grey, runStep)
        button("Clear", (1025,240), 100, 50, white, d_grey, game_clear)
        button("Quit", (1025,340), 100, 50, white, d_grey, game_exit)

        runStep()        

        clock.tick(30)
        draw_grid()
        
        pygame.display.update()


def game_clear():
    for i in range(27):
        for j in range(47):
            o[i][j].cs = 0


def game_exit():
    pygame.quit()
    sys.exit()


def game_help():
    import os
    os.startfile("Help.html")


## To start the game  ##


start_screen()


