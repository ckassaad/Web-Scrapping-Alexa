#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Éditeur de Spyder
Titre: recuperer les donnees web scrapper a traver la library web_scrapping
Auteur: Karim ASSAAD
Date: 15/05/2017
Commentaire: 
Language: Python2.7
"""    

import pandas as pd


import web_scrapping as ca

if __name__=="__main__":

    columns_name=['rank', 'country', 'rank_country', 'keywords','keywords_percent', 'get_bounceRate', 
                 'totalSitesLinking', 'sitesLinking', 'upstream_sites', 'sitesRelated', 'sitesSimilar',
                 'categories','male','male_confidence','female','female_confidence',
                 'noCollege','noCollege_confidence','someCollege','someCollege_confidence',
                 'graduateSchool','graduateSchool_confidence','college','college_confidence',
                 'home','home_confidence','school','school_confidence','work','work_confidence',
                 'childSafety','childSafety_confidence','trustWorthiness','trustWorthiness_confidence']
    
    media_url=pd.read_csv('./url.csv', header=None)
    
    #Scrapping in batch automatically
    def batch(media_url):
        data_web=ca.get_data_web(media_url)
        temp=pd.DataFrame(media_url,columns=['url'])
        temp = temp.reset_index(drop=True)
        data_web=pd.concat([temp, data_web], axis=1)
        return data_web    

    data = batch(media_url[0])
    
    print data
