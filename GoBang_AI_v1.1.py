#-*- coding:utf-8 -*-

import numpy as np
import pygame as pyg
import os

Grid_Width = 40
Grid_Height = 40
offset_left = 40
offset_top = 40
NoPiece = 0
WhitePiece = 1
BlackPiece = 2
WinCount = 0
Running = True
Movement = True 
GG = NoPiece

chess_data = np.zeros([15,15], dtype = np.int)  # 存放棋盘数据
piece = np.zeros([2], dtype = np.int)  # 存放玩家落子位置
mark = np.zeros([2], dtype = np.int)  # 标记AI落子的当前点

# 赢法与赢法统计
wins = np.zeros([15,15,600], dtype = np.int)  # 赢法数组

for i in range (15):  # 横线所有赢法
    for j in range(11):
        for k in range(5):
            wins[j+k][i][WinCount] = True
        WinCount += 1  

for i in range (15):  # 竖线所有赢法
    for j in range(11):
        for k in range(5):
            wins[i][j+k][WinCount] = True
        WinCount += 1        

for i in range (11):  # 斜线所有赢法
    for j in range(11):
        for k in range(5):
            wins[i+k][j+k][WinCount] = True
        WinCount += 1   

for i in range (11):  # 反斜线所有赢法
    for j in range(14,3,-1):
        for k in range(5):
            wins[j-k][i+k][WinCount] = True
        WinCount += 1  
        
print WinCount  #15*15五子棋中所有赢法的数量

# 赢法统计数组
player_win = np.zeros([WinCount], dtype = np.int)
AI_win = np.zeros([WinCount], dtype = np.int)

         
# 初始化pyg
pyg.init()

# 初始化mixer
pyg.mixer.init()

WIDTH = 640
HEIGHT = 640
screen = pyg.display.set_mode((WIDTH, HEIGHT))
pyg.display.set_caption("GoBang")

# 设置一个定时器，用于固定时间刷新屏幕
FPS = 30
clock = pyg.time.Clock()

# 加载背景图片
base_folder = os.path.dirname(__file__)
img_folder = os.path.join(base_folder, 'images')
background_img = pyg.image.load(os.path.join(img_folder, 'background.jpg')).convert()		

# 绘制文本    
def drawText(self,text,posx,posy,textHeight=30,fontColor=(0,0,0),backgroudColor=(255,255,255)):
        fontObj = pyg.font.SysFont('SimHei', textHeight)  # 通过字体文件获得字体对象
        textSurfaceObj = fontObj.render(unicode(text, 'utf-8'), True,fontColor,backgroudColor)  # 配置要显示的文字
        textRectObj = textSurfaceObj.get_rect()  # 获得要显示的对象的rect
        textRectObj.center = (posx, posy)  # 设置显示对象的坐标
        self.blit(textSurfaceObj, textRectObj)  # 绘制字    

# 绘制棋盘
def draw_chessmap(surface):
	# 加载背景图片
	surface.blit(background_img, (0,0)) 
	
	# 绘制横线
	pyg.draw.line(surface, (0,0,0), (offset_left, offset_top), (Grid_Width*14+offset_left, offset_top), 2)
	
	for i in range(13):
		pyg.draw.line(surface, (0,0,0), (offset_left, Grid_Height*(i+1)+offset_top), (Grid_Width*14+offset_left, Grid_Height*(i+1)+offset_top), 1)
		
	pyg.draw.line(surface, (0,0,0), (offset_left, Grid_Height*14+offset_top), (Grid_Width*14+offset_left, Grid_Height*14+offset_top), 2)
	
	# 绘制竖线
	pyg.draw.line(surface, (0,0,0), (offset_left, offset_top), (offset_left, Grid_Height*14+offset_top), 2)
	
	for i in range(13):
		pyg.draw.line(surface, (0,0,0), (Grid_Width*(i+1)+offset_left, offset_top), (Grid_Width*(i+1)+offset_left, Grid_Height*14+offset_top), 1)
		
	pyg.draw.line(surface, (0,0,0), (Grid_Width*14+offset_left, offset_top), (Grid_Width*14+offset_left, Grid_Height*14+offset_top), 2)

	# 绘制9个圆心点
	for i in range(3):
		for j in range(3):
			pyg.draw.circle(surface, (0,0,0), (Grid_Width*4*j+(Grid_Width*3+offset_left), Grid_Height*4*i+(Grid_Height*3+offset_top)), 5)
        

        
# 绘制棋子(遍历整个棋盘判断落子)
def draw_piece(surface):   
    # 绘制所有落子
    for i in range(15):
        for j in range(15):
            if chess_data[i,j] == NoPiece:  #不能落子
                pass
            elif chess_data[i,j] == BlackPiece:  #落黑子
                pyg.draw.circle(surface, (0,0,0), ((i*Grid_Width+offset_left), (j*Grid_Height+offset_top)), 15)
            elif chess_data[i,j] == WhitePiece:  #落白子
                pyg.draw.circle(surface, (255,255,255), ((i*Grid_Width+offset_left), (j*Grid_Height+offset_top)), 15)

                
