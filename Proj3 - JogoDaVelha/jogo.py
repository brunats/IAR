import time
import pygame
import csv
from copy import deepcopy
import sys
import os

####define funções

def mostraTerminal(mat):
	a = ''
	for m in range(3):
		if(mat[m][0] == 1):
			a = 'x'
		elif(mat[m][0] == -1):
			a = 'o'
		else:
			a = '0'
			
		if(mat[m][1] == 1):
			b = 'x'
		elif(mat[m][1] == -1):
			b = 'o'
		else:
			b = '0'
			
		if(mat[m][2] == 1):
			c = 'x'
		elif(mat[m][2] == -1):
			c = 'o'
		else:
			c = '0'
			
		print('{}  {}  {}'.format(a, b, c))
	return 

def convert_Pos(pos):
	if(pos == "1"):
		return (0, 0)
	elif(pos == "2"):
		return (0, 1)
	elif(pos == "3"):
		return (0, 2)
	elif(pos == "4"):
		return (1, 0)
	elif(pos == "5"):
		return (1, 1)
	elif(pos == "6"):
		return (1, 2)
	elif(pos == "7"):
		return (2, 0)
	elif(pos == "8"):
		return (2, 1)
	elif(pos == "9"):
		return (2, 2)
	else:
		print ("socooooroo")
		return 

def add_Ponto(mat, pos, jogador):
	#print("{}".format(pos))
	lin = pos[0]
	col = pos[1]
	if(jogador == 'x'):
		mat[lin][col] = 1
	else:
		mat[lin][col] = -1

	return 1

def jogada_Valida(mat, pos):
	#pos = convert_Pos(jogada)
	if(mat[pos[0]][pos[1]] == 0):
		return True
	return False

def jogada_Valida_Vet(mat, pos):
	if(mat[pos[0]][pos[1]] == 0):
		return True
	return False
	
def empate_Jogo(mat):
	for i in range(3):
		for j in range(3):
			if(mat[i][j] == 0):
				return False
	return True
	
def fim_De_Jogo(mat):
	#vencedor em linha
	aux = mat[0][0] + mat[0][1] + mat[0][2]
	aux2 = mat[1][0] + mat[1][1] + mat[1][2]
	aux3 = mat[2][0] + mat[2][1] + mat[2][2]

	#vencedor em coluna
	aux4 = mat[0][0] + mat[1][0] + mat[2][0]
	aux5 = mat[0][1] + mat[1][1] + mat[2][1]
	aux6 = mat[0][2] + mat[1][2] + mat[2][2]

	#vencedor em diagonal
	aux7 = mat[0][0] + mat[1][1] + mat[2][2]
	aux8 = mat[0][2] + mat[1][1] + mat[2][0]

	#return 1 indica vencedor computador, return -1 vencedor humano, return 0, nenhum vencedor
	if(aux == 3 or aux2 == 3 or aux3 == 3 or aux4 == 3 or aux5 == 3 or aux6 == 3 or aux7 == 3 or aux8 == 3):
		return 1
	elif(aux == -3 or aux2 == -3 or aux3 == -3 or aux4 == -3 or aux5 == -3 or aux6 == -3 or aux7 == -3 or aux8 == -3):
		return -1
	else:
		if(empate_Jogo(mat)):
			return -2
		else:
			return 0

def jogador_vs_jogador():
	mat = []
	jogador = 1
	#posicao = []
	ganhador = 99

	for i in range(3):
		mat.append([0]*3)
		
	while(fim_De_Jogo(mat) == 0):
		#os.system('clear')
		mostraTerminal(mat)
		if(jogador == 1):
			jogada = input('Jogador 1: ')
			while(not jogada_Valida(mat, convert_Pos(jogada))):
				print('Jogada inválida!')
				jogada = input('Jogador 1: ')
			add_Ponto(mat, convert_Pos(jogada), 'x')
			jogador += 1
		else:
			jogada = input('Jogador 2: ')
			while(jogada_Valida(mat, convert_Pos(jogada)) == 0):
				print('Jogada inválida!')
				jogada = input('Jogador 2: ')
			add_Ponto(mat, convert_Pos(jogada), 'o')
			jogador -= 1

	#os.system('clear')
	mostraTerminal(mat)
	ganhador = fim_De_Jogo(mat)

	if(ganhador == 1):
		print("Vencedor Jogador 1!")
	elif(ganhador == -1):
		print("Vencedor Jogador 2!")
	elif(ganhador == -2):
		print("Empate!")

	return 1

#funções jogador vs computador

def jogaTeclado(mat):
	jogada = input('Jogador 1: ')
	while(not jogada_Valida(mat, convert_Pos(jogada))):
		print('Jogada inválida!')
		jogada = input('Jogador 1: ')
	add_Ponto(mat, convert_Pos(jogada), 'x')

def jogada_Jogador(mat, nivel):
	#jogaTeclado(mat)
	jogaMouse(mat)
	
	
	mostraTerminal(mat)
	mostraCampo(mat)
	fim = fim_De_Jogo(mat)
	if(fim == 1):
		print('Você venceu!')
		return 1
	elif(fim == -2):
		print('Empate!')
		return 1
	else:
		jogada_computador(mat, nivel+1)

