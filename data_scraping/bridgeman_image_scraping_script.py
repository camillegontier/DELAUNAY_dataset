# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 07:21:41 2021

@author: gontier
"""

import os
import xlwt
from bs4 import BeautifulSoup
from urllib.request import urlopen

queries = [
# "Frantisek%20Kupka",
"Jean%20Arp",
"Sophie%20Taeuber-Arp",
"Sonia%20Robert%20Delaunay",
"Naum%20Gabo",
"Laszlo%20Moholy-Nagy",
"Antoine%20Pevsner",
"Luigi%20Russolo",
"Jean%20Helion",
"Otto%20Freundlich",
"Georges%20Vantongerloo",
"Theo%20van%20Doesburg",
"Cesar%20Baldaccini",
"Cesar%20Domela",
"Jean%20Gorin",
"Josef%20Albers",
"Harry%20Holtzman",
"Charmion%20Von%20Wiegand",
"Leon%20Polk%20Smith",
"Auguste%20Herbin",
"Etienne%20Beothy",
"Alberto%20Magnelli", 
"Felix%20Del%20Marle",
"Ellsworth%20Kelly",
"Francois%20Morellet",
"Henry%20Lhotellier",
"Yves%20Klein",
"Piero%20Manzoni",
"Lucio%20Fontana",
"Victor%20Vasarely",
"Ad%20Reinhardt",
"Franz%20Kline",
"Mark%20Rothko",
"Vassily%20Kandinsky",
"Jean%20Fautrier",
"Jean%20Dubuffet",
"Emilio%20Vedova",
"Pierre%20Soulages", 
"Maria%20Helena%20Vieira%20da%20Silva",
"Hans%20Hartung",
"Jean%20Degottex",
"Georges%20Mathieu",
"Fernand%20Leger",
"Berto%20Lardera",
"Aurelie%20Nemours",
"Richard%20Paul%20Lohse",
"Olle%20Baertling",
"Max%20Bill",
"Alfred%20Manessier",
"Jean%20Bazaine",
"Charles%20Lapicque",
"Gustave%20Singier",
"Leon%20Gischia",
"Pierre%20Tal%20Coat",
"Roger%20Bissiere",
"Kenneth%20Noland",
"Morris%20Louis",
"Sam%20Francis",
"Joan%20Mitchell",
"Anthony%20Caro",
]

for query in queries:
    print(query)
    os.chdir(r"P:\research\Private_code\arts_dnn\dataset_bridgeman")
    # os.mkdir(query)
    os.chdir(query)
    search_url = "https://www.bridgemanimages.com/de/search?filter_text={q}&filter_group=all&filter_region=CHE&sort=most_popular&page=3"
    try:
        url = search_url.format(q=query)
        soup = BeautifulSoup(urlopen(url).read())
        links = soup.find_all('img')
        counter = 720
        # book = xlwt.Workbook(encoding="utf-8")
        # sheet1 = book.add_sheet("Sheet 1")
        for link in links:
            if link["class"] == ['img-responsive']:
                txt = open(str(counter) + ".jpg", "wb")
                link = link["src"].split("src=")[-1]
                download_img = urlopen(link)
                txt.write(download_img.read())           
                txt.close()
                
                # sheet1.write(counter,0,link)
                
                counter = counter + 1
    except:
        print("No second page")
    # book.save(str(query + ".xls"))
    