# 判定输赢
def game_over(color, p1, p2):
    i = p1
    j = p2
    for k in range(WinCount):
        if wins[i, j, k]:
            if color == BlackPiece:
                player_win[k] += 1
                AI_win[k] = 6  # 如果第k种赢法上有黑子, 则对白子来说第k种赢法已经不可能实现
                if player_win[k] == 5:
                    return True
            elif color == WhitePiece:
                AI_win[k] += 1
                player_win[k] = 6  # 如果第k种赢法上有白子, 则对黑子来说第k种赢法已经不可能实现
                if AI_win[k] == 5:
                    return True  
    return False

# 计算机AI
def computer_AI():
    player_score = np.zeros([15, 15], dtype = np.int)
    AI_score = np.zeros([15, 15], dtype = np.int)
    max_score = 0  # 记录当前最高分数
    u = 0  # 记录最优点
    v = 0
    
    for i in range(15):  # 遍历整个棋盘
        for j in range(15):
            if chess_data[i, j] == NoPiece:
                for k in range(WinCount):  # 为玩家给每个点打分, AI对最优点进行拦截(防守)
                    if wins[i, j, k]:
                        if player_win[k] == 1:
                            player_score[i, j] += 200
                        elif player_win[k] == 2:
                            player_score[i, j] += 400
                        elif player_win[k] == 3:
                            player_score[i, j] += 2000
                        elif player_win[k] == 4:
                            player_score[i, j] += 10000
                        
                        if AI_win[k] == 1:  # 为AI给每个点打分, AI对最优点落子(进攻)
                            AI_score[i, j] += 220
                        elif AI_win[k] == 2:
                            AI_score[i, j] += 420
                        elif AI_win[k] == 3:
                            AI_score[i, j] += 2100
                        elif AI_win[k] == 4:
                            AI_score[i, j] += 20000
                
                #  获取分值最高的最优点
                # 为玩家获取最优点(如果最优点是玩家的则AI会在该点落子以进行防守)
                if player_score[i, j] > max_score:
                    max_score = player_score[i, j]
                    u = i
                    v = j
                elif player_score[i, j] == max_score:  # 如果有评分相同的点, 则为AI自己打一次分, 在分高的点落子
                    if AI_score[i, j] > AI_score[u, v]:
                        u = i
                        v = j
                 
                # 为AI获取最优点(如果最优点是AI的则AI会在该点落子以进行进攻)                 
                if AI_score[i, j] > max_score:
                    max_score = AI_score[i, j]
                    u = i
                    v = j
                elif AI_score[i, j] == max_score:  # 如果有评分相同的点, 则为玩家打一次分, 在分高的点落子
                    if player_score[i, j] > player_score[u, v]:
                        u = i
                        v = j      

    chess_data[u, v] = WhitePiece  # AI在最优点落子   
    mark[0] = u
    mark[1] = v
    return game_over(WhitePiece, u, v)
     
                
#主循环
while Running:
	# 设置屏幕刷新频率
    clock.tick(FPS)

	# 处理不同事件
    for event in pyg.event.get():
        
        if event.type == pyg.QUIT:  # 退出程序
            Running = False
        elif event.type == pyg.MOUSEBUTTONDOWN:  # 点击落子
            # 计算离鼠标点击最近的点
            piece[0] = int(round(event.pos[0] / (Grid_Width + .0)) - 1)
            piece[1] = int(round(event.pos[1] / (Grid_Width + .0)) - 1)
            #print piece[0]
            #print piece[1]
            
            # 如果该点没有落子
            if chess_data[piece[0], piece[1]] == NoPiece:

                chess_data[piece[0], piece[1]] = BlackPiece
                draw_chessmap(screen)  # 画出棋盘
                draw_piece(screen)  #  画出棋子
                
                if game_over(BlackPiece, piece[0], piece[1]):  # 输赢判定
                    GG = BlackPiece
                    
                elif computer_AI():  # 如果玩家还没赢则AI落子
                    GG = WhitePiece
            
    draw_chessmap(screen)  # 画出棋盘
    draw_piece(screen)  #  画出棋子
    
    # 标记AI落子的当前点
    pyg.draw.line(screen, (255,0,0), (mark[0]*Grid_Width+offset_left-5, mark[1]*Grid_Height+offset_top), (mark[0]*Grid_Width+offset_left+5, mark[1]*Grid_Height+offset_top), 1)
    pyg.draw.line(screen, (255,0,0), (mark[0]*Grid_Width+offset_left, mark[1]*Grid_Height+offset_top-5), (mark[0]*Grid_Width+offset_left, mark[1]*Grid_Height+offset_top+5), 1)
    
    # 显示胜负结果
    if GG == BlackPiece:
        drawText(screen,'游戏结束: 你赢了!',320,320)
    elif GG == WhitePiece:
        drawText(screen,'游戏结束: 你输了!',320,320)

	# 刷新屏幕
    pyg.display.flip()