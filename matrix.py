# MIT License

# Copyright (c) 2023 Ericsson Research

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
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
