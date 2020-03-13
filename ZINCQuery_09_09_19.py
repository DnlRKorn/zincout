
# coding: utf-8

# # ZINC ID -> purchasability -> affordability

# In[69]:


import csv 
import numpy as np
#import smilite
import sys
import urllib
import requests

import pandas as pd
from bs4 import BeautifulSoup
import itertools

import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')

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

'''
print("# without duplicates removed =",len(zinc_list))
zinc_list = Remove(zinc_list)
print('# with duplicates removed =',len(zinc_list))
'''

# In[5]:

'''
# get rid of brackets and quotations in values => zinc_list_2
zinc_list_2 = []
for zinc in zinc_list[1:]:
    string = str(zinc)
    zinc_list_2.append(string[2:-2]+" ")

# something weird going on with first value in zinc_list, fixing + appending
string0 = str(zinc_list[0])
zinc_list_2[0] = string0[8:-2]

print(len(zinc_list_2))
'''

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

'''
cid = zinc_list_2[2]
print(cid)
'''

# In[8]:

'''
response = requests.get("http://zinc15.docking.org/substances/" + cid + "/catitems/subsets/for-sale/table.html")
response.status_code # 200 means it was downloaded successfully
'''

# In[9]:


#xml = BeautifulSoup(response.content,"lxml")
#print(xml.prettify())


# In[10]:


def vendorURLs(zinc_id_list):
    para_1 = []
    for cid in zinc_id_list:
        response = requests.get("http://zinc15.docking.org/substances/"+ cid+"/catitems/subsets/for-sale/table.html")
        xml = BeautifulSoup(response.content,"lxml")
        for paragraphs in xml.find_all("td"):
            #print(paragraphs)
            try:
               # paragraphs = xml.find_all("td")[i]
                lines = str(paragraphs).splitlines()
                for l in lines:
                    para = str(l).splitlines()
                    for p in para:
                        if("/catalogs/" in p):
                            name = p.split("/catalogs/")[1]
                            if("title" in name):
                               name = "http://zinc15.docking.org/catalogs/" + name.split('"')[0]
                               para_1.append([name,cid])
                        elif p[:12] == "<td><a href=":
                            for x in range(len(p)):
                                if p[x:x+6] == ' title':
                                    if p[12:x] not in para_1:
                                        para_1.append([p[13:x-1],cid])
            except:
                continue
    return para_1


# In[11]:


#compdlinks= vendorURLs(zinc_list_2)


# In[12]:


#for compd in compdlinks:
#    print(compd)


# In[13]:

'''
file1 = open("these_are_the_mother_fucking_links.txt","a") 
for compL in compdlinks:
    for line in compL:
        if line[:6] == "mailto":
            del compL
            continue
        else:
            file1.write(line) 
            file1.write("\n")
file1.close() 
'''

# NOT: achemblblock, Ambinter, astatechinc, biochempartner, cactus.nci.nih, chemistryondemand, combi-blocks (login),
#     hit2lead, labnetwork (~), molcore (no price listed), orderbb, orders.frontierssi,
#     otavachemicals, ox-chem, pipharm, princetonbio, rostarglobal, specs, synquestlabs (sometimes loads, req. price),
#     tocris, vitasmlab, Wonder-Chem 
#     <br>
# unknown: asis, apollo scientific, echemstore, synquest

# In[15]:

'''
outF = open("sigma.txt", "w")
for line in compdlinks:
  # write line to output file
  if "sigma" in line[0]:
    if "|" in line[0]:
        outF.write(line[0])
        outF.write("\n")
outF.close()
'''

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

# In[13]:


def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list


# In[14]:


def findEasyVendors(urlist):
    vendors = []
    goodvendors = ["caymanchem", "chem-space", "indofinechemical", "matrixscientific", "mcule", "molport", "apexbt", "abovchem", "bldpharm", "targetmol", "trc-canada", "chemscene", "medchemexp", "sigma", "enamine","aksci"]
    for row in urlist:
        if("zinc15.docking.org" in row[0]):continue
        for v in goodvendors:
            if v in row[0]:
                vendors.append(row)
                break
    return vendors


