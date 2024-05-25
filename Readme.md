# 推箱子小游戏

### 1.运行环境

- `pip install pygame==2.5.2`

- `pip install -r requirements.txt`

项目运行基于`python3.11`，`pygame2.5.2`,同时，使用了`pyinstaller`进行文件的打包,如果你只是想体验推箱子的乐趣，clone仓库后使用仓库`main.exe`即可

### 2.文件说明

- `sokoban.py`  关于`sokoban`的类的构造，并使用了其中一张简单的图，算是一个基础版地图的推箱子
- `main.py` 在基础版推箱子的基础上，推出了更多的功能，以及可视化的主页面
- `answer`:每张map(map文件夹内)的参考答案
- `.ttf`文件：pygame用于文本的引入字体				

### 3.功能介绍

![index](https://s2.loli.net/2024/05/25/m2RPhnI8l5s6YEM.png)

- 该项目记录了的每张map都保存有answer，当你没有思路时，点击**h键**即可给你答案的参考
- 你可以随时按下**z键**返回所走的上一步
- 以及,可以点击**esc键**返回主页面

![map](https://s2.loli.net/2024/05/25/GP3eJ7liELozDVr.png)