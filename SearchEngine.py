#Author - Matthew Jacobson
#CS 600A Search Engine Project
"""
Input: HTML files from /SearchEngineAlgorithims/IndexedWebsiteStorage
Output: Keyword Inverted File for searching 

"""
#need a hack for convertinf from string to dictionary 
import ast
#imports for ascii fun for a close to GUI result
import pyfiglet
#Import regex
import re
#Import web crawler for text parsing
from bs4 import BeautifulSoup
#Import methods for working with files
import os
#Work around for encoding errors
import sys
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
#make imports for keyword extractions
from summa import keywords
#-----------------------------------------------------------------------------------------------
#my implementation of a trie node as well what a normal node should look like
#Trie Node, 
# must contain a value that it stores & all of its children
class Node: 
    #constructor will only take in a value
    def __init__(self,value):
        self.value = value
        #collection of children, the root node needs at least one for every letter in the alphabet so it has to be a collection
        #I will use a dictionary to find the next letter quickly.
        self.children = {}        
class Trie: 
    #the first node in a trie will contain nothing but refrences to children nodes
    def __init__(self):
        #add an empty node
        # print("Successfully Created")
        self.root = Node('')
    #Add a word to the search trie
    def addWord(self,word):
        currNode = self.root
        #split letters into a list that is easly manipulated
        letters = [char for char in word]
        #iterate through each of the letters in the word to see if they are in the trie, if there then theres nothing to do.
        for char in letters:
            #check if the letter is already there.
            if currNode.children.get(char) == None:
                #if its not there then add the letter to the Trie
                currNode.children[char] = Node(char)
                # print(str(currNode.children))
                #then iterate through the node we just made
                currNode = currNode.children[char]
            else:
                #Otherwise, move onto the next node in the sequence
                currNode = currNode.children[char]        
    def findWord(self,word):
        #follows the same structure as befor
        currNode = self.root
        # print(str(currNode.value))
        #as before, get the list of letters to check 
        letters = [char for char in word]
        for char in letters: 
            # print(char)
            if currNode.children.get(char) == None: 
                #if its not in the next dictionary then the word cant be there
                #so return false
                return False 
            else:
                # move to the next node
                currNode = currNode.children[char]
        #now check if this is the last letter in the word buy checking the letter at -1 indicey 
        if currNode.value == letters[-1]:
            return True
        else:
            print("how did you get here") # The program should never get here but put a print for debugging
            return False       

#Call this method to create index files for all already generated 
def createInvertedFiles():
    webpageCount = 0 
    #remember base directory
    webPages = 'IndexedWebsiteStorage'
    currDirectory = os.getcwd()
    #Iterate through parsed websites to index their contents
    occurenceListExport = []
    websitenameLists = []
    for filename in os.scandir(webPages):
        #if it finds something that is a file then parse its content
        if filename.is_file():
            with open(filename.path, 'r', encoding='UTF-8') as file:
                soup = BeautifulSoup(file.read(), 'lxml')
                # Grab all the text from the file. Processess it into something that summa can index for getting words we'd want to search
                removeSpaces = str(soup.get_text()).replace('\n','')
                removeSpecialChars = re.sub(r'[^\w]', ' ', removeSpaces)
                text = " ".join(removeSpecialChars.split())
                # with open('testoutput.txt', 'w', encoding= 'utf-8') as tempfile:
                #     tempfile.write(text)
                # Now lets extract the keywords to get rid of phrases that arent valueable and remove all stop words all in one line 
                myKeywords = keywords.keywords(text).split("\n")
                # print(myKeywords)
                # Now that we have the keywords we can make our index files to make them searchable  \
                occurenceList = dict()              
                for word in myKeywords:
                    if len(word) <= 1: 
                        continue
                    else:
                        occurenceList[word] = text.count(word)     
                #now add corresponding occurences into the current dictionary occurence list 
                occurenceListExport.append(occurenceList) 
                websitenameLists.append(str(filename)[11:-7])   
                webpageCount+=1
    print("Webpages Indexed: "+ str(webpageCount))         
    # #change into the inverted files directory for storage. 
    invertedFileStorage = 'InvertedFiles'
    os.chdir(invertedFileStorage)
    namecount = 0
    #now write each to their own file for easy access and storage
    for occlist in occurenceListExport:
        # print(occlist)
        #then write them to file for storage
        with open(str(websitenameLists[namecount])+".txt", 'w', encoding='UTF-8') as file:
            file.write(str(occlist))
            namecount += 1
    #now return a trie of words all the words in the occurance lists.
    listOfTries = []
    #for each occurence list, grab all of the keys and put them into the Trie
    for occlist in occurenceListExport:
        tempTrie = Trie()
        for x in occlist:
            tempTrie.addWord(x)
        listOfTries.append(tempTrie)
    os.chdir(currDirectory)
    return listOfTries