# In[15]:

'''
easy = findEasyVendors(compdlinks)


# In[16]:


easypeesy = []
for e in easy:
    if "sigma" not in e[0]:
        easypeesy.append(e)
    elif "|" in e[0]:
        easypeesy.append(e)
'''

# ### Abovchem

# In[17]:
debug = True
def makeEasy(cid):
   compdlinks = vendorURLs([cid])
   if(debug): print(compdlinks)
   easy = findEasyVendors(compdlinks) 
   easypeesy = []
   for e in easy:
       if "sigma" not in e[0]:
           easypeesy.append(e)
       elif "|" in e[0]:
           easypeesy.append(e)
   noteasy = [x for x in compdlinks if x not in easypeesy]
   if(debug):
       print("COMP",compdlinks)
       print("EASY",easy)
       print("EASYPEASY",easypeesy)
       print('NOT EASY',noteasy)
   return [easypeesy,noteasy]



def abovchemPrice(urlid):
    try:  
       prices = []
       sizes = []
       response = requests.get(urlid)
       xml = BeautifulSoup(response.content,"lxml")
       #fetching quantity
       for size_td in xml.find_all("td","col1"):
           size = size_td.text
           size = size.encode('ascii','ignore').strip()
           if len(size) <= 5: #this might cause problems if they sell things in DMSO
               sizes.append(size)
       #fetching prices
       for price_td in xml.find_all("td","col3"):
           price = price_td.text
           price = price.encode('ascii','ignore').strip()
           price = str(price)
           if "$" in price:
               prices.append(price[3:].replace(" ", ""))
       aff = np.column_stack((sizes,prices))
    except:
       aff = np.column_stack(([],[]))
    return aff


# ### Apex Biotech


def apxbtPrice(urlid):
    # example url: https://www.apexbt.com/sd-169.html
    sizes = []
    prices = []
    response = requests.get(urlid)
    xml = BeautifulSoup(response.text,features="lxml")
    for size_str in xml.find_all("strong","product-item-name"):
        #fetching size
        size = size_str.text
        size = size.encode('ascii','ignore').strip()
        sizes.append(size)
        #fetching price
        price_sp = size_str.find_next("span", "price")
        price = price_sp.text
        price = price.encode('ascii','ignore').strip()
        prices.append(price[1:])

    aff = np.column_stack((sizes,prices))
    return aff


# ### Cayman Chemical

# In[68]:


def caymanPrice(urlpage):
    
    #calling driver
    print('cayman1')
    idx = urlpage.split('/')[-1]
    urlpage = "https://www.caymanchem.com/product/%s" % idx
    driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
    driver.get(urlpage);
    print('cayman2')
    #innerHTML = driver.execute_script("return document.body.innerHTML")
    #time.sleep(5) # lets the user see something
    print('cayman3')
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-lato-bold"))
    )
    '''
    try:
       print('hi')
       element = WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.ByClassName, "text-lato-bold"))
       )
    except:
        print('hi2')
        return
    finally:
        driver.quit()
        '''
    innerHTML = driver.execute_script("return document.body.innerHTML")
    #html = str(innerHTML).splitlines()
    html = innerHTML.encode("ascii", "ignore").splitlines()


    print('cayman4')
    #time.sleep(5) # lets the user see something
    print('cayman5')
    driver.quit()
    print('cayman6')
    
    #text-lato-bold
    # fetching price and sizes
    sizes = []
    prices = []
    for h in html:
        hnew = h.split("<")
        for n in hnew:
            if '"text-lato-bold"' in n:
                idx1 = n.find(">")
                sizes.append(n[idx1+1:].replace(" ",""))
            elif '"mb-0"' in n:
                idx1 = n.find(">")
                prices.append(n[idx1+2:].replace(",",""))
    
    aff = np.column_stack((sizes, prices))
    return aff


