from flask import request,jsonify, Flask

import zinc

app = Flask(__name__)

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
    easypeesy = zinc.getVendorList(cid)
    buylist = zinc.makeBuyList(easypeesy)
    affordable = []
    
    for b1,b2,b3 in buylist:
       pr = [b1,b2,b3]
       print(pr)
       if desiredsize=='*' or str(pr[0]) == desiredsize:
         if desiredlimit=='*' or float(pr[1]) <= desiredlimit:
            affordable.append(pr)
    print(affordable)
    return jsonify(affordable)

@app.route('/')
def static_file():
        return app.send_static_file('index.html')
