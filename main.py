# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 22:14:07 2020

@author: aitor
"""

from AutoSuzukiScraper import AutoSuzukiScraper
#import importlib
#importlib.reload(AutoSuzukiScraper)
#output_file = "dataset.csv"
# Sembla que utilitzant urllib el certifict de https://auto.suzuki.es no es troba
# Les seguesnt dos linies ens deixen fer un workaround 
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Tambe podriem modificar el codi i utlitzar requests.get en compte de urllib

scraper = AutoSuzukiScraper();
scraper.scrape();
