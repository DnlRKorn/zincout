import zinc

cid = "ZINC19795634"

easypeesy = zinc.getVendorList(cid)
print(easypeesy)
buylist = zinc.makeBuyList(easypeesy)
print(buylist)
affordable = []

desiredlimit = 100.0
desiredsize = "10mg"

for b in buylist:
    for pr in b:
        if desiredsize=='*' or str(pr[0]) == desiredsize:
            if desiredlimit=='*' or float(pr[1]) <= desiredlimit:
                affordable.append(pr)
print(affordable)

