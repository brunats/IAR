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
  
def dij(matriz, inicio, fim, lista):
    i0 = inicio[0]
    i1 = inicio[1]
    f0 = fim[0]
    f1 = fim[1]
    encontrou = 0
    aux = deepcopy(matriz)
    nos = 0
    
    #ini = []
    #ini.append([i0, i1, 0])
    lista.append([i0, i1, 0])
    matriz[i0][i1][1] = 0
    #matriz[i0][i1][2] = 0
    while(encontrou == 0):
        if(len(lista) == 0):
            print("Não há caminho!")
            break
         
        a0, a1, total = lista.pop(0)
        
        if(total != matriz[a0][a1][1]):
            continue
            
        if(a0 == f0 and a1 == f1):
            encontrou = 1
            continue
        
        #norte
        if(a0 > 0 and (matriz[a0-1][a1][1] == -1 or (matriz[a0][a1][1] + peso(matriz[a0-1][a1][0]) < matriz[a0-1][a1][1]) ) ):
            total = matriz[a0][a1][1] + peso(matriz[a0-1][a1][0])
            pos = posInsert(lista, total)
            if(pos==-1):
                break
            lista.insert(pos, [a0-1, a1, total])
            matriz[a0-1][a1][1] = total
            nos+=1
        #leste
        if(a1 < 41 and (matriz[a0][a1+1][1] == -1 or (matriz[a0][a1][1] + peso(matriz[a0][a1+1][0]) < matriz[a0][a1+1][1]) )):
            total = matriz[a0][a1][1] + peso(matriz[a0][a1+1][0])
            pos = posInsert(lista, total)
            if(pos==-1):
                break
            lista.insert(pos, [a0, a1+1, total])
            matriz[a0][a1+1][1] = total
            nos+=1
        #sul
        if(a0 < 41 and (matriz[a0+1][a1][1] == -1 or (matriz[a0][a1][1] + peso(matriz[a0+1][a1][0]) < matriz[a0+1][a1][1]) )):
            total = matriz[a0][a1][1] + peso(matriz[a0+1][a1][0])
            pos = posInsert(lista, total)
            if(pos==-1):
                break
            lista.insert(pos, [a0+1, a1, total])
            matriz[a0+1][a1][1] = total
            nos+=1
        #oeste
        if(a1 > 0 and (matriz[a0][a1-1][1] == -1 or (matriz[a0][a1][1] + peso(matriz[a0][a1-1][0]) < matriz[a0][a1-1][1]) )):
            total = matriz[a0][a1][1] + peso(matriz[a0][a1-1][0])
            pos = posInsert(lista, total)
            if(pos==-1):
                break
            lista.insert(pos, [a0, a1-1, total])
            matriz[a0][a1-1][1] = total
            nos+=1
        
        
        mostraCampo(matriz, inicio, fim)
        #pygame.display.flip()
        
    
    print("Peso total: ")
    print(matriz[f0][f1][1])
    print("Nós expandidos: ")
    print(nos)
    #fila.get() pega o topo da fila
    #fila.empty() verifica se está vazia
    
    if(encontrou == 1):
        backTrack(matriz, aux, fim)
    
    mostraCampo(aux, inicio, fim)
    #pygame.display.flip()
    #espera()
    
    return (matriz[f0][f1][1], nos)

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
    #aux[a0][a1][1] = 0
    pronfundidade = 0
    
    while(matriz[a0][a1][1] != 0):
        atual = anterior(matriz, atual)
        pronfundidade += 1
        if(atual[0] == -1):
            return
        
        a0 = atual[0]
        a1 = atual[1]
        aux[a0][a1][1] = 128
    print("aqui e a profundidade {}". format(pronfundidade))

def posInsert(lista, custo):
    inicio = 0
    fim = len(lista)-1
    encontrou = False
    
    if(fim==-1):
        return 0
    
    while(inicio<=fim and (not encontrou)):
        pos = (inicio+fim)//2
        if(lista[pos][2] == custo):
            encontrou = True
        else:
            if(custo<lista[pos][2]):
                fim = pos-1
            else:
                inicio = pos+1
    
    if(encontrou):
        while(pos<len(lista) and lista[pos][2] == custo):
            pos+=1
    else:
        if(lista[pos][2] > custo):
            while(pos>=0 and lista[pos][2] > custo):
                pos-=1
            pos+=1
        else:
            while(pos<len(lista) and lista[pos][2] < custo):
                pos+=1
        
    return pos
    
def exec_mouse(matriz, lista):
    inicio = []
    fim = []
    posicoes(matriz, inicio, fim)
    dij(matriz, inicio, fim, lista)

def exec_teste(matriz, lista):
    inicio = [[34, 4], [19, 19], [9, 9], [0,0], [17,6], [8,3], [39, 4], [14, 14], [0,1], [0,19]]
    fim = [[24,39], [40,16], [29,31], [22,34], [37,24], [8,34], [1,34], [39,39], [41,41], [19,41]]
    pesos = []
    nos = []
    
    for i in range(0, 10):
        print(i)
        aux = deepcopy(matriz)
        (p, n) = dij(aux, inicio[i], fim[i], lista)
        pesos.append(p)
        nos.append(n)
        
    print(pesos)
    print(nos)
    
####fim das funções

lista = []

matriz = leitura()
#print (np.matrix(matriz))

#inicio = []
#fim = []

pygame.init()

#definindo tela 840x840
screen = pygame.display.set_mode((840, 840))
# carregando fonte
font = pygame.font.SysFont(None, 55)

pygame.display.set_caption('IAR - Robô')

# preenchendo o fundo com preto
screen.fill(BLACK)

mostraCampo(matriz, [], [])
#posicoes(matriz, inicio, fim)

#exec_mouse(matriz, lista)
exec_teste(matriz, lista)

espera()
  
    
    
    
    
    
    
    
    
    
    
