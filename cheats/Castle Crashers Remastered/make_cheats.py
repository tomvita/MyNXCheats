"""Castle Crashers Remastered (010001300D14A000, BID 9CF2AF5B7FD156BC) cheats on the AS2 SetMember call.

M+47EA8 `blr x8` is object->SetMember(x0 = object, w1 = member name id, x2 = new value) in the VM's
set-member opcode. A value: tag u32 at +8 (0x10 float, 4 int, 2 bool); a new value's payload is at +0x10,
a stored member value's at +0xC. An object's members: +8 count, +0x10 sorted u16 name ids, +0x18 value
pointers. Players are the objects with a `gold` member.

One hook cheat (hook + cave), and feature cheats that each set one flag word in the cave in the code-patch
block form (C046E5E0 never-run block holds the original 0, so turning a feature off writes 0 back).
"""
from keystone import Ks, KS_ARCH_ARM64, KS_MODE_LITTLE_ENDIAN
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

import sys

# Per build: main offsets and the script's member name IDs (an update that changes the scripts can shift
# the IDs: 1.0.7 inserted two names between `y` and `gold`, so every ID from gold up is +2).
VERSIONS = {
    '9CF2AF5B7FD156BC': dict(    # 1.0.0
        name='1.0.0', HOOK=0x47EA8, BACK=0x47EAC, DISP=0x53250, BASE=0x5FA30,
        CAVE=0x279800, FLAGS=0x279F00,    # zero tail of main's r-x: M+2797B0..M+27A000
        ID_X=0x79, ID_Y=0x7C, ID_GOLD=0x1A9, ID_HEALTH=0x1AD, ID_MAG=0x1AE, ID_EXP=0x53E,
        ID_STR=0x544, ID_DEF=0x545, ID_AGI=0x546, ID_POTS=0x548, ID_MAGIC_CUR=0x561),
    '5E85F631BFA6930E': dict(    # 1.0.7
        name='1.0.7', HOOK=0x120EF0, BACK=0x120EF4, DISP=0x12C540, BASE=0x139500,
        CAVE=0x276400, FLAGS=0x276F00,    # zero tail of main's r-x: M+276330..M+277000
        ID_X=0x79, ID_Y=0x7C, ID_GOLD=0x1AB, ID_HEALTH=0x1AF, ID_MAG=0x1B0, ID_EXP=0x540,
        ID_STR=0x546, ID_DEF=0x547, ID_AGI=0x548, ID_POTS=0x54A, ID_MAGIC_CUR=0x563),
}
BID = next((a.upper() for a in sys.argv[1:] if a.upper() in VERSIONS), '9CF2AF5B7FD156BC')
V = VERSIONS[BID]
HOOK, BACK, DISP, BASE, CAVE, FLAGS = V['HOOK'], V['BACK'], V['DISP'], V['BASE'], V['CAVE'], V['FLAGS']
ORIG = 0xD63F0100           # blr x8
ID_HEALTH, ID_GOLD, ID_MAGIC_CUR = V['ID_HEALTH'], V['ID_GOLD'], V['ID_MAGIC_CUR']
ID_X, ID_Y = V['ID_X'], V['ID_Y']   # set all the time while a player moves: max gold / stats ride on them
GOLD_MAX = 99999
ID_EXP = V['ID_EXP']
EXP_MUL = 10
ID_STR, ID_DEF, ID_AGI, ID_MAG = V['ID_STR'], V['ID_DEF'], V['ID_AGI'], V['ID_MAG']
STAT_MAX, STAT_MAX_F = 25, 0x41C80000    # 25 and 25.0f
ID_POTS = V['ID_POTS']      # healthpots; bombs and beefies are the next two IDs

FEATURES = [  # (flag index, cheat name)
    (0, 'Infinite health (players)'),
    (1, 'Infinite magic (players)'),
    (2, 'Potions, bombs and beefies never run out'),
    (3, 'Gold never goes down (free shopping)'),
    (4, 'One-hit kills (anything with health that is not a player)'),
    (5, 'Max gold (99999)'),
    (6, 'EXP x10'),
    (7, 'Max stats (strength, magic, defense, agility 25)'),
]

