def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		pass
 
	try:
		import unicodedata
		unicodedata.numeric(s)
		return True
	except (TypeError, ValueError):
		pass
 
	return False

def findMatch(xlat, xlon, ylat, ylon, data):
    for f in data:
        # print(f)
        feat = f.split(", ")
        # print(feat)
        myx = str(feat[0]) + ", " + str(feat[1])
        myy = str(feat[2]) + ", " + str(feat[3])
        if len(feat) == 8:
            myy = str(feat[6]) + ", " + str(feat[7])
        xmatch = str(xlat) + ", " + str(xlon)
        ymatch = str(ylat) + ", " + str(ylon)
        if myx == xmatch and myy == ymatch:
            data.remove(f)
            return f