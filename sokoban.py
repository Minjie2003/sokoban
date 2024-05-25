import sys, pygame
from pygame.locals import *


class sokoban(object):
    def __init__(self, filename):
        self.step = 0  # 步数
        self.gameMap = []  # 地图，通过外部的文件进行加载

        # 分别显示player的坐标，init用于回溯
        self.playerX = 0
        self.playerXInit = 0
        self.playerY = 0
        self.playerYInit = 0
        self.destCoordinate = []  # 用于记录目的地的列表
        self.destNumber = 0  # 用于记录
        self.move = []  #用于记录行动的轨迹，方便回溯

        f = open(filename, "r")
        mapData = f.readlines()
        f.close()

        # count and clean up trivia data
        for mapDataLine in mapData:
            self.gameMap.append(list(mapDataLine.strip()))  #将其构造成一个双重列表

        for y in range(15):
            for x in range(15):
                tem = self.gameMap[y][x]
                if tem == '5':
                    self.playerX = x
                    self.playerXInit = x
                    self.playerY = y
                    self.playerYInit = y
                    self.gameMap[y][x] = '2'
                if tem == '4':
                    self.destCoordinate.append([x, y])
                    self.destNumber += 1

        self.gameMapInit = tuple(tuple(row) for row in self.gameMap)  # 作为一个元组，起矫正作用
        # 加载背景图片
        self.backgroundImg = pygame.image.load('./bmp/Bmp0.gif')
        self.wallImg = pygame.image.load('./bmp/Bmp1.gif')
        self.floorImg = pygame.image.load('./bmp/Bmp2.gif')
        self.boxImg = pygame.image.load('./bmp/Bmp3.gif')
        self.destinationImg = pygame.image.load('./bmp/Bmp4.gif')
        self.playerImg = pygame.image.load('./bmp/Bmp5.gif')

        #加载字体和颜色,用字典序的方式存储，rgb(r,g,b)
        self.color = {}
        self.color['white'] = 255, 255, 255
        self.color['cyan'] = 0, 255, 255
        self.color['yellow'] = 255, 255, 0
        self.color['purple'] = 255, 0, 255
        self.color['green'] = 0, 255, 0
        self.color['red'] = 255, 0, 0
        self.color['black'] = 0,0,0

    #对动作进行判断
    def is_valid_move(self, dx, dy):
        new_x = self.playerX + dx
        new_y = self.playerY + dy
        if self.gameMap[new_y][new_x] == '1':   #wall
            return False
        if self.gameMap[new_y][new_x] == '3':   #box
            # 箱子更改
            box_new_x = new_x + dx
            box_new_y = new_y + dy
            # 判断：箱子的下一个位置是2还是4,4是destination
            if self.gameMap[box_new_y][box_new_x] in '24':
                self.gameMap[box_new_y][box_new_x] = '3'
                if self.gameMapInit[new_y][new_x] == '4':
                    self.gameMap[new_y][new_x] = '4'
                else:
                    self.gameMap[new_y][new_x] = '2'
                self.move.append([1,dx, dy]) #第二种情况是参与了箱子
                return True
            return False
        # 剩余2和5的情况为真，第一种情况是只有player参与了move
        self.move.append([0,dx,dy])
        return True
    #回退上一步
    def game_back(self):
        try:
            listTem = self.move.pop()
            # 判断回溯的上一个
            if listTem[0] == 1:
                self.gameMap[self.playerY][self.playerX] = '3'
                temY = self.playerY + listTem[2]
                temX = self.playerX + listTem[1]
                self.gameMap[temY][temX] = self.gameMapInit[temY][temX] if self.gameMapInit[temY][temX] != '3'  else '2'
            self.playerX -= listTem[1]
            self.playerY -= listTem[2]
            self.step -= 1
        except:
            print("已是最新状态")

    def reset_game(self):
        #回溯到游戏刚开始的状态
        self.gameMap = [list(row) for row in self.gameMapInit]
        self.playerX = self.playerXInit
        self.playerY = self.playerYInit
        self.step = 0
        self.move.clear()

    #判断获胜
    def win(self):
        for i in range(self.destNumber):
            if self.gameMap[int(self.destCoordinate[i][1])][int(self.destCoordinate[i][0])] != '3':
                return False
        return True

    #渲染
    def draw_map(self, screen):
        for y in range(15):
            for x in range(15):
                tile = self.gameMap[y][x]
                if tile == '0':
                    screen.blit(self.backgroundImg, (x * 34, y * 34))
                elif tile == '1':
                    screen.blit(self.wallImg, (x * 34, y * 34))
                elif tile == '2':
                    screen.blit(self.floorImg, (x * 34, y * 34))
                elif tile == '3':
                    screen.blit(self.boxImg, (x * 34, y * 34))
                elif tile == '4':
                    screen.blit(self.destinationImg, (x * 34, y * 34))
        screen.blit(self.playerImg,(self.playerX*34,self.playerY*34))
    #初始化文本
    def text_init(self,screen,font):
        print_text(screen,font,0,0,"按r键重新开始游戏")
        print_text(screen,font,0,30,"按z键返回上一步")
        print_text(screen,font,0,60, "按q键退出游戏")
        print_text(screen,font,0,470,"注意:以上都是小写字母，未触发请调整输入法",(255, 0, 0))
        print_text(screen,font, 420, 10, f"step:{str(self.step)}", self.color['white'])

def print_text(screen,font, x, y, text, color=(255,255,255)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x,y))

if __name__ == '__main__':
    pygame.init()  # pygame初始化
    pygame.display.set_caption('推箱子游戏')
    # 屏幕大小和方块大小
    gridSize = 15
    tileSize = 33
    screenSize = gridSize * tileSize
    # 设置屏幕像素
    screen = pygame.display.set_mode((screenSize, screenSize))

    font1 = pygame.font.Font("./谦度手写楷体.ttf", 40)
    font2 = pygame.font.Font("./谦度手写楷体.ttf", 24)
    sokobanTest = sokoban("./map/map2.txt")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                elif event.key == pygame.K_UP:
                    if sokobanTest.is_valid_move(0, -1):
                        sokobanTest.playerY -= 1
                        sokobanTest.step += 1
                elif event.key == pygame.K_DOWN:
                    if sokobanTest.is_valid_move(0, 1):
                        sokobanTest.playerY += 1
                        sokobanTest.step += 1
                elif event.key == pygame.K_LEFT:
                    if sokobanTest.is_valid_move(-1, 0):
                        sokobanTest.playerX -= 1
                        sokobanTest.step += 1
                elif event.key == pygame.K_RIGHT:
                    if sokobanTest.is_valid_move(1, 0):
                        sokobanTest.playerX += 1
                        sokobanTest.step += 1
                elif event.key == pygame.K_z:
                    sokobanTest.game_back()
                elif event.key == pygame.K_r:  # 按下r键
                    sokobanTest.reset_game()  # 重新开始游戏

        sokobanTest.draw_map(screen)
        sokobanTest.text_init(screen,font2)
        if sokobanTest.win():
            print_text(screen,font1,200,235,"挑战成功",sokobanTest['red'])
        # update the display
        pygame.display.update()
