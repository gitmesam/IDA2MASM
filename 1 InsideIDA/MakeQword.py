import re
pattern = re.compile(r"dq\s+offset")
cnt = 0
# recognize some hidden pointers, which startswith 0x14...
def SearchIn(segname):
	global cnt
	segStart = SegByBase(SegByName(segname))
	segEnd = SegEnd(segStart)
	for addr in range(segStart, segEnd, 8):
		if pattern.search(GetDisasm(addr)):
			continue
		value = Qword(addr)
		if value>=MinEA() and value<=MaxEA():	# a suspicious address
			# if there is no Xref to this, then it must be a pointer
			if RfirstB(addr+2) != BADADDR:
				continue
			if RfirstB(addr+4) != BADADDR:
				continue
			if RfirstB(addr+6) != BADADDR:
				continue
			if DfirstB(addr+2) != BADADDR:
				continue
			if DfirstB(addr+4) != BADADDR:
				continue
			if DfirstB(addr+6) != BADADDR:
				continue
			MakeUnknown(addr, 8, 2)
			MakeQword(addr)
			cnt+=1

SearchIn(".rdata")
SearchIn(".data")
print str(cnt)+" new \"dq offset\" have been found."
