from pathlib import Path
from contextlib import contextmanager
import json
TARGETS=json.loads((Path(__file__).resolve().parent/'targets.json').read_text())
class Asm:
 def __init__(self):self.lines=[]
 def emit(self,*words):self.lines.append(' '.join(f'{v:08X}' for v in words))
 def imm(self,r,v):
  # XOR-self clears all 64 bits in one word, preserving the VM's code budget.
  if v==0:self.math(r,r,8,other=r)
  else:self.emit(0x40000000|(r<<16),v>>32,v&0xffffffff)
 def ld(self,r,offset,base=None,width=8):self.emit(0x50000000|(width<<24)|(r<<16)|(0 if base is None else 0x2000|(base<<8)),offset)
 def move(self,d,s):self.emit(0x98900000|(d<<16)|(s<<12))
 def math(self,d,s,op,value=None,other=None):
  first=0x98000000|(op<<20)|(d<<16)|(s<<12)
  if value is None:self.emit(first|(other<<4))
  else:self.emit(first|0x100,value>>32,value&0xffffffff)
 def add(self,r,v):self.emit(0x78000000|(r<<16),v)
 def store(self,s,d,offset,width=4):self.emit(0xA0000200|(width<<24)|(s<<20)|(d<<16),offset)
 @contextmanager
 def cond(self,r,op,value=None,other=None,width=8):
  first=0xC0000000|(width<<20)|(op<<16)|(r<<12)
  if other is None:
   if width==8:self.emit(first|0x400,value>>32,value&0xffffffff)
   else:self.emit(first|0x400,value)
  else:self.emit(first|0x500|(other<<4))
  yield
  self.emit(0x20000000)
 @contextmanager
 def nz(self,r):
  with self.cond(r,6,value=0):yield
 @contextmanager
 def follow(self,offsets):
  if not offsets:yield;return
  self.ld(15,offsets[0],base=15)
  with self.nz(15):
   with self.follow(offsets[1:]):yield
 @contextmanager
 def vtable(self,key):
  self.imm(6,0);self.ld(6,0,base=15)
  self.math(7,8,0,value=int(TARGETS[key]['vtable_anchor_offset'],16))
  with self.cond(6,5,other=7):yield
 @contextmanager
 def players(self):
  self.imm(11,0);self.emit(0x300A0000,4)
  with self.cond(11,3,other=12,width=4):
   self.math(14,11,3,value=3);self.math(14,13,0,other=14)
   self.imm(15,0);self.ld(15,0,base=14)
   with self.nz(15):
    with self.follow([0x30]):yield
  self.add(11,1);self.emit(0x310A0000)

master=Asm()
for r in [12,13,8,15]:master.imm(r,0)
master.ld(8,0x85B0000);master.ld(15,0xAD80EE8)
with master.nz(15):
 with master.follow([0x250]):
  master.imm(14,0);master.ld(14,0x40,base=15,width=4)
  with master.cond(14,2,value=1,width=4):
   with master.cond(14,4,value=4,width=4):
    master.ld(13,0x38,base=15)
    with master.nz(13):master.move(12,14)
blocks=[('{Local coop context - required}',master)]
specs=[
 ('Health = HealthMax (all local players)',0x40,0xb4,[0x90,0x94],None),
 ('HealthPotionCharges = Max (all local players)',0x40,0x174,[0x160,0x164],None),
 ('Souls = SoulsMax (all local players)',0x58,0xa4,[0x90,0x94],None),
 ('Emeralds = EmeraldsMax (all local players)',0x60,0xa4,[0x90,0x94],None),
 ('MovementSpeedMultiplier 1.5 (all local players)',0x8,None,[0xa0,0xa4],0x3fc00000),
 ('Movement RollCharges 1000 (all local players)',0x8,None,[0x140],0x447a0000),
 ('Echo Shards = Max (all local players)',0x60,0x114,[0x100,0x104],None),
 ('Enchantment Points refill to Cap (all local players)',0x68,0xe4,[0xd0,0xd4],None),
 ('Rarity bonus chance 0.2 (all local players)',0x80,None,[0xb0,0xb4],0x3e4ccccd),
 ('Rarity bonus chance 0.5 (all local players)',0x80,None,[0xb0,0xb4],0x3f000000),
 ('Rarity bonus chance 1.0 (all local players)',0x80,None,[0xb0,0xb4],0x3f800000),
]
for title,slot,source,dests,value in specs:
 a=Asm()
 with a.players():
  with a.follow([0x350,0xa20,0x10a8,slot]):
   with a.vtable(f'attr_{slot:x}'):
    if source is None:a.imm(3,value)
    else:a.ld(3,source,base=15,width=4)
    for dst in dests:a.store(3,15,dst)
 blocks.append(('['+title+']',a))
