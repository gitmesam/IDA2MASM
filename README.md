# IDA2MASM
Create asm files from IDA, which meet the MASM grammar and can be re-assembled and run as the original version.

1. The difference in assembly syntax between assembly in IDA and MASM:
   1. MASM reports an error name too long for identifiers with a length greater than 247! In addition, if a line of assembly code exceeds 512 characters, an error line too long! will be reported (Do you think this MASM is very low? Anyway, I have complained about it tens of thousands of times in my heart.)
   2. IDA generates a lot of code when analyzing the function stack. Assembly macros. If these macros contain custom data structures, MASM cannot recognize them.
   3. The automatic naming of strings in IDA is prone to conflict with each other or with the MASM keyword.
   4. When the imul instruction in IDA contains a negative number, it is displayed in hexadecimal form, and MASM may not recognize it and report an error.
   5. IDA may name some global variables as keywords in MASM, such as: str;Str;name;Name;neg;SubStr;add;aDD;aDC;aDDSS;mul;imul;inc;cwd;ptr;end ;mask;width;lock;type;in;out;length;looped;offset;db;size, etc.
   Miscellaneous syntax adjustments: 
(1). retn->ret
(2). rep retn->db 0F3h\nret
(3).proc near/far->proc ;near/far (4).align xx->align (xx) (5).segment para public->segment para ;public
(6).assume->;assume
(7).call cs:->call qword ptr
(8).jmp cs:->jmp qword ptr
(9).Delete cs:/ds:
(10).movq rxx->movd rxx
(11).140000000h->CodeStart-1000h
(12).rva->imagerel
(13).gs:30h->gs:[30h]
(14).[rax+rbp] occupies 1 more byte of machine code in MASM (which may cause the short jump instruction to fail), but changing it to [rbp+rax] will not.
(15). Label globalization, ":"->"::"

2. Operation steps:
1.In IDA, shift+F1, Ctrl+A, delete all types
2.press Alt+F7, choose 1.py
3.press Alt+F10, create asm file.
4.press Alt+F7, choose2.py
