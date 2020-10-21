# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 21:41:16 2020

@author: aitor
"""
# Afegim llibreries a utilitzar
import os
import requests
import csv
import argparse
import urllib
import time
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
from urllib import robotparser

class AutoSuzukiScraper():
    
        def __init__(self):
            self.url = "https://auto.suzuki.es"
            #self.subdomain = "/database.htm"
        
        def __robots_analisi_(self,url):
                rp= robotparser.RobotFileParser()
                rp.set_url(url + '/robots.txt')
                rp.read()
                user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/5\
            37.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
                return rp.can_fetch (user_agent,url)

    
        def __descarrega(self, url, num_intents=2):
            print ('Descarrregant:', url)
            # Definim header 
            headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,\
            */*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "en-US,en;q=0.8",
            "Cache-Control": "no-cache",
            "dnt": "1",
            "Pragma": "no-cache",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/5\
            37.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
            }
            #request = urllib.request.Request(url, headers=headers)
            try:
                #html = urllib.request.urlopen(request).read()
                response = urllib.request.urlopen(url)
                html = response.read()
            except urllib.URLError as e:
                print ('Error en la descarrega:', e.reason)
                html = None
                if num_intents > 0:
                    if hasattr(e, 'code') and 500 <= e.code < 600:
                        # retry 5XX HTTP errors
                        return self.__descarrega(url, num_intents-1)
            return html
    
        def scrape(self):
            print ("Web Scrapping sobre dades dels differents models de cotxe Suzuki:" + self.url ) 
            print ("Aquest process pot tardar fins X minuts .\n")
            
            # Executem timer 
            start_time = time.time()
            
            if self.__robots_analisi_(self.url) == True:
            
                # Descarregem HTML de pagina web
                html = self.__descarrega(self.url)
                soup = BeautifulSoup(html, 'html.parser')
                print ("Extraguent data")
                # Extraiem enllaços per a cada model
                #models_enllaços = self.models_enllaços(html)
                
            else:
                print("Bloquejat per robots.txt",self.url)