#method to make quick comparisons, NoneValues need to be translated to 0 
def sortHelp(x):
    if x[0] == None:
        return 0 
    else:
        return x[0]
     
def searchCurrentlyIndexedByTerm(tries):
    #Title output 
    print(pyfiglet.figlet_format('Search Engine', font='banner3-D'))
    print("Search Engine by Matthew Jacobson")
    name = input("Have you made sure that you have indexed all websites before proceeding using the WebCrawler.py found in this folder? (y/n) ")
    if name == 'n':
        print('Come back later when you have input all links into the WebCrawler.py')
        return None
    print("---------------------------------")
    inputQuery = input("Please enter search terms seperated by a space\n")
    currDirectory = os.getcwd()
    query = []
    if inputQuery[0] == ' ':
        query = inputQuery[1:].lower().split()
    else:
        query = inputQuery.lower().split()
    #Load in occurences and tries
    inputTries = tries
    #input the folder that contains inverted files
    invertedFileStorage = 'InvertedFiles'
    listOfOccuranceLists = []
    websiteTitles =[]
    #Iterate through stored dictionaries and input them 
    for filename in os.scandir(invertedFileStorage):
        if filename.is_file():
            with open(filename.path, 'r', encoding='UTF-8') as file:
                dict = file.read()
                #use this hack from https://favtutor.com/blogs/string-to-dict-python to utilzie the built in ast package to convert text stored in files to a useable dictionary
                listOfOccuranceLists.append(ast.literal_eval(dict))
                websiteTitles.append(str(filename))          
    # print(listOfOccuranceLists)            
    #output result
    #now search the tries and search for the word/s in question
    #we want to find how many times that word occurences occur so we'll keep track which one of the websites we are on. 
    #this dictionary "toBePrinted" stores the word/occurence pairs 
    toBePrinted = []
    #I've set up my code in a way that the tries match the websites occurence list in order so [0] will be the same in tries and occurance lists
    trackWebsite = 0
    for words in query: 
        for trie in inputTries:
            if trie.findWord(words):
                #Grab values and put them in our list for easy access
                toBePrinted.append([listOfOccuranceLists[trackWebsite].get(words),str(websiteTitles[trackWebsite][11:-6]).replace("_"," ")])
                trackWebsite+=1
            else:
                #iterate website to keep track
                trackWebsite+=1
                continue
    # Print Output
    # print(toBePrinted)
    print("Results: -------------------------------")
    #sort output
    toBePrinted.sort(key = lambda x : sortHelp(x), reverse=True)
    # print(toBePrinted)
    temp = 1 
    for result in toBePrinted: 
        print(str(temp)+ ": "+ " ".join(str(result[1]).split()) + ", had the search term appear "+ str(result[0]) + " times")
        temp+=1
        
def main():
    #run program
    searchCurrentlyIndexedByTerm(createInvertedFiles())

#main method
if __name__ == "__main__":
    main()
