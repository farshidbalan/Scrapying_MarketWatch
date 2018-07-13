
#----------------------------------------------
#client = MongoClient('localhost', 27017)

#mydb = client.testDatabas1

#myCollection = mydb.testDatabas1

fileName = 'cleaned file.txt'
with open(fileName, 'r+') as f:
    links = f.read().split('\n')
subLinks = links[0:50]

test_text = {}

headlineCounter = 0  # counts the nimber of links that include news text
titleCounter = 0    # counts the number of links that encompasses only title
oponionCounter = 0  # counts the number of links that include oponions and not news articles 

baseURL = 'http://www.marketwatch.com'
for url in subLinks:
    print('='*180)
    print(url)
    textPage = urllib2.urlopen(url)
    soup = BeautifulSoup(textPage,"lxml")
       
    isTitle = soup.find('h1',attrs={'id':'article-headline'}).string  
    dateTime = soup.find('p', attrs={'id':'published-timestamp', 'class':'timestamp'}).get_text()
    isRelatedArticles = soup.find('div',attrs={'class':'module','id':'related-articles'})

    if isTitle:
        if len(isTitle) == 1:
            title = ''.join([i for i in url if not i.isdigit()]).\
                    replace('http://www.marketwatch.com/story/','').replace('-',' ')
            print('The title is: \n {}'.format(title))
            print(dateTime)
            body = ''
            print(body)
            findLinks = isRelatedArticles.findAll('a',\
                        attrs = {'data-track-click':'MW_Article_More from MarketWatch'})
            otherLink = [baseURL + currentLink['href'] for currentLink in findLinks]
            print(otherLink)
            titleCounter += 1
            
        else:
            headline = soup.find('h1',attrs={'id':'article-headline'}).string.encode('utf-8')
            print('The headline is: \n{}'.format(headline))
            print(dateTime)
            body = soup.find('div',attrs = {'id':'article-body'}).\
                  get_text(strip=True, separator='  ')
            print(body)
            findLinks = soup.find('div',attrs = {'id':'article-body'}) .find_all('a', href=True)  
            otherLink = [baseURL + currentLink['href'] for currentLink in findLinks]
            print(otherLink)  
            headlineCounter += 1
    else:
        oponion = soup.find('span',attrs={'class':'article-template opinion'})
        print('The oponion is \n {}'.format(oponion.next_sibling.encode('utf-8')))
        print(dateTime)
        body = soup.find('div',attrs = {'id':'article-body'}).\
                  get_text(strip=True, separator='  ')
        print(body)
        findLinks = soup.find('div',attrs = {'id':'article-body'}) .find_all('a', href=True)  
        otherLink = [baseURL + currentLink['href'] for currentLink in findLinks]
        print(otherLink)  
        oponionCounter += 1
        
    
print('there are {} headlines, {} titles without text and {} links as oponions'\
         .format(headlineCounter, titleCounter, oponionCounter))
    
def extract_names(text):
    # Change the path according to your system
    stanford_classifier = 'C:\Farshid\programming\Java\stanford-ner-2016-10-31\classifiers\english.all.3class.distsim.crf.ser.gz'
    stanford_ner_path = 'C:\Farshid\programming\Java\stanford-ner-2016-10-31\stanford-ner.jar'

    # Creating Tagger Object
    st = StanfordNERTagger(stanford_classifier, stanford_ner_path, encoding='utf-8')
    
    tokenizedText = word_tokenize(text)
    classifiedText = st.tag(tokenizedText)
    
    person_names = [" ".join(x[0] for x in names) 
          for typ, names in groupby(classifiedText, key=lambda x: x[1]) 
          if typ == "PERSON"]
    organization_names = [" ".join(x[0] for x in names) 
          for typ, names in groupby(classifiedText, key=lambda x: x[1]) 
          if typ == "ORGANIZATION"]
    locatoin_names = [" ".join(x[0] for x in names) 
          for typ, names in groupby(classifiedText, key=lambda x: x[1]) 
          if typ == "LOCATION"]
    print(person_names)
    print(organization_names)
    print(locatoin_names)    

