from __future__ import print_function

import random
import time       # for adding sleeping time
import requests    #sending requests
import json
import datetime
import re        # librarz for regular expressions 
import pytz
import sys       #redirecting links to a file
import os        #define the current working directory
from bs4 import BeautifulSoup   # working with HTML file
from pytz import timezone  # working with timezones 

def main():
    os.chdir("C:\\Farshid\\Heidelberg\\third semester\\practical 2\\textFile")  # defining the current directory
    symbol_list = ['APC', 'XEC', 'CXO', 'COP', 'DVN', 'EOG', 'EQT', 'MRO', 'NFX', 'NBL', 'OXY',
                 'OKE','PXD','RRC','SWN','WMB','CHK', 'CVX', 'XOM', 'HES', 'MUR', 'KMI', 'MPC', 
                  'PSX', 'SE', 'TSO', 'VLO']
    
    #symbol_list = ['XEC','TSO']
    for symbol in symbol_list:
        print('='*10)
        print('loading %s......\n' % symbol)
    
        unique_id, timestamp, title = load_params_from_html(symbol)
        # for debug
        # unique_id, timestamp, title = '765715675', '6:00 p.m. Nov. 03, 1997', 'testing'
        print('got unique_id=%r, from %r' % (unique_id, title))

        baseUrl = 'http://www.marketwatch.com/news/headline/getheadlines'
        parameters =  extract_first_parameters(unique_id, symbol, timestamp)
        parameters.update(extract_uid(unique_id))

        page_cnt = 0
        while True:
            page_cnt += 1
            resp = requests.get(baseUrl, params = parameters)
            if resp.status_code != 200:
                print("exception! status=%s, response:%s" % (resp.status_code, resp.text))
                break

            data = json.loads(resp.text) # array of size 10 
            print('\n--- page:%d' % page_cnt)
            print("got %d data, with args: " % (len(data)))
            print("%17s: %s" % ('messageNumber', parameters['messageNumber']))
            print("%17s: %s" % ('dateTime', parameters['dateTime']))
            print("%17s: %s" % ('sequence', parameters['sequence']))
            print("%17s: %s" % ('docId', parameters['docId']))

            # Section 1: Save links to file
            newsLink = []
            filename = symbol + '.txt'
            with open(filename, 'a') as fp:
                for item in data:
                    link = "http://www.marketwatch.com/story" +  item['SeoHeadlineFragment'] 
                    newsLink.append(link)
                if len(newsLink):
                    fp.write('\n'.join(newsLink) + '\n')
            # Section 2: print results, and extract parameters
            if len(data) > 1:
                first = data[0] # get first item of array
                last = data[-1] # get last item of array
                print("results:\n\tfirst: %-42s, %s" % (first['UniqueId'], first['HeadlineText']))
                print("\t last: %-42s, %s" % (last['UniqueId'], last['HeadlineText']))

                uid = last['UniqueId'] # get value of UniqueId from dict object `last`
                TimestampUtc = last['TimestampUtc'] # get the value of TimestampUtc
                offset = last['EasternTimeOffset']
                parameters.update(extract_uid(uid))
                parameters['dateTime'] = extract_link_timeStamp(TimestampUtc, offset)

            # raw_input("press <enter> to get next")
            time.sleep(random.randint(5, 9))

            # Section 3: check continuing condition
            if len(data) < 10:
                break
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# this function loads the first page and returns parameters for sending the next request
def load_params_from_html(symbol):
    html_url = 'http://www.marketwatch.com/investing/stock/' + symbol

    resp = requests.get(html_url)
    if resp.status_code != 200:
        raise Exception("http request failed: %s" % resp)
    soup = BeautifulSoup(resp.text, 'lxml')

    # get value of `data-uniqueid` from last news node of 'MarketWatch News on XOM'
    li_node = soup.select("#mwheadlines > div.headlinewrapper > ol > li[data-uniqueid]")[1]
    unique_id = li_node['data-uniqueid']
    timestamp = li_node.select('.timestamp')[0].text
    return unique_id, timestamp, li_node.text.replace('\n', ' ').strip()
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# A function that extracts required parameters for for sending requests
def extract_uid(uid):
    sequence = ''
    messageNumber = ''
    docId = ''
    if ':' in uid: # if the symbol ':' in string `uid`
        # uid looks like `e5a00f51-8821-4fbc-8ac6-e5f64b5eb0f2:8499`
        # so split it by ':'
        sequence, messageNumber = uid.split(':')
    else:
        docId = uid
        
    return {
        'sequence': sequence,
        'messageNumber': messageNumber,
        'docId': docId,
    }
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# extract the timestamp of the links with integer UniqieIds
def extract_link_timeStamp(TimestampUtc, offset):   
    pst = timezone('America/New_York')
    TimestampUtc = re.split('\(|\)', TimestampUtc)[1]
    TimestampUtc = int(TimestampUtc)/1000
    date = datetime.datetime.utcfromtimestamp(TimestampUtc)
    newDate = date + datetime.timedelta(hours=int(offset))
    dateTime =  newDate.strftime('%I:%M %p %b. %d, %Y').replace('AM', 'a.m.').replace('PM', 'p.m.').lstrip('0')
    return(dateTime)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# different symbols start with one of two differen 'data-uniqueid', 
# the following function returns the first uniqe_id of the news links to send a new request
def extract_first_parameters(first_uid, symbol, timestamp):
    parameters = {
     'ticker':symbol,
     'countryCode':'US',
     'docType':'806',
     'count':'10',
     'channelName': '/news/latest/company/us/' + symbol,
     'count':'10',
    'channelName': '/news/latest/company/us/xom',
    'dateTime': timestamp,
    }
    if ':' in first_uid:
        sequence, messageNumber = first_uid.split(':')
        parameters.update({
            'docId': '', # (Optional) initial value extract from HTML page
            'sequence':sequence, # initial value extract from HTML page
            'messageNumber':messageNumber, # initial value extract from HTML page
        })
    else:
        parameters.update({
            'docId': first_uid, # (Optional) initial value extract from HTML page
            'sequence' : '',
            'messageNumber' : ''  
            })
    return parameters   
        
if __name__ == '__main__':
    main()