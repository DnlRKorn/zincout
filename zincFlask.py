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
    cid = request.args.get('cid', default = "ZINC19795634", type = str)
    desiredlimit = request.args.get('price', default = '*', type = str)
    if(desiredlimit!='*'):
            try:
               desiredlimit = float(desiredlimit)
            except:
                return jsonify(["Price Not Float",'',''])
    desiredsize = request.args.get('size', default = '*', type = str)
    print('PRICE QUERY',cid,desiredlimit,desiredsize)
    easypeesy = zinc.makeEasy(cid)
    for i in range(5): 
        try: 
            buylist = zinc.makeBuyList(easypeesy)
            break
        except:
            print('cid %s missed %i'%(cid,i))
            continue

    affordable = []
    
    #affordable = []
    vend = []
    
    #desiredlimit = 200.0
    #desiredsize = "10mg"
    ''' 
    for b in buylist:
        for pr in b:
            if desiredsize in str(pr[0]):
                if float(pr[1]) <= desiredlimit:
                    affordable.append(pr)
                    vend.append(zinc.getVendorName(pr[2]))
                    
    affordable = np.array(affordable)
    affordable = affordable[np.argsort(affordable[:,1])]
    
    
    data = {'ZINC ID': affordable[:,3],'Amount': affordable[:,0], 'Price ($)': affordable[:,1],'Vendor': vend,'Link': affordable[:,2]}
    
    pd.set_option('display.max_colwidth', -1)
    df = pd.DataFrame(data=data)
    size = df["Amount"]
    amt = []
    units = []
    for a in size:
        units.append(''.join(i for i in a if not i.isdigit()))
        amt.append(''.join(i for i in a if i.isdigit()))
    prices = df["Price ($)"]
   ''' 
    
    # In[54]:
    
    
    # calculating the price per mg of each 
    pricepmg = []
    
        

    for b in buylist:
       for pr in b:
        # pr[0] = zinc.convertToMg(pr[0])
         if desiredsize=='*' or str(pr[0]) == desiredsize:
           if desiredlimit=='*' or float(pr[1]) <= desiredlimit:
              unit = ''.join(i for i in pr[0] if not i.isdigit())
              amt  = ''.join(i for i in pr[0] if i.isdigit())
         #     ratio = "%.2f" % (float(pr[1])/float(pr[0]))
              if unit == "mg":
                  val = float(pr[1])/float(amt)
              elif units[i] == "g":
                  val = float(pr[1])/(float(amt)*1000)
              vend = zinc.getVendorName(pr[2])
              affordable.append([pr[0],pr[1],pr[2],"%.2f"%val,vend])
    return jsonify(affordable)

@app.route('/')
def static_file():
        return app.send_static_file('index.html')
