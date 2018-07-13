from bs4 import BeautifulSoup

import urllib2
import httplib
import time
import json

def extract_news(list_of_links):
    
    count_titles = 0
    count_body = 0
    count_oponion = 0
    count_excepts = {}
    
    list_of_news = []
    httplib.HTTPConnection._http_vsn = 10                  # for dealing with IncompleteRead Error
    httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'     # for dealing with IncompleteRead Error along with the previous line 
    baseURL = 'http://www.marketwatch.com'

    store_news = open("news.jsl", "a+")
    store_urls = open("urls.txt", "a+")
    with open('urls.txt', 'r') as fp:
        crawled_urls = fp.read().split('\n')

    for url in list_of_links:
        if url in crawled_urls:
            continue

        Dictionary = {}
        # time.sleep(3)
        try:
            req = urllib2.Request(url)         
            textPage = urllib2.urlopen(req)
        except Exception as e:
            count_excepts.setdefault(e, 0)
            count_excepts[e] += 1

            print(e, url)
            time.sleep(30) ##Just needs more time.      
            continue
            
        soup = BeautifulSoup(textPage,"lxml")
        if soup.find('h1',attrs={'id':'article-headline'}):
            isTitle =  soup.find('h1',attrs={'id':'article-headline'}).string
        else: continue
        if soup.find('p', attrs={'id':'published-timestamp', 'class':'timestamp'}):    
            dateTime = soup.find('p', attrs={'id':'published-timestamp', 'class':'timestamp'}).get_text()
        else: continue    
        otherLink = ''
        if isTitle:
            if len(isTitle) == 1: 
                # there is no news story and we can extract onle the title    
                headline = ''.join([i for i in url if not i.isdigit()]).\
                        replace('http://www.marketwatch.com/story/','').replace('-',' ')
                body = ''
                #titleCounter += 1
                count_titles += 1
            else:  
                # there is  text body and we extract headline and the body      
                headline = soup.find('h1',attrs={'id':'article-headline'}).string.encode('utf-8')
                body = soup.find('div',attrs = {'id':'article-body'}).\
                      get_text(strip=True, separator='  ')
                findLinks = soup.find('div',attrs = {'id':'article-body'}) .find_all('a', href=True)  
                otherLink = [baseURL + currentLink['href'] for currentLink in findLinks]
                count_body += 1              
        else:
            # it's oponion and the HTML is different from common news
            headline = soup.find('span',attrs={'class':'article-template opinion'}).\
                        next_sibling.encode('utf-8')
            body = soup.find('div',attrs = {'id':'article-body'}).\
                      get_text(strip=True, separator='  ')
            findLinks = soup.find('div',attrs = {'id':'article-body'}) .find_all('a', href=True)  
            otherLink = [baseURL + currentLink['href'] for currentLink in findLinks]
            count_oponion += 1
            
        headline = headline.strip()
        news = {'url':url ,'headline':headline,'dateTime': dateTime,'body':body,'otherLinks':otherLink}
        print(dateTime, headline, url)

        store_news.write(json.dumps(news) + '\n')
        store_news.flush()

        store_urls.write(url+'\n')
        store_urls.flush()
        
    print("There are {0} links which are only titles \n"
          "There are {1} links which are news stories \n"
          "There are {2} links which are oponions"
          .format(count_titles, count_body, count_oponion) )
    for e, tot in count_excepts.items():
        print("There are {} links with {}".format(tot, e))
    store_news.close()
    store_urls.close()

# To test the code if it works properly
fileName = 'cleaned file.txt'
with open(fileName, 'r+') as f:
    links = f.read().split('\n')
subLinks = links[18260:]
#subLinks = links[0:10]

extract_news(subLinks)
