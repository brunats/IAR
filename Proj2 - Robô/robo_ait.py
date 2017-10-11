# -*- coding: utf-8 -*-
    # ****************************************************************************
    # This program is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.
    
    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.
    
    # You should have received a copy of the GNU General Public License
    # along with this program.  If not, see <http://www.gnu.org/licenses/>.
    # ****************************************************************************
    # Autores:
    #     Bruna Tavares Silva @brunats
    #     Christopher Renkavieski @ChrisRenka
    # Disciplina:
    #     Inteligência Artificial - BCC  - CCT UDESC
    # Profº:
    #     Rafael Parpinelli
    # ****************************************************************************
	# Material de apoio:
	#     https://github.com/humrochagf/desbravando-pygame
	# ****************************************************************************

import time
import pygame
import csv
#import queue
from copy import deepcopy
import sys
#import numpy as np

# definindo cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

BLUE =  (0, 0, 255) #Pântano (azul) – Custo: 10 – N: 2
MARRON = (92,64,51) #Montanhoso (marrom) – Custo: 5 – N: 1
GREEN = (0, 255, 0) #Sólido e plano (verde) – Custo: 1 – N: 0 
RED =   (255, 0, 0) #Fogo (vermelho) – Custo: 15 – N: 3

ORANGE = (255, 165, 0)

####define funções
def leitura():
    #definindo matriz
    entrada = []


    #lendo ambiente e construindo matriz
    with open('Robo_ambiente.txt','r') as csvfile:
        plots = csv.reader(csvfile, delimiter=' ')
        for row in plots:
            cod = []
            for i in row:
                cod.append(i)
                #print '{:1}'.format(i) #prints de teste
            entrada.append(cod)
    
    matriz = []
    for i in range(0,42):
        linha = []
        for j in range(0, 42):
            sub = []
            sub.append(int(entrada[i][j]))
            sub.append(-1)
            linha.append(sub)
        matriz.append(linha)

    return matriz

def mostraCampo(matriz, inicio, fim):
    for i in range(0, 42):
        for j in range(0, 42):
            if (matriz[i][j][1] != -1):
                COR = ((255-matriz[i][j][1])%255, (255-matriz[i][j][1])%255, (255-matriz[i][j][1])%255)
                pygame.draw.rect(screen, COR, [j*20, i*20, 20, 20])
            elif (matriz[i][j][0] == 0):
                pygame.draw.rect(screen, GREEN, [j*20, i*20, 20, 20])
            elif (matriz[i][j][0] == 1):
                pygame.draw.rect(screen, MARRON, [j*20, i*20, 20, 20])
            elif (matriz[i][j][0] == 2):
                pygame.draw.rect(screen, BLUE, [j*20, i*20, 20, 20])
            else:
                pygame.draw.rect(screen, RED, [j*20, i*20, 20, 20])
    
    if(len(inicio) != 0):
        pygame.draw.rect(screen, BLACK, [inicio[1]*20, inicio[0]*20, 20, 20])
    if(len(fim) != 0):
        pygame.draw.rect(screen, BLACK, [fim[1]*20, fim[0]*20, 20, 20])
    pygame.display.flip()
    
    return

def peso(valor):
    if (valor == 0):
        return 1
    elif (valor == 1):
        return 5
    elif (valor == 2):
        return 10
    elif (valor == 3):
        return 15
    else:
        print("Erro nos valores da matriz")
        return -1
  
def espera():
    while True:
        # capturando eventos
        event = pygame.event.poll()
        # caso o evento QUIT (clicar no x da janela) seja disparado
        if event.type == pygame.QUIT:
            # saia do loop finalizando o programa
            break

