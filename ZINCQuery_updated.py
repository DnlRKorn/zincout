
# coding: utf-8

# # ZINC ID -> purchasability -> affordability

# In[1]:


import csv 
import numpy as np
#import smilite
import sys
import urllib
import requests

#import pandas as pd
from bs4 import BeautifulSoup
import itertools

import time
from selenium import webdriver
#from joblib import Parallel, delayed
#import concurrent.futures
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')

#driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)


# ## Curation of ZINC ID list

# In[2]:


# opens csv file with zinc ids
#with open('zincids.csv', 'rt') as csvfile:
#    reader = csv.reader(csvfile)
#    zinc_list = list(reader)


# In[3]:


#remove duplicates in each list
def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list


# In[4]:


#print("# without duplicates removed =",len(zinc_list))
#zinc_list = Remove(zinc_list)
#print('# with duplicates removed =',len(zinc_list))


# In[5]:


# get rid of brackets and quotations in values => zinc_list_2
#zinc_list_2 = []
#for zinc in zinc_list[1:]:
#    string = str(zinc)
#    zinc_list_2.append(string[2:-2]+" ")

# something weird going on with first value in zinc_list, fixing + appending
#string0 = str(zinc_list[0])
#zinc_list_2[0] = string0[8:-2]

#print(len(zinc_list_2))


# In[6]:


'''
# writing csv file with purchasable ZINC IDs
purchasable = open('zinc_purchase.txt', 'w')
for zinc in zinc_list_2:
    purchasable.write(zinc)
purchasable.close()
'''


# ## Fetching vendor links for each compound

# In[7]:


#cid = zinc_list_2[2]
#print(cid)


# In[8]:


#print(xml.prettify())


# In[10]:


def vendorURLs(cid):
        para_1 = []
        response = requests.get("http://zinc15.docking.org/substances/"+ cid+"/catitems/subsets/for-sale/table.html")
        xml = BeautifulSoup(response.content,"lxml")
        for i in range(0, 20):
            try:
                paragraphs = xml.find_all("td")[i]
                lines = str(paragraphs).splitlines()
                for l in lines:
                    para = str(l).splitlines()
                    for p in para:
                        if p[:12] == "<td><a href=":
                            for x in range(len(p)):
                                if p[x:x+6] == ' title':
                                    if p[12:x] not in para_1:
                                        para_1.append([p[13:x-1],cid])
            except:
                continue
        return para_1


# In[11]:


#response = requests.get("http://zinc15.docking.org/substances/" + cid + "/catitems/subsets/for-sale/table.html")
#response.status_code # 200 means it was downloaded successfully


# In[9]:


#xml = BeautifulSoup(response.content,"lxml")
#compdlinks= vendorURLs(zinc_list_2)


# In[12]:


#file1 = open("these_are_the_mother_fucking_links.txt","a") 
#for compL in compdlinks:
#    for line in compL:
#        if line[:6] == "mailto":
#            del compL
#            continue
#        else:
#            file1.write(line) 
#            file1.write("\n")
#file1.close() 


# NOT: achemblblock, Ambinter, astatechinc, biochempartner, cactus.nci.nih, chemistryondemand, combi-blocks (login),
#     hit2lead, labnetwork (~), molcore (no price listed), orderbb, orders.frontierssi,
#     otavachemicals, ox-chem, pipharm, princetonbio, rostarglobal, specs, synquestlabs (sometimes loads, req. price),
#     tocris, vitasmlab, Wonder-Chem 
#     <br>
# unknown: asis, apollo scientific, echemstore, synquest

# In[13]:


#outF = open("organics.txt", "w")
#for line in compdlinks:
  # write line to output file
#  if "organics" in line[0]:
#    outF.write(line[0])
#    outF.write("\n")
#outF.close()


# ## Affordability/Vendor Filtering

# these are all good vendors:
#     <br>cayman - DONE
#     <br>chemscene - addtl click/filter - DONE
#     <br>indofinechemical - DONE
#     <br>matrixscientific - DONE
#     <br>mcule - DONE
#     <br>medchemexpress - addtl click - DONE
#     <br>molport - DONE
#     <br>targetmol - DONE
#     <br>trc-canada - DONE
#     <br>apexbt - DONE
#     <br>abovchem - DONE
#     <br>bldpharm - DONE
#         <br>keyorganicsinc - addtl click + javascript rendering
#         <br>chem-space - javascript rendering
#         <br>enaminestore - javascript rendering - DONE
#         <br>sigmaaldrich - addtl click + javascript rendering - DONE

