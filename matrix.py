##################################################################

# Author: Shilpa Budhkar

# Dated: 3 Feb 2023

# Module Name: Microservice Model Generator

# Copyright Ericsson 2023

##################################################################
#function to print the weighted graph
def printgraph(mat):
	row, col = len(mat), len(mat[0]);
	for i in range(row):
		for j in range(col):
			if i==j:
				mat[i][j]='M-'+str(i) #shows microservice id
			print(mat[i][j], end="\t")
		print()

file1 = open("mat-input.txt","r+")  #opening the trace file to read the source microservice
#destination microservice and edge weight tuple

vert, edge = map(int,file1.readline().split()) # reading no. of vertices and edges
mat= [[0]*vert for i in range(vert)] 
for i in range(edge):
	s,d,wt= map(str, file1.readline().split()) # read one line at a time from the trace file
	s=ord(s) - ord('A')
	d=ord(d) - ord('A')
	#wt=int(wt)
	mat[s][d]=wt #put weight tuple for each edge in the graph matrix
	
printgraph(mat)