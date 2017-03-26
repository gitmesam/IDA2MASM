map = {}

def TailExplore(addr):
	if Dword(addr) != 0 or Name(addr) != "":
		return False
	MakeUnknown(addr, 4, 2)
	MakeDword(addr)
	return True

def ParseTypeDes(addr):
	if addr in map.keys():
		return
	map[addr] = 1
	MakeQword(addr)
	addr+=8
	MakeQword(addr)	# void *space
	addr+=8
	MakeStr(addr, BADADDR)
	while Byte(addr) != 0:
		addr+=1
	addr+=1	# skip '\0'
	algnBase = addr
	while Byte(addr) == 0:
		addr+=1
	MakeAlign(algnBase, addr-algnBase, 0)

def ParseBaseClassDes(addr):
	if addr in map.keys():
		return
	map[addr] = 1
	MakeUnknown(addr, 28, 2)
	
	MakeDword(addr)
	OpOffEx(addr, 0, REF_OFF64|REFINFO_RVA, -1, 0, 0)
	ParseTypeDes(0x140000000 + Dword(addr))
	addr+=4
	
	for i in range(0, 5):
		MakeDword(addr)
		addr+=4
	
	MakeDword(addr)
	OpOffEx(addr, 0, REF_OFF64|REFINFO_RVA, -1, 0, 0)
	ParseClassHier(0x140000000 + Dword(addr))
	addr+=4
	
	while TailExplore(addr):
		addr+=4

def ParseBaseClassArray(addr, size):
	if addr in map.keys():
		return
	map[addr] = 1
	MakeUnknown(addr, size*4, 2)
	
	for i in range(0, size):
		MakeDword(addr)
		OpOffEx(addr, 0, REF_OFF64|REFINFO_RVA, -1, 0, 0)
		ParseBaseClassDes(0x140000000 + Dword(addr))
		addr+=4
	
	while TailExplore(addr):
		addr+=4

def ParseClassHier(addr):
	if addr in map.keys():
		return
	map[addr] = 1
	MakeUnknown(addr, 16, 2)
	
	for i in range(0, 4):
		MakeDword(addr)
		addr+=4
	
	OpOffEx(addr-4, 0, REF_OFF64|REFINFO_RVA, -1, 0, 0)
	ParseBaseClassArray(0x140000000 + Dword(addr-4), Dword(addr-8))
	
	while TailExplore(addr):
		addr+=4

def ParseObjLocator(addr):
	if addr in map.keys():
		return
	map[addr] = 1
	MakeUnknown(addr, 24, 2)
	
	ParseTypeDes(0x140000000 + Dword(addr+12))
	ParseClassHier(0x140000000 + Dword(addr+16))
	
	for i in range(0, 3):
		MakeDword(addr)
		addr+=4
	
	for i in range(0, 3):
		MakeDword(addr)
		OpOffEx(addr, 0, REF_OFF64|REFINFO_RVA, -1, 0, 0)
		addr+=4
	
	while TailExplore(addr):
		addr+=4

rdataStart = SegByBase(SegByName(".rdata"))
rdataEnd = SegEnd(rdataStart)
for addr in range(rdataStart, rdataEnd, 4):
	dname = Demangle(Name(addr), 0)
	if dname and dname.find("RTTI Complete Object Locator") != -1:
		ParseObjLocator(addr)
print "RTTI has been fixed."
