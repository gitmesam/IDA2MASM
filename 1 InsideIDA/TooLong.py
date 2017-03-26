count = 0

for name in Names():
	addr = name[0]
	oldname = name[1]
	if len(oldname) > 246:
		count += 1
		if count == 1:
			logfile = open(r"toolong.txt", "w")
		newname = "toolong"+str(count)
		MakeName(addr, newname)
		print >> logfile, hex(addr)+":\t"+newname+"\t->\t"+oldname

if count > 0:
	logfile.close()
	print str(count)+" names have been renamed, log in toolong.txt."
