import os
import nltk
import sys
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.tag import StanfordNERTagger
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from itertools import groupby  # for attaching names with similar entities



def text_tokinization(text):    
    # Change the path according to your system
    stanford_classifier = 'C:\Farshid\programming\Java\stanford-ner-2016-10-31\classifiers\english.all.3class.distsim.crf.ser.gz'
    stanford_ner_path = 'C:\Farshid\programming\Java\stanford-ner-2016-10-31\stanford-ner.jar'

    # Creating Tagger Object
    st = StanfordNERTagger(stanford_classifier, stanford_ner_path, encoding='utf-8')
    
    tokenizedText = word_tokenize(text)
    classifiedText = st.tag(tokenizedText)
    
    return(classifiedText)
#=========================================================================
# extracting names of PERSON, LOCATION and ORGANIZATION from the text 
def extract_names(classifiedText):
    person_names = [" ".join(x[0] for x in names) 
          for typ, names in groupby(classifiedText, key=lambda x: x[1]) 
          if typ == "PERSON"]
    
    organization_names = [" ".join(x[0] for x in names) 
          for typ, names in groupby(classifiedText, key=lambda x: x[1]) 
          if typ == "ORGANIZATION"]
    
    locatoin_names = [" ".join(x[0] for x in names) 
          for typ, names in groupby(classifiedText, key=lambda x: x[1]) 
          if typ == "LOCATION"]
    
    name_dict = {'names':{"PERSON":person_names, "ORGANIZATION": organization_names, "LOCATION":locatoin_names}}

    return(name_dict)
#===========================================================================
#counting items frequency in each name group
def extract_name_frequency(name_dict):
    count_person = dict((i, name_dict['names']['PERSON'].count(i))
                        for i in name_dict['names']['PERSON'])
    
    count_location = dict((i, name_dict['names']['LOCATION'].count(i)) 
                          for i in name_dict['names']['LOCATION'])
    
    count_organization = dict((i, name_dict['names']['ORGANIZATION'].count(i))
                              for i in name_dict['names']['ORGANIZATION'])
    
    name_count = {'count': {'count_person':count_person, 'count_location':count_location,
                            'count_organization': count_organization}}
    
    return(name_count)


def extract_information(text):
    
    classified_text =  text_tokinization(text)
    name_dict =  extract_names(classified_text)
    extract_name_frequency(name_dict)
    DICTIONARY = []
    DICTIONARY.append(name_dict)
    DICTIONARY.append(name_count)
    
    print(DICTIONARY)