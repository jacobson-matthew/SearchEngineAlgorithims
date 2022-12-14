#Author - Matthew Jacobson
#CS 600A Search Engine Project

# import the web crawling library
from bs4 import BeautifulSoup
# need to be able to make HTTPS requests to parse web page info from links
# BS4 does not do this natively
import requests

#from Todd @ https://hackersandslackers.com/scraping-urls-with-beautifulsoup/. Websites can have defences
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


# initalize list to store webpage data to be pre-processed
textStorage = []

for webpage in webpages:
    r = requests.get(webpage)
    soup = BeautifulSoup(r.text, 'lxml')
    temp = []
    for x in soup.find_all('p'):
        temp.append(x.text)
    textStorage.append(temp)

for x in textStorage:
    for y in x:
        print(y)



