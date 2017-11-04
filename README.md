# IDA2MASM
Create asm files from IDA, which meet the MASM grammar and can be re-assembled and run as the original version.

一、IDA中汇编与MASM的汇编语法上的差异：
1.MASM对于长度大于247的标示符报错name too long！另外，如果汇编代码一行超过512个字符也会报错line too long!（是不是觉得这MASM很low，反正我在心里已经对它吐槽几万遍了。）
2.IDA分析函数堆栈时生成了许多汇编宏，如果这些宏里面有自定义的数据结构，MASM不能识别。
3.IDA中字符串的自动命名容易相互冲突或与MASM关键字冲突。
4.IDA中imul指令包含负数时显示为十六进制的形式，而MASM可能不识别报错。
5.IDA可能会将一些全局变量命名为MASM中的关键字，如：str;Str;name;Name;neg;SubStr;add;aDD;aDC;aDDSS;mul;imul;inc;cwd;ptr;end;mask;width;lock;type;in;out;length;looped;offset;db;size等等。
语法杂项调整：
(1). retn->ret  
(2). rep retn->db 0F3h\nret  
(3).proc near/far->proc ;near/far 
(4). align xx->align (xx) 
(5).segment para public->segment para ;public  
(6).assume->;assume  
(7).call cs:->call qword ptr  
(8).jmp cs:->jmp qword ptr  
(9).删除cs:/ds:  
(10).movq rxx->movd rxx  
(11).140000000h->CodeStart-1000h  
(12).rva->imagerel  
(13).gs:30h->gs:[30h]  
(14).[rax+rbp]在MASM中要多占1字节的机器码（可能会导致短跳指令失败），改为[rbp+rax]则不会。
(15).标签全局化，”:”->”::” 

二、操作步骤：
1.In IDA, shift+F1, Ctrl+A, delete all types
2.press Alt+F7, choose 1.py
3.press Alt+F10, create asm file.
4.press Alt+F7, choose 2.py
