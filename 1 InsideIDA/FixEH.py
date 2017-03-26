map = {}

def ParseCHandlerData(addr):
	MakeDword(addr)
	arrSize = Dword(addr)
	addr+=4
	
	# MakeUnknown(addr, arrSize * 16, 2)
	for i in range(0, arrSize):
		MakeStructEx(addr, -1, "C_SCOPE_TABLE")
		addr += 16
	return addr

def ParseUnwindInfo(infoAddr):
	if infoAddr in map.keys():
		return True
	map[infoAddr] = 1
	
	if infoAddr == 0x140000000:
		return False
	
	MakeName(infoAddr, "edata_%x"%(infoAddr))
	flag = Byte(infoAddr) >> 3
	numOfCodes = Byte(infoAddr + 2)
	
	# MakeUnknown(addr, 4+2*numOfCodes+8, 2)
	infoAddr+=4
	
	for i in range(0, numOfCodes):
		MakeStructEx(infoAddr, -1, "UNWIND_CODE")
		infoAddr+=2
	if numOfCodes%2 == 1:
		infoAddr += 2
	if flag >= 4:	# RUNTIME_FUNCTION
		# MakeUnknown(infoAddr, 12, 2)
		MakeStructEx(infoAddr, -1, "RUNTIME_FUNCTION")
		infoAddr+=12
	elif flag != 0:	# has SEH
		lshName = Name(0x140000000 + Dword(infoAddr))
		MakeDword(infoAddr)
		OpOffEx(infoAddr, 0, REF_OFF64|REFINFO_RVA, -1, 0, 0)	# language specific handler
		infoAddr+=4
		if lshName.find("CxxFrameHandler") != -1:
			MakeDword(infoAddr)
			OpOffEx(infoAddr, 0, REF_OFF64|REFINFO_RVA, -1, 0, 0)
			ParseFuncInfo(0x140000000 + Dword(infoAddr))
		elif lshName.find("C_specific_handler") != -1:
			ParseCHandlerData(infoAddr)
		elif lshName == "__GSHandlerCheck":
			MakeDword(infoAddr)
		elif lshName == "__GSHandlerCheck_SEH":
			infoAddr = ParseCHandlerData(infoAddr)
			MakeDword(infoAddr)
		elif lshName == "__GSHandlerCheck_EH":
			MakeDword(infoAddr)
			OpOffEx(infoAddr, 0, REF_OFF64|REFINFO_RVA, -1, 0, 0)
			ParseFuncInfo(0x140000000 + Dword(infoAddr))
			infoAddr+=4
			MakeDword(infoAddr)
	return True

def ParseFuncInfo(funcInfoAddr):
	if funcInfoAddr in map.keys():
		return
	map[funcInfoAddr] = 1
	
	# MakeUnknown(funcInfoAddr, 40, 2)
	
	MakeName(funcInfoAddr, "funcInfo_%x"%(funcInfoAddr))
	MakeStructEx(funcInfoAddr, -1, "FuncInfo")
	
	unwindArrSize = Dword(funcInfoAddr+4)
	if unwindArrSize > 0:
		base1 = 0x140000000 + Dword(funcInfoAddr+8)
		MakeName(base1, "unwindMap_%x"%(base1))
		for r1 in range(0, unwindArrSize):
			ParseUnwindArray(base1 + r1*8)
	
	tryBlockArrSize = Dword(funcInfoAddr+12)
	if tryBlockArrSize > 0:
		base2 = 0x140000000 + Dword(funcInfoAddr+16)
		MakeName(base2, "tryBlock_%x"%(base2))
		for r2 in range(0, tryBlockArrSize):
			ParseTryBlockArray(base2 + r2*20)
	
	stateArrSize = Dword(funcInfoAddr+20)
	if stateArrSize > 0:
		base3 = 0x140000000 + Dword(funcInfoAddr+24)
		MakeName(base3, "ip2state_%x"%(base3))
		for r3 in range(0, stateArrSize):
			ParseIP2StateArray(base3 + r3*8)
	
	ParseExpectedList(0x140000000 + Dword(funcInfoAddr+32))

def ParseUnwindArray(addr):
	if addr in map.keys():
		return
	map[addr] = 1
	
	# MakeUnknown(addr, 8, 2)
	MakeStructEx(addr, -1, "UnwindMapEntry")

def ParseTryBlockArray(addr):
	if addr in map.keys():
		return
	map[addr] = 1
	
	# MakeUnknown(addr, 20, 2)
	MakeStructEx(addr, -1, "TryBlockMapEntry")
	
	size = Dword(addr+12)
	if size > 0:
		base = 0x140000000 + Dword(addr+16)
		MakeName(base, "catchBlock_%x"%(base))
		for r4 in range(0, size):
			ParseCatchBlockArray(base + r4*20)

def ParseCatchBlockArray(addr):
	if addr in map.keys():
		return
	map[addr] = 1
	
	# MakeUnknown(addr, 20, 2)
	MakeStructEx(addr, -1, "HandlerType")

def ParseIP2StateArray(addr):
	if addr in map.keys():
		return
	map[addr] = 1
	
	# MakeUnknown(addr, 8, 2)
	MakeStructEx(addr, -1, "IP2StateEntry")

