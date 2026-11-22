# Cheat VM module for emulators

Run this repo's cheats in Eden, Lichii and other yuzu-family emulators, with an in-game
cheat menu. **Version 1.2.**

## Install in three steps

1. **Download [`cheatvm.zip`](cheatvm.zip).**
2. **Unzip it into the game's mod folder.** In the emulator, right-click the game in
   the game list and choose **Open Mod Data Location**. Unzip `cheatvm.zip` into the
   folder that opens. It makes a `cheatvm` folder there; that is all.
3. **Put the game's cheat file on the emulated SD card.** Take the cheat file from this
   repo (`cheats/<game>/<BID>.txt`). Open the emulator's SD card folder (Lichii: **File >
   Open Lichii Folders > SDMC Folder**; Eden: **File > Open Eden Folder**, then `sdmc`)
   and put it at:

   ```
   atmosphere/contents/<TID>/cheats/<BID>.txt
   ```

   Not sure of `<TID>` or `<BID>`? Start the game once: the module shows both, and the
   exact place it looks for the file.

Then start the game. Hold **L+R** and press **Down** to open the cheat menu; **A** turns
a cheat on or off, **B** goes back and closes the menu. Your choices are kept for next
time.

To remove it, delete the `cheatvm` folder from the game's mod folder.

**You can probably stop reading here.** Everything below is detail, for when something
does not work or you want to know more.

---

## What it is

The cheat codes in this repo are made with Breeze and use the full Atmosphère cheat
VM: ASM cheats, Breeze split cheats (`[code cave]` folder), code-patch cheats that put
the game's code back when turned off, the extended key opcode (C4), float math and
more. The cheat engines built into yuzu-family emulators are older ports that miss
some of these, and they run **every** cheat in a file at once.

This module is Atmosphère's cheat VM running **inside the game** as an exefs module
(`subsdk9`), so the emulator only has to load a game mod. It reads the same cheat file
as Breeze and dmnt, with per-cheat on/off, and adds the in-game menu.

Tested on Eden (Windows and Android) and Lichii (Switch 2 games too), and on a real
Switch.

## Files here

| File | What it is |
|---|---|
| `cheatvm.zip` | the module with the in-game menu, ready to unzip into a game's mod folder (use this one) |
| `cheatvm_no-menu.zip` | the same without the menu, if the menu build gives trouble in a game |
| `cheatvm/exefs/subsdk9`, `subsdk9` | the menu build as loose files (what `cheatvm.zip` holds) |
| `no-menu/subsdk9` | the no-menu build as a loose file |
| `cheatvm.ini` | optional settings, every value at its default |
| `source/` | the module's source code (GPLv2) |

The module does not depend on the game: the same file works for every title.

## Version

The version is shown on the first line of `cheatvm_log.txt`, at the top of
`cheatvm_status.txt` and in the menu under the build ID. Give it when you report a
problem.

- **1.2** (November 22 2026): a cheat's writes into the game's code are made once a
  pass, with the value the pass ends with. Two cheats that write the same instruction (one
  changing the other's code cave) no longer rewrite it twice a pass, which on an emulator
  stopped the game for a moment each time.
- **1.1** (November 22 2026): code-patch cheats behind a C4 key (the kind Breeze's Make cheat
  writes) put the game's code back when turned off too.
- **1.0** (November 2026): the first numbered version. Code-patch cheats made by Breeze
  beta129.02 put the game's code back when turned off, also in games whose code is in
  a loaded module.

## Where the files go, in detail

The emulator's user folder (Eden: **File > Open Eden Folder**; Lichii: **File > Open
Lichii Folders > Root Data Folder**) holds both places:

```
load/<TID>/cheatvm/exefs/subsdk9                            the module (what the zip makes)
sdmc/atmosphere/contents/<TID>/cheats/<BID>.txt              the cheat file
sdmc/atmosphere/contents/<TID>/cheats/cheatvm.ini            optional
```

- **Do not copy `main.npdm`.** The game keeps its own; emulators do not check it.
- **Never put the cheat file under `load/`.** The emulator would then run it with its
  own cheat engine as well, every cheat on.
- **"cheatvm" shows in the game's Add-ons list** when the module is found. Leave it ticked.
- **Folders moved in the settings:** `load/` and the SD card folder can be moved.
  **Open Mod Data Location** and the emulator's Open Folders menu open the ones in use.
- **Lichii, portable or not:** if a `user` folder sits next to `lichii.exe`, that is the
  data folder; otherwise it is `%APPDATA%\lichii` (older builds: `%APPDATA%\eden`).
- **An emulator with its own Breeze cheat engine** (Lichii builds from Breeze's author)
  runs the same cheat file itself. Use either that or the module, not both, or every
  cheat runs twice.

A cheat file Breeze wrote starts with a `[Breeze ...]` line (and maybe a signature line).
Those are labels with no code: as in Atmosphère they are not cheats, take none of the 255
cheat slots, and the cheats keep the numbers Atmosphère gives them.

### Games kept as an extracted folder

A game opened by its `main` file (a folder with `main`, `main.npdm`, `rtld`, `sdk`,
...) skips `load/`. Put `subsdk9` straight into the game's exefs folder, next to
`main`, after checking the game has no `subsdk9` of its own (back up the folder). The
cheat file stays under `sdmc/` as above.

## Using it, in detail

- **Banner:** after the game's first button press a banner shows for 10 s with the menu
  keys, the title ID and build ID, and how many cheats run.
- **Menu keys:** change the chord with `menu_keys` in `cheatvm.ini`. Left/Right page
  through long lists. The game gets no input while the menu is open.
- **Cheats start off.** Your choices are saved in
  `sdmc/atmosphere/contents/<TID>/cheats/cheatvm_toggles.txt`. Set
  `enabled_by_default = 1` in `cheatvm.ini` to start with all on.
- **Settings with several values** (for example EXP x2 / x4 / x1 (default)) are one at a
  time: turning one on turns the others off, and turning the last off puts the default
  back.
- **Code-patch cheats** (made by Breeze beta129.02 and later) keep the game's own
  instructions in the cheat: turning one off puts them back, so the cheat really stops.
- **No restart needed:** edits to the cheat file, toggles or ini are picked up within
  about a second.
- **Without the menu** (`cheatvm_no-menu.zip`), turn cheats on by editing
  `cheatvm_toggles.txt`: the module writes it on first run with every cheat listed as
  `off`; change a cheat's line to `on`.

## When something does not work

The module writes two files next to the cheat file:

- `cheatvm_log.txt`: the version, start-up, which cheat file was loaded, faults.
- `cheatvm_status.txt`: what is running now.

Check these first:
- **No log file at all:** the module did not load. Check that the zip made
  `cheatvm/exefs/subsdk9` inside the game's mod folder (not `cheatvm/cheatvm/...`), and
  that "cheatvm" is ticked in Add-ons.
- **"not running: no cheat file":** the menu shows the path it looks for; the `<BID>.txt`
  name must match the build ID shown there.
- **Menu missing or wrong but cheats run:** try `cheatvm_no-menu.zip` and, for an
  upside-down menu, `menu_flip = 1`.

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