src = f"""
    // only the members the cheats care about
    cmp w1, #{ID_HEALTH:#x}
    b.eq interesting
    cmp w1, #{ID_MAGIC_CUR:#x}
    b.eq interesting
    cmp w1, #{ID_GOLD:#x}
    b.eq interesting
    sub w9, w1, #{ID_POTS:#x}
    cmp w9, #2
    b.ls interesting
    cmp w1, #{ID_X:#x}
    b.eq interesting
    cmp w1, #{ID_Y:#x}
    b.eq interesting
    cmp w1, #{ID_EXP:#x}
    b.eq interesting
    b call
interesting:
    // only objects whose SetMember (x8, loaded by the game) is the display object's (DISP)
    // or the base object's (BASE): both keep members as count +8, sorted ids +0x10, values +0x18
    adr x16, call                   // patched below to adrp x16, page of DISP
    add x16, x16, #{DISP & 0xFFF:#x}
    cmp x8, x16
    b.eq layout_ok
    adr x17, call                   // patched below to adrp x17, page of BASE
    add x17, x17, #{BASE & 0xFFF:#x}
    cmp x8, x17
    b.ne call
layout_ok:
    ldr x9, [x0, #0x10]
    cbz x9, call
    ldr w11, [x0, #8]
    mov w10, wzr
    mov w13, #-1            // index of the member being set
    mov w14, wzr            // 1: the object is a player (has gold)
scan:
    cmp w10, w11
    b.hs scanned
    ldrh w12, [x9, w10, uxtw #1]
    cmp w12, #{ID_GOLD:#x}
    b.ne 1f
    mov w14, #1
    mov w17, w10            // index of gold
1:
    cmp w12, w1
    b.ne 2f
    mov w13, w10
2:
    add w10, w10, #1
    b scan
scanned:
    adr x15, #{FLAGS - CAVE:#x}     // patched below: flags
    cmp w1, #{ID_X:#x}
    b.eq position
    cmp w1, #{ID_Y:#x}
    b.ne not_position
position:                           // a player's x or y: write max gold / max stats into its members
    cbz w14, call
    ldr w16, [x15, #20]
    cbz w16, pos_stats
    ldr x16, [x0, #0x18]
    cbz x16, pos_stats
    ldr x16, [x16, w17, uxtw #3]
    cbz x16, pos_stats
    ldr w12, [x16, #8]
    cmp w12, #4
    b.ne 7f
    mov w12, #{GOLD_MAX & 0xFFFF:#x}
    movk w12, #{GOLD_MAX >> 16:#x}, lsl #16
    str w12, [x16, #0xc]
    b pos_stats
7:
    cmp w12, #0x10
    b.ne pos_stats
    mov w12, #0x4f80                // 99999.0f = 0x47C34F80
    movk w12, #0x47c3, lsl #16
    str w12, [x16, #0xc]
pos_stats:
    ldr w16, [x15, #28]
    cbz w16, call
    mov w10, #{ID_STR:#x}
    bl set_max_stat
    mov w10, #{ID_DEF:#x}
    bl set_max_stat
    mov w10, #{ID_AGI:#x}
    bl set_max_stat
    mov w10, #{ID_MAG:#x}
    bl set_max_stat
    b call

// w10 = member id: when the object (x0, keys x9, count w11) has it, its stored value becomes STAT_MAX.
// Uses w12, w13, x16.
set_max_stat:
    mov w13, wzr
sms_loop:
    cmp w13, w11
    b.hs sms_ret
    ldrh w12, [x9, w13, uxtw #1]
    cmp w12, w10
    b.eq sms_found
    add w13, w13, #1
    b sms_loop
sms_found:
    ldr x16, [x0, #0x18]
    cbz x16, sms_ret
    ldr x16, [x16, w13, uxtw #3]
    cbz x16, sms_ret
    ldr w12, [x16, #8]
    cmp w12, #4
    b.ne sms_float
    mov w12, #{STAT_MAX}
    str w12, [x16, #0xc]
    ret
sms_float:
    cmp w12, #0x10
    b.ne sms_ret
    movz w12, #{STAT_MAX_F >> 16:#x}, lsl #16
    str w12, [x16, #0xc]
sms_ret:
    ret
not_position:
    cmp w1, #{ID_HEALTH:#x}
    b.ne not_health
    cbz w14, onehit
    ldr w16, [x15, #0]
    cbnz w16, skip
    b call
not_health:
    cbz w14, call                   // the rest is for players only
    cmp w1, #{ID_MAGIC_CUR:#x}
    b.ne not_magic
    ldr w16, [x15, #4]
    cbnz w16, skip
    b call
not_magic:
    cmp w1, #{ID_EXP:#x}
    b.ne not_exp
    ldr w16, [x15, #24]
    cbz w16, call
    bl compare                      // s0 new, s1 stored; Z set when it cannot tell
    b.le call                       // not a gain
    fcmp s1, #0.0
    b.le call                       // stored 0: the player being set up from the save, not a kill
    fsub s2, s0, s1
    mov w12, #1000
    scvtf s3, w12
    fcmp s2, s3
    b.ge call                       // a jump of 1000 or more is a reload, not a reward
    fmov s3, #{EXP_MUL:.1f}
    fmadd s0, s2, s3, s1            // stored + gain * EXP_MUL
    ldr w12, [x2, #8]
    cmp w12, #0x10
    b.ne exp_int
    str s0, [x2, #0x10]
    b call
exp_int:
    fcvtzs w12, s0
    str w12, [x2, #0x10]
    b call
not_exp:
    cmp w1, #{ID_GOLD:#x}
    b.ne items
    ldr w16, [x15, #12]
    cbz w16, call
    b nodec
items:
    ldr w16, [x15, #8]
    cbz w16, call
nodec:                              // skip the set when the new value is below the stored one
    bl compare
    b.mi skip
    b call
onehit:                             // a non-player's health going down goes to 0
    ldr w16, [x15, #16]
    cbz w16, call
    bl compare
    b.pl call
    str wzr, [x2, #0x10]            // 0 and 0.0f are both all-zero bits
    b call
call:
    blr x8
skip:
    b back

// flags N set when new < stored (both as floats); returns with N clear (b.pl) when it cannot tell.
// Uses x16, x17, w12, s0, s1 only; x30 is saved in x17 around nothing (leaf).
compare:
    cmp w13, #0
    b.lt cmp_unknown
    ldr x16, [x0, #0x18]
    cbz x16, cmp_unknown
    ldr x16, [x16, w13, uxtw #3]
    cbz x16, cmp_unknown
    ldr w12, [x16, #8]
    cmp w12, #0x10
    b.ne 3f
    ldr s1, [x16, #0xc]
    b 4f
3:
    cmp w12, #4
    b.ne cmp_unknown
    ldr w12, [x16, #0xc]
    scvtf s1, w12
4:
    ldr w12, [x2, #8]
    cmp w12, #0x10
    b.ne 5f
    ldr s0, [x2, #0x10]
    b 6f
5:
    cmp w12, #4
    b.ne cmp_unknown
    ldr w12, [x2, #0x10]
    scvtf s0, w12
6:
    fcmp s0, s1                     // N set iff s0 < s1
    ret
cmp_unknown:
    cmp w12, w12                    // N clear
    ret
back:
    b {BACK:#x}
"""

