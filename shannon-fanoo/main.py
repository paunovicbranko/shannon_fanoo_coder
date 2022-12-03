from cgi import print_form
from itertools import count
import math


def listCreate(symbols,probabilities,numberOfSymbols,codes):
    #sortiranje nizova u zavisnosti od verovatnoca - opadajuce

    for i in range(numberOfSymbols):
        for j in range(i+1, numberOfSymbols):
            if (probabilities[i] < probabilities[j]):
            
                temp = probabilities[i]
                probabilities[i] = probabilities[j]
                probabilities[j] = temp

                temp = symbols[i]
                symbols[i] = symbols[j]
                symbols[j] = temp

    sum1 = 0

    # Prva dodela 0 i 1
    tempArray = [0] * numberOfSymbols
    half = sum(probabilities) / 2

    for i in range(numberOfSymbols):
        tempArray[i] = abs(sum1 + probabilities[i] - half)
        sum1 += probabilities[i]


    index = tempArray.index(min(tempArray))

    for i in range (index + 1):
        codes[i] = "0"

def listSeparation(listOfSymbols,listOfProb,listOfCodes):
    tempListOfProb = []
    tempListOfSymb = []

    # Prolazi kroz simbole i za dati simbol proverava da li neki drugi simbol ima iste bite kao taj
    for k in range(math.ceil(math.log2(len(listOfSymbols)))):
        for i in range(len(listOfCodes)):
            tempSymb = listOfSymbols[i]
            for j in range(len(listOfCodes)):
                if listOfCodes[i] == listOfCodes[j]:
                    tempListOfProb.append(listOfProb[j])     # U slucaju da ima, doda verovatnocu u trenutni niz
                    tempListOfSymb.append(listOfSymbols[j])  # U slucaju da ima, doda simbol u trenutni niz
            addBits(listOfSymbols,tempListOfProb,listOfCodes,tempListOfSymb)
            tempListOfProb = []
            tempListOfSymb = []

def addBits(listOfSymbols,tempListOfProb,listOfCodes,tempListOfSymb):

    # U slucaju da podlista ima samo jedan simbol zavrsava se
    if(len(tempListOfSymb)) == 1:
        return

    # Nalazi sumu od podniza
    tempSumOfProb = 0
    for i in range(len(tempListOfProb)):
        tempSumOfProb = tempSumOfProb + tempListOfProb[i]
    
    tempHalf = tempSumOfProb/2

    # Trazi gde da stavi "crtu" u podnizu
    newArray = [tempListOfProb[0]]
    for i in range(1,len(tempListOfProb)):
        if abs(sum(newArray) - tempHalf) >= abs(sum(newArray) + tempListOfProb[i] - tempHalf):
            newArray.append(tempListOfProb[i])
        else:
            break
    newArrayOfSymb = []
    for i in range(len(newArray)):
        newArrayOfSymb.append(tempListOfSymb[i])
    
    

    # "Gornjem" delu podskupa dodeljuje vrednost 1
    for i in range(len(newArrayOfSymb)):
        indexx = listOfSymbols.index(newArrayOfSymb[i])
        listOfCodes[indexx] += "0" 
    
    # "Donjem" delu podskupa dodeljuje vrednost 0
    for i in range(len(newArrayOfSymb),len(tempListOfSymb)):
        indexx = listOfSymbols.index(tempListOfSymb[i])
        listOfCodes[indexx] += "1" 

def calculateValeus(probabilities,codes):
    L = H = ni = ro = 0.0
    # Srednja duzina kodne reci
    for i in range(len(probabilities)):
        L = probabilities[i]*100*len(codes[i]) + L
    L = L/100
    L = round(L,4)

    # Entropija
    for i in range(len(probabilities)):
        H = math.log2(1/probabilities[i])*probabilities[i]*100 + H
    H = H/100
    H = round(H,4)


    # Efikasnost
    ni= round(H/L,4)

    # Stepen kompresije
    ro= math.ceil(math.log2(len(probabilities)))/L
    ro= round(ro,4)
    return L,H,ni,ro

def printAll(listOfSymbols,listOfProb,codes,L,H,ni,ro):
    
    
    print("\n\n|----------------------------------------------------")
    print("| Symbol" + "\t" + "| Probability" + "\t" + "\t| Code" + "\n|----------------------------------------------------")
    for i in range(len(listOfSymbols)):
        print("| " + listOfSymbols[i] + "\t\t" + "| " + "%.4f" % listOfProb[i] + "\t\t" + "| " + codes[i] + "\t\n|----------------------------------------------------")


    #print("\nSymbols")
    #print(listOfSymbols)

    #print("\nProbabilities")
    #print(listOfProb)

    #print("\nCodes")
    #print(codes)

    print("\nAvarage length of codes: " + str(L))
   # print(L)

    print("Entropy: " + str(H))
   # print(H)

    print("Efficiency: " + str(ni))
   # print(ni)

    

    print("Compression: " + str(ro))
    #print(ro)
    print("----------------------------------------------------\n")

