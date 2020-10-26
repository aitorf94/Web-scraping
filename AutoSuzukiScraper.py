# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 21:41:16 2020
@author: aitor
Version: 23/10/2020
"""
@@ -1,8 +1,8 @@
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 21:41:16 2020
@author: aitor
Version: 23/10/2020
@author: aitor,alonso
Version: 26/10/2020
"""
# Afegim llibreries a utilitzar
import os
@@ -71,27 +71,28 @@ def scrape(self):

            if self.__robots_analisi_(self.url) == True:

                # Descarregem HTML de pagina web
                # Descarreguem l'HTML de la pàgina web (url+subdomini)
                html = self.__descarrega(self.url+self.subdomain)
                soup = BeautifulSoup(html, 'html.parser')
                #soup = BeautifulSoup(html, 'lxml')
                print ("Extraient data")
                # Extraiem enllaços per a cada model
                tables = soup.find_all("table")
                #models = self.models_enllaços(links)
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

                print ("---------------------------------")
                print("DATA; MODEL; ACABAT; PREU")
                print ("---------------------------------")
                v_csv = []
                #print ("---------------------------------")
                #print("DATA; MODEL; ACABAT; PREU")
                # Afegim la capçalera a la llista
                v_csv.append(["DATA","MODEL","ACABAT","PREU"])
                #print ("---------------------------------")
                #inici de la lectura de les taules
                for table in tables:
                        if "tableDATA" in table["class"]:
@@ -100,23 +101,38 @@ def scrape(self):
                                       num_cols = 0
                                       for column in columns:
                                                num_cols +=1
                                                # Càrrega del preu
                                                if num_cols == 3:
                                                        v_preu = (column.contents[0]).strip()
                                                        #print (column.contents[0])
                                                        print (v_data+"; "+v_model+"; "+v_acabat+"; "+v_preu)
                                                        print ("---------------------------------") 
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

                                #for tabletd in table.td:
                                #       print (table.td.get_text())
                                #print (table.td.get_text())
                                #print ("------------------")                    
                                #print("\n")
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