def posicoes(matriz, inicio, fim):
    cont = 0
    
    while(cont == 0):
        event = pygame.event.poll()
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            inicio.append(pos[1]//20)
            inicio.append(pos[0]//20)
            print(inicio)
            cont+=1
    mostraCampo(matriz, inicio, fim)
    
    while(cont == 1):
        event = pygame.event.poll()
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            fim.append(pos[1]//20)
            fim.append(pos[0]//20)
            print(fim)
            cont+=1
            
def dfs_start(matriz, inicio, fim, nivel, nos):
    aux = deepcopy(matriz)
    
    encontrou = []
    encontrou.append(0)
    
    nos[0]+=1
    matriz[inicio[0]][inicio[1]][1] = 0
    
    natual = 0
    
    dfs_rec(matriz, inicio, fim, encontrou, nos, natual, nivel)
    
    #print(matriz[inicio[0]][inicio[1]][1])
    #print(matriz[inicio[0]-1][inicio[1]][1])
    #print(matriz[fim[0]-2][fim[1]][1])
    #print(matriz[fim[0]-1][fim[1]][1])
    #print(matriz[fim[0]][fim[1]][1])
    
    if(encontrou[0] == 0):       
        return 0
    
    backTrack(matriz, aux, fim)
    print(matriz[fim[0]][fim[1]][1])
    print(nos[0])
    
    mostraCampo(aux, inicio, fim)
    espera()
    
    return 1
    

def dfs_rec(matriz, atual, fim, encontrou, nos, natual, nivel):
    a0 = atual[0]
    a1 = atual[1]
    f0 = fim[0]
    f1 = fim[1]
    
    nos[0]+=1
    
    #print(matriz[a0][a1][1])
    if (encontrou[0]==1):
        return
    elif (a0==f0 and a1==f1):
        encontrou[0] = 1
        return
        
    mostraCampo(matriz, inicio, fim)
    
    #print(matriz[a0][a1][1])
    #norte
    #if(a0 > 0 and (matriz[a0-1][a1][1] == -1 or (matriz[a0][a1][1] + peso(matriz[a0-1][a1][0]) < matriz[a0-1][a1][1])) and encontrou[0]==0):
    if(a0 > 0 and matriz[a0-1][a1][1] == -1 and encontrou[0]==0 and natual < nivel):
        matriz[a0-1][a1][1] = matriz[a0][a1][1] + peso(matriz[a0-1][a1][0])
        natual += 1
        dfs_rec(matriz, [a0-1, a1], fim, encontrou, nos, natual, nivel)
    #leste
    #if(a1 < 41 and (matriz[a0][a1+1][1] == -1 or (matriz[a0][a1][1] + peso(matriz[a0][a1+1][0]) < matriz[a0][a1+1][1])) and encontrou[0]==0):
    if(a1 < 41 and matriz[a0][a1+1][1] == -1 and encontrou[0]==0 and natual < nivel):
        matriz[a0][a1+1][1] = matriz[a0][a1][1] + peso(matriz[a0][a1+1][0])
        natual += 1
        dfs_rec(matriz, [a0, a1+1], fim, encontrou, nos, natual, nivel)
    #sul
    #if(a0 < 41 and (matriz[a0+1][a1][1] == -1 or (matriz[a0][a1][1] + peso(matriz[a0+1][a1][0]) < matriz[a0+1][a1][1])) and encontrou[0]==0):
    if(a0 < 41 and matriz[a0+1][a1][1] == -1 and encontrou[0]==0 and natual < nivel):
        matriz[a0+1][a1][1] = matriz[a0][a1][1] + peso(matriz[a0+1][a1][0])
        natual += 1
        dfs_rec(matriz, [a0+1, a1], fim, encontrou, nos, natual, nivel)
    #oeste
    #if(a1 > 0 and (matriz[a0][a1-1][1] == -1 or (matriz[a0][a1][1] + peso(matriz[a0][a1-1][0]) < matriz[a0][a1-1][1])) and encontrou[0]==0):
    if(a1 > 0 and matriz[a0][a1-1][1] == -1 and encontrou[0]==0 and natual < nivel):
        matriz[a0][a1-1][1] = matriz[a0][a1][1] + peso(matriz[a0][a1-1][0])
        natual += 1
        dfs_rec(matriz, [a0, a1-1], fim, encontrou, nos, natual, nivel)
    
def executa(matriz, inicio, fim):
    nivel = 1
    aux = deepcopy(matriz)
    nos = []
    nos.append(0)
    
    while(dfs_start(aux, inicio, fim, nivel, nos) == 0):
        nivel +=1
        aux = deepcopy(matriz)      

def anterior(matriz, atual):
    a0 = atual[0]
    a1 = atual[1]
    
    #oeste
    if (a1 > 0 and matriz[a0][a1-1][1] == matriz[a0][a1][1] - peso(matriz[a0][a1][0])):
        return [a0, a1-1]
    #sul
    elif (a0 < 41 and matriz[a0+1][a1][1] == matriz[a0][a1][1] - peso(matriz[a0][a1][0])):
        return [a0+1, a1]
    #leste
    elif(a1 < 41 and matriz[a0][a1+1][1] == matriz[a0][a1][1] - peso(matriz[a0][a1][0])):
        return [a0, a1+1]
    #norte
    elif(a0 > 0 and matriz[a0-1][a1][1] == matriz[a0][a1][1] - peso(matriz[a0][a1][0])):
        return [a0-1, a1]
    else:
        print("Não foi possível encontrar posição anterior")
        return [-1, -1]


def backTrack(matriz, aux, fim):
    a0 = fim[0]
    a1 = fim[1]
    atual = [a0, a1]
    aux[a0][a1][1] = 0
    
    while(matriz[a0][a1][1] != 0):
        atual = anterior(matriz, atual)
        if(atual[0] == -1):
            return
        
        a0 = atual[0]
        a1 = atual[1]
        aux[a0][a1][1] = 128
    

####fim das funções

sys.setrecursionlimit(1765)

matriz = leitura()
#print (np.matrix(matriz))

#inicio = [33, 9]
#fim = [12, 21]
inicio = []
fim = []

pygame.init()

#definindo tela 840x840
screen = pygame.display.set_mode((840, 840))
# carregando fonte
font = pygame.font.SysFont(None, 55)

pygame.display.set_caption('IAR - Robô')

# preenchendo o fundo com preto
screen.fill(BLACK)

#mostraCampo(matriz, inicio, fim)

mostraCampo(matriz, inicio, fim)
posicoes(matriz, inicio, fim)

executa(matriz, inicio, fim)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
