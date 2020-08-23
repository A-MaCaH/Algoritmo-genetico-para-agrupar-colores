import random
import numpy as np
import re 
import cv2
import math
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
                                #mejores valores encontrados
generaciones=100               #1000
num_ind_poblacion=100           #100
longitud_Cromosoma=8            #(8*8)
ProbCruza=0.075                 #0.075
probMuta=0.2                    #0.2

poblacion=np.zeros((num_ind_poblacion,longitud_Cromosoma,longitud_Cromosoma),np.uint8)
poblacionConFitness=np.zeros((num_ind_poblacion,longitud_Cromosoma,longitud_Cromosoma,2),np.uint8)
soloFitness=np.zeros((num_ind_poblacion,longitud_Cromosoma,longitud_Cromosoma),np.uint8)
individuoConfit=[]
listadelosmejores10por=[]
listaDeLospadreSigGen=[]
img = np.zeros((8,8,3),np.uint8)
d_azul=np.zeros((3),np.uint8)
d_verde=np.zeros((3),np.uint8)
d_amarillo=np.zeros((3),np.uint8)
d_rojo=np.zeros((3),np.uint8)

#Codificación para los colores
C_azul=3
C_verde=2
C_amarillo=1
C_rojo=0
#valores de los colores en RGB
d_azul=[0,118,193]
d_verde=[41,193,35]
d_amarillo=[180,255,255]
d_rojo=[255,100,18]
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------

def decodificar(img_mejor,nombreImg):
    for i in range(8):
        for j in range(8):
            if img_mejor[i][j]==0:
                img[i][j]=d_rojo
            if img_mejor[i][j]==1:
                img[i][j]=d_amarillo
            if img_mejor[i][j]==2:
                img[i][j]=d_verde
            if img_mejor[i][j]==3:
                img[i][j]=d_azul
    cv2.imwrite(nombreImg,img)

def generarPobInicial():
    for individuo in range(num_ind_poblacion):
        cromosoma=generarIndividuo()
        poblacion[individuo]=cromosoma

def generarIndividuo():
    #numero de pixeles por color 17 rojos, 18 azules,  13 verdes y 16 amarillos
    #rojo->0 (17)
    #amarillo->1 (16)
    #verdes->2 (13)
    #azules->3 (18)
    cromosoma = np.zeros((longitud_Cromosoma,longitud_Cromosoma),np.uint8)
    rojo = [0 for x in range(17)]
    amarillo= [1 for x in range(16)]
    verde= [2 for x in range(13)]
    azul= [3 for x in range(18)]
    lsDePosiblesGenes=rojo+amarillo+verde+azul
    for x in range(longitud_Cromosoma):
        for y in range(longitud_Cromosoma):
            # Cambiamos el color de cada uno de los pixeles de forma aleatoria
            cromosoma[x,y] = random.choice(lsDePosiblesGenes) 
            lsDePosiblesGenes.remove(cromosoma[x,y])
    return cromosoma

def fitness():
    individuoConfit.clear()
    for individuo in range(num_ind_poblacion):
        fitnessDelIndv=0
        for i in range(longitud_Cromosoma):
            for j in range(longitud_Cromosoma):
                fit=0
                if  (i-1)>=0 and (j-1)>=0 and poblacion[individuo][i][j] != poblacion[individuo][i-1][j-1]:
                    fit=fit+1
                if (i-1)>=0 and poblacion[individuo][i][j] != poblacion[individuo][i-1][j]:
                    fit=fit+1
                if (i-1)>=0 and (j+1)<8 and poblacion[individuo][i][j] != poblacion[individuo][i-1][j+1]:
                    fit=fit+1
                if (j-1)>=0 and poblacion[individuo][i][j] != poblacion[individuo][i][j-1]:
                    fit=fit+1
                if (j+1)<8 and poblacion[individuo][i][j] != poblacion[individuo][i][j+1]:
                    fit=fit+1
                if (i+1)<8 and (j-1)>=0 and poblacion[individuo][i][j] != poblacion[individuo][i+1][j-1]:
                    fit=fit+1
                if (i+1)<8 and poblacion[individuo][i][j] != poblacion[individuo][i+1][j]:
                    fit=fit+1
                if (i+1)<8 and (j+1)<8 and poblacion[individuo][i][j] != poblacion[individuo][i+1][j+1]:
                    fit=fit+1
                fitnessDelIndv=fitnessDelIndv+fit
        individuoConfit.append([poblacion[individuo],fitnessDelIndv])

def bubbleSort(lista):
    n = len(lista)
    for i in range(1, n):
        for j in range(n-i):
            if lista[j][1] > lista[j+1][1]:
                aux=lista[j]
                lista[j]=lista[j+1]
                lista[j+1]=aux
    return lista

def mergeSort_(arr): 
    if len(arr) >1: 
        mid = len(arr)//2 # Finding the mid of the array 
        L = arr[:mid] # Dividing the array elements  
        R = arr[mid:] # into 2 halves 
  
        mergeSort_(L) # Sorting the first half 
        mergeSort_(R) # Sorting the second half 
  
        i = j = k = 0
          
        # Copy data to temp arrays L[] and R[] 
        while i < len(L) and j < len(R): 
            if L[i][1] < R[j][1]: 
                arr[k] = L[i] 
                i+= 1
            else: 
                arr[k] = R[j] 
                j+= 1
            k+= 1
          
        # Checking if any element was left 
        while i < len(L): 
            arr[k] = L[i] 
            i+= 1
            k+= 1
          
        while j < len(R): 
            arr[k] = R[j] 
            j+= 1
            k+= 1 
    return arr

def seleccion(fit):
    ordenadoPorMejor=mergeSort_(fit)
    return ordenadoPorMejor[:int(num_ind_poblacion*.1)], ordenadoPorMejor[:2]

