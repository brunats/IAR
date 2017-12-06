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

import time
import csv
import random
import math
from copy import deepcopy
#import numpy as np

####define funções
def leitura(arq):
    #definindo matriz
    entrada = []


    #lendo ambiente e construindo matriz
    with open(arq,'r') as csvfile:
        plots = csv.reader(csvfile, delimiter='\n')
        for row in plots:
            linha = ""
            if(row != []):
                linha = row.pop(0)
                if(linha[0] != 'c'):
                    if(linha[0] == 'p'):
                        p, tipo, var, clau = linha.split()
                        var = int(var)
                        clau = int(clau)
                    elif(linha[0] != '%' and linha[0] != '0'):
                        a, b, c, zero = linha.split()
                        a = int(a)
                        b = int(b)
                        c = int(c)
                        clausula = []
                        clausula.append(a)
                        clausula.append(b)
                        clausula.append(c)
                        entrada.append(clausula)
    #print(entrada)
    return var, clau, entrada
                
def geraRandom(n):
    
    lista = []
    
    for i in range (0, n+1):
        lista.append(random.choice([True, False]))
    
    return lista
    
def inverte(a):
    if (a == True):
        return False
    return True
    
def avalia(cnf, sol):
    
    total = 0
    
    for i in cnf:
        cl = False
        for j in i:
            if (j>0):
                cl = cl or sol[j]
            else:
                cl = cl or inverte(sol[-j])
        if (cl == False):
            total+=1
    
    return total

def randomSearch(cnf, sol, var, clau, it, num):
    
    arqNome = 'random{}.txt'.format(num)
    f = open(arqNome, 'w')
    #it = 5000
    
    resultado = avalia(cnf, sol)
    #print(resultado/clau)
    s = '0 {}\n'.format(resultado/clau)
    f.write(s)
    lista = []
    lista.append(resultado/clau)
    
    for i in range(1,it):
        sTemp = geraRandom(var)
        rTemp = avalia(cnf, sTemp)
        #print(rTemp/clau)
        s = '{} {}\n'.format(i, rTemp/clau)
        f.write(s)
        lista.append(rTemp/clau)
        if(rTemp < resultado):
            sol = deepcopy(sTemp)
            resultado = rTemp
    
    f.close()
    return sol, resultado, lista

def reduzLinear(t, ti, passos):
    return t - ti/passos

def reduzExp(ti, passo, alpha):
    return ti*pow(alpha, passo)   

def perturba(sol, var):
    
    nova = deepcopy(sol)
    flip = random.randint(1, var)
    nova[flip] = inverte(nova[flip])
    
    return nova
    
def simAne(cnf, sol, var, clau, it, num):
    
    arqNome = 'simAne{}.txt'.format(num)
    f = open(arqNome, 'w')
    
    ti = 0.010
    t = ti
    resultado = avalia(cnf, sol)/clau
    s = '0 {}\n'.format(resultado)
    f.write(s)
    
    lista = []
    lista.append(resultado)
    
    melhorSol = deepcopy(sol)
    melhorResult = resultado
    for i in range(1, it):
        sTemp = perturba(sol, var)
        rTemp = avalia(cnf, sTemp)/clau
        #s = '{} {}\n'.format(i, rTemp)
        s = '{} {}\n'.format(i, resultado)
        f.write(s)
        lista.append(resultado)
        deltaE = rTemp - resultado
        if(deltaE<=0):
            sol = deepcopy(sTemp)
            resultado = rTemp
            if(rTemp < melhorResult):
                melhorResult = rTemp
                melhorSol = deepcopy(sTemp)
        elif(random.uniform(0,1) <= math.exp(-deltaE/t)):
            #print(math.exp(-deltaE/t))
            sol = deepcopy(sTemp)
            resultado = rTemp
        t = reduzLinear(t, ti, it)
        #t = reduzExp(ti, i, 0.9999)
        #print(t)
    
    f.close()
    return melhorSol, melhorResult, lista
    
def executa(cnf, var, clau, it):
    
    melhorRand = []
    melhorSimAne = []
    
    listaRand = []
    listaSimAne = []
    
    for i in range(0, 10):
        print(i)
        
        solInicial = geraRandom(var)
        
        solFinal, rFinal, totalRand = randomSearch(lista, solInicial, var, clau, it, i)
        melhorRand.append(rFinal)
        listaRand.append(totalRand)
        
        solFinal, rFinal, totalSimAne = simAne(lista, solInicial, var, clau, it, i)
        melhorSimAne.append(rFinal)
        listaSimAne.append(totalSimAne)
    
    print(melhorRand)
    print(melhorSimAne)
    
    return listaRand, listaSimAne

def media(listaRand, listaSimAne, it):
    
    print('Calculando médias e desvios padrão')
    
    fRand = open('mediaRand.txt', 'w')
    fSimAne = open('mediaSimAne.txt', 'w')
    
    for j in range(0, it):
        mediaRand = 0.0
        mediaSimAne = 0.0
        for i in range(0, 10):
            mediaRand += listaRand[i][j]
            mediaSimAne += listaSimAne[i][j]
        mediaRand = mediaRand/10
        mediaSimAne = mediaSimAne/10
        
        sdRand = 0.0
        sdSimAne = 0.0
        for i in range(0, 10):
            sdRand += (listaRand[i][j] - mediaRand)*(listaRand[i][j] - mediaRand)
            sdSimAne += (listaSimAne[i][j] - mediaSimAne)*(listaSimAne[i][j] - mediaSimAne)
        sdRand = sdRand/10
        sdRand = math.sqrt(sdRand)
        
        sRand = '{} {} {} {}\n'.format(j, mediaRand, mediaRand-sdRand, mediaRand+sdRand)
        fRand.write(sRand)
        
        sdSimAne = sdSimAne/10
        sdSimAne = math.sqrt(sdSimAne)
        
        sSimAne = '{} {} {} {}\n'.format(j, mediaSimAne, mediaSimAne-sdSimAne, mediaSimAne+sdSimAne)
        fSimAne.write(sSimAne)
    
    fRand.close()
    fSimAne.close()
        
    
    
####fim das funções

arq = 'uf20-01.cnf'
#arq = 'teste.txt'
n_var, n_clau, lista = leitura(arq)
it = 50000

listaRand, listaSimAne = executa(lista, n_var, n_clau, it)

media(listaRand, listaSimAne, it)

'''
solInicial = geraRandom(n_var)
print("Solução inicial:")
print(solInicial)

#solFinal, rFinal = randomSearch(lista, solInicial, n_var, n_clau, it)
#print("Solução final random:")
#print (solFinal)
#print (rFinal)

#solFinal, rFinal = simAne(lista, solInicial, n_var, n_clau, it)
#print("Solução final simulated annealing:")
#print (solFinal)
#print (rFinal*n_clau)
'''


  
    
    
    
    