# In[14]:


def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list


# In[15]:


def findEasyVendors(urlist):
    vendors = []
    goodvendors = ["caymanchem", "chem-space", "indofinechemical", "matrixscientific", "mcule", "molport", "apexbt", 
                  "abovchem", "bldpharm", "targetmol", "trc-canada", "chemscene", "medchemexp", "sigma", "enamine"]
    for row in urlist:
        for v in goodvendors:
            if v in row[0]:
                vendors.append(row)
                break
    return vendors


# In[16]:
def makeEasy(cid):
   compdlinks = vendorURLs(cid)
   easy = findEasyVendors(compdlinks)
   
   
   # In[17]:
   
   
   easypeesy = []
   for e in easy:
       if "sigma" not in e[0]:
           easypeesy.append(e)
       elif "|" in e[0]:
           easypeesy.append(e)
   return easypeesy


# ### Abovchem

# In[18]:


def abovchemPrice(urlid):
    prices = []
    size = []
    sizes = []
    units = []
    response = requests.get(urlid)
    xml = BeautifulSoup(response.content,"lxml")
    for div in xml:
        try:
            d = str(div).splitlines()
            for ind in d: 
                line = str(ind.splitlines())
                if "size: " in line:
                    for i in range(len(line)):
                        if line[i:i+6] == "size: ":
                            for j in range(len(line)):
                                if line[j:j+2] == ", ":
                                    prices.append(line[i+6:j])
                elif "className = className.replace(" in line:
                    for i in range(len(line)):
                        if line[i:i+2] == '-/':
                            for j in range(len(line)):
                                if line[j:j+2] == ", ":
                                    units.append(line[i+2:j])
                elif "count: " in line:
                    for i in range(len(line)):
                        if line[i:i+7] == "count: ":
                            for j in range(len(line)):
                                if line[j:j+2] == ", ":
                                    size.append(line[i+7:j])
        except:
            continue
                
        for x in range(len(size)):
            sizes.append(size[x]+units[x])
    aff = np.column_stack((sizes, prices))
    return aff


# ### Apex Biotech

# In[19]:


def apxbtPrice(urlid):
    sizes = []
    prices = []
    response = requests.get(urlid)
    xml = BeautifulSoup(response.content,"lxml")
    for z in range(0,20):
        paragraphs = xml.find_all("td")[z]
        lines = str(paragraphs).splitlines()
        for m in lines:
            for i in range(len(m)):
                if 'item-name">' == m[i:i+11]:
                    sizes.append(m[i+11:i+14].replace(" ",""))
                if '="price">' == m[i:i+9]:
                    for j in range(len(m)):
                        if "</span></span>" == m[j:j+14]:
                            prices.append(m[i+9:j])
    aff = np.column_stack((sizes,prices))
    return aff


# ### Cayman Chemical

# In[20]:


def caymanPrice(urlid):
    #Example url https://www.caymanchem.com/product/10011249 
    sizes = []
    prices = []
    response = requests.get(urlid)
    xml = BeautifulSoup(response.text,features="lxml")
    
    #Find all td elements with class Size. These have the size of molecule for sale.
    for size_td in xml.find_all('td',{'class':'size'}):
      #Get the text from the element.
      size = size_td.text
      #Remove all the non-ascii characters (weird characters to help chrome display, not useful to us). Leaves only 50 mg.
      size = size.encode('ascii','ignore').strip()
      #Find the next element in the page with the class "price". This will be the price of the drug for the size we just saw.
      price_td = size_td.find_next_sibling('td',{'class','price'})
      #Get the price text.
      price = price_td.text
      price = price.encode('ascii','ignore').strip()
      #Remove the dollar sign from the price. Also removes comma, because price can be $1,200. Python doesn't like that.
      print(price)
      price = price.strip('$').replace(",",'')
      print(price)
      sizes.append(size)
      prices.append(price)

    aff = np.column_stack(((sizes, prices)))
    return aff

# ### Chemscene

# In[21]:


