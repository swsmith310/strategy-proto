import pygame
import requests
import sys
from colors import COLORS

SERVER = sys.argv[1]

SCREEN_SIZE = (640, 480)
BLOCK_SIZE = 40
running = True

class Player():
    def __init__(self,name,x,y,rgb):
        self.name = name
        self.x = x
        self.y = y
        self.mapX = (self.x * BLOCK_SIZE) + 4
        self.mapY = (self.y * BLOCK_SIZE) + 4
        self.w = 32
        self.h = 32
        self.rgb = rgb
        self.color = rgb
        self.active = False
        self.range = 3
        print(requests.get(F"http://{SERVER}/?player={self.name}").text)
    def isClicked(self, mouse):
        return mouse[0] > self.mapX and mouse[0] < self.mapX + self.w and mouse[1] > self.mapY and mouse[1] < self.mapY + self.h
    def draw(self, screen):
        if self.active:
            self.color = (0x00, 0xFF, 0x00)
        else:
            self.color = self.rgb
        pygame.draw.rect(screen, self.color, [self.mapX, self.mapY, self.w, self.h])  
    def move(self, x, y):
        self.x = x
        self.y = y
        self.mapX = (x * BLOCK_SIZE) + 4
        self.mapY = (y * BLOCK_SIZE) + 4
        self.active = False
    def disconnect(self):
        print(requests.get(F"http://localhost:8080/?player={self.name}&logout=True").text)

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("STRATEGY PROTO CLIENT v0.0.1a")
    screen = pygame.display.set_mode(SCREEN_SIZE)
    player_one = Player("P1",1,1, (0,0,255))
    player_two = Player("P2",14,10, (255,0,0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1]
            if (player_one.active):
                x = int(mouseX / BLOCK_SIZE) if abs(player_one.x - int(mouseX / BLOCK_SIZE)) <= player_one.range else 0 
                y = int(mouseY / BLOCK_SIZE) if abs(player_one.y - int(mouseY / BLOCK_SIZE)) <= player_one.range else 0
                if x != 0 and y != 0:
                    player_one.move(x, y)
                print(requests.get(F"http://{SERVER}/?player={player_one.name}&x={x}&y={y}").text)
            if (player_one.isClicked(pygame.mouse.get_pos())):
                player_one.active = not player_one.active
                print(requests.get(F"http://{SERVER}/?player={player_one.name}&clicked=True&active={player_one.active}").text)
                break
            if (player_two.isClicked(pygame.mouse.get_pos())):
                player_two.active = not player_two.active
                print(requests.get(F"http://{SERVER}/?player={player_two.name}&clicked=True&active={player_two.active}").text)
                break

    screen.fill(COLORS["BLACK"])
    for x in range(int(SCREEN_SIZE[0]/BLOCK_SIZE)):
        for y in range(int(SCREEN_SIZE[1]/BLOCK_SIZE)):
            pygame.draw.rect(screen, COLORS["WHITE"], [x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE , BLOCK_SIZE], 1)
    player_one.draw(screen)
    player_two.draw(screen)
    pygame.display.flip()

player_one.disconnect()
player_two.disconnect()
