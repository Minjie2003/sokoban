import pygame
import sys
from sokoban import *
import os
# 初始化 Pygame
pygame.init()
files = os.listdir("./map")
# 统计文件数量,其实就是有多少关
map_count = len(files)
# 屏幕尺寸
screen = pygame.display.set_mode((15*34, 15*34))
pygame.display.set_caption('推箱子')

# 颜色定义
white = (255, 255, 255)
black = (0, 0, 0)
gary = (200, 200, 200)
red = (255,0,0)

#设立字体
font_theme = pygame.font.Font("./谦度手写楷体.ttf", 36)
font_search = pygame.font.Font("./谦度手写楷体.ttf", 24)
font_ins = pygame.font.Font("./谦度手写楷体.ttf",20)
font_step = pygame.font.Font("BKANT.TTF",25)
icon = pygame.image.load("./bmp/icon.png")

# 关卡选择相关变量
input_box = []
for i in range(map_count):
    circle_rect = pygame.Rect(40+(i%6)*70, 230+(i//6)*60, 50, 50)  # 这里的矩形尺寸可以根据圆的直径来调整
    input_box.append(circle_rect)
goal = 0 #所选择的目标关卡
active = False

def draw_box(op,location):
    # 绘制关卡选择
    for i in range(map_count):
        if op and i == location:
            pygame.draw.ellipse(screen, black, input_box[i])  # 画关卡
            print_text(screen, font_theme, 57 + (i % 6) * 70, 235 + (i // 6) * 170, f'{i + 1}',white)
        else:
            pygame.draw.ellipse(screen, black, input_box[i], width=2)  #画关卡
            print_text(screen,font_theme,57+(i%6)*70, 235+(i//6)*170,f'{i+1}',black)


#画主页面
def main():
    global active, goal
    run = True
    while run:
        op = False
        location = 0
        mouse_pos = pygame.mouse.get_pos()
        for i in range(map_count):
            if input_box[i].collidepoint(mouse_pos):
                op = True
                location = i
                break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:   #鼠标按下时产生
                for i in range(map_count):
                    if input_box[i].collidepoint(event.pos):
                        goal = i+1
                        run = False
                #如果用户点击输入框


        screen.fill(white)
        draw_box(op,location)
        screen.blit(icon,(200,70))
        print_text(screen,font_theme,160,180,"推箱子小游戏",black)
        print_text(screen, font_ins, 5, 5, f"(游戏目前已有{map_count}关)", black)
        print_text(screen, font_ins, 5, 30, "游戏内容说明：q键退出，r键重置，z键返回上一步", black)
        print_text(screen, font_ins, 5, 55, "挑战成功后点击enter键可以进入下一关", black)
        print_text(screen, font_ins, 5, 80, "esc键返回主页面", black)
        print_text(screen, font_ins, 5, 105, "h键可以查看答案", black)
        print_text(screen, font_ins, 5, 145, "注意:", red)
        print_text(screen, font_ins, 60, 145, "小写字母", black)
        print_text(screen, font_ins, 5, 170, "请及时更改输入法", black)
        print_text(screen, font_ins, 330, 210, "(使用鼠标进行交互)", black)
        pygame.display.flip()

def soko(filename):
    run = True
    global goal
    sokobanTest = sokoban(filename)
    screen.fill(white)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not sokobanTest.win():
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
                    elif event.key == pygame.K_h:
                        get_reference_answer(sokobanTest)
                    elif event.key == pygame.K_ESCAPE:   #按下esc返回主页面
                        run=False
                else:
                    if event.key == pygame.K_ESCAPE:  # 按下esc返回主页面
                        run = False
                    elif event.key == pygame.K_RETURN:   #按下enter
                        goal = goal+1 if goal < map_count else 1
                        sokobanTest = sokoban(filename = f"./map/map{goal}.txt")

        sokobanTest.draw_map(screen)
        print_text(screen, font_step, 20, 10, f"Level:{goal}", white)
        print_text(screen, font_step, 380, 10, f"step:{str(sokobanTest.step)}", white)
        if sokobanTest.win():
            print_text(screen, font_theme, 200, 30, "挑战成功", white)
        # update the display
        pygame.display.update()

#读取answer
def get_reference_answer(sokoban):
    ans = ""
    with open(f'./answer/answer{goal}.txt','r') as f:
        ans += f.read()
        f.close()
    playerXTem = sokoban.playerX
    playerYTem = sokoban.playerY
    gameMapTem = tuple(tuple(row) for row in sokoban.gameMap)
    move = tuple(sokoban.move)
    stepTem = sokoban.step
    sokoban.reset_game()
    for i in range(len(ans)):
        if ans[i]== '1':
            if sokoban.is_valid_move(0, -1):
                sokoban.playerY -= 1
                sokoban.step += 1
        elif ans[i]== '2':
            if sokoban.is_valid_move(0, 1):
                sokoban.playerY += 1
                sokoban.step += 1
        elif ans[i]== '3':
            if sokoban.is_valid_move(-1, 0):
                sokoban.playerX -= 1
                sokoban.step += 1
        elif ans[i]== '4':
            if sokoban.is_valid_move(1, 0):
                sokoban.playerX += 1
                sokoban.step += 1
        sokoban.draw_map(screen)
        print_text(screen, font_step, 380, 10, f"step:{str(sokoban.step)}", white)
        if sokoban.win():
            print_text(screen, font_theme, 200, 30, "挑战成功", white)
        # update the display
        pygame.display.update()
        pygame.time.delay(200)
    pygame.time.delay(1000)
    sokoban.playerX = playerXTem
    sokoban.playerY = playerYTem
    sokoban.gameMap = [list(row) for row in gameMapTem]
    sokoban.move = list(move)
    sokoban.step = stepTem

if __name__ == '__main__':
    while True:
        main()
        filename = f"./map/map{goal}.txt"
        soko(filename)