def chemscenePrice(compdurl):
    for i in range(len(compdurl)):
        if compdurl[i:i+11] == "productObj=":
            choiceID = compdurl[i+11:]

    response = requests.get(compdurl)

    casNos = []
    vendorid = []
    xml = BeautifulSoup(response.content,"lxml")
    for div in xml:
        d = str(div).splitlines()
        for ind in d: 
            line = ind.splitlines()
            if "CAS No." in str(line):
                for i in range(len(str(line))):
                    if str(line)[i:i+2] == "</":
                        casNos.append(str(line)[23:i])
            if 'class="img-responsive"' in str(line):
                for i in range(len(str(line))):
                    if str(line)[i:i+7] == ' class=':
                        vendorid.append(str(line)[12:i-1])
    while '' in casNos:
        casNos.remove('')
    crossref = np.column_stack((casNos, vendorid))

    for i in range(len(crossref)):
        if crossref[i][1] == choiceID:
            correctcas = crossref[i][0]

    sizes = []
    prices = []
    response = requests.get("https://www.chemscene.com/" + correctcas + ".html")
    xml = BeautifulSoup(response.content,"lxml")
    for div in xml:
        d = str(div).splitlines()
        for ind in d:
            if ' prctbl-size' in str(ind):
                for i in range(len(ind)):
                    if ind[i:i+8] == 'id="size':
                        line = ind[i+11:]
                        for j in range(len(ind)):
                            if line[j:j+3] == "</s":
                                sizes.append(line[:j].replace(" ",""))
            elif 's" id="price' in ind:
                for i in range(len(ind)):
                    if ind[i:i+9] == 'id="price':
                        for j in range(len(ind)):
                            if ind[j:j+8] == "</span><":
                                 prices.append(ind[i+12:j])

    aff = np.column_stack((sizes,prices))
    return aff


# ### Enamine

# In[22]:


# this function is not perfect, does not filter search results by stereochem, requires user to do this
def enaminePrice(urlpage):
    
    #1st and only driver call
    
    driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
    driver.get(urlpage);
    innerHTML = driver.execute_script("return document.body.innerHTML")
    time.sleep(5) # lets the user see something
    html = str(innerHTML).splitlines()
    time.sleep(5) # lets the user see something
    driver.quit()
    
    #checking that valid search results page was found
    pagefound = 0
    for h in html:
        if "Sorry, nothing found matching your search criteria." in h:
            pagefound = 1
    
    # returns prices and sizes, some issue with showing results that don't exist? or maybe they do
    prices = []
    size_excl = []
    sizes = []
    if pagefound == 0:
        for h in html:
            if "$ " in h:
                for j in range(len(h)):
                    if h[j] == " ":
                        prices.append(h[j+1:])
            elif '</a></span><span class="c-price">' in h:
                if len(h) < 42:
                    for j in range(len(h)):
                        if h[j:j+4] == "</a>":
                            sizes.append(h[:j].replace(" ",""))
    '''for h in html:
        if '</a></span><span class="c-price">' in h:
            if len(h) < 42:
                val = 0
                for s in size_excl:
                    if s in h:
                        val = 1
                if val == 0:
                    for j in range(len(h)):
                        if h[j:j+4] == "</a>":
                            sizes.append(h[:j])'''

    aff = np.column_stack((sizes, prices))

    return aff


# ### Indofine Chemical

# In[23]:


def indofinePrice(urlid):
    sizes = []
    prices = []
    response = requests.get(urlid)
    xml = BeautifulSoup(response.content,"lxml")
    for z in range(0,20):
        paragraphs = xml.find_all("div")[z]
        lines = str(paragraphs).splitlines()
        for l in lines:
            ind = l.splitlines()
            for i in ind:
                if "gm @ $" in i[30:]:
                    sizes.append(i[28:33].replace(" ","").replace("gm","mg"))
                    prices.append(i[36:42])
    aff = np.column_stack((sizes, prices))
    return aff


# ### Matrix Scientific

# In[24]:


def matrixPrice(urlid):
    sizes = []
    prices = []
    response = requests.get(urlid)
    xml = BeautifulSoup(response.content,"lxml")
    for z in range(0,20):
        try:
            paragraphs = xml.find_all("td")[z]
            lines = str(paragraphs).splitlines()
            for m in lines:
                if 'class="price"' in m:
                    prices.append(m[21:27].replace(",",""))
                elif "			" in m:
                    if ("<" not in m) and ("g" in m):
                        for x in range(len(m)):
                            if m[x+1] == 'g':
                                sizes.append(m[3:x+2].replace(" ",""))
        except:
            continue
        
    aff = np.column_stack((sizes,prices))
    return aff


# ### MCULE

# In[25]:


