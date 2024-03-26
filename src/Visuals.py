# Example file showing a basic pygame "game loop"
import pygame
import pygame_menu
from pygame_menu import themes
import math

game_state = 'menu' 

def set_difficulty(value, difficulty):
    print(value)
    print(difficulty)
    
def set_players(value, players):
    print(value)
    print(players)

def set_ai(value, ai):
    print(value)
    print(ai)
 
def start_the_game():
    global game_state
    game_state = 'game'
    pygame.display.set_mode((1220,1172),pygame.RESIZABLE)
 
def level_menu():
    mainmenu._open(level)
    
def draw_grid(screen, center_x, center_y, radius, num_rings, num_lines):
    for i in range(1, num_rings + 1):
        pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), radius * i / num_rings, 1)
    
    for i in range(num_lines):
        angle = 2 * math.pi * i / num_lines
        end_x = center_x + radius * math.cos(angle)
        end_y = center_y + radius * math.sin(angle)
        pygame.draw.line(screen, (255, 255, 255), (center_x, center_y), (end_x, end_y), 1)

if __name__ == '__main__':
    screenWidth = 1280
    screenHeight = 720
    
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    clock = pygame.time.Clock()
    running = True

    '''
        Menu Stuff
    '''
    mainmenu = pygame_menu.Menu('KingOil the Board Game', screenWidth, screenHeight, 
                                    theme=themes.THEME_DEFAULT)
    mainmenu.add.button('Play', start_the_game)
    mainmenu.add.button('Level', level_menu)
    mainmenu.add.button('Quit', pygame_menu.events.EXIT)
    
    level = pygame_menu.Menu('Select Settings', screenWidth, screenHeight, 
                                    theme=themes.THEME_DEFAULT)
    level.add.selector('Difficulty: \t',[('Hard',1),('Easy',2)], 
                       onchange=set_difficulty)
    level.add.selector('Players: \t', [('One',1),('Two',2), ('Three',3), ('Four',4)],  
                       onchange=set_players)
    level.add.selector('AI: \t', [('On',1),('Off',2)],  
                       onchange=set_ai)

    bg = pygame.image.load("background.png")
    #bg = pygame.transform.scale(bg, (screenWidth, screenHeight))
    
    '''
        Main Loop
    '''
    while running:
    
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False
    
        if game_state == 'menu':
            if mainmenu.is_enabled():
                mainmenu.update(events)
                mainmenu.draw(screen)
                
        elif game_state == 'game':
            x = (screen.get_width() - bg.get_width()) // 2
            y = (screen.get_height() - bg.get_height()) // 2
            
            screen.fill((32,79,81))
            screen.blit(bg,(x,y))
            draw_grid(screen, (screen.get_width()/2), (screen.get_height()/2), (screenHeight-100), 7, 48)

        pygame.display.flip()
        pygame.display.update()

        clock.tick(30)  # limits FPS to 30

    pygame.quit()
    