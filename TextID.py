# TextID project!
#
# AKA   : Akshay Trikha, Violet Burbank, Elena Ehrlich

from collections import defaultdict
import math

# TODO: fix getWords to include case for non-sentence ending punctuation with two spaces in between it

endPunc = [".", "!", "?"] # sentence ending punctuation
nonEndPunc = [";", ":", ",", "-", "&", "â€“", "(", ")", "{", "}", "[", "]", "<", ">", '"', "'", "`", "â€", "â€œ"] # non-sentence ending punctuation
# different quotation mark types are included in list
# TODO: consider slanted single quotes
# TODO: consider the newline
suffixes = ["e", "es", "ly", "est", "ing", "s", "ism", "ist", "est", "ness", "ship", "sion", "tion", "ies", "ate", "ed", "en", "ize", "ise", "able", "ible", "al", "esque", "ful", "fully", "ic", "ical", "ious", "ous", "ish", "less", "y"]
suffixes.sort(key = len, reverse = True)
suffixCons = ["s"]
suffixVow2Cons = ["ing"]

def readTextFromFile (fileName1):
    """ returns a wordList after reading text from a textFile """
    currentFile = open(fileName1, "r")
    text = currentFile.readlines()
    currentFile.close()

    cleanList = list(map(lambda x: x.strip("\n"), text)) # removes the new line character, "\n" from text

    wordList = []
    for i in cleanList:
        wordList += i.split() # 

    return wordList # main list for algorithm

def getSentences (wordList):
    """ returns a list containing sentences """
    if (wordList == []):
        return []
    else:
        sentenceList = []
        for i in range(len(wordList)):
            if (wordList[i][-1] in endPunc):
                sentenceList.append(wordList[:i + 1])
                return sentenceList + getSentences(wordList[i + 1:])
    return sentenceList

def makeSentenceLengths (sentenceList):
    """ returns a dictionary of sentences lengths and their frequencies """
    sentenceDictionary = {}
    for i in sentenceList:
        if not (len(i) in list(sentenceDictionary.keys())):
            sentenceDictionary[len(i)] = 1
        else:
            sentenceDictionary[len(i)] += 1
    
    return sentenceDictionary

def getWords (wordList):
    """ returns a list containing words (with no punctuation) """
    outputList = []

    for i in range(len(wordList)): # to clean list of all puntuation
        if wordList[i] in nonEndPunc or wordList[i] in endPunc: # to clean word if it is just punctuation
            pass
        elif wordList[i][-1] in nonEndPunc or wordList[i][-1] in endPunc: # to clean end of word punctuation
            if len(wordList[i]) >= 2: # to avoid a index out of bounds error
                if wordList[i][-2] in nonEndPunc or wordList[i][-2] in endPunc: # to clean 2nd from last punctuation
                    outputList.append(wordList[i][:-2])
                else:
                    outputList.append(wordList[i][:-1])
            else:
                outputList.append(wordList[i][:-1])
        elif wordList[i][0] in nonEndPunc or wordList[i][0] in endPunc:
            outputList.append(wordList[i][1:])

    return outputList

def makeWordLengthDictionary (wordList):
    """ returns a dictionary of word lengths and their frequencies """
    wordLengthDictionary = {}
    for i in wordList:
        if not (len(i) in list(wordLengthDictionary.keys())):
            wordLengthDictionary[len(i)] = 1
        else:
            wordLengthDictionary[len(i)] += 1
    
    return wordLengthDictionary

def makeWordCountDictionary (wordList):
    """ returns a dictionary of words and their frequencies """
    wordCountDictionary = {}
    for i in wordList:
        if not (i in list(wordCountDictionary.keys())):
            wordCountDictionary[i] = 1
        else:
            wordCountDictionary[i] += 1
    
    return wordCountDictionary

def getPunc (wordList):
    """ returns a list containing all forms of punctuation found """
    puncList = []
    for i in range(len(wordList)): # to clean list of all puntuation
        if wordList[i][-1] in nonEndPunc or wordList[i][-1] in endPunc:
            puncList.append(wordList[i][-1])

            if len(wordList[i]) >= 2: # to avoid a index out of bounds error
                if wordList[i][-2] in nonEndPunc or wordList[i][-2] in endPunc: 
                    puncList.append(wordList[i][-2])

        if wordList[i][0] in nonEndPunc or wordList[i][0] in endPunc:
            puncList.append(wordList[i][0])

    return puncList

def makePuncCountDictionary (puncList):
    """ returns a dictionary of punctuation marks and their frequencies """
    puncCountDictionary = {}
    for i in puncList:
        if not (i in list(puncCountDictionary.keys())):
            puncCountDictionary[i] = 1
        else:
            puncCountDictionary[i] += 1
    
    return puncCountDictionary

def getStems (wordList):
    """ returns a list of all word stems found """
    stemList = []
    for i in wordList:
        for j in suffixes:
            l = len(j)
            if i[-l:] == j:
                stemList.append(i[:-l])
                break
        stemList.append(i)        

    return stemList       

def makeStemsDictionary (stemList):
    """ returns a dictionary of stems and their frequencies """
    stemsDictionary = {}
    for i in stemList:
        if not (i in list(stemsDictionary.keys())):
            stemsDictionary[i] = 1
        else:
            stemsDictionary[i] += 1

    return stemsDictionary