# ### Chemscene

# In[21]:


def chemscenePrice(compdurl):
    print('chemscene1')
    for i in range(len(compdurl)):
        if compdurl[i:i+11] == "productObj=":
            choiceID = compdurl[i+11:]
    print('chemscene2')

    response = requests.get(compdurl)
    print('chemscene3')

    casNos = []
    vendorid = []
    xml = BeautifulSoup(response.content,"lxml")
    print('chemscene4')
    
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
    print('chemscene5')
    while '' in casNos:
        casNos.remove('')
    crossref = np.column_stack((casNos, vendorid))
    print('chemscene6')

    for i in range(len(crossref)):
        if crossref[i][1] == choiceID:
            correctcas = crossref[i][0]
    print('chemscene7')

    sizes = []
    prices = []
    print(correctcas)
    print("https://www.chemscene.com/" + correctcas + ".html")
    response = requests.get("https://www.chemscene.com/" + str(correctcas) + ".html")
    print('chemscene8')
    xml = BeautifulSoup(response.content,"lxml")
    #print(xml)
    prices = xml.findAll('input', {'class' : 'originalPrice'})
    prices = [x['value'] for x in prices]
    print(prices)
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
                                '''
            elif 's" id="price' in ind:
                for i in range(len(ind)):
                    if ind[i:i+9] == 'id="price':
                        for j in range(len(ind)):
                            if ind[j:j+8] == "</span><":
                                 prices.append(ind[i+12:j])
                                 '''
    print(sizes)
    aff = np.column_stack((sizes,prices))
    return aff


# ### Enamine

# In[22]:


# this function is not perfect, does not filter search results by stereochem, requires user to do this
def enaminePrice(urlpage):
    print(urlpage)
    
    #1st and only driver call
    
    driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
    driver.get(urlpage);
    innerHTML = driver.execute_script("return document.body.innerHTML")
    #time.sleep(5) # lets the user see something
    #html = innerHTML.encode('ascii','ignore').splitlines()
#c-price
    try:
       element = WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.CLASS_NAME, "c-price"))
       )
       html = innerHTML.encode('ascii','ignore').splitlines()
    except:
       html = ["Sorry, nothing found matching your search criteria."]
    finally:
       driver.quit()

    #time.sleep(5) # lets the user see something
    #html = innerHTML.encode('ascii','ignore').splitlines()
    
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
    for size_str in xml.find_all("div","col-sm-8"):
        #fetching size
        size = size_str.text
        size = size.encode('ascii','ignore').strip()
        size = str(size)
        if len(size) <=50:
            idx1 = size.find("@")
            sizes.append(size[2:idx1].replace("gm","mg").replace(" ",""))
            prices.append(size[idx1+3:].replace("'",""))

    aff = np.column_stack((sizes,prices))
    return aff


# ### Matrix Scientific

# In[27]:


def matrixPrice(urlid):
    sizes = []
    prices = []
    response = requests.get(urlid)
    xml = BeautifulSoup(response.text,features="lxml")
    #cnt = 0
    for size_str in xml.find_all("td"):
        #fetching size
        #print(size_str.text)
        size = size_str.text.strip()
        #size = size.encode('ascii','ignore').strip()
        size = str(size)
        #print(size,cnt)
        #cnt+=1
        if "g" in size:
            idx1 = size.find("g")
            sizes.append(size[0:idx1+1])
        #fetching price
    for price_sp in xml.find_all("span", "price"):
        price = price_sp.text
        price = price.encode('ascii','ignore').strip()
        prices.append(price[1:])

    print(sizes)
    print(prices)
    aff = np.column_stack((sizes,prices))
        
    return aff

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

# In[29]:


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

# In[30]:


def molportPrice(urlid):
    print('molport1')
    sizes = []
    prices = []
    response = requests.get(urlid)
    xml = BeautifulSoup(response.content,"lxml")
    print('molport2')
    for div in xml:
        print('molport3')
        d = str(div).splitlines()
        print('molport3')
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

