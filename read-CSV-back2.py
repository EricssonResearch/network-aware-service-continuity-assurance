##################################################################

# Author: Shilpa Budhkar

# Dated: 3 Feb 2023

# Module Name: Microservice Model Generator

# Copyright Ericsson 2023

##################################################################

# importing the module
import csv
import zulu
import pandas as pd 
import numpy
from datetime import timedelta
#creating a csv of unique source and destination list
#-----------------------------------------------------------------------------------------------------------------------------------------
# open the file in read mode
filename = open('backend-v2-cluster-2.csv', 'r')

# creating dictreader object
file = csv.DictReader(filename)

# creating empty lists
source = []
dest = []

# iterating over each row and append
# values to empty list
for col in file:
	source.append(col['downstream_pod_ip'])
	dest.append(col['upstream_pod_ip'])
	#totalunit.append(col['total_units'])

# printing lists
# print('Source:', source)
# print('Destination:', dest)
     
dict = {'SourceIP': source, 'DestinationIP': dest}  
       
df = pd.DataFrame(dict) 
uniq= df.drop_duplicates()
    
uniq.to_csv('dependency-b2.csv') 
#----------------------------------------------------------------------------------------------------------------------------------------
#Function to Change time into seconds for frequency calculation
def get_seconds(time_str):
    #print('Time in hh:mm:ss:', time_str)
    # split in hh, mm, ss
    hh, mm, ss = time_str.split(':')
    return float(hh) * 3600 + float(mm) * 60 + float(ss)
#Data Frame to Read source desti IP from dependecny.csv and retrieving parameters for corresponding IP pair from traces
sd = pd.read_csv('dependency-b2.csv')
sdtrace = pd.read_csv("backend-v2-cluster-2.csv", usecols=["timestamp","duration","bytes_sent","bytes_received","downstream_pod_ip","upstream_pod_ip"])
#create empty time and other paramters list
timecount = []
allPairFreq = []
bandlist1 = []
bandlist2 = []
rtdlist = []
allPairBand = []
allPairRTD = []
for i in sd.index:
	x1 = sd['SourceIP'][i] 
	y1 = sd['DestinationIP'][i] 
	# print (x1)
	# print (y1)
	for j in sdtrace.index:
		x2 = sdtrace['downstream_pod_ip'][j]		
		y2 = sdtrace['upstream_pod_ip'][j]
		# print (x2)
		# print (y2)
		if ((x1== x2) and (y1==y2)): 
			# print("source and dest match")
			timecount.append(sdtrace['timestamp'][j]) # create a list of all time stamps for IP Pair
			bandlist1.append(sdtrace['bytes_sent'][j])
			bandlist2.append(sdtrace['bytes_received'][j])
			rtdlist.append(sdtrace['duration'][j])
	#-----------------------------------------------------------------------------------------------------------------------
	#Caclulate frequency for no of messages per second
	t1 = 0
	t2 = 0
	count =0
	t1 = zulu.parse(timecount[0])
	k1 = 0
	freq = []
	for k in timecount:
		t2= zulu.parse(timecount[k1])
		temp = get_seconds(str(t2-t1))		
		if temp < 1:
			count =count+1
			# print("time difference not one now = ", get_seconds(str(t2-t1)))
		else:
			# print("time difference is one now = ", get_seconds(str(t2-t1)), " and count is ", count)
			freq.append(count) # add no. of messages exchange within 1 sec in freq list
			count =0 # resent counter for another second
			t1 = zulu.parse(timecount[k1]) # reset start point to count frequency
		k1 = k1+1
		
	freq.append(count) # add last no. of messages exchange within 1 sec in freq list
	# print("Freq list is ", freq)
	# print("Average of the freq is ", numpy.average(freq))
	#add average freq to allPairFreq
	allPairFreq.append(round(numpy.average(freq)))
	freq.clear() # reset freq for another IP pair
	timecount.clear() # reset timecount list for another IP pair
	#---------------------------------------------------------------------------------------------------------------------------------------
	#calculate bandwdth consumption in no. of bytes 
	# print(bandlist1, " Average is ", numpy.average(bandlist1))
	# print(bandlist2, " Average is ", numpy.average(bandlist2))
	B = (numpy.average(bandlist1) + numpy.average(bandlist2))/2
	allPairBand.append(round(B))
	# print("Average bandwith usage is ", B)
	bandlist1.clear()
	bandlist2.clear()
	#---------------------------------------------------------------------------------------------------------------------------------------
	#calculate average of round trip delay in milliseconds 
	allPairRTD.append(round(numpy.average(rtdlist)))
	rtdlist.clear() # reset freq for another IP pair

#add allPairFreq to csv
addcol = pd.read_csv('dependency-b2.csv')
addcol['Frequency'] = allPairFreq
addcol['Bandwidth_C'] = allPairBand
addcol['RT_Delay'] = allPairRTD
addcol.to_csv("dependency-b2.csv",index=False)
