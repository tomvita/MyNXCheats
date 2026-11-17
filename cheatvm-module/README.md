# Cheat VM module for emulators

The cheat codes in this repo are made with Breeze and use the full Atmosphère cheat
VM: ASM cheats, Breeze split cheats (`[code cave]` folder), the extended key opcode
(C4), float math and more. The cheat engines built into yuzu-family emulators (Eden,
Lichii and others) are older ports that miss some of these, and they run **every**
cheat in a file at once.

This module fixes that. It is Atmosphère's cheat VM running **inside the game** as an
exefs module (`subsdk9`), so the emulator only has to load a game mod. It reads the
same cheat file as Breeze and dmnt, with per-cheat on/off, and the default build adds
an in-game cheat menu.

Tested on Eden (Windows and Android) and Lichii (Switch 2 games too), and on a real
Switch.

## Files here

| File | What it is |
|---|---|
| `subsdk9` | the module **with the in-game menu** (use this one) |
| `no-menu/subsdk9` | the module without the menu, if the menu build gives trouble in a game |
| `cheatvm.ini` | optional settings, every value at its default |
| `source/` | the module's source code (GPLv2) |

`subsdk9` does not depend on the game: the same file works for every title.

## Install (Eden, Lichii and other yuzu-family emulators)

You need the game's title ID (`<TID>`, 16 hex digits) and the cheat file from this
repo: `cheats/<game>/<BID>.txt`, where `<BID>` is the build ID of your game version.

Open the emulator's user folder (Eden: **File > Open Eden Folder**; Lichii: **File >
Open Lichii Folders > Root Data Folder**) and put the files here:

```
load/<TID>/cheatvm/exefs/subsdk9                            the module
sdmc/atmosphere/contents/<TID>/cheats/<BID>.txt              the cheat file
sdmc/atmosphere/contents/<TID>/cheats/cheatvm.ini            optional
```

- **Do not copy `main.npdm`.** The game keeps its own; emulators do not check it.
- **Never put the cheat file under `load/`.** The emulator would then run it with its
  own cheat engine as well, every cheat on.
- **"cheatvm" shows in the game's Add-ons list** when the module is found. Leave it ticked.
- **Folders moved in the settings:** `load/` and the SD card folder can be moved. The
  emulator's Open Folders menu opens the ones in use (Lichii: Mod Folder, SDMC Folder).
- **Lichii, portable or not:** if a `user` folder sits next to `lichii.exe`, that is the
  data folder; otherwise it is `%APPDATA%\lichii` (older builds: `%APPDATA%\eden`).

### Games kept as an extracted folder

A game opened by its `main` file (a folder with `main`, `main.npdm`, `rtld`, `sdk`,
...) skips `load/`. Put `subsdk9` straight into the game's exefs folder, next to
`main`, after checking the game has no `subsdk9` of its own (back up the folder). The
cheat file stays under `sdmc/` as above.

To uninstall, delete `load/<TID>/cheatvm` (or the `subsdk9` you added).

## Using it

- **Open the menu:** hold **L+R** and press **Down** (change it with `menu_keys` in
  `cheatvm.ini`). A turns a cheat on or off or opens a folder, B goes back and closes
  the menu, Left/Right page through long lists. The game gets no input while the menu
  is open.
- **Cheats start off.** Your choices are saved in
  `sdmc/atmosphere/contents/<TID>/cheats/cheatvm_toggles.txt` and come back next time.
  Set `enabled_by_default = 1` in `cheatvm.ini` to start with all on.
- **Settings with several values** (for example EXP x2 / x4 / x1 (default)) are one at a
  time: turning one on turns the others off, and turning the last off puts the default
  back.
- **No restart needed:** edits to the cheat file, toggles or ini are picked up within
  about a second.
- **Without the menu** (`no-menu/subsdk9`), turn cheats on by editing
  `cheatvm_toggles.txt`: the module writes it on first run with every cheat listed as
  `off`; change a cheat's line to `on`.

## When something does not work

The module writes two files next to the cheat file:

- `cheatvm_log.txt`: start-up, which cheat file was loaded, faults.
- `cheatvm_status.txt`: what is running now.

Check these first:
- **No log file at all:** the module did not load. Check the path and that "cheatvm"
  is ticked in Add-ons.
- **Log says no cheat file:** the `<BID>.txt` name must match your game version.
- **Menu missing or wrong but cheats run:** try `no-menu/subsdk9` and, for an upside-down
  menu, `menu_flip = 1`.

Include both files when you report a problem.

## Real Switch

The module works on Atmosphère too, but there it needs a `main.npdm` made for the
game, and dmnt plus Breeze already run these cheats. Use Breeze on a Switch.

## Credit and licences

- [exlaunch](https://github.com/shadowninja108/exlaunch) by shadowninja108, the base
  of the module (GPLv2).
- [Atmosphère](https://github.com/Atmosphere-NX/Atmosphere): the cheat VM (GPLv2).
- [Dear ImGui](https://github.com/ocornut/imgui) by Omar Cornut (MIT).
- [SMO-Exlaunch-Base](https://github.com/CraftyBoss/SMO-Exlaunch-Base) (GPLv2): the
  ImGui shader; `nvn.h` (MIT, h1k421).

The full source of these builds is in `source/`.
