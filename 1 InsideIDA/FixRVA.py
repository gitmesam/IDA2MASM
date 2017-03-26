import re

def fix(addr):
	size = ItemSize(addr)
	MakeUnknown(addr, size, 0)
	MakeArray(addr, size-4)
	pos = addr + size - 4
	MakeDword(pos)
	OpOffEx(pos, 0, REF_OFF64|REFINFO_RVA, -1, 0, 0)
	pos2 = 0x140000000+Dword(pos)
	if GetDisasm(pos2).split(";")[0].find("- 140000000h") != -1:
		OpOffEx(pos2, 0, REF_OFF64|REFINFO_RVA, -1, 0, 0)

pat1 = re.compile(r"lea\s+([a-z0-9]+),\s*__ImageBase")
pat2 = re.compile(r"\[([a-z0-9]+)\+[a-z0-9]+(\*[0-9]+)?\+([0-9A-F]+)h\]")
pat3 = re.compile(r"mov\s+([a-z0-9]+),\s*([a-z0-9]+)")

keyRegs = []
addr = SegByBase(SegByName(".text"))
funcEnd = GetFunctionAttr(addr, FUNCATTR_END)
while addr != BADADDR:
	if addr > funcEnd:
		funcEnd = GetFunctionAttr(addr, FUNCATTR_END)
		keyRegs = []
	line = GetDisasm(addr)
	if line.find("- 140000000h") != -1 or line.find("ds:rva") != -1:
		fix(addr)
		MakeComm(addr, line)
	else:
		m1 = pat1.search(line)
		m2 = pat2.search(line)
		m3 = pat3.search(line)
		if m1:
			keyRegs.append(m1.group(1))
		elif m2:
			firstReg = m2.group(1)
			offset = int(m2.group(3), 16)
			if firstReg in keyRegs and offset>0x1000:
				fix(addr)
				MakeComm(addr, line)
		elif m3:
			firstReg = m3.group(1)
			secReg = m3.group(2)
			if firstReg in keyRegs:
				keyRegs.remove(firstReg)
			elif secReg in keyRegs:
				keyRegs.append(firstReg)
	addr = FindCode(addr, 1)
print "ImageBase Addresses have been fixed."
