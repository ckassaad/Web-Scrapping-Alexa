# -*- coding: utf-8 -*-
"""
Titre: Web Scrapping
Auteur: Karim ASSAAD
Date: 17/04/2017
Commentaire: Ce fichier contient des fonctions et des classe qui facilite le web scrapping des sites Alexa et MyWot
Language: Python2.7
"""
#import needed Libraries
from __future__ import division
import pandas as pd
import re 
from collections import OrderedDict
from bs4 import BeautifulSoup
import urllib
import json
import time



######################################################################
#start of class ScrapingAlexa
######################################################################
#input: The name of the website that we want to find its traffic, statistics, and analytics
class ScrapingAlexa:
    def __init__(self,url):
        #defining the url of Alexa
        self.thirdParty='http://www.alexa.com/siteinfo/'
        #adding the website that we're interested to Alexa url
        self.url=url
        #Loading Alexa (website information) page (where we find all the information needed about the website we're interested in)        
        html=urllib.urlopen(self.thirdParty+ self.url).read()    
        #using the library beautifulsoup to structure the html
        self.soup = BeautifulSoup(html, "lxml")    

    #Method that retreive the rank of the website in the world, in its country of origin and the name of that country
    #Output: list 
    def get_ranks(self):
        L=list()
        #global rank
        try :
            rank=self.soup.find_all("strong", attrs={'class':'metrics-data align-vmiddle'})[0].text
            if(re.sub("[^0-9,^0-9]", "", rank).replace(',','')==''):
                L.append(None)
            else:
                L.append(re.sub("[^0-9,^0-9]", "", rank).replace(',',''))
        except: L.append(None)
        #Country name
        try :L.append(self.soup.find('a', attrs={'href':re.compile('/topsites/countries/')}).text)
        except: L.append(None)
        #Country rank
        try:
            rank=self.soup.find_all("strong", attrs={'class':'metrics-data align-vmiddle'})[1].text            
            if(re.sub("[^0-9.,^0-9]", "", rank).replace(',','')==''):
                L.append(None)
            else:
                L.append(re.sub("[^0-9.,^0-9]", "", rank).replace(',',''))
        except: L.append(None)
        return L

    #Method that gets the the bounce rate of the website
    #output: numeric(type string)
    def get_bounceRate(self):
        try: 
            b=re.sub("[^0-9.,^0-9]", "",self.soup.find_all("strong", attrs={'class':'metrics-data align-vmiddle'})[2].text)
            if(b==''):
                b=None
        except: b=None
        return b
        
    #Method that gets the key words of the website and the percent of search traffic
    #output: list of two lists
    def get_keywords(self):
        L1=''
        L2=''
        try:
            t=self.soup.find("table", id='keywords_top_keywords_table')
            names=t.find_all('td',attrs={'class':"topkeywordellipsis"})
            percent=t.find_all('td',attrs={'class':"text-right"})
            for i in range(len(names)):
                  L1=L1+','+names[i].find_all('span')[1].text
                  L2=L2+','+percent[i].find_all('span')[0].text
            if(L2==''): 
                L2=''
            if(L1==''): 
                L1=''
            return L1[1:], L2[1:]                  
        except:
            return ['','']
    
    #Method that gets the top 5 websites that people visit immediately before this website
    #output: list
    def upstream_sites(self):
        L=''
        try:
            t=self.soup.find('table',id="keywords_upstream_site_table").find_all('td')
            for i in range(len(t)):
                if(t[i].find('a')!=None):
                    L=L+','+t[i].find('a').text
        except: L=''  
        return L[1:]

    def totalSitesLinking(self):
        try:
            d=self.soup.find_all('div')
            for i in range(len(d)):         
                if('Total Sites Linking In' in str(d[i])):
                    j=i
                    j=re.sub("[^0-9^0-9%]", "",d[j].find('span').text)
            return float(j)
        except: return None    

    #Method that get the top 5 sites linking in to this website and the total number of sites linking in to this website
    #output: list
    def sitesLinking(self):
        L=''
        try:
            #s=self.soup.find_all('span', attrs={'class':'word-wrap'}, text=True)
            t=self.soup.find('table',id="linksin_table").find_all('td', attrs={'class':''})
            for i in range(len(t)):         
                L=L+','+t[i].find('a').text
            if(L==''):
                L=''
        except: L=''
        return L[1:]
    
    #Method that get the top 5 similar sites by Audience Overlap
    #output: list
    def sitesRelated(self):
        L=list()
        try:
            t=self.soup.find('table',id="audience_overlap_table").find_all('td')
            for i in range(len(t)):
                L.append(t[i].find('a').text)
        except: L=None  
        return L

    #Method that get the top 5 sites with similar names
    #output: list    
    def sitesSimilar(self):
        L=''
        try:
            t=self.soup.find('table',id="similar_link_table").find_all('td')
            for i in range(len(t)):
                L=L+','+t[i].find('a').text
        except: L=''  
        return L[1:]
        
    #Method that get the Categories with Related Sites
    #output: list
    def categories(self):
        L=list()
        try:
            s=self.soup.find_all('a', attrs={'href':re.compile('/topsites/category')})
            for i in range(len(s)):
                temp=''.join(s[i].text).encode('utf-8')
                L.append(temp.replace('\xc3\xa7', 'c').replace('\xc3\xa9', 'e').replace('\xc3\xa0', 'a').replace('\xc3\xb1','gn'))
                        
            L=OrderedDict.fromkeys(L).keys()
            if(L==[]):
                L=None
        except: L=None
        return L
    
    
    #Method that get Audience Demographics informations of this website
    #output: disctionnary
    def audienceDemographics(self):
        try:
            d=self.soup.find('div', id='demographics-content').find_all('span',attrs={'class':'pybar-bg'})
            c=self.soup.find('div', id='demographics-content').find_all('span',attrs={'class':'container'})
            L=list()
            Conf=list()
            for i in xrange(0,len(d),2):
                try:
                    d0=d[i].find('span').get('style')
                    d1=d[i+1].find('span').get('style')
                    dTemp=float(re.sub("[^0-9.^0-9]", "",d0))+float(re.sub("[^0-9.^0-9]", "",d1))-100
                    cTemp=c[int(i/2)].text.split('Confidence: ')[1].split('\n')[0]
                    L.append(dTemp)
                    Conf.append(cTemp)
                except:
                    L.append(None)
                    Conf.append(None)
        except: 
            L=[None,None, None, None, None, None, None, None, None]
            Conf=[None,None, None, None, None, None, None, None, None]
        D=OrderedDict()
        N=['male','Femele', 'NoCollege', 'SomeCollege', 'GraduateSchool', 'College', 'Home', 'School', 'Work']
        for i,key in enumerate(N):
            try:
                D[key]=[L[i],Conf[i]]
            except:
                D[key]=[None,None]
        return D

