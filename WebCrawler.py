#Author - Matthew Jacobson
#CS 600A Search Engine Project
"""
Input: URL's of websites to be parsed
Output: HTML files that can be paresed by the search engine

"""
#import os
import os
#import regex for washing strings of specific characters
import re
# import the web crawling library
from bs4 import BeautifulSoup
# need to be able to make HTTPS requests to parse web page info from links
# BS4 does not do this natively
import requests
#from Todd @ https://hackersandslackers.com/scraping-urls-with-beautifulsoup/. Websites can have defences against
# to prevent webscraping, a simple way to get around this is to impersonate a browser by crafting our HTTP
# request packets. With the following code we can craft our own header.
# these are generic parameters to fool basic website security.

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

#make soup from given links
webpages = ['https://www.techrepublic.com/article/top-cybersecurity-threats/',
             'https://www.washingtonpost.com/politics/2022/11/15/two-enormous-cyberattacks-convince-australia-hack-hackers/',
             'https://thehill.com/policy/cybersecurity/3737050-mayorkas-ties-with-private-sector-foreign-partners-increasingly-vital-as-cyber-threats-rise/',
            'https://finance.yahoo.com/news/statement-government-canada-welcomes-auditor-181900119.html',
             'https://news.usni.org/2022/11/15/gao-report-on-pentagon-cybersecurity-incidents',
            'https://www.darkreading.com/edge-ask-the-experts/modern-ciso-more-than-a-security-officer',
            'https://www.darkreading.com/vulnerabilities-threats/how-routine-pen-testing-can-reveal-the-unseen-flaws-in-your-cybersecurity-posture',
            'https://thehill.com/policy/cybersecurity/3737251-fbi-head-china-has-stolen-more-us-data-than-every-other-nation-combined/',
            'https://cyware.com/cyber-security-news-articles',
            'https://www.securityweek.com/zendesk-vulnerability-could-have-given-hackers-access-customer-data']

#For the given webpages
urlCount = 0 

for webpage in webpages:
    cwd = os.getcwd()
    #Make Request
    r = requests.get(webpage)
    #now make 'soup' from the www Request
    soup = BeautifulSoup(r.text, 'lxml')
    #Grab information for storing website information
    #Grab title for 
    webTitle = str(soup.title)
    webContents = soup.prettify()
    if webTitle == 'None':
        # If there is no explict title, another alternative must be found 
        # The alternative will be the url if no title is found
        fileName = re.sub(r'[^\w]', ' ', webpages[urlCount]).replace(' ','_') +'.html'
        os.chdir("IndexedWebsiteStorage")
        with open(fileName, 'w', encoding='utf-8') as file:
            file.write(webContents) # put html in file
            file.write('\n----\n') # unique seperator
            for link in soup.find_all('a'): # all of the links on a page 
                if link == None:
                    file.write("None")
                else:
                    file.write(link.get('href'))
            # file.close()
        #lazy work around for tracking url position
        urlCount+=1
        os.chdir(cwd)
    else:
        fileName = re.sub(r'[^\w]', ' ', str(webTitle[7:webTitle.index('</title>')].replace(" ","_"))) + '.html'
        # print(fileName)
        # #Otherwise, the title gives us a good Name of the webpage indexed but for the sake of simplicity we will narrow it down to the first 4 words. 
        # #If the file already exists, the operation fails using the 'X' parameter
        os.chdir("IndexedWebsiteStorage")
        with open(fileName, 'w', encoding='utf-8') as file:
        #     #if it can be opened then write to the file
            file.write(webContents) # put html in file
            file.write('\n----\n') # unique seperator
            for link in soup.find_all('a'): # all of the links on a page 
                if link == None:
                    file.write("None")
                else:
                    file.write(link.get('href'))
            # file.close()
        #     #f.close is not required using the "with .. as .." structure 
        #lazy work around for tracking url position
        urlCount+=1
        os.chdir(cwd)
                       
            
            
            
        

    
    

        



