hack1:		STP X25, X26, [SP,#-0x90]	
			STP X27, X28, [SP,#-0x80]	
			STP X29, X30, [SP,#-0x70]	
mod:		add x25, 	{target}
			ldr x26,[x25]
			ldr w27,[x26,0x8]
			cmp w27,#4
			b.ne enemyhack
			cmp w8, 0xF
			b.eq save
			cmp w8, 0x10
			b.eq save
			b continue	
save:		bl hpfillcheck
			ldr x26,[x25,8]
			ldr x26,[x26,8]
			mov x29, (data_end - data_start)/16
			adrp x27, (data_start & 0xFFFFFFFF000) 
			add x27,x27, (data_start & 0xFFF)
			bl	findslot
continue:	LDP X25, X26, [SP,#-0x90]	
			LDP X27, X28, [SP,#-0x80]	
			LDP X29, X30, [SP,#-0x70]	
original:	{original}	
Return:		b code1+4
findslot:	ldr x28,  [X27]
			CBZ X28, Saveptr
			cmp x28,x25
			B.EQ Saveptr
			ADD X27,X27,#0x10
			SUB x29,x29,#1
			CBNZ X29, findslot
			b Done
Saveptr:	STP X25,X26, [X27]
Done:		ret
hpfillcheck:ldr x26,[x25,8]
			ldr w27,[x26,0xC]
			ldr w28, low
			cmp w27, w28
			b.lo return
			ldr w27, heroHP
			str w27,[x26,0xC]
return:		ret
enemyhack:	cmp w8, #0xE
			b.ne continue
			ldr w27,[x26,0xC]
			ldr w28, high
			cmp w27, w28
			b.hi continue
			ldr w28, low
			cmp w27, w28
			b.lo continue
			str w28,[x26,0xC]
			b continue
low: 		nop
high: 		nop
heroHP: 	nop		