def cruza(listaPadres):#lista de papas, se van a manejar solo los 2 
    #individuos apartir de aqui hasta la gen de nueva poblacion
    numeroAleatoreo=random.random()
    if numeroAleatoreo<=ProbCruza:
        listaCruce1=[0,1,2,3,4,5,6,7]
        cruce1=random.choice(listaCruce1)
        ListaCruce2=[0,1,2,3,4,5,6,7]
        cruce2=random.choice(ListaCruce2)
        
        auxInd1C1=list(listaPadres[0][0][cruce1])
        auxInd1C2=list(listaPadres[0][0][cruce2])

        listaPadres[0][0][cruce2]=auxInd1C1
        listaPadres[0][0][cruce1]=auxInd1C2
        
        auxInd2C1=list(listaPadres[1][0][cruce1])
        auxInd2C2=list(listaPadres[1][0][cruce2])
        listaPadres[1][0][cruce1]=auxInd2C2
        listaPadres[1][0][cruce2]=auxInd2C1
    return listaPadres


def mutacion(listaLegado):
    numeroAleatoreo=random.random()
    if numeroAleatoreo<=probMuta:
        ind1numAleatorioRenglon1=random.choice([0,1,2,3,4,5,6,7])
        ind1numAleatorioFila1=random.choice([0,1,2,3,4,5,6,7])
        ind1numAleatorioRenglon2=random.choice([0,1,2,3,4,5,6,7])
        ind1numAleatorioFila2=random.choice([0,1,2,3,4,5,6,7])
        
        ind2numAleatorioRenglon1=random.choice([0,1,2,3,4,5,6,7])
        ind2numAleatorioFila1=random.choice([0,1,2,3,4,5,6,7])
        ind2numAleatorioRenglon2=random.choice([0,1,2,3,4,5,6,7])
        ind2numAleatorioFila2=random.choice([0,1,2,3,4,5,6,7])
        
        auxInd1C1=listaLegado[0][0][ind1numAleatorioRenglon1][ind1numAleatorioFila1]
        auxInd1C2=listaLegado[0][0][ind1numAleatorioRenglon2][ind1numAleatorioFila2]
        auxInd2C1=listaLegado[1][0][ind2numAleatorioRenglon1][ind2numAleatorioFila1]
        auxInd2C2=listaLegado[1][0][ind2numAleatorioRenglon2][ind2numAleatorioFila2]
        
        listaLegado[0][0][ind1numAleatorioRenglon1][ind1numAleatorioFila1]=auxInd1C2
        listaLegado[0][0][ind1numAleatorioRenglon2][ind1numAleatorioFila2]=auxInd1C1
        listaLegado[1][0][ind2numAleatorioRenglon1][ind2numAleatorioFila1]=auxInd2C2
        listaLegado[1][0][ind2numAleatorioRenglon2][ind2numAleatorioFila2]=auxInd2C1
    return listaLegado

def generarNuevaPob(listaLegado,listamejores):
    i=0
    k=0
    for individuo in range(num_ind_poblacion):
        if individuo<=1:
            poblacion[individuo]=listaLegado[individuo][0]
        elif individuo>=2 and individuo<=1+(math.floor(num_ind_poblacion*.1)) and (math.floor(num_ind_poblacion*.1))>0 :
            poblacion[individuo]=listamejores[i][0]
            i=i+1
        else:
            listadelosmejores10por,listaDeLospadreSigGen= seleccion(individuoConfit)
            recvCruza=cruza(listaDeLospadreSigGen)
            cromosoma=mutacion(recvCruza)
            poblacion[individuo]=cromosoma[k][0]
            if k==1:
                k=0
            k=k+1
def generarNuevaPob_(listaLegado,listamejores):
    i=0
    for individuo in range(num_ind_poblacion):
        if individuo<=1:
            poblacion[individuo]=listaLegado[individuo][0]
        elif individuo>=2 and individuo<=1+(math.floor(num_ind_poblacion*.1)) and (math.floor(num_ind_poblacion*.1))>0 :
            poblacion[individuo]=listamejores[i][0]
            i=i+1
        else:
            cromosoma=generarIndividuo()
            poblacion[individuo]=cromosoma
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
from tqdm import tqdm
def algoGen():
    loop = tqdm(total=generaciones, position=0, leave=False, unit=" Generaciones")
    generarPobInicial()   
    for i in range(generaciones):  
        fitness()
        if i==0:
            decodificar(individuoConfit[0][0],"mejorIndivpriPobAlgoDif3.png")
            #file_w.write("\n---el mejor es de la poblacion---"+str(i)+"\n"+str(individuoConfit[0][0])+"\n Con un fitness de(heuristica): "+str(individuoConfit[0][1]))
        if i==1:
            decodificar(individuoConfit[0][0],"mejorIndivSegPobAlgoDif3.png")
            #file_w.write("\n---el mejor es de la poblacion---"+str(i)+"\n"+str(individuoConfit[0][0])+"\n Con un fitness de(heuristica): "+str(individuoConfit[0][1]))
        
        #print("\n---el mejor es de la poblacion---",i,"\n",individuoConfit[0][0],"\n Con un fitness de(heuristica): ", individuoConfit[0][1])
        listadelosmejores10por,listaDeLospadreSigGen = seleccion(individuoConfit)
        recvCruza=cruza(listaDeLospadreSigGen)
        recvMutacion=mutacion(recvCruza)
        generarNuevaPob(recvMutacion,listadelosmejores10por)
        if individuoConfit[0][1]<115:
            print("salí en: ",i,"\n")
            break
        loop.set_description("Gen Actual/Gen Total ".format(i))
        loop.update(1)
    loop.close()
#-----------------------------------------------------------------------
# -----------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------

