# copied from hacktrack/loaders.py

import math, pandas

# if the plot looks wrong, don't forget to check the aspect ratio and force it like this:
#plt.figure(figsize=(10, 20))
#plt.subplot(111, aspect="equal")
lng0, lat0 = 0, 0  # make things easier, we don't want different origins really
nyfac0, exfac0 = 0, 0  # multiply by 1/60000 to find the precision of the IGC file
def processQaddrelEN(pQ, fd=None):
    global lng0, lat0, nyfac0, exfac0
    if type(pQ) == str and pQ == "setorigin":
        lng0, lat0 = fd
        return
    if fd is None:
        if len(pQ) != 0 and lng0 == 0 and lat0 == 0:
            ph = pQ.iloc[min(10, len(pQ)-1)]    # set the origin we use for all the conversions
            lng0, lat0 = ph.lng, ph.lat
    else: 
        if len(pQ) != 0 and fd.lng0 == 0 and fd.lat0 == 0:
            ph = pQ.iloc[min(10, len(pQ)-1)]    # set the origin we use for all the conversions
            fd.lng0, fd.lat0 = ph.lng, ph.lat
        lng0, lat0 = fd.lng0, fd.lat0
    earthrad = 6378137
    nyfac = 2*math.pi*earthrad/360
    exfac = nyfac*math.cos(math.radians(lat0))
    if fd:
        fd.nyfac = nyfac
        fd.exfac = exfac
    nyfac0 = nyfac
    exfac0 = exfac
        
    # vector computations
    pQ["x"] = (pQ.lng - lng0)*exfac  
    pQ["y"] = (pQ.lat - lat0)*nyfac
    
    pQmean = pQ.mean()
    lenpQ = len(pQ)
    pQ = pQ[(abs(pQ.lat - pQmean.lat)<1) & (abs(pQ.lng - pQmean.lng)<1)]
    if lenpQ != len(pQ):
        print("despiked", lenpQ-len(pQ), "points from Q")
    return pQ

def GLoadIGC(fname):
    fin = open(fname, "rb")   # sometimes get non-ascii characters in the header
    IGCdatetime0 = None
    recs, tind = [ ], [ ]
    hfcodes = { }
    for l in fin:
        if l[:5] == b'HFDTE':    #  HFDTE090317
            l = l.decode("utf8") 
            if l.find(":") != -1:
                l = l[l.find(":")+1:]
            else:
                l = l[5:]
            hfcodes["HFDTE"] = l
            IGCdatetime0 = pandas.Timestamp("20"+l[4:6]+"-"+l[2:4]+"-"+l[0:2])
        elif l[:2] == b'HF' and l.find(b":") != -1:
            k, v = l[2:].split(b":", 1)
            if v.strip():
                hfcodes[k.decode()] = v.decode().strip()
        elif l[0] == ord("B"):   #  B1523345257365N00308169WA0030800393000
            utime = int(l[1:3])*3600+int(l[3:5])*60+int(l[5:7])
            latminutes1000 = int(l[7:9])*60000+int(l[9:11])*1000+int(l[11:14])
            lngminutes1000 = (int(l[15:18])*60000+int(l[18:20])*1000+int(l[20:23]))*(l[23]==ord('E') and 1 or -1) 
            s = int(l[35:]) if len(l) >= 40 else 0
            recs.append((latminutes1000/60000, lngminutes1000/60000, int(l[25:30]), int(l[30:35]), s, utime*1000))
            tind.append(IGCdatetime0 + pandas.Timedelta(seconds=utime))
    return pandas.DataFrame.from_records(recs, columns=["lat", "lng", "alt", "altb", "s", "u"], index=tind), hfcodes

