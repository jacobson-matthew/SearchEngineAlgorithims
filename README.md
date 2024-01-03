# Matthew Jacobson - Search Engine 
# High Level Explaination
For the high level explaination for my code, it has 3 main steps. First, users can use the WebCrawler script to input URL's into the code. The WebCrawler will then get html from the internet and save it to local directory for faster parsing, rather than requesting to the internet each time. My program takes on average 2.8 seconds to run. With web requests the time would be at the mercy of server response times. Second, SearchEngine.py works it's magic. SearchEngine creates 'inverted files' of all the html documents in the IndexedWebsiteStorage Directory. 

As per the instructions in the Chapter 23.6 subsection "Search Engine" It seperates these 'inverted files' into two seperate parts. The first, " An array storing the occurrence lists of the terms (in no particular order)", which I decided to implement occurence lists as a dictonary for a time efficent search when I go to find the number of occurences for ranking outputs. The second, "A compressed trie for the set of index terms, where each external node stores the index of the occurrence list of the associated term." This I have done with my implementation of Node and Trie at the top of the SearchEngine.py File. 

Finally, my program uses the searchCurrentlyIndexedByTerm which will search the tries for quick access to occurences and finds where it occurs as well as what webpage corresponds to the occurance and how many times it was in that webpage. At the very end, output is sorted by occurence (Ranking) and outputted to the console. 
# Data Structure
The two datastructures that I used in my implementation of the search engine was maps/dictonaries and my implementation of a trie. 

As for the first of the two, I used dictionaries extensively most importantly in the occurence list implementation. There is one dictionary for each webpage and it stores keys, which are keywords that have been parsed via summa and their corresponding values which are number of occurences in the article. 

Next, the other major data stucture I used was my implementation of a Trie. Because of the wide number of words that start with different letters I chose to have an open ended dictionary to store refrences to children nodes. The node is defined as follows:

```python
class Node: 
    #constructor will only take in a value
    def __init__(self,value):
        self.value = value
        #collection of children, the root node needs at least one for every letter in the alphabet so it has to be a collection
        #I will use a dictionary to find the next letter quickly.
        self.children = {}
```

The comments speak for themselves, but all the node constructor does is store a value and a dictionary of refrence to the next child node in the form {value : Node}. Next, the Trie is implemented as follows: 

```python
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
                #if its not there then add the letter to the Trie.
                currNode.children[char] = Node(char)
                # print(str(currNode.children))
                #then iterate through the node we just made
                currNode = currNode.children[char]
            else:
                #Otherwise, move onto the next node in the sequence
                currNode = currNode.children[char]  

    def findWord(self,word):
        #follows the same structure as before
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
                #move to the enxt node
                currNode = currNode.children[char]
        #now check if this is the last letter in the word buy checking the letter at -1 indicey 
        if currNode.value == letters[-1]:
            return True
        else:
            print("how did you get here") # The program should never get here but put a print for debugging
            return False       
```

A trie is initalized with a empty trie consisting of the root node that contains a None data. Then the two methods, addWord(word): and findWord(word): operations will manipulate and return the information that we request. These work essentially the same by iterating through the tree by accessing subsequent "edges" between nodes that connect each word.

## Libraries Used 

Webcrawler.py:

I used several libraries in my implementation of the search engine. In WebCrawler.py I used 4 libraries; os, re, bs4 and requests. I used os to manipulate directory and files. I used re for using regex expressions to work with strings. I used bs4 to parse HTML files, I also installed lxml for bs4 which is a more efficent html parser and can parse more text than the built in html parser that bs4 ships with. Finally, I used requests to make web requests to get html via GET requests. 

