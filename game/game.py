import pygame
import sys
from random import randint
import config

pygame.init()

speed = [0, -1]

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH + 200, config.SCREEN_HEIGHT))
        pygame.display.set_caption(config.CAPTION)
        self.clock = pygame.time.Clock()
        self.running = True
        self.snake = Snake()
        self.collectable = Collectable()
        self.score = 0
        self.font = pygame.font.Font(None, 36)

    def Run(self):
        while self.running:
            self.screen.fill(config.COLOR_GREEN)
            pygame.draw.rect(self.screen, config.COLOR_DARK_GREEN, pygame.Rect(config.SCREEN_WIDTH, 0, 200, config.SCREEN_HEIGHT))
            self.Event(pygame.event.get())
            self.collectable.Draw(self.screen)
            self.snake.Draw(self.screen)
            self.snake.Move()
            self.screen.blit(self.Create_scorring(), (config.SCREEN_WIDTH + 10, 10))

            collision = self.snake.Get_body_collision()
            if collision:
                self.running = False
                print("Votre score est de " + str(self.score) + " points.")
            
            collision = self.snake.Get_collectable_collision(self.collectable.coordinate)
            if collision:
                self.collectable.New_coordinate(self.snake.coordinate)
                self.snake.Enlarge()
                self.score += 1

            collision = self.snake.Get_wall_collision()
            if collision:
                self.running = False
                print("Votre score est de " + str(self.score) + " points.")

            pygame.display.flip()
            self.clock.tick(5)

    def Event(self, events):
        global speed
        for event in events:
                if event.type == pygame.QUIT:
                    print("Votre score est de " + str(self.score) + " points.")
                    self.running == False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d and speed != [-1, 0]:
                        speed = [1, 0]
                    if event.key == pygame.K_q and speed != [1, 0]:
                        speed = [-1, 0]
                    if event.key == pygame.K_z and speed != [0, 1]:
                        speed = [0, -1]
                    if event.key == pygame.K_s and speed != [0, -1]:
                        speed = [0, 1]

    def Create_scorring(self):
        text = "score: " + str(self.score)
        return self.font.render(text, True, config.COLOR_WHITE)

class Snake:
    def __init__(self):
        self.head = (config.CELL_X // 2, config.CELL_Y // 2 + 1)
        self.coordinate = [
            (self.head[0], self.head[1]),
            (self.head[0], self.head[1] + 1),
            (self.head[0], self.head[1] + 2),
            (self.head[0], self.head[1] + 3)
        ]

    def Draw(self, screen):
        global speed
        for coordinate in self.coordinate:
            if self.coordinate.index(coordinate) % 2 == 0:
                color = config.COLOR_BLUE
            else:
                color = config.COLOR_LIGHT_BLUE
            rect = pygame.Rect(coordinate[0] * config.CELL_SIZE, coordinate[1] * config.CELL_SIZE, config.CELL_SIZE, config.CELL_SIZE)
            pygame.draw.rect(screen, color, rect)

    def Move(self):
        new_coordinate = self.coordinate.copy()
        new_coordinate.insert(0, (self.head[0] + speed[0], self.head[1] + speed[1]))
        new_coordinate.pop(-1)
        self.head = new_coordinate[0]
        self.coordinate = new_coordinate

    def Enlarge(self):
        x_0, y_0 = self.coordinate[-1]
        x_1, y_1 = self.coordinate[-2]

        if x_0 - x_1 > 0:
            self.coordinate.append((x_0 + 1, y_0))
        elif x_0 - x_1 < 0:
            self.coordinate.append((x_0 - 1, y_0))
        elif y_0 - y_1 > 0:
            self.coordinate.append((x_0, y_0 + 1))
        elif y_0 - y_1 < 0:
            self.coordinate.append((x_0, y_0 - 1))

    def Get_body_collision(self):
        if self.head in self.coordinate[1:]:
            return True
        else:
            return False
    
    def Get_collectable_collision(self, collectable):
        if self.head == collectable:
            return True
        else: 
            return False
        
    def Get_wall_collision(self):
        if self.head[0] < 0 or self.head[0] > config.CELL_X - 1:
            return True
        elif self.head[1] < 0 or self.head[1] > config.CELL_Y - 1:
            return True
        else: 
            return False

class Collectable:
    def __init__(self):
        self.coordinate = (config.CELL_X // 2, config.CELL_Y // 2 - 3)

    def New_coordinate(self, snake):
        while self.coordinate in snake:
            self.coordinate = (randint(0, config.CELL_X - 1), randint(0, config.CELL_Y -1))

    def Draw(self, screen):
        stick = pygame.Rect(self.coordinate[0] * config.CELL_SIZE + 9, self.coordinate[1] * config.CELL_SIZE - 8, 2, 8)
        rect = pygame.Rect(self.coordinate[0] * config.CELL_SIZE, self.coordinate[1] * config.CELL_SIZE, config.CELL_SIZE, config.CELL_SIZE)
        pygame.draw.rect(screen, config.COLOR_RED, rect)
        pygame.draw.rect(screen, config.COLOR_BROWN, stick)