def proccesingText(hmongText,hmongSymbols,probabilitiesOfSymbols, hmongCodes):
    
    hmongText = ''.join(e for e in hmongText if e.isalnum())
    hmongText = hmongText.lower()

    
    for i in hmongText:
        if i not in hmongSymbols:
            hmongSymbols.append(i)

    
    for i in hmongSymbols:
        probabilitiesOfSymbols.append(hmongText.count(i)) 


    sum1= 0
    for i in range(len(probabilitiesOfSymbols)-1):
        probabilitiesOfSymbols[i] = probabilitiesOfSymbols[i] / len(hmongText)
        probabilitiesOfSymbols[i] = round(probabilitiesOfSymbols[i],4)
        sum1 += probabilitiesOfSymbols[i]

    probabilitiesOfSymbols[len(probabilitiesOfSymbols)-1] = 1 - sum1
    probabilitiesOfSymbols[len(probabilitiesOfSymbols)-1] = round(probabilitiesOfSymbols[len(probabilitiesOfSymbols)-1],4)

    hmongCodes = ["1"] * len(hmongSymbols)
    lengthOfText = len(hmongSymbols)
    listCreate(hmongSymbols,probabilitiesOfSymbols,lengthOfText,hmongCodes)
    listSeparation(hmongSymbols, probabilitiesOfSymbols, hmongCodes)

    return hmongCodes

def coder(listOfSymbols,codes,text):

    coderOutput = ''
    for i in text:
        j=listOfSymbols.index(i)
        coderOutput += str(codes[j])
    
    return coderOutput

def decoder(listOfSymbols,codes,decoderInput):

    tempCode = ''
    decoderOutput = ''
    for i in decoderInput:
        tempCode += i
        if tempCode in codes:
            j = codes.index(tempCode)
            decoderOutput += listOfSymbols[j]
            tempCode = ''
    
    return decoderOutput

def isEqual(text1,text2):

    len1 = len(text1)
    len2 = len(text2)

    minLen = min(len1,len2)
    countErrors = 0
    for i in range(minLen):
        if text1[i] != text2[i]:
            countErrors +=1

    if (countErrors == 0): return "There is no errors!"
    
    return "There is " + str(countErrors) + " errors of " + str(len1) + " characters\n"

def channelError(coderOutput):
    
    coderOutput = list(coderOutput)

    T = 2000
    for i in range(T,len(coderOutput),T):
        if(coderOutput[i] == "1"): 
            coderOutput[i] = "0"
        else: coderOutput[i] = "1"

    return coderOutput

# Input

print("Enter the number of symbols: ")
numberOfSymbols = int(input())

symbols = []
probabilities = []
codes = ["1"] * numberOfSymbols

for i in range(numberOfSymbols):
    print("Enter " + str(i+1) + ". symbol: ")
    symbols.append(input())

for i in range(numberOfSymbols):
    print("Enter the probability of the " + str(i+1) + ". symbol: ")
    probabilities.append( float( input( )))
    if (probabilities[i] > 1 or probabilities[i] < 0):
        exit("ERROR: Wrong input")

checkSum = 0
for i in probabilities:
    bigI = i*100 #Mnozimo sa 100 kako bi izbegli bag u pajtonu(npr. desi se da 0.2 prevede u 0.19999999... i dolazi do greske)
    checkSum = checkSum + bigI
if checkSum != 100:
    exit ("ERROR: Sum of probabilities is not equal 1")




listCreate(symbols,probabilities,numberOfSymbols,codes)
listSeparation(symbols,probabilities,codes)
L,H,ni,ro = calculateValeus(probabilities,codes)
printAll(symbols,probabilities,codes,L,H,ni,ro)


# Kodovanje texta na Hmong jeziku
HmongData = open("GV_Hmong.txt", 'r')
hmongText = HmongData.read()
HmongData.close()

hmongSymbols = []
probabilitiesOfSymbols = []
hmongCodes = []
hmongText = ''.join(e for e in hmongText if e.isalnum())
hmongText = hmongText.lower()
hmongCodes = proccesingText(hmongText, hmongSymbols, probabilitiesOfSymbols, hmongCodes)
L,H,ni,ro = calculateValeus(probabilitiesOfSymbols,hmongCodes)
coderOutput = coder(hmongSymbols,hmongCodes,hmongText)
coderOutput = channelError(coderOutput)
decoderOutput = decoder(hmongSymbols,hmongCodes,coderOutput)
printAll(hmongSymbols,probabilitiesOfSymbols,hmongCodes,L,H,ni,ro)
print(isEqual(hmongText,decoderOutput))
#print(decoderOutput)

