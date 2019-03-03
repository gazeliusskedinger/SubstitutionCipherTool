##############################################################
##
##  MADE ORIGINALLY BY Rasmus A. S. Gazelius Skedinger
##
##  Changes made by:[NAME HERE][DATE]  
##                 :[NAME HERE][DATE]
##                 :[NAME HERE][DATE]
##                 :... 
##                 :please add more if they run out :)
##
## 
##  
##  With License To:
##  USE
##  SHARE
##  CHANGE
##  LEARN
##  
##  But keep my name on top of it!
##  
##  And i will not to be held responsible for the consequences
##  of what you might use it for!
##
##  Enjoy :)
##  
##  Made on Python 2.7 Anaconda
## 
##############################################################

from pwn import *
import re

#teststring contains two 'the' and 'u' together with four 'o's
teststring = "the quick brown fox jumps over the lazy dog"
#theusual english alphabet... nothing new really
alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

#receives the whole text
r = remote("2018shell.picoctf.com","18990")
cipherText = r.recvall()

versionIndex = 0
decryptVersions = [''] * 26

# setts all letters to lowercase

#remove strange symbols
def justLetters(text):
    pureCT = ""
    for i in range(0, len(text)):
        if text[i].isalpha():
            pureCT += text[i]
    return pureCT

#frequency analysis array
def freqAnalysis(text):
    freq = [0] * 26
    for i in text:
        letter  = ord(i)
        letter = letter - 97
        freq[letter] = freq[letter]+1

    return freq

#make printable string list for freq analysis
def makeStringList(stringArray,intArray):
    stringList = []
    for i in range(0, len(stringArray)):
        stringList.append(stringArray[i]+" = "+str(intArray[i]))
    return stringList

#TODO:
#Sort higest Lists
def sortHighestValueFirst(charArray, intArray):
    index = 0
    tempi = 0
    tempc = 0
    highest = 0
    returnArray = []
    for i in range(0, len(intArray)):
        
        highest = intArray[i]

        for j in range(i, len(intArray)):
            if highest <= intArray[j]:
                highest = intArray[j] 
                index = j
        tempi = intArray[i]
        tempc = charArray[i]
        intArray[i] = intArray[index]
        charArray[i] = charArray[index]
        intArray[index] = tempi
        charArray[index] = tempc
        
    return charArray, intArray

#function for bigrams trigrams letter combinations
def gramsSet(text,rangeMin,rangeMax):    
    gramsSet = set()
    gramsArray = []
    for i in range(rangeMin,len(text)-rangeMax+1):
        temp = text[i:i+rangeMax]
        if temp not in gramsSet:
            gramsSet.add(temp)
            gramsArray.append(temp)
    return gramsArray

def gramFreq(text,gram):
    length = len(gram[0])
    freq = [0]*len(gram)
    for i in range(0, len(text)-length+1):
        test = text[i:i+length]
        for j in range(0, len(gram)):
            if test == gram[j]:
                freq[j] = freq[j] + 1
    return freq

#prints list 
def printList(array):
    for i in range(0, len(array)):
        print(array[i])

#def findTHE(bigramsArray,trigramsArray,letterFreq):
cipherText = cipherText.lower()
pureCT = justLetters(cipherText)
val = -1
while val != 0:
    print('0-Exit')
    print('1-Print ciphertext')
    print('2-Print stat analysis')
    print('3-Decrypt THE')
    print('4-Decrypt letter/letters')
    print('5-Undo')
    val = input('Your Choise : ')
    if val == 0:
        print('Exiting!')
    elif val == 1:
        print('Ciphertext : ')
        print(cipherText)
    elif val == 2:
        print('Stat analysis : ')
        
        letterFreq = freqAnalysis(pureCT)
        alpha, letterFreq = sortHighestValueFirst(alpha,letterFreq)
        stringList = makeStringList(alpha,letterFreq)
        printList(stringList)

        bigramsArray = gramsSet(pureCT,0,2)
        bigramFreq = gramFreq(pureCT,bigramsArray)
        bigramsArray, bigramFreq = sortHighestValueFirst(bigramsArray,bigramFreq)
        stringList = makeStringList(bigramsArray,bigramFreq)
        printList(stringList)
    
        trigramsArray = gramsSet(pureCT,0,3)
        trigramFreq = gramFreq(pureCT,trigramsArray)
        trigramsArray, trigramFreq = sortHighestValueFirst(trigramsArray,trigramFreq)
        stringList = makeStringList(trigramsArray, trigramFreq)
        printList(stringList)

    elif val == 3:
        print('Decrypt THE : TODO')
    elif val == 4:
        print('Decrypt letter/letters')
        plainLetters = raw_input('Enter plain : ')
	cipherLetters = raw_input('Enter cipher : ')
        plainLetters = plainLetters.upper()
        decryptVersions[versionIndex] = cipherText
        versionIndex += 1
	pList=list(plainLetters)
	cList=list(cipherLetters)
        for i in range(0,len(pList)):
	    cipherText = cipherText.replace(cList[i], pList[i])
    elif val == 5:
        print('Undo')
        if versionIndex == 0:
	    print("Cipher can't go backmore") 
        else:
            versionIndex -= 1
	    theCipherText = cipherTextVersions[versionIndex] 
    else:
        print('Fel val')