def aksciPrice(urlid):
    #https://aksci.com/item_detail.php?cat=F336
   ak_id = urlid.split('=')[1] 
   
   cookies = {
       'PHPSESSID': '4b289e9ols212h2h2hss60kct6',
       'aksci': '99+50+1+1+DESC',
       'wcsid': 'kshzPG57lRP76TdU7G5Jx0U5C62SBrId',
       'hblid': 'mTfqmwGq6tN8P3lj7G5Jx0U2BoyBCODr',
       '_okdetect': '%7B%22token%22%3A%2215785917718880%22%2C%22proto%22%3A%22https%3A%22%2C%22host%22%3A%22aksci.com%22%7D',
       'olfsk': 'olfsk06708603080311826',
       '_okbk': 'cd4%3Dtrue%2Cvi5%3D0%2Cvi4%3D1578591775255%2Cvi3%3Dactive%2Cvi2%3Dfalse%2Cvi1%3Dfalse%2Ccd8%3Dchat%2Ccd6%3D0%2Ccd5%3Daway%2Ccd3%3Dfalse%2Ccd2%3D0%2Ccd1%3D0%2C',
       '_ok': '3507-598-10-5787',
       'aksci_b': '%3B+4334AH',
       '_oklv': '1578592098764%2CkshzPG57lRP76TdU7G5Jx0U5C62SBrId',
   }
   
   headers = {
       'Connection': 'keep-alive',
       'Pragma': 'no-cache',
       'Cache-Control': 'no-cache',
       'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.86 Mobile Safari/537.36',
       'Accept': '*/*',
       'Sec-Fetch-Site': 'same-origin',
       'Sec-Fetch-Mode': 'cors',
       'Referer': 'https://aksci.com/item_detail.php?cat=4334AH',
       'Accept-Encoding': 'gzip, deflate, br',
       'Accept-Language': 'en-US,en;q=0.9',
   }
   
   params = (
       ('cat', ak_id),
       ('width', '420'),
   )
   
   try:
      response = requests.get('https://aksci.com/pricing.php', headers=headers, params=params, cookies=cookies,timeout=1)
   except requests.exceptions.Timeout:
      aff = np.column_stack(([], []))
      return aff
   
   soup = BeautifulSoup(response.text, 'lxml')
   sizes = []
   prices = []
   for x in soup.findAll('input'):
      prices.append(x['price'])
      sizes.append(x['id'].split('_')[1])
   #return prices
   aff = np.column_stack((sizes, prices))
   return aff

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

# In[34]:


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
            if "data-price=" in m:
                #prices
                idx1 = m.find('data-price="')
                idx2 = m.find('" data-size')
                prices.append(m[idx1+12:idx2])
                #sizes
                idx3 = m.find('data-size="')
                idx4 = m.find('" id')
                sizes.append(m[idx3+11:idx4])
            
    aff = np.column_stack((sizes,prices))
    return aff


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


# In[32]:


def sigmaPrice(urlpage):
    try: 
       urlpage2 = newURL(urlpage) #transforming url because sigma aldrich sucks
       
       #first driver call
       
       driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
       driver.get(urlpage2);
       innerHTML = driver.execute_script("return document.body.innerHTML")
       time.sleep(5) # lets the user see something
       innerHTML = innerHTML.encode("ascii","ignore")
       html = str(innerHTML).splitlines()

       time.sleep(5) # lets the user see something
       driver.quit()
       
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

           innerHTML = innerHTML.encode("ascii","ignore")
           html = str(innerHTML).splitlines()

           time.sleep(5) # lets the user see something
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
    except:
      sizes = []
      prices = []
      aff = np.column_stack((sizes, prices))

    
    return aff


# ### Targetmol

# In[33]:


