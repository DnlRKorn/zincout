from flask import request,jsonify, Flask
import re

#import zinc
import ZINCQuery_09_09_19 as zinc

app = Flask(__name__)

def convertToMg(x):
    mult = 1000
    if('mg' in x or 'MG' in x or 'Mg' in x): mult = 1
    if('kg' in x or 'KG' in x or 'Kg' in x): mult = 1000000
    r = re.search(r'\d+',x)
    if(r==None):return "N\A"
    else: return str(mult * int(r.group(0)))

@app.route('/price',methods=['GET'])
def my_route():
    print('hi')
    cid = request.args.get('cid', default = "ZINC19795634", type = str)
    print(cid)
    cids = cid.split('\n')
    print(cids)
    desiredlimit = request.args.get('price', default = '*', type = str)
    if(desiredlimit!='*'):
            try:
               desiredlimit = float(desiredlimit)
            except:
                return jsonify(["Price Not Float",'',''])
    desiredsize = request.args.get('size', default = '*', type = str)
    affordable = []
    notavail = set() 
    for cid in cids:
       if('ZINC' not in cid):continue
       cid = cid.strip()
       print('PRICE QUERY',cid,desiredlimit,desiredsize)
       [easypeesy,noteasy] = zinc.makeEasy(cid)
       for i in range(5): 
           try: 
               buylist = zinc.makeBuyList(easypeesy)
               break
           except:
               print('cid %s missed %i'%(cid,i))
               continue

       

       debug = True
       for b in buylist:
          for pr in b:
            print('pr',pr)
           # pr[0] = zinc.convertToMg(pr[0])
            if desiredsize=='*' or str(pr[0]) == desiredsize:
              if desiredlimit=='*' or float(pr[1]) <= desiredlimit:
                 unit = ''.join(i for i in pr[0] if not (i.isdigit() or i=='.'))
                 amt  = ''.join(i for i in pr[0] if (i.isdigit() or i=='.'))
            #     ratio = "%.2f" % (float(pr[1])/float(pr[0]))
                 if('http://www.enaminestore.com/catalog/BBV-85460309' in pr[2]):
                     print(unit)
                 if(len(unit)==0):continue
                 elif unit == "mg":
                     val = float(pr[1])/float(amt)
                 elif unit[i] == "g":
                     val = float(pr[1])/(float(amt)*1000)
                 else:
                     continue
                 val = "%.2f"%val
                 vend = zinc.getVendorName(pr[2])
                 affordable.append([pr[0],pr[1],pr[2],val,vend,pr[3]])
       for x in noteasy:
           link = x[0]
           vend = zinc.getVendorName(link)
           notavail.add((link,vend,cid))
       print(cid,'Done')

    return jsonify({"available":affordable,"notavailable":list(notavail)})

@app.route('/')
def static_file():
        return app.send_static_file('index.html')
