#encoding=utf-8
import random
import sys
import pygame
from pygame.locals import *

SIZE = 4
PIXEL = 150
SCORE_PIXEL = 100

class Array(object):
    ''' 2048 Matric '''
    def __init__(self, size):
        self.size = size
        self.score = 0
        self.array = [[0 for i in range(size)] for j in range(size)]
        self.add()
        self.add()

    def add(self):
        while True:
            pos = random.randint(0, self.size*self.size-1)
            if self.array[pos/self.size][pos%self.size-1] == 0:
                num = 2 if random.randint(0, 4) > 0 else 4 
                self.array[pos/self.size][pos%self.size-1] = num
                self.score += 10 * num
                break

    def MoveLeft(self):
        change = False
        for i in range(self.size):
            ind = 0
            for j in range(1, self.size):
                if self.array[i][j] != 0:
                    k = j - 1
                    while k - ind >= 0:
                        if self.array[i][k] == 0:
                            self.array[i][k], self.array[i][k+1] = self.array[i][k+1], self.array[i][k]
                            change = True
                            k -= 1
                            continue
                        if self.array[i][k] == self.array[i][k+1]:
                            self.array[i][k] *= 2
                            self.array[i][k+1] = 0
                            ind += 1
                            change = True
                            break
                        break
        return change

    def MoveRight(self):
        change = False
        for i in range(self.size):
            ind = 0
            for j in range(self.size-2, -1, -1):
                if self.array[i][j] != 0:
                    k = j + 1
                    while k + ind < self.size:
                        if self.array[i][k] == 0:
                            self.array[i][k], self.array[i][k-1] = self.array[i][k-1], self.array[i][k]
                            change = True
                            k += 1
                            continue
                        if self.array[i][k] == self.array[i][k-1]:
                            self.array[i][k] *= 2
                            self.array[i][k-1] = 0
                            ind += 1
                            change = True
                            break
                        break
        return change

    def MoveUp(self):
        change = False
        for i in range(self.size):
            ind = 0
            for j in range(1, self.size):
                if self.array[j][i] != 0:
                    k = j - 1
                    while k - ind >= 0:
                        if self.array[k][i] == 0:
                            self.array[k][i], self.array[k+1][i] = self.array[k+1][i], self.array[k][i]
                            change = True
                            k -= 1
                            continue
                        if self.array[k][i] == self.array[k+1][i]:
                            self.array[k][i] *= 2
                            self.array[k+1][i] = 0
                            ind += 1
                            change = True
                            break
                        break
        return change

    def MoveDown(self):
        change = False
        for i in range(self.size):
            ind = 0
            for j in range(self.size-2, -1, -1):
                if self.array[j][i] != 0:
                    k = j + 1
                    while k + ind < self.size:
                        if self.array[k][i] == 0:
                            self.array[k][i], self.array[k-1][i] = self.array[k-1][i], self.array[k][i]
                            change = True
                            k += 1
                            continue
                        if self.array[k][i] == self.array[k-1][i]:
                            self.array[k][i] *= 2
                            self.array[k-1][i] = 0
                            ind += 1
                            change = True
                            break
                        break
        return change

    def Over(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.array[i][j] == 0:
                    return False
                if j - 1 >= 0 and self.array[i][j-1] == self.array[i][j]:
                    return False
                if i - 1 >= 0 and self.array[i-1][j] == self.array[i][j]:
                    return False
        return True

# 更新屏幕
def show(array):
    for i in range(SIZE):
        for j in range(SIZE):
            # 背景颜色块
            screen.blit(array.array[i][j] == 0 and block[(i + j) % 2] or block[2 + (i + j) % 2], (PIXEL * j, PIXEL * i))
            # 数值显示
            if array.array[i][j] != 0:
                map_text = map_font.render(str(array.array[i][j]), True, (106, 90, 205))
                text_rect = map_text.get_rect()
                text_rect.center = (PIXEL * j + PIXEL / 2, PIXEL * i + PIXEL / 2)
                screen.blit(map_text, text_rect)
    # 分数显示
    screen.blit(score_block, (0, PIXEL * SIZE))
    score_text = score_font.render((array.Over() and "Game over with score " or "Score: ") + str(array.score), True, (106, 90, 205))
    score_rect = score_text.get_rect()
    score_rect.center = (PIXEL * SIZE / 2, PIXEL * SIZE + SCORE_PIXEL / 2)
    screen.blit(score_text, score_rect)
    pygame.display.update()

if __name__ == '__main__':
    arr = Array(SIZE)
    pygame.init()
    screen = pygame.display.set_mode((PIXEL * SIZE, PIXEL * SIZE + SCORE_PIXEL))
    pygame.display.set_caption("2048")
    block = [pygame.Surface((PIXEL, PIXEL)) for i in range(4)]
    # 设置颜色
    block[0].fill((152, 251, 152))
    block[1].fill((240, 255, 255))
    block[2].fill((0, 255, 127))
    block[3].fill((225, 255, 255))
    score_block = pygame.Surface((PIXEL * SIZE, SCORE_PIXEL))
    score_block.fill((245, 245, 245))
    # 设置字体
    map_font = pygame.font.Font(None, PIXEL * 2 / 3)
    score_font = pygame.font.Font(None, SCORE_PIXEL * 2 / 3)
    clock = pygame.time.Clock()
    show(arr)
    while not arr.Over():
        event = pygame.event.poll()
        if event.type == QUIT:
            sys.exit()
        # 接收玩家操作
        if event.type == KEYDOWN:
            if event.key in [K_w, K_UP]:
                if arr.MoveUp():
                    arr.add()
            elif event.key in [K_s, K_DOWN]:
                if arr.MoveDown():
                    arr.add()
            elif event.key in [K_a, K_LEFT]:
                if arr.MoveLeft():
                    arr.add()
            elif event.key in [K_d, K_RIGHT]:
                if arr.MoveRight():
                    arr.add()
        show(arr)
    # 游戏结束
    pygame.time.delay(3000) 