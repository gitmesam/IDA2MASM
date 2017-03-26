import re

pat1 = re.compile(r"\sproc\s+(near|far)")
pat2 = re.compile(r"^[\w$]+:")
pat3 = re.compile(r"(call|jmp)\s+cs:__")
pat4 = re.compile(r"\s(d|c)s:")
pat5 = re.compile(r"gs:([0-9]+h?)")
pat6 = re.compile(r"(\W)rva(\s+)")

oldfile = open(r"X64Test2.asm","r")
newfile = open(r"X64Test3.asm","w")
for line in oldfile:
	newline = line
	line = line.strip()
	
	if line.startswith("retn"):
		newline = newline.replace("retn", "ret")
	elif pat1.search(line):
		newline = pat1.sub(" proc", newline)
	elif pat2.search(line):
		newline = newline.replace(":", "::", 1)
	elif pat3.search(line):
		newline = newline.replace("cs:", "qword ptr ")
	elif line.startswith("assume") or line.find("NULL_THUNK_DATA") != -1:
		continue
	elif line.startswith("align"):
		newline = "align ("+line[6:]+")\n"
	elif pat4.search(line):
		newline = pat4.sub(" ", newline)
	elif line.find("para public") != -1:
		newline = newline.replace("para public", "para ;public")
	elif pat5.search(line):
		newline = pat5.sub("gs:[\g<1>]", newline)
	
	newline = newline.replace("movq\tr", "movd\tr")
	newline = newline.replace("__ImageBase", "(CodeStart - 1000h)")
	newline = pat6.sub("\g<1>imagerel\g<2>", newline)
	newline = newline.replace("[rax+rbp]", "[rbp+rax]")
	if len(newline) > 511:	# line too long
		newline = newline[:510]+"\n"
	
	newfile.write(newline)
oldfile.close()
newfile.close()
print "Grammar adjusted."
