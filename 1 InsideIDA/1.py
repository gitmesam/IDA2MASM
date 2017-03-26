import os
os.chdir(r"E:\Projects\Scripts\IDA2MASM\OneKey\1 InsideIDA")  # here change to the filepath
execfile("FixEH.py")
execfile("FixRTTI.py")
execfile("MakeQword.py")
execfile("Rename.py")
execfile("TooLong.py")
execfile("FixRVA.py")
execfile("FixOthers.py")
execfile("DelFuncFrame.py")