def normaliseDictionary (dictionary):
    """ returns a normalised version (value = between 0 and 1) of any input dictionary """
    counts = sum(list(dictionary.values()))
    for i in list(dictionary.keys()):
        dictionary[i] = dictionary[i]/counts
    
    return dictionary

def createAllDictionaries (fileName):
    """ calls dictionary building functions to create 5 dictionaries for a given text file.
        returns the dictionaries in a list. """
    text = readTextFromFile(fileName) # a wordList
    sentences = getSentences(text) # a sentenceList
    puncs = getPunc(text) # a puncList
    justWords = getWords(text) # a list of only words (no punctuation), MODIFIES TEXT SO THAT IT HAS NO PUNCTUATION
    stems = getStems(justWords)

    wordLength = makeWordLengthDictionary(justWords) # dictionary of key = length of word, value = frequency
    wordCount = makeWordCountDictionary(justWords) # dictionary of key = word, value = frequency
    punctuation = makePuncCountDictionary(puncs) # dictionary of key = punctuation, value = frequency
    sentenceLength = makeSentenceLengths(sentences) # dictionary of key = length of sentences, value = frequency
    stemsDictionary = makeStemsDictionary(stems) # dictionary of key = stem, value = frequency

    return [wordCount, wordLength, stemsDictionary, sentenceLength, punctuation]

def normaliseModel (TM):
    """ normalises all dictionaries in textModel """
    outputTextModel = []
    for i in TM:
        outputTextModel.append(normaliseDictionary(i))
    
    return outputTextModel

def smallestValue (dictionary1, dictionary2):
    """ returns the smallest value between both dictionary1 and dictionary2 """
    min1 = min(dictionary1.values())
    min2 = min(dictionary2.values())
    return min(min1, min2)

def compareDictionaries (unknownDictionary, dictionary1, dictionary2):
    """ """
    minvalue = smallestValue(dictionary1, dictionary2)

    probability1 = 1
    probability2 = 1

    for i in unknownDictionary:
        if i in dictionary1.keys(): 
            probability1 *= dictionary1[i]**unknownDictionary[i]
        else:
            probability1 *= minvalue/2
    
        if i in dictionary2.keys(): 
            probability2 *= dictionary2[i]**unknownDictionary[i]
        else:
            probability2 *= minvalue/2

    if probability1 == 0 and probability2 == 0:
        return[0,0]
    elif probability1 == 0:
        return[0, math.log(probability2)]
    elif probability2 == 0:
        return[math.log(probability2), 0]
    else:
        return [math.log(probability1), math.log(probability2)]

def compareAllDictionaries (textModel, normalModel1, normalModel2):
    """ Returns a list including: [ model with best fit, # attributes that model1 was better at, # attributes that model2 was better at. 
    Takes in a non-normalised text model and two normalised models. """
    results = []
    model1WinCount = 0
    model2WinCount = 0
    tieCount = 0
    for i in range(len(textModel)):
        comparison = compareDictionaries(textModel[i], normalModel1[i], normalModel2[i])
        if comparison[0] > comparison[1]: 
            results.append("Model 1.")
            model1WinCount += 1
        elif comparison[1] > comparison[0]: 
            results.append("Model 2.")
            model2WinCount += 1
        else:
            results.append("a tie.")
            tieCount += 1

    return [results, model1WinCount, model2WinCount]

# TODO: change TM to textModel
# a function to print all of the dictionaries in a TextModel1
def printAllDictionaries (TM):
    """ a function to print all of the dictionaries in TM
        input: TM, a text model (a list of 5 or more dictionaries) """
    words = TM[0]
    wordlengths = TM[1]
    stems = TM[2]
    sentencelengths = TM[3]
    punctuation = TM[4]

    print("\nWords:\n", words)
    print("\nWord lengths:\n", wordlengths)
    print("\nStems:\n", stems)
    print("\nSentence lengths:\n", sentencelengths)
    print("\nPunctuation:\n", punctuation)
    # print("\nNormalised Words:\n", TM[5])
    print("\n\n")


def compareTexts (fileName1, fileName2, fileName3):
    """ Model 1 is the one used to compare against Model 2 and Model 3.
    Main function for algorithm. """
    TextModel1 = createAllDictionaries(fileName1) 

    TextModel2 = createAllDictionaries(fileName2) 
    normalModel2 = normaliseModel(TextModel2)

    TextModel3 = createAllDictionaries(fileName3) 
    normalModel3 = normaliseModel(TextModel3)

    results = compareAllDictionaries(TextModel1, normalModel2, normalModel3)
    print("The better model for words was", results[0][0])
    print("The better model for word lengths was", results[0][1])
    print("The better model for stems was", results[0][2])
    print("The better model for sentence lengths was", results[0][3])
    print("The better model for punctuation was", results[0][4])
    
    if results[1] > results[2]: 
        print("Model 1 was a better model overall.")
    elif results[1] < results[2]: 
        print("Model 2 was a better model overall.")
    else:
        print("Model 1 ties with Model 2.")

compareTexts("rowling1.txt", "rowling2.txt", "shakespeare.txt")