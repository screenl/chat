# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 14:42:01 2022

@author: 86137
"""

import pygame
import sys
from pygame.locals import *
from collections import Counter
from socket import *
from time import ctime
import json
import select
import socket
from chat_utils import CHAT_IP,CHAT_PORT

def run():
    screen=pygame.display.set_mode((400,450))
    pygame.display.set_caption('gobang game user')
    pygame.init()

    img_board=pygame.image.load('chess_board.png')
    img_bchess=pygame.image.load('black_chess.png')
    img_wchess=pygame.image.load('white_chess.png')
    white=(255,255,255)
    black=(0,0,0)

    msg=[]

    chess_board=[[]]
    def set_chess_board():
        x,y=0,0
        while True:
            if x==400:
                x=0
                y+=40
                if y<400:
                    chess_board.append([])
            if y==400:
                break
            chess_board[-1].append([x,y])
            x+=40
    set_chess_board()
    chess_exist=[[0 for i in range(10)]for j in range(10)]

    black_chess,white_chess=[],[]
    chess_kind=1
    wcx,wcy,bcx,bcy=[],[],[],[]
    def draw_board():
        for i in chess_board:
            for j in i:
                screen.blit(img_board,(j[0],j[1]))
                pygame.display.update()
                
    def set_chess():
        if event.type==pygame.MOUSEBUTTONDOWN:
            pos=pygame.mouse.get_pos()
            for i in range(len(chess_board)):
                for j in range(len(chess_board[i])):
                    if chess_board[i][j][0]<pos[0]<chess_board[i][j][0]+40 and chess_board[i][j][1]<pos[1]<chess_board[i][j][1]+40:
                        if chess_exist[i][j]==0:
                            white_chess.append([i,j])
                            wcx.append(black_chess[-1][0])
                            wcy.append(black_chess[-1][1])
                            msg.extend((i,j))
                            chess_exist[i][j]=1
                            pygame.display.update()
                            return 1
                        
    def draw_chess():
        for i in white_chess:
            screen.blit(img_wchess,(i[1]*40,i[0]*40))
        for i in black_chess:
            screen.blit(img_bchess,(i[1]*40,i[0]*40))
        pygame.display.update()
        
    def row_column_win(x,m,n,chess):
        for i in x:
            if x[i]>=5:
                xy=[]
                for j in chess:
                    if j[m]==i:
                        xy.append(j[n])
                xy.sort()
                count=0
                for j in range(len(xy)-1):
                    if xy[j]+1==xy[j+1]:
                        count+=1
                    else:
                        count=0
                if count>=4:
                    return 1
                
    def xiejiao_win(chess):
        x,y=[],[]
        chess.sort()
        for i in chess:
            x.append(i[0])
            y.append(i[1])
        c,first,last=0,0,0
        for i in range(len(x)-1):
            if x[i+1]!=x[i]:
                if x[i]+1==x[i+1]:
                    c+=1
                    last=i+1
                else:
                    if c<4:
                        first=i+1
                        c=0
                    else:
                        last=i
                        print(last)
                        break
            else:
                last=i+1
        if c>=4:
            dis=[]
            for i in range(first,last+1):
                dis.append(x[i]-y[i])
            count=Counter(dis)
            for i in count:
                if count[i]>=5:
                    return 1
            dis=[]
            x2=[i*(-1) for i in x]
            for i in range(first,last+1):
                dis.append(x2[i]-y[i])
            count=Counter(dis)
            for i in count:
                if count[i]>=5:
                    return 1
                
    def gameover():
        wcx_count,wcy_count,bcx_count,bcy_count=Counter(wcx),Counter(wcy),Counter(bcx),Counter(bcy)
        if row_column_win(wcx_count,0,1,white_chess)==1:
            return 1
        elif row_column_win(bcx_count,0,1,black_chess)==1:
            return 0
        elif row_column_win(wcy_count,1,0,white_chess)==1:
            return 1
        elif row_column_win(bcy_count,1,0,black_chess)==1:
            return 0
        elif xiejiao_win(white_chess)==1:
            return 1
        elif xiejiao_win(black_chess)==1:
            return 0
        
    def draw_text(text,x,y,size):
        pygame.font.init()
        fontObj=pygame.font.SysFont('SimHei',size )
        textSurfaceObj=fontObj.render(text, True, white,black)
        textRectObj=textSurfaceObj.get_rect()
        textRectObj.center=(x,y)
        screen.blit(textSurfaceObj, textRectObj)
        pygame.display.update()
        
    HOST = CHAT_IP
    PORT = CHAT_PORT
    BUFSIZE = 1024
    ADDR = (HOST,PORT)

    tcpCliSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    inputs=[tcpCliSock]

    draw_board()
    settable=0
    while True:
        rs,ws,es=select.select(inputs,[],[],0)
        for r in rs:
            if r is tcpCliSock:
                data,addr = r.recvfrom(BUFSIZE)
                draw_text("your turn",200,420,15)
                data=json.loads(data)
                settable=1
                black_chess.append(data)
                bcx.append(data[0])
                bcy.append(data[1])
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                tcpCliSock.close()
                pygame.quit()
                sys.exit()
            if settable==1:
                if set_chess()==1:
                    draw_text("your opponent's turn",200,420,15)
                    settable=0
                    msg1=json.dumps(msg)
                    tcpCliSock.sendto(msg1.encode(),ADDR)
                    msg=[]
        draw_chess()
        if gameover()==1:
            draw_text("you win the game！",200,420,15)
            while True:
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        pygame.quit()
                        sys.exit()
        elif gameover()==0:
            draw_text('you lose the game！',200,420,15)
            while True:
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        pygame.quit()
                        sys.exit()

if __name__=='__main__':
    run()