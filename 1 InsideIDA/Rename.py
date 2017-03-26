keywords = ["str", "substr", "name", "neg", "add", "adc", "addss", "mul",
"imul", "inc", "dec", "cwd", "ptr", "end", "mask", "width", "length",
"loop", "looped", "offset", "db", "size", "lock", "in", "out", "type"]	# and so on, add if you need.
map = {}

for string in Strings():
	addr = string.ea
	isStr = True
	for pos in range(addr, addr+string.length):
		if Byte(pos) > 127:	# not ascii
			isStr = False
			MakeUnkn(addr, 0)
			break
	if isStr:
		MakeName(addr, "str_%x"%(addr))
		if string.type == 3:	# delete Unicode string
			MakeUnkn(addr, 0)
		elif string.length >= 3:
			MakeStr(addr, BADADDR)

for name in Names():
	addr = name[0]
	oldname = name[1].lower()
	if oldname in keywords or oldname in map.keys():
		MakeName(addr, "gbl_%x"%(addr))
	else:
		map[oldname] = True
print "Renamed some names."
