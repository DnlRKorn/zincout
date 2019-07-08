from flask import request,jsonify, Flask

import zinc

app = Flask(__name__)

@app.route('/price',methods=['GET'])
def my_route():
    cid = request.args.get('cid', default = "ZINC19795634", type = str)
    desiredlimit = request.args.get('price', default = '*', type = str)
    desiredsize = request.args.get('size', default = '*', type = str)
    easypeesy = zinc.getVendorList(cid)
    buylist = zinc.makeBuyList(easypeesy)
    affordable = []
    
    for b in buylist:
       for pr in b:
         if desiredsize=='*' or str(pr[0]) == desiredsize:
           if desiredlimit=='*' or float(pr[1]) <= desiredlimit:
                affordable.append(pr)
    print(affordable)
    return jsonify(affordable)

