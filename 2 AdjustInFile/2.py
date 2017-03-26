import os
os.chdir(r"E:\Projects\Scripts\IDA2MASM\OneKey")
oldfile = open("X64Test.asm", "r")
newfile = open("X64Test2.asm", "w")
skip = True

for line in oldfile:
	if line.startswith(("_text\t\tsegment", "_data\t\tsegment", "_rdata\t\tsegment", "_pdata\t\tsegment")):
		skip = False
	if line.startswith(("_rsrc\t\tsegment", "_reloc\t\tsegment")):
		skip = True
	if not skip:
		newfile.write(line)


execfile("AdjustGrammar.py")