def mculePrice(urlid):
    sizes = []
    prices = []
    response = requests.get(urlid)
    xml = BeautifulSoup(response.content,"lxml")
    for z in range(0,20):
        paragraphs = xml.find_all("td")[z]
        lines = str(paragraphs).splitlines()
        for m in lines:
            if "USD" in m:
                for x in range(len(m)):
                    if m[x:x+4] == ' USD':
                        prices.append(m[4:x])
                del m
            elif "g</td>" in m:
                if "class" not in m:
                    for x in range(len(m)):
                        if m[x:x+5] == '</td>':
                            sizes.append(m[4:x].replace(" ",""))
    aff = np.column_stack((sizes, prices))
    return aff


# ### MedChem Expresss

# In[26]:


def medchemexpPrice(urlid):
    response = requests.get(urlid)
    xml = BeautifulSoup(response.content,"lxml")

    #if there's a space in the compound name you're going to need to replace it with "-"

    # extracting compound name from the search result
    for z in range(0,20):
        try:
            paragraphs = xml.find_all("dt")[z]
            lines = str(paragraphs).splitlines()
            for l in lines:
                if "s_pro_list_cat" in l:
                    for j in range(len(l)):
                        if l[j:j+4] == 'f="/':
                            for k in range(len(l)):
                                if l[k:k+5] == ".html":
                                    compdname = (l[j+4:k].replace(" ","-"))
        except:
            continue


    # fetching actual vendor link
    prices = []
    sizes = []
    urlid = "https://www.medchemexpress.com/" + compdname+ ".html"
    response = requests.get(urlid)
    xml = BeautifulSoup(response.content,"lxml")
    for z in range(0,20):
        paragraphs = xml.find_all("td")[z]
        lines = str(paragraphs).splitlines()
        for m in lines:
            if "USD" in m:
                if "input" not in m:
                    prices.append(m[4:].replace(" ", ""))
                else:
                    for j in range(len(m)):
                        if m[j:j+3] == ";HY":
                            line = (m[:j])
                            for k in range(len(line)):
                                if line[k] == ";":
                                    sizes.append(line[k+1:].replace(" ", ""))  
                                    
    aff = np.column_stack((sizes, prices))
    return aff


# ### MolPort

# In[27]:


def molportPrice(urlid):
    sizes = []
    prices = []
    response = requests.get(urlid)
    xml = BeautifulSoup(response.content,"lxml")
    for div in xml:
        d = str(div).splitlines()
        for ind in d:
            if '"sku"' in ind:
                for j in range(len(ind)):
                    if ind[j] == "_":
                        indn = ind[j+1:]
                        for i in range(len(indn)):
                            if indn[i] == '"':
                                sizes.append(indn[:i])
            elif '"price"' in ind:
                for j in range(len(ind)):
                    if ind[j:j+2] == ' "':
                        for k in range(len(ind)):
                            if ind[k:k+2] == '",':
                                prices.append(ind[j+2:k])
    aff = np.column_stack((sizes, prices))
    return aff


# ### Sigma Aldrich

# In[28]:


def newURL(urlid):
    for x in range(len(urlid)):
        if urlid[x:x+12] == "search?term=":
            for y in range(len(urlid)):
                if urlid[y:y+4] == "&int":
                    compdname = str(urlid[x+12:y])
                    break
                elif urlid[y:y+4] == "&amp":
                    compdname = str(urlid[x+12:y])
                    break
                elif urlid[y] == "|":
                    compdname = str(urlid[x+12:y])   
                    break
    
    newurlid = "https://www.sigmaaldrich.com/catalog/search?term="+compdname+"&interface=All&N=0&mode=match%20partialmax&lang=en&region=US&focus=product"              

    return newurlid


# In[29]:


