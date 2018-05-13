#Imports+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import pygame, sys, random, math ,time
from pygame.locals import *




        

#Game Data++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Black = (0,0,0)
White = (255,255,255)
Red = (200,0,0)
Bright_Red = (255,0,0)
Blue = (0,0,255)
Green = (0,200,0)
Bright_Green = (0,255,0)
fps = 30
fpsclock = pygame.time.Clock()


#Initialising Pygame and setting Display +++++++++++++++++++++++++++++++++++++++
pygame.init()                                                                   
SurfObj = pygame.display.set_mode((500,500))
pygame.display.set_caption("Random Run")



#CatImg+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Catgirl_img = pygame.image.load("catgirl.png")

cat_posx = 20
cat_posy = 410
cat_width = (50-10)     #Actual Width of Image body = 40 (5 pixels from both right and leftside have to be ommited)++++++  o1o
cat_hieght = (85 - 30) #Actual Hieght of catgirl body = 55 
Cat_all = [cat_posx,cat_posy,cat_width,cat_hieght]

T_hieght = 100
Upper_limit = (410 - T_hieght)
Lower_limit = 410
jump_state = 1
speed = 3
a = 0.9
s = 0


    

#Box+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Box_posx = 600
Box_posy = 430
Box_width = 30
Box_hieght = 30
Box_all = [Box_posx,Box_posy,Box_width,Box_hieght]

Box_speed = 7
speed_increas = 0


#Score +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
score = 0

# High Score +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def get_HS():
    High_score_file_r = open("Highscore.txt",'r')
    High_score = int(High_score_file_r.read())                          
    High_score_file_r.close()
    return(High_score)

def save_HS(score):
    High_score_file_w = open("Highscore.txt",'w')                        
    High_score_file_w.write(str(score))
    High_score_file_w.close()
    #return(True)

previous_High_score = (get_HS())

# Some Func. +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def cat_jump(x,y,UL,LL,speed,state = 1):
    'Handels the Cat jump'
    if state == 1:
        return(x,y,state)                         #1 = rest
    elif state == 2:                              #2 = jump
        if y > UL:                                #UL = Upper limit
            y -= speed
        elif y <= UL:
            state = 3
            #y = UL
    elif state == 3:                              #3 = fall
        if y < LL:                                #LL = Lower limit
            y += speed
        elif y >= LL:
            state = 1
            y = LL #++++++++++++++++++++++++++++++# Keeps the cat on the Surface
    return((x,y,state))




def cal_speed(s,a):
    'Handels the speed change during cat\'s jump'
    v = (math.sqrt(2*a*s))
    return(v)



def Overlap(fig1,fig2):        #fig = [x,y,w,h] #[Fig1 = box,Fig2 = cat]
    'check\'s if cat\'s image overlapped with the Box\'s'
    
    top_fig1 = fig1[1]
    left_fig1 = fig1[0]
    right_fig1 = fig1[0]+fig1[2]
    bottom_fig1 = fig1[1]+fig1[3]

    top_fig2 = fig2[1]
    left_fig2 = fig2[0]+10
    right_fig2 = fig2[0]+fig2[2]  #o1o Actual Width of Image body = 30(10 pixels from both right and leftside have to be ommited)
    bottom_fig2 = fig2[1]+fig2[3] 

    if left_fig2 < left_fig1 < right_fig2 or left_fig2 < right_fig1 < right_fig2:
        if top_fig2 < top_fig1 <= bottom_fig2:
            return(top_fig2,top_fig1,bottom_fig2)
            

#Button ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def Button(x,y,w,h,Deep_color,Bright_color,text):
    border = 7
    top_left_border = 3
    #color = Deep_color
    pygame.draw.rect(SurfObj,Deep_color,(x-top_left_border,y-top_left_border,w+border,h+border))       #Button rect

    fontObj = pygame.font.Font("ariali.ttf",15)#
    textObj = fontObj.render(text,True,Black)        #Button Text   
    textRectObj = textObj.get_rect()                 #
    textRectObj.topleft = (x,y)                      #   
    SurfObj.blit(textObj,textRectObj)                #

    mouse_pos = pygame.mouse.get_pos()                        #
    if x < mouse_pos[0] < (x+w) and y < mouse_pos[1] < (y+h): #Button Hover
        pygame.draw.rect(SurfObj,Bright_color,(x,y,w,h))      #
        SurfObj.blit(textObj,textRectObj)
        
        Right_clicked = (pygame.mouse.get_pressed()[0] == 1)#
        if Right_clicked:                                   #Button Clicking
            return (True)                                   #

