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
Running = True
Movement = True 
GG = NoPiece

chess_data = np.zeros([15,15], dtype = np.int)  # 存放棋盘数据
piece = np.zeros([2], dtype = np.int)  # 存放玩家落子位置

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
    for i in range(15):
        for j in range(15):
            if chess_data[i,j] == NoPiece:  #不能落子
                pass
            elif chess_data[i,j] == BlackPiece:  #落黑子
                pyg.draw.circle(surface, (0,0,0), ((i*Grid_Width+offset_left), (j*Grid_Height+offset_top)), 15)
            elif chess_data[i,j] == WhitePiece:  #落白子
                pyg.draw.circle(surface, (255,255,255), ((i*Grid_Width+offset_left), (j*Grid_Height+offset_top)), 15)

                
# 判定输赢
def game_over(color): 
    Counter  = 0  # 计数器
    Gameover = False
    
    # 左右
    for i in range(4):
        if piece[0]-(i+1) < 0:  # 超出棋盘判定范围
            break
        elif chess_data[piece[0]-(i+1), piece[1]] == color:
            Counter = Counter + 1
            if Counter == 4:
                Counter = 0
                Gameover = True
                return Gameover
                break
        else:
            break
    
    for i in range(4):
        if piece[0]+(i+1) > 14:  # 超出棋盘判定范围
            Counter = 0
            break 
        elif chess_data[piece[0]+(i+1), piece[1]] == color:
            Counter = Counter + 1
            if Counter == 4:
                Counter = 0
                Gameover = True
                return Gameover
                break
        else:
            Counter = 0
            break
            
    # 上下
    for i in range(4):
        if piece[1]-(i+1) < 0:  # 超出棋盘判定范围 
            break
        elif chess_data[piece[0], piece[1]-(i+1)] == color:
            Counter = Counter + 1
            if Counter == 4:
                Counter = 0
                Gameover = True
                return Gameover
                break
        else:
            break
    
    for i in range(4):
        if piece[1]+(i+1) > 14:  # 超出棋盘判定范围
            Counter = 0
            break
        elif chess_data[piece[0], piece[1]+(i+1)] == color:
            Counter = Counter + 1
            if Counter == 4:
                Counter = 0
                Gameover = True
                return Gameover
                break
        else:
            Counter = 0
            break
            
    # 左上右下
    for i in range(4):
        if piece[0]-(i+1) < 0 or piece[1]-(i+1) < 0:  # 超出棋盘判定范围
            break 
        elif chess_data[piece[0]-(i+1), piece[1]-(i+1)] == color:
            Counter = Counter + 1
            if Counter == 4:
                Counter = 0
                Gameover = True
                return Gameover
                break
        else:
            break
    
    for i in range(4):
        if piece[0]+(i+1) > 14 or piece[1]+(i+1) > 14:  # 超出棋盘判定范围
            Counter = 0
            break
        elif chess_data[piece[0]+(i+1), piece[1]+(i+1)] == color:
            Counter = Counter + 1
            if Counter == 4:
                Counter = 0
                Gameover = True
                return Gameover
                break
        else:
            Counter = 0
            break
            
    # 左下右上
    for i in range(4):
        if piece[0]-(i+1) < 0 or piece[1]+(i+1) > 14:  # 超出棋盘判定范围
            break
        elif chess_data[piece[0]-(i+1), piece[1]+(i+1)] == color:
            Counter = Counter + 1
            if Counter == 4:
                Counter = 0
                Gameover = True
                return Gameover
                break
        else:
            break
    
    for i in range(4):
        if piece[0]+(i+1) > 14 or piece[1]-(i+1) < 0:  # 超出棋盘判定范围
            Counter = 0
            break
        elif chess_data[piece[0]+(i+1), piece[1]-(i+1)] == color:
            Counter = Counter + 1
            if Counter == 4:
                Counter = 0
                Gameover = True
                return Gameover
                break
        else:
            Counter = 0
            break   
            
    return Gameover
    

# 绘制文本    
def drawText(self,text,posx,posy,textHeight=48,fontColor=(0,0,0),backgroudColor=(255,255,255)):
        fontObj = pyg.font.Font(None, textHeight)  # 通过字体文件获得字体对象
        textSurfaceObj = fontObj.render(text, True,fontColor,backgroudColor)  # 配置要显示的文字
        textRectObj = textSurfaceObj.get_rect()  # 获得要显示的对象的rect
        textRectObj.center = (posx, posy)  # 设置显示对象的坐标
        self.blit(textSurfaceObj, textRectObj)  # 绘制字      
        
    	
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
            print piece[0]
            print piece[1]
            
            # 如果该点没有落子
            if chess_data[piece[0], piece[1]] == NoPiece:
                if Movement:
                    chess_data[piece[0], piece[1]] = BlackPiece
                    Movement = False
                    
                    if game_over(BlackPiece):
                        GG = BlackPiece
                        
                else:
                    chess_data[piece[0], piece[1]] = WhitePiece
                    Movement = True
                    
                    if game_over(WhitePiece):
                        GG = WhitePiece 
            
    draw_chessmap(screen)  # 画出棋盘
    draw_piece(screen)  #  画出棋子
    
    if GG == BlackPiece:
        drawText(screen,'GameOver: Black is Winner!',320,320)
    elif GG == WhitePiece:
        drawText(screen,'GameOver: White is Winner!',320,320)

	# 刷新屏幕
    pyg.display.flip()