SearchEngine.py:
* I used ast, to simplify parsing a dictionary structure from the str() representation that is stored in the file.
* I used pyfiglet to draw ascii art for my user facing interactions
* I used re for regex expressions the same as in WebCrawler.py
* I used bs4 to parse specific parts of html files stored in the directory
* I used os to manipulate those direcories and files from bs4
* I used summa to parse keywords from chunks of text, this libraries advantages are pre-trained on stopwords and other non keywords in english and its efficency of doing the parsing.
* Finally, I used sys and the following edits to prevent encoding errors: 
  sys.stdin.reconfigure(encoding='utf-8') &
  sys.stdout.reconfigure(encoding='utf-8')


## Sample Input
Find the sample input under the "IndexedWebsiteStorage folder in my code submission. This will include urls as can be seen in webcrawler.py and the html files. 
Other input is just in the form of the character 'y' or 'n' that the program makes sure that you have all the files you want to search through. For development and testing 
I chose 6 cybersecurity articles to search through.
The next part of the input is in the form of keywords. The program asks that the keywords are seperated by keywords.
## Sample output
The following is a sample output of my search engine implementation
```
Webpages Indexed: 6
:'######::'########::::'###::::'########:::'######::'##::::'##:
'##... ##: ##.....::::'## ##::: ##.... ##:'##... ##: ##:::: ##:
 ##:::..:: ##::::::::'##:. ##:: ##:::: ##: ##:::..:: ##:::: ##:
. ######:: ######:::'##:::. ##: ########:: ##::::::: #########:
:..... ##: ##...:::: #########: ##.. ##::: ##::::::: ##.... ##:
'##::: ##: ##::::::: ##.... ##: ##::. ##:: ##::: ##: ##:::: ##:
. ######:: ########: ##:::: ##: ##:::. ##:. ######:: ##:::: ##:
:......:::........::..:::::..::..:::::..:::......:::..:::::..::
'########:'##::: ##::'######:::'####:'##::: ##:'########:
 ##.....:: ###:: ##:'##... ##::. ##:: ###:: ##: ##.....::
 ##::::::: ####: ##: ##:::..:::: ##:: ####: ##: ##:::::::
 ######::: ## ## ##: ##::'####:: ##:: ## ## ##: ######:::
 ##...:::: ##. ####: ##::: ##::: ##:: ##. ####: ##...::::
 ##::::::: ##:. ###: ##::: ##::: ##:: ##:. ###: ##:::::::
 ########: ##::. ##:. ######:::'####: ##::. ##: ########:
........::..::::..:::......::::....::..::::..::........::

Search Engine by Matthew Jacobson
---------------------------------
Please enter search terms seperated by a space
cloud

Results: -------------------------------
1: Modern CISO More Than a Security Officer, had the search term appear 5 times
2: Statement Government of Canada welcomes Auditor General s Report on Cybersecurity of Personal Information in the Cloud, had the search term appear 3 times
3: How Routine Pen Testing Can Reveal the Unseen Flaws in Your Cybersecurity Posture, had the search term appear 1 times
```

## Video Demonstration 
Find the Video Demo in my submission .zip archive
## List of websites used for my demo
[ 'https://www.washingtonpost.com/politics/2022/11/15/two-enormous-cyberattacks-convince-australia-hack-hackers/', 'https://thehill.com/policy/cybersecurity/3737050-mayorkas-ties-with-private-sector-foreign-partners-increasingly-vital-as-cyber-threats-rise/', 'https://finance.yahoo.com/news/statement-government-canada-welcomes-auditor-181900119.html', 'https://news.usni.org/2022/11/15/gao-report-on-pentagon-cybersecurity-incidents', 'https://www.darkreading.com/edge-ask-the-experts/modern-ciso-more-than-a-security-officer', 'https://www.darkreading.com/vulnerabilities-threats/how-routine-pen-testing-can-reveal-the-unseen-flaws-in-your-cybersecurity-posture' , 'https://thehill.com/policy/cybersecurity/3737251-fbi-head-china-has-stolen-more-us-data-than-every-other-nation-combined/' , 'https://cyware.com/cyber-security-news-articles' , 'https://www.securityweek.com/zendesk-vulnerability-could-have-given-hackers-access-customer-data']

