# Land of Glarefall (PC) cheats

For the Windows version of Land of Glarefall (Unity 2022.3.62f3, IL2CPP, build id `A9C292BF4E263744`).
The cheats run in **pchost 0.6c**, from [Breeze Studio 0.06](https://github.com/tomvita/Breeze-Studio/releases/tag/0.06):
pchost.exe alone is enough, no Python or Studio needed.

| Cheat | What it does |
|---|---|
| Coins 10k | Holds the coins at 10,000 |
| Wood 5k | Holds the wood at 5,000 |
| player hp 9000 | Holds the player's hp at 9000 |
| phy_atk 2000 | Holds the player's physical attack at 2000 |
| phy_def 2000 | Holds the player's physical defence at 2000 |
| mp 1000 | Holds the player's mp at 1000 |
| black_gold  hp 3000 | Holds black_gold's hp at 3000 (2999.9) |

## Use

1. Download `pchost_0.6c.zip` from [Breeze Studio 0.06](https://github.com/tomvita/Breeze-Studio/releases/tag/0.06) and unzip it.
2. Unzip `LandOfGlarefall_pchost_A9C292BF4E263744.zip` (from this release) into the same folder: it adds
   `pchost_sd\atmosphere\contents\FC2D6F4F3C4D1735\cheats\A9C292BF4E263744.txt` beside `pchost.exe`.
3. Start the game, then run `pchost "Land of Glarefall"` (or double-click pchost.exe and pick the game).
4. The cheat window opens: tick the cheats you want. They all start off. **Ctrl+Alt+C** shows or hides the window.

`A9C292BF4E263744.txt` is the same cheat file on its own.

The file is named by the game's build id (`GameAssembly.dll`'s). Another build, a game update or
another store's release, has another id: pchost prints the cheat file path it looks for when it
attaches, and if the name there is not `A9C292BF4E263744.txt`, these cheats do not fit that build.

Single-player game. Do not use pchost on games with online anti-cheat.

## How they were made

All are pointer chains from IL2CPP static fields, found with Breeze Studio's Search, Objects and
Memory tabs.

- Coins and wood are two entries of the bag's item counts, a `Dictionary<int, int>`:
  `BagData.instance > basedata > _entries[0].value` = `[[[[[main+4468F70]+B8]+0]+10]+18]+2C` (key 999, coins)
  and `_entries[1].value` = `...+3C` (key 1001, wood).
- The player's stats are fields of its unit attributes:
  `UnitManager.instance > player_org > att_crn` (a `Game.Config.UnitAttEntity`) =
  `[[[[[main+44298C0]+B8]+0]+30]+208]`, then `hp` +20, `mp` +24, `phy_atk` +28, `phy_def` +2C (floats).
- black_gold's hp is the same field of `UnitManager.instance > black_gold > att_crn`
  (`[[[[[main+44298C0]+B8]+0]+20]+208]+20`).

The coins and wood cheats write a dictionary entry by its place, not by its key: if the game ever
stores another item before them, `[0]` and `[1]` would no longer be coins and wood.

## Tested

On Nov 23 2026, with the game running: each cheat's value was read back in memory while it was on
(hp 9000, mp 1000, phy_atk 2000, phy_def 2000, black_gold hp 2999.9, coins 10000, wood 5000).
black_gold's cheat writes 2999.9, not exactly 3000.
