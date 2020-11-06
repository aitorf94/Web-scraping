# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 21:41:16 2020
@author: aitor,alonso
Version: 05/11/2020
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
            self.subdomain = "/precios"
        
        def __robots_analisi_(self,url):
                rp= robotparser.RobotFileParser()
                rp.set_url(url + '/robots.txt')
                rp.read()
                user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/5\
            37.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
                return rp.can_fetch (user_agent,url)

    
        def __descarrega(self, url, num_intents=2):
            print (">>>>>------------------------------------------------------------------------------------------")
            print ('Descarregant:', url)
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
            print ("-----------------------------------------------------------------------------------------------")
            print ("Web Scrapping sobre dades dels differents models de cotxe Suzuki:" + self.url + self.subdomain ) 
            print ("Aquest process pot tardar fins X minuts .\n")
            
            # Executem timer 
            start_time = time.time()
           
            if self.__robots_analisi_(self.url) == True:
            
                # Descarreguem l'HTML de la pàgina web (url+subdomini)
                html = self.__descarrega(self.url+self.subdomain)
                soup = BeautifulSoup(html, 'html.parser')
                print ("Extraient data")
                # Extraiem enllaços per a cada model
                tables = soup.find_all("table")
                #print (">> TABLES 4-----------------")
                #print(tables)
                #print("\n")
                # Inicialitzem variables
                avui = datetime.now()
                v_data = avui.strftime("%d/%m/%Y")
                v_data_csv = avui.strftime("%Y%m%d")
                v_model = ""
                v_acabat = ""
                v_preu = ""
                v_csv = []
                #print ("---------------------------------")
                #print("DATA; MODEL; ACABAT; PREU")
                # Afegim la capçalera a la llista
                v_csv.append(["DATA","MODEL","ACABAT","PREU"])
                #print ("---------------------------------")
                #inici de la lectura de les taules
                for table in tables:
                        if "tableDATA" in table["class"]:
                                for row in table.find_all("tr"):
                                       columns = row.find_all("td")
                                       num_cols = 0
                                       for column in columns:
                                                num_cols +=1
                                                # Càrrega del preu
                                                if num_cols == 3:
                                                        #Treiem els blancs, i els punts per evitar problemes de decimals segons codificació
                                                        v_preu = ((column.contents[0]).strip()).replace('.', '')
                                                        #print (column.contents[0])
                                                        #print (v_data+"; "+v_model+"; "+v_acabat+"; "+v_preu)
                                                        #print ("---------------------------------")
                                                        # Afegim el model a la llista amb totes les dades
                                                        v_csv.append([v_data,v_model,v_acabat,v_preu])
                                                        break
                                                # Càrrega del model
                                                if num_cols == 1:
                                                        v_model = (column.get_text())
                                                # Càrrega de l'acabat
                                                if num_cols == 2:
                                                        v_acabat = (column.get_text())
                                                #print (column.get_text())

                #print (v_csv)
                # Carreguem les dades en el csv "models_autosuzuki_es_aaaammdd.csv"
                # Si ja existeix es sobreescriurà. Si no hi ha dades no el tractarem.
                if len(v_csv)<=1:
                        print(v_data+" - No hi ha models a carregar")
                else:
                        print(v_data+" - Nombre de models en la llista : "+str(len(v_csv)-1))
                        try:
                                with open("models_autosuzuki_es_"+v_data_csv+".csv", "w", newline="") as f:
                                        writer = csv.writer(f)
                                        writer.writerows(v_csv)
                                        print("   Desat correctament el fitxer models_autosuzuki_es_"+v_data_csv+".csv")
                        except IOError:
                                print("ATENCIÓ : NO PUC DESAR EL FITXER models_autosuzuki_es_"+v_data_csv+".csv")
                                print("          PROBABLEMENTE ESTIGUI OBERT EN UNA ALTRA APLICACIÓ.")
            else:
                print("Bloquejat per robots.txt",self.url)

                       