from flask import request,jsonify, Flask

#import zinc
import ZINCQuery_updated as zinc

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
    easypeesy = zinc.makeEasy(cid)
    buylist = zinc.makeBuyList(easypeesy)
    affordable = []
    
    for b in buylist:
       for pr in b:
         if desiredsize=='*' or str(pr[0]) == desiredsize:
           if desiredlimit=='*' or float(pr[1]) <= desiredlimit:
              affordable.append([pr[0],pr[1],pr[2]])
    print(affordable)
    affordable.sort(key=lambda x: float(x[1]))
    print(affordable)
    return jsonify(affordable)

@app.route('/')
def static_file():
        return app.send_static_file('index.html')
