#Summary Script for Usage
#Dependency: Apache LibCloud
#Written by: Seelan , Guan Hong
#hello

import os
import datetime
import ast

##CREATE A CREDENTIALS FILE NAME "credentials.txt", CONTENTS AS FOLLOWS: ['$USERNAME','$PASSWORD']
##THE PROGRAM SHOULD HAVE NO ISSUE READING THE CREDENTIALS FILE.

fileCredentials = open("credentials.txt","r")
credentialList = fileCredentials.read()
fileCredentials.close()
credentialList = ast.literal_eval(credentialList)

username = credentialList[0]
password = credentialList[1]

#when reading Bandwidth file/Price file [JP-HK-SG-AU-NZ]
filePrice = open("price.txt","r")
priceList = filePrice.read()
filePrice.close()
priceList = ast.literal_eval(priceList) # converts string to list type

#readying libcloud driver
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
cls = get_driver(Provider.DIMENSIONDATA)

#creating of summary log, based on the current date | use this only when you're running a local copy
#datenow = datetime.datetime.now()
#datenow = datenow.strftime("%Y%m%d")
#datenowfile = datenow
#datenowfile = datenowfile + '-Summary.txt'
fileSummary = open ("output.txt", 'w+')

#range for price estimation
startdate = input("Key the start-date for the range you would like to estimate (YYYY-MM-DD):")
enddate = input("Key the end-date for the range you would like to estimate (YYYY-MM-DD):")
fileSummary.write("MCP 2.0 Usage Estimator\n")
tempprint = "Startdate: " + startdate + "\n"
fileSummary.write(tempprint)
tempprint = "Enddate: " + enddate + "\n\n"
fileSummary.write(tempprint)

apdriver = cls(username, password,region='dd-ap')
apvalue = apdriver.ex_summary_usage_report(startdate,enddate)
audriver = cls(username, password,region='dd-au')
auvalue = audriver.ex_summary_usage_report(startdate,enddate)
headers = apvalue[0]

#create total usage lists for each DataCenter
ctul = 0
HKTotal = []
HKPrice = []
JPTotal = []
JPPrice = []
SGTotal = []
SGPrice = []
AUTotal = []
AUPrice = []
NZTotal = []
NZPrice = []
while ctul < len(headers):
    HKTotal.insert(ctul, float(0))
    HKPrice.insert(ctul, float(0))
    JPTotal.insert(ctul, float(0))
    JPPrice.insert(ctul, float(0))
    SGTotal.insert(ctul, float(0))
    SGPrice.insert(ctul, float(0))
    AUTotal.insert(ctul, float(0))
    AUPrice.insert(ctul, float(0))
    NZTotal.insert(ctul, float(0))
    NZPrice.insert(ctul, float(0))
    ctul +=1

i=1
j=2
while i < len(apvalue)-1:
    #print (apvalue[i]) # debug line
    line = apvalue[i]
    while j < len(headers):
        if line[1] == 'AP1' or line[1] == 'AP4':
            JPTotal[j]+=float(line[j])
        elif line[1] == 'AP2' or line[1] == 'AP5':
            HKTotal[j]+=float(line[j])
        else:
            SGTotal[j]+=float(line[j])
        j+=1
    j=2
    i=i+1
print ("------")
i=1
j=2
while i < len(auvalue)-1:
    #print (auvalue[i]) # debug line
    line = auvalue[i]
    while j < len(headers):
        if line[1] == 'AU8' or line[1] == 'AU11':
            NZTotal[j]+=float(line[j])
        else:
            AUTotal[j]+=float(line[j])
        j+=1
    #print(auvalue[i])
    j = 2
    i=i+1

k = 0
j = 2
while k < len(priceList):
    prices = priceList[k]
    if k == 0:
        while j < len(headers):
            #print ("In JP")
            JPPrice[j] = JPTotal[j] * float(prices[j])
            j+=1
    elif k == 1:
        while j < len(headers):
            #print("In HK")
            HKPrice[j] = HKTotal[j] * float(prices[j])
            j += 1
    elif k == 2:
        while j < len(headers):
            #print("In SG")
            SGPrice[j] = SGTotal[j] * float(prices[j])
            j += 1
    elif k == 3:
        while j < len(headers):
            #print("In AU")
            AUPrice[j] = AUTotal[j] * float(prices[j])
            j += 1
    elif k == 4:
        while j < len(headers):
            #print("In NZ")
            NZPrice[j] = NZTotal[j] * float(prices[j])
            j += 1
    k+=1
    j=2

#Printer Number 1
k = 0
while k < len(priceList):
    print ("All prices used are shamelessly stolen from the Public")
    fileSummary.write("All prices used are shamelessly stolen from the Public\n")
    if k == 0:
        print ("CaaS Estimator JP425000 12 Month Term Plan")
        fileSummary.write("CaaS Estimator JP425000 12 Month Term Plan\n")
        printList = JPPrice
    if k == 1:
        print("CaaS Estimator HK40000 12 Month Term Plan")
        fileSummary.write("CaaS Estimator HK40000 12 Month Term Plan\n")
        printList = HKPrice
    if k == 2:
        print("CaaS Estimator SG7500 12 Month Term Plan")
        fileSummary.write("CaaS Estimator SG7500 12 Month Term Plan\n")
        printList = SGPrice
    if k == 3:
        print("CaaS Estimator AU5000 12 Month Term Plan")
        fileSummary.write("CaaS Estimator AU5000 12 Month Term Plan\n")
        printList = AUPrice
    if k == 4:
        print("CaaS Estimator NZ5000 12 Month Term Plan")
        fileSummary.write("CaaS Estimator NZ5000 12 Month Term Plan\n")
        printList = NZPrice
    print("-----------------------------------------")
    fileSummary.write("-----------------------------------------\n")
    y = 1
    totalval = float(0)
    while j < len(headers):
        tempval = round(printList[j],2)
        totalval = totalval+tempval
        print (y,')',headers[j],':',tempval)
        tempprint = str(y)+")"+headers[j]+":"+str(tempval)+"\n"
        fileSummary.write(tempprint)
        if j == len(headers)-1:
        	totalval = round(totalval)
        	print ('Total =', totalval)
        y+=1
        j+=1
    y = 1
    j = 2
    totalval = 0
    print ("\---------------------------------------/")
    fileSummary.write("\---------------------------------------/\n")
    k+=1
fileSummary.close()