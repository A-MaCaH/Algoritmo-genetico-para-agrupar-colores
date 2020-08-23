import algoritmoGenetico
import sys

file_w=open(r"../Resultados/elIndividuoResultante.txt","w")
#algoritmoGenetico.generaciones=100
algoritmoGenetico.algoGen()
file_w.write("\n---el mejor es---\n")
file_w.write(str(algoritmoGenetico.individuoConfit[0][0]))
file_w.write("\n Con un fitness de(heuristica): ")
file_w.write(str(algoritmoGenetico.individuoConfit[0][1]))
#print("\n---el mejor es---\n",individuoConfit[0][0],"\n Con un fitness de(heuristica): ", individuoConfit[0][1])
file_w.close()
algoritmoGenetico.decodificar(algoritmoGenetico.individuoConfit[0][0],"../Resultados/elIndividuoResultante.png")