def targetmolPrice(urlid):
    sizes = []
    prices = []
    response = requests.get(urlid)
    xml = BeautifulSoup(response.content,"lxml")
    div = xml.find("div", class_="cpdprice")
    if(div==None):return
    #print(div)

    for row in div.find_all("tr"):
        cols = list(row.find_all("td"))
        cols = [x.text for x in cols]
        if(len(cols)!=4):continue
        if('mg' not in cols[0]):continue
        if('In stock' not in cols[1]):continue
        price = cols[2].replace("\n","").replace("\r","").strip()
        size = cols[0].replace("\n","").replace("\r","").strip()
        sizes.append(str(size))
        prices.append(str(price))



    #for z in range(0,20):
    #    paragraphs = xml.find_all("td")[z]
#    for paragraphs in xml.find_all("td"):
#        lines = str(paragraphs).splitlines()
#        mat = lines[0].splitlines()
#        for m in mat:
#            print(m)
#            if "." in str(m):
#                for x in range(len(m)):
#                    if m[x:x+5] == '</td>':
#                        prices.append(m[4:x])
#                del m
#            elif " " in m:
#                if "<p" not in m:
#                    if "td " not in m:
#                        for x in range(len(m)):
#                            if m[x:x+5] == '</td>':
#                                sizes.append(m[4:x].replace(" ",""))
#    print(sizes)
#    print(prices)

    aff = np.column_stack((sizes, prices))
    return aff


# ### Toronto Research Chemicals - Canada

# In[34]:


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
            if "data-price=" in m:
                #prices
                idx1 = m.find('data-price="')
                idx2 = m.find('" data-size')
                prices.append(m[idx1+12:idx2])
                #sizes
                idx3 = m.find('data-size="')
                idx4 = m.find('" id')
                sizes.append(m[idx3+11:idx4])
            
    aff = np.column_stack((sizes,prices))
    return aff


# ## Vendor Prices

# In[35]:

def makeBuyList(easypeesy): 
    print('making buylist')
    start = time.time()
    
    buylist = []
    for url in easypeesy[:50]:
        #print(buylist)
        print(url)
        if "abovchem" in url[0]:
            aff = abovchemPrice(url[0])
            length = len(aff)
            rep = list(itertools.repeat(url, length))
            aff_2 = np.column_stack((aff, rep))
            buylist.append(aff_2)
        elif "apxbt" in url[0]:
            aff = apxbtPrice(url[0])
            length = len(aff)
            rep = list(itertools.repeat(url, length))
            aff_2 = np.column_stack((aff, rep))
            buylist.append(aff_2)
        elif "cayman" in url[0]:
            aff = caymanPrice(url[0])
            length = len(aff)
            rep = list(itertools.repeat(url, length))
            aff_2 = np.column_stack((aff, rep))
            buylist.append(aff_2)
        elif "chemscene" in url[0]:
            aff = chemscenePrice(url[0])
            length = len(aff)
            rep = list(itertools.repeat(url, length))
            aff_2 = np.column_stack((aff, rep))
            buylist.append(aff_2)
        elif "indofine" in url[0]:
            aff = indofinePrice(url[0])
            length = len(aff)
            rep = list(itertools.repeat(url, length))
            aff_2 = np.column_stack((aff, rep))
            buylist.append(aff_2)
        elif "matrixscientific" in url[0]:
            aff = matrixPrice(url[0])
            length = len(aff)
            rep = list(itertools.repeat(url, length))
            aff_2 = np.column_stack((aff, rep))
            buylist.append(aff_2)
        elif "mcule" in url[0]:
            aff = mculePrice(url[0])
            length = len(aff)
            rep = list(itertools.repeat(url, length))
            aff_2 = np.column_stack((aff, rep))
            buylist.append(aff_2)
        elif "medchemexp" in url[0]:
            aff = medchemexpPrice(url[0])
            length = len(aff)
            rep = list(itertools.repeat(url, length))
            aff_2 = np.column_stack((aff, rep))
            buylist.append(aff_2)
        elif "molport" in url[0]:
            aff = molportPrice(url[0])
            length = len(aff)
            rep = list(itertools.repeat(url, length))
            aff_2 = np.column_stack((aff, rep))
            buylist.append(aff_2)
        elif "targetmol" in url[0]:
            aff = targetmolPrice(url[0])
            length = len(aff)
            rep = list(itertools.repeat(url, length))
            aff_2 = np.column_stack((aff, rep))
            buylist.append(aff_2)
        elif "trc-canada" in url[0]:
            aff = trcPrice(url[0])
            length = len(aff)
            rep = list(itertools.repeat(url, length))
            aff_2 = np.column_stack((aff, rep))
            buylist.append(aff_2)
        elif "sigma" in url[0]:
            aff = sigmaPrice(url[0])
            length = len(aff)
            rep = list(itertools.repeat(url, length))
            aff_2 = np.column_stack((aff, rep))
            buylist.append(aff_2)
        elif "enamine" in url[0]:
            aff = enaminePrice(url[0])
            length = len(aff)
            rep = list(itertools.repeat(url, length))
            aff_2 = np.column_stack((aff, rep))
            buylist.append(aff_2)
        elif "aksci" in url[0]:
            aff = aksciPrice(url[0])
            length = len(aff)
            rep = list(itertools.repeat(url, length))
            aff_2 = np.column_stack((aff, rep))
            buylist.append(aff_2)
        
    
    end = time.time()
    return buylist
    
    
