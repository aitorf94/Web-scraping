# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 22:14:07 2020

@author: aitor,alonso
"""

from AutoSuzukiScraper import AutoSuzukiScraper

# Sembla que utilitzant urllib el certificat de https://auto.suzuki.es no es troba
# Les seguents dos linies ens deixen descarregar el HTMl encara que urllib no trobe el certificat
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


scraper = AutoSuzukiScraper();
scraper.scrape();