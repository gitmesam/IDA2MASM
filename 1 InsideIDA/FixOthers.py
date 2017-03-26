addr = SegByBase(SegByName(".text"))
endAddr = SegEnd(addr)
while addr <= endAddr:
	line = GetDisasm(addr).split(";")[0].strip()
	if line.find(", 0FFFFFFF") != -1:
		OpDecimal(addr, 2)
		OpSign(addr, 2)
	elif line == "rep retn":
		MakeUnknown(addr, 2, 0)
		MakeByte(addr)
		MakeCode(addr+1)
		MakeComm(addr, line)
	elif line.startswith("align"):
		MakeUnkn(addr, 0)
		MakeArray(addr, FindCode(addr, 1)-addr)
		MakeName(addr, "aln_%x"%(addr))
	addr = FindExplored(addr, 1)

def shrink(segname):
	addr = SegByBase(SegByName(segname))
	segEnd = SegEnd(addr)
	while addr < segEnd:
		MakeArray(addr, FindExplored(addr, 1)-addr)
		addr = FindUnexplored(addr, 1)

shrink(".data")
shrink(".rdata")
print "Fix some MASM's grammar details."
