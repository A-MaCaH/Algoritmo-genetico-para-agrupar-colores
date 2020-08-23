import algoritmoGenetico


file_w=open("algoGenAlgoDif3.txt","w")
algoritmoGenetico.generaciones=1000
algoritmoGenetico.algoGen()
file_w.write("\n---el mejor es---\n")
file_w.write(str(algoritmoGenetico.individuoConfit[0][0]))
file_w.write("\n Con un fitness de(heuristica): ")
file_w.write(str(algoritmoGenetico.individuoConfit[0][1]))
#print("\n---el mejor es---\n",individuoConfit[0][0],"\n Con un fitness de(heuristica): ", individuoConfit[0][1])
file_w.close()
algoritmoGenetico.decodificar(algoritmoGenetico.individuoConfit[0][0],"mejorIndivAlgoDif3.png")