def jogada_computador(mat, nivel):
	#valor, novo = minimax(mat, nivel, True)
	valor, novo = alphabeta(mat, nivel, -50000, +50000, True)
	mat = novo
	
	print('Computador:')
	mostraTerminal(mat)
	mostraCampo(mat)
	fim = fim_De_Jogo(mat)
	if(fim == -1):
		print('Computador venceu!')
		return 1
	elif(fim == -2):
		print('Empate!')
		return 1
	else:
		jogada_Jogador(mat, nivel+1)
	
def minimax(mat, nivel, computador):
	fim = fim_De_Jogo(mat)
	if(fim == 1):
		return -1, mat
	elif(fim == -1):
		return 1, mat
	elif(fim == -2):
		return 0, mat
	
	global contP
	
	if(computador):
		#print("computador")
		melhor = -50000
		proximos = filhos(mat, 'o')
		novo = []
		
		for i in proximos:
			contP+=1
			valor, campo = minimax(i, nivel+1, False)
			if(valor > melhor):
				melhor = valor
				novo = deepcopy(i)
		
		return melhor, novo
	
	else:
		#print("usuario")
		melhor = 50000
		proximos = filhos(mat, 'x')
		novo = []
		
		for i in proximos:
			contP+=1
			valor, campo = minimax(i, nivel+1, True)
			if(valor < melhor):
				melhor = valor
				novo = deepcopy(i)
		
		return melhor, novo

def alphabeta(mat, nivel, al, be, computador):
	fim = fim_De_Jogo(mat)
	if(fim == 1):
		return -(10-nivel), mat
	elif(fim == -1):
		return 10-nivel, mat
	elif(fim == -2):
		return 0, mat
		
	global contP

	if(computador):
		proximos = filhos(mat, 'o')
		novo = []
		
		for i in proximos:
			contP+=1
			result, ml = alphabeta(i, nivel+1, al, be, False)
			if(al < result):
				al = result
				novo = deepcopy(i)
			if(be <= al):
				break
		
		return al, novo
		
	else:
		proximos = filhos(mat, 'x')
		novo = []
		
		for i in proximos:
			contP+=1
			result, ml = alphabeta(i, nivel+1, al, be, True)
			#print(be, result)
			if(be > result):
				be = result
				novo = deepcopy(i)
			if(be <= al):
				break

		return be, novo

def filhos(mat, jogador):
	proximas = []
	global contG
	
	for i in range(1, 10):
		aux = []
		if(jogada_Valida(mat, convert_Pos(str(i)))):
			aux=deepcopy(mat)
			
			add_Ponto(aux, convert_Pos(str(i)), jogador)
			proximas.append(aux)
			contG+=1
			#mostraTerminal(aux)
			#print('')
	
	return proximas
			
def jogador_vs_computador():
	global contG
	global contP
	mat = []

	for i in range(3):
		mat.append([0]*3)
	
	mostraTerminal(mat)
	mostraCampo(mat)
	jogada_Jogador(mat, 0)
	
	print('Nós gerados:')
	print(contG)
	print('Nós percorridos:')
	print(contP)

###funções pygame

# definindo cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

BLUE =  (0, 0, 255) #Pântano (azul) – Custo: 10 – N: 2
RED =   (255, 0, 0) #Fogo (vermelho) – Custo: 15 – N: 3

def espera():
    while True:
        # capturando eventos

        event = pygame.event.poll()

        # caso o evento QUIT (clicar no x da janela) seja disparado ou esc
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # saia do loop finalizando o programa
            return -1
            

        if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
            # volte e reinicie o jogo
            return 1

def mostraCampo(mat):
	pygame.draw.line(screen, BLACK, (200, 0), (200, 600), 10)
	pygame.draw.line(screen, BLACK, (400, 0), (400, 600), 10)
	pygame.draw.line(screen, BLACK, (0, 200), (600, 200), 10)
	pygame.draw.line(screen, BLACK, (0, 400), (600, 400), 10)
	
	for i in range(0, 3):
		for j in range(0, 3):
			if(mat[i][j] == 1):
				pygame.draw.line(screen, BLUE, (j*200 + 20, i*200 + 20), (j*200 + 180, i*200 + 180), 10)
				pygame.draw.line(screen, BLUE, (j*200 + 180, i*200 + 20), (j*200 + 20, i*200 + 180), 10)
			elif(mat[i][j] == -1):
				pygame.draw.circle(screen, RED, (j*200 + 100, i*200 + 100), 90, 10)
	
	pygame.display.flip()
	
def jogaMouse(mat):
	jogou = False	
	
	while(not jogou):
		event = pygame.event.poll()
		if (event.type == pygame.MOUSEBUTTONUP):
			pos = pygame.mouse.get_pos()
			jogada = []
			jogada.append(pos[1]//200)
			jogada.append(pos[0]//200)
			print(jogada)
			#jogou = True
			if(jogada_Valida(mat, jogada)):
				jogou = True
				add_Ponto(mat, jogada, 'x')
			
	
	#return jogada

####fim das funções

#################################################

novojogo = 1
while(novojogo == 1):
	contG = 0
	contP = 0

	pygame.init()

	#definindo tela 600x600
	screen = pygame.display.set_mode((600, 600))
	# carregando fonte
	font = pygame.font.SysFont(None, 55)

	pygame.display.set_caption('IAR - Jogo da Velha')

	# preenchendo o fundo com branco
	screen.fill(WHITE)

	#jogador_vs_jogador()
	jogador_vs_computador()

	#mostraCampo()
	novojogo = espera()

#################################################

#sys.setrecursionlimit(1765)

#if __name__ == '__main__':
#    main()