def ParseExpectedList(addr):
	if addr == 0x140000000 or addr in map.keys():
		return
	map[addr] = 1
	
	# MakeUnknown(addr, 8, 2)
	MakeStructEx(addr, -1, "ESTypeList")
	size = Dword(addr)
	if size > 0:
		base = 0x140000000 + Dword(addr+4)
		MakeName(base, "expectedList_%x"%(base))
		for i in range(0, size):
			MakeStructEx(base + i*20, -1, "HandlerType")

sid = AddStrucEx(-1, "FuncInfo", 0)
memNames = ["magicNumber", "maxState", "pUnwindMap", "nTryBlocks", "pTryBlockMap",
"nIPMapEntries", "pIPtoStateMap", "unknown", "pESTypeList", "EHFlags"]
memComments = ["compiler version", "number of entries in unwind table", 
"table of unwind destructors", "number of try blocks in the function", 
"mapping of catch blocks to try blocks","number of IP2State entries", "IPtoState map", 
"unknown", "expected exceptions list", "bit 0 set if function was compiled with /EHs"]
for i in range(0, 10):
	if i%2 == 0 and i > 0:
		AddStrucMember(sid, memNames[i], i*4, 0x25500400, 0X140000000, 4, 0XFFFFFFFFFFFFFFFF, 0, 0x000039)
	else:
		AddStrucMember(sid, memNames[i], -1, (FF_DWRD|FF_DATA), -1, 4)
	SetMemberComment(sid, i*4, memComments[i], 1)

sid = AddStrucEx(-1, "UnwindMapEntry", 0)
AddStrucMember(sid, "toState", -1, (FF_DWRD|FF_DATA), -1, 4)
SetMemberComment(sid, 0, "target state", 1)
AddStrucMember(sid, "action", 4, 0x25500400, 0X140000000, 4, 0XFFFFFFFFFFFFFFFF, 0, 0x000039)
SetMemberComment(sid, 4, "action to perform (unwind funclet address)", 1)

sid = AddStrucEx(-1, "IP2StateEntry", 0)
AddStrucMember(sid, "action", 0, 0x25500400, 0X140000000, 4, 0XFFFFFFFFFFFFFFFF, 0, 0x000039)
SetMemberComment(sid, 0, "action to perform", 1)
AddStrucMember(sid, "toState", -1, (FF_DWRD|FF_DATA), -1, 4)
SetMemberComment(sid, 0, "target state", 1)

sid = AddStrucEx(-1, "TryBlockMapEntry", 0)
memNames = ["tryLow", "tryHigh", "catchHigh", "nCatches"]
memComments = ["", "", "highest state inside catch handlers of this try", "number of catch handlers"]
for i in range(0, 4):
	AddStrucMember(sid, memNames[i], -1, (FF_DWRD|FF_DATA), -1, 4)
	SetMemberComment(sid, i*4, memComments[i], 1)
AddStrucMember(sid, "pHandlerArray", 16, 0x25500400, 0X140000000, 4, 0XFFFFFFFFFFFFFFFF, 0, 0x000039)
SetMemberComment(sid, 16, "catch handlers table", 1)

sid = AddStrucEx(-1, "HandlerType", 0)
AddStrucMember(sid, "adjectives", -1, (FF_DWRD|FF_DATA), -1, 4)
SetMemberComment(sid, 0, "0x01: const, 0x02: volatile, 0x08: reference", 1)
AddStrucMember(sid, "pType", 4, 0x25500400, 0X140000000, 4, 0XFFFFFFFFFFFFFFFF, 0, 0x000039)
SetMemberComment(sid, 4, "RTTI descriptor of the exception type. 0=any (ellipsis)", 1)
AddStrucMember(sid, "dispCatchObj", -1, (FF_DWRD|FF_DATA), -1, 4)
SetMemberComment(sid, 8, "ebp-based offset of the exception object in the function stac", 1)
AddStrucMember(sid, "addressOfHandler", 12, 0x25500400, 0X140000000, 4, 0XFFFFFFFFFFFFFFFF, 0, 0x000039)
SetMemberComment(sid, 12, "address of the catch handler code", 1)
AddStrucMember(sid, "unknown", -1, (FF_DWRD|FF_DATA), -1, 4)

sid = AddStrucEx(-1, "ESTypeList", 0)
AddStrucMember(sid, "nCount", -1, (FF_DWRD|FF_DATA), -1, 4)
SetMemberComment(sid, 0, "number of entries in the list", 1)
AddStrucMember(sid, "pTypeArray", 4, 0x25500400, 0X140000000, 4, 0XFFFFFFFFFFFFFFFF, 0, 0x000039)
SetMemberComment(sid, 4, "list of exceptions", 1)

sid = GetStrucIdByName("C_SCOPE_TABLE")
SetMemberType(sid, 12, 0x25500400, 0X140000000, 4, 0XFFFFFFFFFFFFFFFF, 0, 0x000039)

startEA = SegByBase(SegByName(".pdata"))
endEA = SegEnd(startEA)
# MakeUnknown(0x1421215b0, 0x161e38, 2)	# delete all data in exception rdata section
for addr in range(startEA + 8, endEA, 12):
	if ParseUnwindInfo(0x140000000 + Dword(addr)) == False:
		print "The SEH/EH autoanalysis has been finished."
		break
