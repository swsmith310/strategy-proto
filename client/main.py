import pygame
import requests

SCREEN_SIZE = (640, 480)
BLOCK_SIZE = 40
running = True

class Player():
    def __init__(self,name,x,y):
        self.name = name
        self.x = x
        self.y = y
        self.w = 32
        self.h = 32
        print(requests.get(F"http://localhost:8080/?player={self.name}").text)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), [(self.x * BLOCK_SIZE) + 4, (self.y * BLOCK_SIZE) + 4, self.w, self.h])  
    def disconnect(self):
        print(requests.get(F"http://localhost:8080/?player={self.name}&logout=True").text)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    player_one = Player("P1",1,1)
    player_two = Player("P2",9,9)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,25,25))
    for x in range(int(SCREEN_SIZE[0]/BLOCK_SIZE)):
        for y in range(int(SCREEN_SIZE[1]/BLOCK_SIZE)):
            pygame.draw.rect(screen, (0,0,0), [x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE , BLOCK_SIZE], 1)
    player_one.draw(screen)
    player_two.draw(screen)
    pygame.display.flip()

player_one.disconnect()
player_two.disconnect()
