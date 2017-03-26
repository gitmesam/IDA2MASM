def DelFuncFrame(addr):
	id = GetFrame(addr)
	try:
		offset = GetLastMember(id)	# id maybe NoneType
	except:
		return
	while offset != BADADDR:
		DelStrucMember(id, offset)
		offset = GetLastMember(id)

funcAddr = NextFunction(0)
while funcAddr != BADADDR:
	DelFuncFrame(funcAddr)
	funcAddr = NextFunction(funcAddr)

print "Functions frame have been removed."
