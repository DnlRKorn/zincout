import requests
import itertools
from bs4 import BeautifulSoup

cid = "ZINC19795634"
cid = "ZINC06665770"
def getVendorList(cid):
  response = requests.get("http://zinc15.docking.org/substances/" + cid + "/catitems/subsets/for-sale/table.html")
  print(response.status_code) # 200 means it was downloaded successfully
  
  xml = BeautifulSoup(response.content,"lxml")
  para_1 = []
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
                if p[13:x-1] not in para_1:
                  para_1.append(p[13:x-1])
    except:
      continue
  return para_1
#print(getVendorList(cid))

def findEasyVendors(urlist):
    vendors = []
    goodvendors = ["caymanchem", "chem-space", "indofinechemical", "matrixscientific", "mcule", "molport", "apexbt", 
                  "abovchem", "bldpharm", "targetmol", "trc-canada", "chemscene", "medchemexp"]
    for row in urlist:
        for v in goodvendors:
            if v in row:
                vendors.append(row)
                break
    return vendors

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
    aff = [sizes,prices]
    return aff
#MedChem Expresss
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
                                    
    aff = [sizes,prices]
    return aff
#Chemscene
def chemscenePrice(compdurl):
    for i in range(len(compdurl)):
        if compdurl[i:i+11] == "productObj=":
            choiceID = compdurl[i+11:]

    #print(choiceID)
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
    #print('ven',vendorid)
    #print('cas',casNos)
    while '' in casNos:
        casNos.remove('')
    crossref = [casNos, vendorid]
    
    for i in range(len(crossref)):
        if crossref[1][i] == choiceID:
            correctcas = crossref[0][i]

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

    #print('size',sizes)
    #print(prices)
    aff = [sizes,prices]
    return aff
#MolPort
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
                    if ind[j:j+3] == ': "':
                        for k in range(len(ind)):
                            if ind[k:k+2] == '",':
                                sizes.append(ind[j+1:k].replace(" ",""))
            if '"price"' in ind:
                for j in range(len(ind)):
                    if ind[j:j+2] == ' "':
                        for k in range(len(ind)):
                            if ind[k:k+2] == '",':
                                prices.append(ind[j+2:k])
    aff = [sizes,prices]
    return aff
#Apex Biotech
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
    aff = [sizes,prices]
    return aff
#Toronto Research Chemicals - Canada
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
            if '<td class="optionscol">' in m:
                if '.' in m:
                    for j in range(len(m)):
                        if m[j:j+2] == "  ":
                            for i in range(len(m)):
                                if m[i] == "$":
                                    pr.append(m[i+1:j].replace(" ",""))
    prices = Remove(pr)
    aff = [sizes,prices]
#Matrix Scientific
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
        
    aff = [sizes,prices]
    return aff
#MCULE
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
    aff = [sizes,prices]
    return aff
#Targetmol
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
    aff = [sizes,prices]
    return aff
#Indofine Chemical
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
                    sizes.append(i[28:33].replace(" ",""))
                    prices.append(i[36:42])
    aff = [sizes,prices]
    return aff
#Cayman Chemical
def caymanPrice(urlid):
    
    sizes = []
    prices = []
    response = requests.get(urlid)
    xml = BeautifulSoup(response.content,"lxml")
    for z in range(0,20):
        try:
            paragraphs = xml.find_all("td")[z]
            lines = str(paragraphs).splitlines()
            for l in lines:
                para = str(l).splitlines()
                for p in para:
                    if p[:15] == '<td class="size':
                        idx1 = p.find('\xc2\xa0\xc2\xa0\xc2\xa0\xc2\xa0\xc2\xa0')
                        idx2 = p.find('mg') 
                        sizes.append(p[idx1+10:idx2+2].replace(' ',''))
                    elif p[:16] == '<td class="price':
                        prices.append(p[36:].replace(",",""))
        except:
            continue

    aff = [sizes,prices]
    return aff

def makeBuyList(easypeesy):
  buylist = []
  for url in easypeesy:
    if "abovchem" in url:
        aff = abovchemPrice(url)
        length = len(aff)
        rep = list(itertools.repeat(url, length))
        aff_2 = zip(aff[0],aff[1],rep)
        buylist.extend(aff_2)
    if "cayman" in url:
        aff = caymanPrice(url)
        length = len(aff)
        rep = list(itertools.repeat(url, length))
        aff_2 = zip(aff[0],aff[1],rep)
        buylist.extend(aff_2)
    elif "indofine" in url:
        aff = indofinePrice(url)
        length = len(aff)
        rep = list(itertools.repeat(url, length))
        aff_2 = zip(aff[0],aff[1],rep)
        buylist.extend(aff_2)
    elif "mcule" in url:
        aff = mculePrice(url)
        length = len(aff)
        rep = list(itertools.repeat(url, length))
        aff_2 = zip(aff[0],aff[1],rep)
        buylist.extend(aff_2)
    elif "matrixscientific" in url:
        aff = matrixPrice(url)
        length = len(aff)
        rep = list(itertools.repeat(url, length))
        aff_2 = zip(aff[0],aff[1],rep)
        buylist.extend(aff_2)
    elif "apxbt" in url:
        aff = apxbtPrice(url)
        length = len(aff)
        rep = list(itertools.repeat(url, length))
        aff_2 = zip(aff[0],aff[1],rep)
        buylist.extend(aff_2)
    elif "molport" in url:
        aff = molportPrice(url)
        length = len(aff)
        rep = list(itertools.repeat(url, length))
        aff_2 = zip(aff[0],aff[1],rep)
        buylist.extend(aff_2)
    elif "chemscene" in url:
        aff = chemscenePrice(url)
        length = len(aff)
        rep = list(itertools.repeat(url, length))
        aff_2 = zip(aff[0],aff[1],rep)
        buylist.extend(aff_2);
    elif "medchemexp" in url:
        aff = medchemexpPrice(url)
        length = len(aff)
        rep = list(itertools.repeat(url, length))
        aff_2 = zip(aff[0],aff[1],rep)
        buylist.extend(aff_2)
    elif "targetmol" in url:
        aff = targetmolPrice(url)
        length = len(aff)
        rep = list(itertools.repeat(url, length))
        aff_2 = zip(aff[0],aff[1],rep)
        buylist.extend(aff_2)
  return buylist

