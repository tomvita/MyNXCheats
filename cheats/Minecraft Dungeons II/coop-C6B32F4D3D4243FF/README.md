# Local co-op cheats for 1.1.3.0

TID: `0100A7C01B792000`; BID: `C6B32F4D3D4243FF`.
Based on tomvita's original cheats and Breeze attribute guide.

The replacement [cheat file](../C6B32F4D3D4243FF.txt) contains 14 optional entries plus one required master block. It traverses the current local-player list (up to four players) instead of always selecting player 1.

| Entry | Behavior |
| --- | --- |
| Health, potion charges, souls, emeralds, arrows | Refill each character to its own maximum |
| Movement speed | 1.5 multiplier for each character |
| Roll charges | Preserve the original value of 1000 for each character |
| Echo Shards | Refill `ATR_Currency.SpringStone` to its maximum |
| Enchantment points | Refill to that character's `EnchantmentPointsCap`, not the global maximum of 99 |
| Rarity bonus (three entries) | Set `ATR_Loot.RarityBonusChance` to 0.2, 0.5 or 1.0 |
| Moon jump | ZL+A affects only the player pressing both buttons |
| No ability cooldown | Preserve the original path to the shared `GE_AbilityCooldown` default object |

## Use

Replace the complete file in `atmosphere/contents/0100A7C01B792000/cheats/`. If loading from Breeze, update its copy in `switch/breeze/cheats/0100A7C01B792000/` as well.

Keep `{Local coop context - required}`. Do not append the previous player-1 entries: they use registers reserved by the new shared context. Start the game normally, then enable the desired entries.

Enable **only one rarity entry**. They do not add together; if several are enabled, the last enabled entry in file order overwrites the earlier values. These are attribute values, not measured final drop probabilities; 1.0 is not a guarantee of rare drops. Disabling an entry stops writes but does not restore the previous value. No-cooldown modifies a shared default object and requires restarting the game to restore the original behavior.

## Implementation and regeneration

Run `python3 build_cheats.py` from any working directory. It regenerates the adjacent build's cheat file and writes a local `build.json` word-count report. Python's standard library is sufficient.

The master block resolves `UWorld -> GameInstance -> LocalPlayers`, validates a count of 1–4, and preserves R8 (address anchor), RC (count), and RD (list). Each entry iterates current players, checks pointers for null and checks the final vtable before writing. The fixed attribute slots and vtables are build-specific; some attribute sets, including loot, share a vtable, so this is not a substitute for verifying slots after a game update. The arrow entry retains the original attribute-set scan.

Moon jump reads each controller's own `PlayerInput.KeyStateMap` instead of Atmosphere's combined button state. It recognizes `Gamepad_LeftTrigger` and `Gamepad_FaceButton_Right` (Switch A), requires both on the same player, and writes that player's movement component. Maps with free slots or more than 128 entries are skipped to avoid stale entries. These offsets and FName indices are specific to this BID.

The full file is **1013 opcode words**, including all three rarity alternatives, below the 1024-word enabled-program limit. Zeroing registers uses 64-bit XOR-self to save space. There is little room for additional entries.

## Validation

- Two distinct local-player graphs were inspected on a real Switch over USB.
- Player 2's isolated jump was executed using the generated instructions; the tester confirmed only player 2 jumped.
- Generated shard-refill instructions changed player 1 from 82 to 100 and player 2 from 6 to 100, with independent readback.
- 22 local interpreter checks passed using a two-player memory snapshot and synthetic 1–4-player configurations: per-player writes, all three rarity values, input isolation, invalid counts, null players/pawns, incorrect vtables, sparse key maps and shared-register preservation.
- The complete file was installed to Atmosphere and Breeze; an independent USB MTP session read both copies back byte-for-byte.
- After installation, the tester reported that the functions were tested and working. This is user-reported acceptance, not an itemized automated gameplay test.

Three- and four-player execution was simulated, not tested on a four-player console session. No statistical rarity-drop test was performed. Actual enchantment spending was not separately recorded (the NPC was initially locked); map transitions, respawns and every individual ability were not exhaustively tested.