#Crash Func. +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def Crash_screen(score,if_exit):
    previous_High_score = get_HS()    #past_High_score
    if previous_High_score >= score:
        High_score = previous_High_score
    elif previous_High_score < score: 
        High_score = score
        save_HS(score)

        
        
    Myfont3 = pygame.font.Font("ariali.ttf",27)
    High_score_Surf = Myfont3.render("High Score:- %s " %(High_score),True,White,Blue)
    High_score_Rect = High_score_Surf.get_rect()
    High_score_Rect.topleft = (160,248)
    SurfObj.blit(High_score_Surf,High_score_Rect)
    
	
    Myfont = pygame.font.Font("ariali.ttf",75)
    crashSurf = Myfont.render("CRASHED!!!",True,White,Bright_Red)
    crashRect = crashSurf.get_rect()
    crashRect.topleft = (10,150)
    SurfObj.blit(crashSurf, crashRect)

    Myfont2 = pygame.font.Font("ariali.ttf",27)
    scoreSurf = Myfont2.render("Your Score:- %s" %(score),True,Black,Bright_Red)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (160,278)
    SurfObj.blit(scoreSurf,scoreRect)


    if if_exit == 12:
        pygame.quit()
        sys.exit()

# Game State +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
crashed = False
sound_count = 0

#Game loop +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
while True:
    #SurfObj.fill(White)
    #Event Handler++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_UP and jump_state != 3:
            jump_state = 2
        elif cat_posy > 410:
            cat_posy = 410

    SurfObj.fill(White)

    #Score ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    if not crashed:
        MYFONT = pygame.font.Font("ariali.ttf",32)
        scoreSurf = MYFONT.render("Score: %s" %(str(score)),True,White,Bright_Red)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (0,0)
        SurfObj.blit(scoreSurf, scoreRect)
        
    # Crash Screen +++++++++++++++++++++++++++++++++++++++++++++++++++++++
    if crashed:
        Crash_screen(score,event.type)           #Crash Screen
##        if sound_count == 0:
##            soundObj = pygame.mixer.Sound("badswap.wav")
##            soundObj.play()
##            time.sleep(1)
##            soundObj.stop()
##            sound_count = 1
##        
    if crashed and previous_High_score < score:
        Myfont4 = pygame.font.Font("ariali.ttf",23)
        New_record_Surf = Myfont4.render("New   Record!",True,White,Bright_Green)     #New_Record
        New_record_Rect = New_record_Surf.get_rect()
        New_record_Rect.topleft = (175,310)
        SurfObj.blit(New_record_Surf,New_record_Rect)        
        
        
    if crashed:
        Play_again = Button(160,350,75,15,Green,Bright_Green,"Play Again")
        QUIT = Button(260,350,40,15,Green,Bright_Green,"QUIT")
        if Play_again:
            crashed = False                                                            #Buttons(*Play again and *QUIT)
            Box_posx = 600
            score = 0
            previous_High_score = (get_HS())
            sound_count = 0

        elif QUIT:
            pygame.quit()
            sys.exit()
        


            
    #Cat_Jump ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    SurfObj.blit(Catgirl_img,(cat_posx,cat_posy))
    
    if not crashed:                                                                              #Checkes if game Crashed
                 jump = cat_jump(cat_posx,cat_posy,Upper_limit,Lower_limit,speed,jump_state)     #Calling 'cat_jump' function as (jump) which returns (x,y,state)
                 jump_state = jump[2]                                                            #Changing cat's state 
                 cat_posy = jump[1]                                                              #Changing cat's hieght
                 s = abs(cat_posy - Upper_limit)                                                 # s = Hieght Left to cover
                 speed = cal_speed(s,a)                                                          #Calls cal_speed() func. to calculate cat's instantaneous speed
        
    #Box Animation++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    pygame.draw.rect(SurfObj,Black,(Box_posx,Box_posy,Box_width,Box_hieght))
    pygame.draw.line(SurfObj,Black,(0,460),(500,460))
    if Box_posx < -30:
        Box_posx = 600
        score += 1
        Box_speed = (random.randint(8,16))
    else:
        if not crashed:
            Box_posx -= Box_speed
    # Overlap ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    Box_all = [Box_posx,Box_posy,Box_width,Box_hieght]
    Cat_all = [cat_posx,cat_posy,cat_width,cat_hieght]
    
    if Overlap(Box_all,Cat_all):
        crashed = True
        

        
    fpsclock.tick(60)
    pygame.display.update()
    