def sigmaPrice(urlpage):
    
    urlpage2 = newURL(urlpage) #transforming url because sigma aldrich sucks
    
    #first driver call
    
    #driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
    driver = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=chrome_options)
    driver.get(urlpage2);
    innerHTML = driver.execute_script("return document.body.innerHTML")
    driver.quit()
    time.sleep(5) # lets the user see something

    print(type(innerHTML))
    time.sleep(1)
    html = innerHTML.splitlines()

    
    #What's the real compound name because this wasn't already convoluted enough

    compdname = ""
    for h in html:
        if "breadcrumbOriginalTextSearched" in h:
            for x in range(len(h)):
                if h[x:x+7] == 'ched">"':
                    for y in range(len(h)):
                        if h[y:y+13] == '"</span><span':
                            compdname = h[x+7:y].lower()
    
    #Sigma Aldrich's url formatting can go to hell

    if "|" in urlpage:
        if "USP" in urlpage:
            urlpage3 = "https://www.sigmaaldrich.com/catalog/product/usp/" + compdname + "?lang=en&region=US.php"
        elif "VETEC" in urlpage:
            urlpage3 = "https://www.sigmaaldrich.com/catalog/product/vetec/" + compdname + "?lang=en&region=US.php"
        elif "SIGMA" in urlpage:
            urlpage3 = "https://www.sigmaaldrich.com/catalog/product/sigma/" + compdname + "?lang=en&region=US"
        elif "SIAL" in urlpage:
            urlpage3 = "https://www.sigmaaldrich.com/catalog/product/sial/" + compdname + "?lang=en&region=US"
        else: 
            urlpage3 = 'https://www.sigmaaldrich.com/catalog/product/aldrich/' + compdname + '?lang=en&region=US.php'
    else:
        urlpage3 = 'https://www.sigmaaldrich.com/catalog/product/aldrich/' + compdname + '?lang=en&region=US.php'

    # 2nd driver call
    
    if compdname != "":
        driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)

        driver.get(urlpage3);
        innerHTML = driver.execute_script("return document.body.innerHTML")
        time.sleep(5) # lets the user see something

        html = innerHTML.splitlines()

        #time.sleep(5) # lets the user see something
        driver.quit()
    
    #making sure page loads
    
    error404 = 0
    for h in html:
        if "sorry" in h:
            error404 = 1
            
    #making sure product is in stock
    
    discontinued = 0
    for h in html:
        if "discontinued" in h:
            discontinued = 1
        if "still have inventory in stock" in h:
            discontinued = 0

    # finally fetch prices and package sizes
    
    sizes = []
    prices = []
    val = compdname.upper() +"-"

    if error404 == 0:
        if discontinued == 0:
            if compdname != "":
                for h in html:
                    if val in h:
                        d = str(h).split()
                        for ind in d:
                            if "row" in ind: #"CASS" doesn't work
                                for x in range(len(ind)):
                                    if ind[x] == "-":
                                        size = ind[x+1:].replace('"><td','')
                                        sizes.append(size.lower())
                    if "USD" in h:
                        d = str(h).split()
                        for ind in d:
                            for x in range(len(ind)):
                                if ind[x:x+6] == "USD#@#":
                                    for y in range(len(h)):
                                        if ind[y:y+10] == '"></td><td':
                                            prices.append(ind[x+6:y])
    
    aff = np.column_stack((sizes, prices))
    
    return aff


# ### Targetmol

# In[30]:


def targetmolPrice(urlid):
    sizes = []
    prices = []
    response = requests.get(urlid)
    xml = BeautifulSoup(response.content,"lxml")
    for z in range(0,20):
        paragraphs = xml.find_all("td")[z]
        lines = str(paragraphs).splitlines()
        mat = lines[0].splitlines()
        for m in mat:
            if "." in str(m):
                for x in range(len(m)):
                    if m[x:x+5] == '</td>':
                        prices.append(m[4:x])
                del m
            elif " " in m:
                if "<p" not in m:
                    if "td " not in m:
                        for x in range(len(m)):
                            if m[x:x+5] == '</td>':
                                sizes.append(m[4:x].replace(" ",""))
    aff = np.column_stack((sizes, prices))
    return aff


# ### Toronto Research Chemicals - Canada

# In[31]:


def trcPrice(urlid):
    prices = []
    sizes = []
    pr = []
    response = requests.get(urlid)
    xml = BeautifulSoup(response.content,"lxml")
    for z in range(0,20):
        paragraphs = xml.find_all("div")[z]
        lines = str(paragraphs).splitlines()
        for m in lines:
            if "g</td>" in m:
                if "id" not in m:
                    for x in range(len(m)):
                        if m[x:x+2] == "</":
                            sizes.append(m[23:x].replace(" ",""))
            elif '<td class="optionscol">' in m:
                if '.' in m:
                    for j in range(len(m)):
                        if m[j:j+2] == "  ":
                            for i in range(len(m)):
                                if m[i] == "$":
                                    pr.append(m[i+1:j].replace(" ",""))
    prices = Remove(pr)
    aff = np.column_stack((sizes,prices))
    return aff


# ## Vendor Prices

# In[32]:
#import multiprocessing

#inputs = range(10) 
#def processInput(i):
#        return i * i

#    num_cores = multiprocessing.cpu_count()

#    results = Parallel(n_jobs=num_cores)(delayed(processInput)(i) for i in inputs)