# Preserve the original ammo attribute-set scan, inside each player's traversal.
a=Asm()
with a.players():
 with a.follow([0x350,0xa20]):
  a.ld(14,0x10a8,base=15)
  with a.nz(14):
   a.ld(9,0x10b0,base=15,width=4)
   with a.cond(9,2,value=1,width=4):
    with a.cond(9,4,value=64,width=4):
     a.math(7,8,0,value=int(TARGETS['attr_18']['vtable_anchor_offset'],16))
     a.imm(1,0);a.emit(0x30000000,64)
     with a.cond(1,3,other=9,width=4):
      a.math(2,1,3,value=3);a.math(2,14,0,other=2)
      a.imm(4,0);a.ld(4,0,base=2)
      with a.nz(4):
       a.imm(5,0);a.ld(5,0,base=4)
       with a.cond(5,5,other=7):
        a.ld(3,0xc4,base=4,width=4);a.store(3,4,0xb0);a.store(3,4,0xb4)
     a.add(1,1);a.emit(0x31000000)
blocks.append(('[Arrows = Max - scan (all local players)]',a))
a=Asm()
with a.players():
 with a.follow([0x2e8,0xa20,0x508,0x10,0x1b8,0x170]):
  with a.vtable('NoCooldown'):
   a.imm(3,0);a.store(3,15,0x30,width=1)
blocks.append(('[No ability cooldown (all local players)]',a))
# Use each controller's UE key state map, never Atmosphere's merged button state.
a=Asm()
with a.players():
 a.move(9,15)
 with a.follow([0x420]):
  with a.vtable('PlayerInput'):
   a.ld(14,0x2e0,base=15)
   with a.nz(14):
    a.ld(5,0x2e8,base=15,width=4)
    with a.cond(5,2,value=1,width=4):
     with a.cond(5,4,value=128,width=4):
      # TSparseArray free-slot count: do not inspect stale removed key entries.
      a.ld(4,0x314,base=15,width=4)
      with a.cond(4,5,value=0,width=4):
       a.move(15,5);a.imm(6,0);a.imm(1,0);a.emit(0x30000000,128)
       with a.cond(1,3,other=15,width=4):
        a.math(2,1,2,value=0x110);a.math(2,14,0,other=2)
        a.ld(3,0,base=2,width=4);a.ld(5,0x18,base=2)
        with a.cond(5,1,value=0x3fe0000000000000):
         with a.cond(3,5,value=0x109e,width=4):a.math(6,6,6,value=1)
         with a.cond(3,5,value=0x10db,width=4):a.math(6,6,6,value=2)
       a.add(1,1);a.emit(0x31000000)
       with a.cond(6,5,value=3,width=4):
        a.move(15,9)
        with a.follow([0x2e8,0x330]):
         with a.vtable('Movement'):
          a.imm(3,0x4092c00000000000);a.store(3,15,0xe0,width=8)
          a.imm(3,3);a.store(3,15,0x231,width=1)
blocks.append(('[Moon jump ZL+A (pressing player only)]',a))
text='\n\n'.join(title+'\n'+'\n'.join(a.lines) for title,a in blocks)+'\n'
(Path(__file__).resolve().parent.parent/'C6B32F4D3D4243FF.txt').write_text(text)
report=[]
for title,a in blocks:report.append({'title':title,'words':sum(len(l.split()) for l in a.lines)})
(Path(__file__).resolve().parent/'build.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2));print('Total words:',sum(x['words'] for x in report))
assert sum(x['words'] for x in report)<=1024