import re
# keystone: no // comments, numbered local labels renamed (each 1..6 is used once, forward)
src = '\n'.join(l.split('//')[0].rstrip() for l in src.splitlines())
src = re.sub(r'^(\d):', r'L\1:', src, flags=re.M)
src = re.sub(r'\b(\d)f\b', r'L\1', src)
src = src.replace('adr x15, #%#x' % (FLAGS - CAVE), 'adr x15, back')   # placeholder, patched below

ks = Ks(KS_ARCH_ARM64, KS_MODE_LITTLE_ENDIAN)
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
enc, _ = ks.asm(src, CAVE)
words = [int.from_bytes(bytes(enc[i:i + 4]), 'little') for i in range(0, len(enc), 4)]
# fix the two address-dependent words with exact encodings: adr x15 -> FLAGS, final b -> BACK
for idx, w in enumerate(words):
    ins = next(md.disasm(w.to_bytes(4, 'little'), CAVE + idx * 4))
    if ins.mnemonic == 'adr':
        rd = w & 31
        pc = CAVE + idx * 4
        if rd == 15:                                  # adr x15, the flags (in the cave's page range)
            imm = FLAGS - pc
            words[idx] = 0x10000000 | ((imm & 3) << 29) | (((imm >> 2) & 0x7FFFF) << 5) | rd
        else:                                         # adrp x16 / x17: the page of DISP / BASE
            target = DISP if rd == 16 else BASE
            imm = ((target & ~0xFFF) - (pc & ~0xFFF)) >> 12   # main's base is page aligned
            words[idx] = 0x90000000 | ((imm & 3) << 29) | (((imm >> 2) & 0x7FFFF) << 5) | rd
words[-1] = int.from_bytes(bytes(ks.asm('b %#x' % BACK, CAVE + (len(words) - 1) * 4)[0]), 'little')
hook_word = int.from_bytes(bytes(ks.asm('b %#x' % CAVE, HOOK)[0]), 'little')
assert CAVE + len(words) * 4 <= FLAGS, 'cave runs into the flags'

blob = b''.join(w.to_bytes(4, 'little') for w in words)
listing = ['; M+%X  %s %s' % (i.address, i.mnemonic, i.op_str) for i in md.disasm(blob, CAVE)]
assert len(listing) == len(words), 'capstone could not decode every word'

stores = []
for k in range(0, len(words), 2):
    if k + 1 < len(words):
        stores.append('08000000 %08X %08X %08X' % (CAVE + k * 4, words[k + 1], words[k]))
    else:
        stores.append('04000000 %08X %08X' % (CAVE + k * 4, words[k]))
# a cheat holds at most 256 opcode words: the hook pair (6) + 62 eight-byte stores (4 each) in the
# first cheat, the rest of the cave in a second one, listed BEFORE it so the cave is whole by the time
# the hook branch is written in a pass
SPLIT = 62
part2 = ['[SetMember hook part 2 (needed by the cheats below)]'] + stores[SPLIT:]
part1 = ['[Castle Crashers SetMember hook (needed by the cheats below)]',
         '04000000 %08X %08X' % (HOOK, ORIG),
         '04000000 %08X %08X' % (HOOK, hook_word)] + stores[:SPLIT]
for c in (part1, part2):
    assert sum(len(l.split()) for l in c[1:]) <= 256, c[0]
cheats = ['\n'.join(part2), '\n'.join(part1)]
for flag, name in FEATURES:
    a = FLAGS + flag * 4
    cheats.append('\n'.join(['[%s]' % name, 'C046E5E0', '04000000 %08X 00000000' % a, '20000000',
                             '04000000 %08X 00000001' % a]))

if __name__ == '__main__':
    import sys
    if '-l' in sys.argv:
        print('\n'.join(listing))
    print('\n\n'.join(cheats))