######################################################################
#end of class
######################################################################


######################################################################
#start of class ApiAlexa
######################################################################
#this is a similar class to ScrapingAlexa but it uses an api rather than webscrapping. (It's much faster but it does not provide all the information unless we paye for Alexa service)
#input: The name of the website that we want to find its traffic, statistics, and analytics using Alexa Api
class ApiAlexa:
    def __init__(self,url):
        #and url for accessing te Api of Alexa and demanding the information of the website
        url="http://data.alexa.com/data?cli=10&dat=s&url="+  url
        #the result of the api in a html format
        html=urllib.urlopen(url).read()
        #using beautiful soup to structure the html
        self.soup = BeautifulSoup(html, "xml")
    
    #Method that retreive the rank of the website in the world, in its country of origin and the name of that country
    #Output: list 
    def get_ranks(self):
        #url="http://data.alexa.com/data?cli=10&dat=s&url="+ urllib.urlencode({'sensor':'false', 'address': url})
        L=[]
        try :
            L.append(self.soup.find("REACH")['RANK'])
            L.append(self.soup.find("COUNTRY")['NAME'])
            L.append(self.soup.find("COUNTRY")['RANK'])
        except:
            L=[None,None, None]
        return L


######################################################################
#end of class
######################################################################


######################################################################
#start of class ScrapingWot
######################################################################
#input: The name of the website that we want to find its degree of safety
class ApiWot:    
    def __init__(self, url):
        #the 
        thirdParty='http://api.mywot.com/0.4/public_link_json2?hosts='
        #the key used to webscrap
        key='/&callback=process&key=6840647a713d3e6e2d10f54345db300a7232c80f'
        #adding the url to the object
        self.url=url
        #Loading the reulst of MyWot Api in a json format        
        self.html=urllib.urlopen(thirdParty+ url +key).read()

    #Method that gets the TrustWorthiness of this website and its Confidence in addition to the ChildSafety of this website and its Confidence
    #Output: dictionnary        
    def trust_safety(self):
        try: 
            D=dict()
            js=json.loads(str(self.html[8:(len(self.html)-1)]))