# In[36]:


#for b in buylist:
#    print(b)


# ### Affordability Filter

# In[43]:


# getting vendor name from url
def getVendorName(url):
    if("zinc15.docking.org" in url):
        return url.split("/")[-2]
    idx1 = url.find("www.")
    idx2 = url.find(".com")
    if "indofine" in url:
        idx3 = url.find("//")
        vend = (url[idx3+2:idx2].capitalize())
    elif "mcule" in url:
        vend = "Mcule"
    elif "orderbb" in url:
        vend = "Emolecules"
    else:
        vend = (url[idx1+4:idx2].capitalize())
    if('Ps://' in vend): vend = vend[5:].capitalize()
    elif('P://' in vend): vend = vend[5:].capitalize()
    elif('Vitasmlab.biz' in vend): vend = 'Vitasmlab.biz' 

    return vend


# In[44]:

'''
affordable = []
vend = []

desiredlimit = 200.0
desiredsize = "10mg"

for b in buylist:
    for pr in b:
        if desiredsize in str(pr[0]):
            if float(pr[1]) <= desiredlimit:
                affordable.append(pr)
                vend.append(getVendorName(pr[2]))
                
affordable = np.array(affordable)
affordable = affordable[np.argsort(affordable[:,1])]


# ### Results

# In[52]:


# making df with basic info in it
data = {'ZINC ID': affordable[:,3],'Amount': affordable[:,0], 'Price ($)': affordable[:,1],'Vendor': vend,'Link': affordable[:,2]}
pd.set_option('display.max_colwidth', -1)
df = pd.DataFrame(data=data)


# In[53]:


# extracting price and amt columns from pds df
# getting rid of the text from the amt/package size
size = df["Amount"]
amt = []
units = []
for a in size:
    units.append(''.join(i for i in a if not i.isdigit()))
    amt.append(''.join(i for i in a if i.isdigit()))
prices = df["Price ($)"]


# In[54]:


# calculating the price per mg of each 
pricepmg = []
for i in range(len(amt)):
    if units[i] == "mg":
        val = float(prices[i])/float(amt[i])
        pricepmg.append(val)
    elif units[i] == "g":
        val = float(prices[i])/(float(amt[i])*1000)
        pricepmg.append(val)
        
#appending price per mg column to df
df.insert(loc=3, column='Price per mg ($/mg)', value=pricepmg) 


# In[55]:


df.sort_values(by = ["Price per mg ($/mg)"],inplace = True) #inplace actually updates the df
display(df)
'''
