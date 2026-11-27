# Castle Crashers Remastered: how the cheats were made

Title ID `010001300D14A000`. The same cheats come for two versions:

| Version | Cheat file (build ID) |
|---|---|
| 1.0.0 (base game) | **`9CF2AF5B7FD156BC.txt`** |
| 1.0.7 (latest update) | **`5E85F631BFA6930E.txt`** |

`EF5B33316A45337D.txt` and the `asm1*` files are the older cheats for 1.0.5.

| Cheat | What it does |
|---|---|
| SetMember hook part 2 / Castle Crashers SetMember hook | The hook and its code cave. **Keep both on**; every other cheat needs them |
| Infinite health (players) | A player's health is never changed |
| Infinite magic (players) | A player's magic bar is never changed |
| Potions, bombs and beefies never run out | Those counts never go down |
| Gold never goes down (free shopping) | Buying costs nothing |
| One-hit kills | Anything with health that is not a player dies from one hit |
| Max gold (99999) | Gold is set to 99999 whenever you move |
| EXP x10 | Each experience gain is multiplied by 10 |
| Max stats | Strength, magic, defense and agility set to 25 whenever you move |

Each feature cheat can be turned on and off on its own. Turning one off really switches it off.

This guide is about **how** these cheats were found. The same method works for other games that
run their logic in a script interpreter, and it is what to repeat after a game update.

---

## 1. Why the usual way fails here

Castle Crashers is a Flash game at heart. Its gameplay is **ActionScript 2 bytecode** run by
Behemoth's own virtual machine (VM), inside the native `CastleCrashersRemastered.nss`. That changes
everything a normal cheat hunt relies on:

- **A value search finds the wrong thing.** Searching for HP (f32, "decreased" after each hit)
  narrows to a few addresses that really do change when you are hit, but they are **VM registers
  and function arguments** that the value passes through, not where HP is kept. Ours turned out to
  be an argument of the script function `f_FX(x, y, u_depth, n_type, u_xscale, u_yscale)`, which
  spawns the hit effect.
- **Pointer chains do not last.** The script objects (the player, the enemies) are rebuilt for
  every level, so a chain found in one level is broken in the next. A depth 10 scan with 4,247
  chains kept none of them after a level change.
- **The code that writes a value is shared by every value.** A data watch on the value leads to
  the VM's generic "copy a value" routine (`M+5F760` for a float). Hooking it would change every
  variable in the game.

The way in is to go **one level up**: find the VM operation that sets an object's *member* (for
example `player.health = ...`), where the member's **name** is known.

## 2. Tools used

- **Lichii** (the emulator) with its PC connect probe: data watches with full registers and a
  backtrace (`probe data add <addr> 4 w`, `probe data list`, `probe data regs <row>`).
- **Breeze Studio**: Search tab (value search), Pointers tab (pointer scans), Cheats tab.
- Capstone and Keystone (Python) to read and write ARM64 code.

The same steps work on a Switch with Breeze's search and watch tools.

## 3. Find the real HP and watch who writes it

1. Search HP as f32, take hits, step with "decreased", and check the candidates by writing values.
2. Put a **write watch** on the candidate and take a hit. For the real HP every write comes from
   one place:

   ```
   W pc=M+5F760 lr=M+47EAC  before=42C80000 (100.0)  after=42C40000 (98.0)
   ```

   For a candidate that is only a VM register, the writes come from `lr=M+40F5C` (the VM copying
   function arguments) and the slot also gets unrelated integers. That is the sign you have the
   wrong address.

3. Read the registers at the write (`probe data regs 0`). The useful one:
   **`x12 = 0x1AD`**, the ID of the member name `health` (see section 5).

## 4. The set-member call

`M+47EAC` is in the VM's **set-member opcode**. Just before it:

```
M+47E8C  mov  x0, x20          ; the member-name value
M+47E90  bl   M+4D710          ; -> w0 = the name's ID
M+47E94  ldr  x8, [x21]        ; x21 = the target object
M+47E98  ldr  x8, [x8, #0x28]  ; its SetMember (a virtual function)
M+47E9C  mov  w1, w0           ; w1 = name ID
M+47EA0  mov  x0, x21          ; x0 = object
M+47EA4  mov  x2, x19          ; x2 = the new value
M+47EA8  blr  x8               ; object->SetMember(name ID, new value)   <- hook here
M+47EAC  b    ...              ; the result is not used
```

**Every** member set of **every** script object goes through this one `blr x8`. At that point we
know the object, the member's name and the new value, before anything is written.

AOB for this site, unique in main (the hook is at **+0x1C**):

```
E0 03 14 AA ?? ?? ?? ?? A8 02 40 F9 08 15 40 F9 E1 03 00 2A E0 03 15 AA E2 03 13 AA 00 01 3F D6
```

## 5. Reading the script's data

**Values.** A value is a small object: a **type tag** (u32) at `+8`, then the payload.
`0x10` = float, `0x04` = int, `0x02` = bool. The new value passed in `x2` has its payload at
**`+0x10`**; a member's stored value has it at **`+0xC`**.

**Objects.** A script object keeps its members in two parallel arrays:

| Offset | Content |
|---|---|
| `+0x08` | member count (u32) |
| `+0x10` | pointer to the member name IDs, u16 each, **sorted** |
| `+0x18` | pointer to the value pointers, one per ID |

This layout is used by the base object's SetMember (`M+5FA30`, a binary search over the sorted IDs)
and by the display object's (`M+53250`, vtables `M+366CD8` and `M+3674E0`).