#            json.dumps(js,indent=4)
            try:
                D['TrustWorthiness']=js[self.url]['2']
                D['TrustWorthiness'][1]=float(D['TrustWorthiness'][1])/50
            except:
                D['TrustWorthiness']=[None, None]
            try:
                D['ChildSafety']=js[self.url]['4']
                D['ChildSafety'][1]=float(D['ChildSafety'][1])/50
            except:
                D['ChildSafety']=[None, None]
        except:
            D['TrustWorthiness']=[None, None]
            D['ChildSafety']=[None, None]
        return D    
    

######################################################################
#end of class
######################################################################



######################################################################
#start of function get_data
######################################################################
#Retrieve the scrapped data and structure it in dataframe format 
#input: vect=list of websites to be scrapped
#       t_s= time to sleep befre rescrapping
#       w_s=number of site to scrap before sleeping
#output:
def get_data_web(vect,t_s=10,w_s=100):
    columns_name=['rank', 'country', 'rank_country', 'keywords','keywords_percent', 'get_bounceRate', 
             'totalSitesLinking', 'sitesLinking', 'upstream_sites', 'sitesRelated', 'sitesSimilar',
             'categories','male','male_confidence','female','female_confidence',
             'noCollege','noCollege_confidence','someCollege','someCollege_confidence',
             'graduateSchool','graduateSchool_confidence','college','college_confidence',
             'home','home_confidence','school','school_confidence','work','work_confidence',
             'childSafety','childSafety_confidence','trustWorthiness','trustWorthiness_confidence']
    
    data_web=pd.DataFrame(columns=columns_name)
    duration=0
    lim=len(str(len(vect)))
    for i,url in enumerate(vect):
        if((i%w_s==0) & (i!=0)):
            start=time.time()
            print '=> Going to sleep for '+str(t_s)+' s ...'
            time.sleep(t_s)
            stop=time.time()
            duration=duration+stop-start
            print '=> Waking up '+' || '+str(round(stop- start,3)).ljust(5)+' || '+str(round(duration,3))
        
        start=time.time()
        a=ScrapingAlexa(url)
        L=a.get_ranks()
        L.append(a.get_keywords()[0])
        L.append(a.get_keywords()[1])
        L.append(a.get_bounceRate())
        L.append(a.totalSitesLinking())
        L.append(a.sitesLinking())
        L.append(a.upstream_sites())
        L.append(a.sitesRelated())
        L.append(a.sitesSimilar())
        L.append(a.categories())
        D=a.audienceDemographics()
        L.append(D['male'][0])
        L.append(D['male'][1])
        L.append(D['Femele'][0])
        L.append(D['Femele'][1])
        L.append(D['NoCollege'][0])
        L.append(D['NoCollege'][1])
        L.append(D['SomeCollege'][0])
        L.append(D['SomeCollege'][1])
        L.append(D['GraduateSchool'][0])
        L.append(D['GraduateSchool'][1])
        L.append(D['College'][0])
        L.append(D['College'][1])
        L.append(D['Home'][0])
        L.append(D['Home'][1])
        L.append(D['School'][0])
        L.append(D['School'][1])
        L.append(D['Work'][0])
        L.append(D['Work'][1])
        
        w=ApiWot(url)
        D=w.trust_safety()
        L.append(D['ChildSafety'][0])
        L.append(D['ChildSafety'][1])
        L.append(D['TrustWorthiness'][0])
        L.append(D['TrustWorthiness'][1])
        data_web.loc[i]=L
        stop=time.time()
        duration=duration+stop-start
        round(0.005, 2)
        print '=> '+str(i).ljust(lim)+' || '+str(round(stop- start,3)).ljust(5)+' || '+str(round(duration,3))
    return data_web



######################################################################
#end of function
######################################################################