def processUrl(url):
       if "abovchem" in url[0]:
           aff = abovchemPrice(url[0])
           length = len(aff)
           rep = list(itertools.repeat(url, length))
           aff_2 = np.column_stack((aff, rep))
           return aff_2
       elif "apxbt" in url[0]:
           aff = apxbtPrice(url[0])
           length = len(aff)
           rep = list(itertools.repeat(url, length))
           aff_2 = np.column_stack((aff, rep))
           return aff_2
       elif "cayman" in url[0]:
           #url[0] looks like http://www.caymanchem.com/app/template/Product.vm/catalog/10011249
           code = url[0].split('/')[-1]
           #Grab the number at the end of the list. So for example code will be 10011249
           url[0] = 'https://www.caymanchem.com/product/' + code 
           #Make a new link to page https://www.caymanchem.com/product/10011249 which is static
           aff = caymanPrice(url[0])
           length = len(aff)
           rep = list(itertools.repeat(url, length))
           aff_2 = np.column_stack((aff, rep))
           return aff_2
       elif "chemscene" in url[0]:
           aff = chemscenePrice(url[0])
           length = len(aff)
           rep = list(itertools.repeat(url, length))
           aff_2 = np.column_stack((aff, rep))
           return aff_2
       elif "indofine" in url[0]:
           aff = indofinePrice(url[0])
           length = len(aff)
           rep = list(itertools.repeat(url, length))
           aff_2 = np.column_stack((aff, rep))
           return aff_2
       elif "matrixscientific" in url[0]:
           aff = matrixPrice(url[0])
           length = len(aff)
           rep = list(itertools.repeat(url, length))
           aff_2 = np.column_stack((aff, rep))
           return aff_2
       elif "mcule" in url[0]:
           aff = mculePrice(url[0])
           length = len(aff)
           rep = list(itertools.repeat(url, length))
           aff_2 = np.column_stack((aff, rep))
           return aff_2
       elif "medchemexp" in url[0]:
           aff = medchemexpPrice(url[0])
           length = len(aff)
           rep = list(itertools.repeat(url, length))
           aff_2 = np.column_stack((aff, rep))
           return aff_2
       elif "molport" in url[0]:
           aff = molportPrice(url[0])
           length = len(aff)
           rep = list(itertools.repeat(url, length))
           aff_2 = np.column_stack((aff, rep))
           return aff_2
       elif "targetmol" in url[0]:
           aff = targetmolPrice(url[0])
           length = len(aff)
           rep = list(itertools.repeat(url, length))
           aff_2 = np.column_stack((aff, rep))
           return aff_2
       elif "trc-canada" in url[0]:
           aff = trcPrice(url[0])
           length = len(aff)
           rep = list(itertools.repeat(url, length))
           aff_2 = np.column_stack((aff, rep))
           return aff_2
       elif "sigma" in url[0]:
           aff = sigmaPrice(url[0])
           length = len(aff)
           rep = list(itertools.repeat(url, length))
           aff_2 = np.column_stack((aff, rep))
           return aff_2

def makeBuyList(easypeesy):   
   start = time.time()
   
   #buylist = Parallel(n_jobs=3)(delayed(processUrl)(url) for url in easypeesy[:250])
   #buylist = []
   #with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
   #   executor.map(processUrl, easypeesy)
   #   future_to_url = {executor.submit(processUrl, url): url for url in easypeesy}
   #   for future in concurrent.futures.as_completed(future_to_url):
   #       buylist.append(future.result())
   buylist = [processUrl(url) for url in easypeesy[:250]]
   print(buylist)
   end = time.time()
   print(end - start)
   return buylist

# In[33]:
def affordable(cid="ZINC19795634"):
    easypeesy = makeEasy(cid)
    buylist = makeBuyList(easypeesy)


    for b in buylist:
       print(b)




    print('AFFORDABLE')
    affordable = []
    
    desiredlimit = 300.0
    desiredsize = "10mg"
    
    for b in buylist:
        for pr in b:
            print(pr)
            print('0',pr[0])
            print('1',pr[1])
            if str(pr[0]) in desiredsize:
                print("PASSED")

                if float(pr[1]) <= desiredlimit:
                    affordable.append(pr)
                    
    return affordable
#affordable()
#affordable("ZINC00000882")
    #affordable = np.array(affordable)
    #affordable = affordable[np.argsort(affordable[:,1])]
    
    
    # ### Results
    
    # In[35]:
    
     
    #data = {'ZINC ID': affordable[:,3],'Package Size': affordable[:,0], 'Price ($)': affordable[:,1],'Link': affordable[:,2]}
    #json = pd.DataFrame(data=data).to_json()
    #print(json)
    
    