**Names.** A name ID is an index into the VM's name table (an array of pointers to C strings). The
VM context holds it at `+0x20`. To find an ID without that pointer, search memory for the name
string (`health`), find the one pointer to it (`refs`), and take that pointer's index in the
table. Listing a player object's members by name gives the whole menu:

| Member | ID | Type | | Member | ID | Type |
|---|---|---|---|---|---|---|
| health | 1AD | float | | exp | 53E | int |
| health_max | 3E6 | int | | exp_next | 540 | float |
| magic_current | 561 | int | | level | 1B4 | int |
| magic_max | 560 | int | | strength | 544 | int |
| gold | 1A9 | int | | defense | 545 | int |
| healthpots | 548 | int | | agility | 546 | int |
| bombs | 549 | int | | magic (stat) | 1AE | int |
| beefies | 54A | int | | x / y | 79 / 7C | |

**Telling the player apart.** Enemies are the same kind of object. Only the players have a
**`gold`** member, so "the object has ID `0x1A9`" is the player test.

## 6. The cave

The hook cheat replaces `blr x8` at `M+47EA8` with a branch to a cave in the unused zero bytes at
the end of main's code (`M+279800`; the code segment ends at `M+27A000`). The cave:

1. **Lets most calls through at once.** If the name ID is not one the cheats use, it makes the
   original call. This keeps the cost low: SetMember runs many times a frame.
2. **Checks the object type.** It goes on only if `x8` (the SetMember the game loaded) is
   `M+53250` or `M+5FA30`, the two that use the layout above. They are reached with
   `adrp` + `add`: they are too far for `adr`.
3. **Scans the object's IDs.** It notes whether `gold` is there (a player), and where the member
   being set is.
4. **Applies the rules** that are switched on:
   - *Freeze* (health, magic): skip the call.
   - *No decrease* (items, gold): compare the new and stored values as floats, and skip the call
     when the new one is lower.
   - *One-hit kills*: for a non-player's health, a lower new value is changed to 0 before the call.
   - *EXP x10*: new = stored + gain x 10. Only when the stored exp is above 0 and the gain is under
     1000: setting the player up from the save is not a kill.
   - *Max gold / max stats*: when a player's `x` or `y` is set (all the time while moving), the cave
     writes 99999 into the stored gold, and 25 into the four stats.
5. **Returns** to `M+47EAC`.

**Switches.** Each feature cheat writes one flag word at `M+279F00` (+0 health, +4 magic, +8 items,
+C gold, +10 one-hit kills, +14 max gold, +18 EXP, +1C stats). They use the code-patch block form:

```
[EXP x10]
C046E5E0                    if R14 != R14 (never): the original, for "off"
04000000 00279F18 00000000
20000000
04000000 00279F18 00000001  the switch
```

So turning a feature off writes its 0 back.

**Size limit.** A cheat holds at most 256 opcode words, and the cave is 182 instructions. It is
split into two cheats, and **part 2 is listed first**, so each pass the whole cave is written before
the hook branch.

## 7. Porting to another version

This is how the 1.0.7 cheats were made from the 1.0.0 ones. What moved:

| | 1.0.0 | 1.0.7 |
|---|---|---|
| Hook (`blr x8`) / return | M+47EA8 / M+47EAC | M+120EF0 / M+120EF4 |
| Display object SetMember | M+53250 | M+12C540 |
| Base object SetMember | M+5FA30 | M+139500 |
| Cave / flags | M+279800 / M+279F00 | M+276400 / M+276F00 |
| x, y | 79, 7C | 79, 7C |
| gold, health, magic | 1A9, 1AD, 1AE | 1AB, 1AF, 1B0 |
| exp, strength, defense, agility | 53E, 544, 545, 546 | 540, 546, 547, 548 |
| healthpots, bombs, beefies | 548, 549, 54A | 54A, 54B, 54C |
| magic_current | 561 | 563 |

**The member IDs changed.** 1.0.7 added two names to the script between `y` and `gold`, so every ID
from `gold` up is 2 higher. A port that only moves the code offsets would hit the wrong members.

The steps:

1. Find the hook with the AOB in section 4 and note its offset.
2. Check the stock word there is `blr x8` (`D63F0100`).
3. Find the two SetMember functions. The base one starts
   `stp x22,x21,[sp,#-0x30]! ... mov x21,x0; ldr w8,[x21,#8]!; mov x19,x2; mov w20,w1; cmp w8,#3`.
   The display one is the only function that ends in a tail call (`b`) to it.
4. Check the cave area is still zeros at the end of main's code, or choose another spot.
5. Check the member IDs. Find the string `health`, the one table entry pointing at it, and the
   table's start: entry 0 is empty, entry 1 points at "length", and the VM context points at the
   start. Then read each ID's entry. Watching a `health` write and reading `x12` works too.
6. Add the build to `VERSIONS` at the top of **`make_cheats.py`** and run
   `python make_cheats.py <build ID>`. It assembles the cave, checks every word by disassembling
   it back, and prints the cheats (`-l` also prints the listing).

## 8. Traps met on the way

- **The first candidates were VM registers**, not HP: a write watch tells them apart in seconds
  (section 3).
- **`peek` length is decimal** in PC connect; the address is hex.
- **When swapping a hook's cave, restore the original instruction first.** Otherwise the game can
  run a half-written cave between two cheat writes.
- **Cheat names are cut at 64 characters.**
- **Keystone:** `cmp wzr, #0` cannot be encoded (use `cmp w12, w12`). It also rejects `adr` to an
  absolute address on its own, so `make_cheats.py` encodes `adr` / `adrp` itself.
