# Revenge of the Mage (PC) cheats

For the Windows version of Revenge of the Mage (Unreal Engine 5.8, build id `90D70592625DB9B4`).
The cheats run in **pchost 0.6c**, from [Breeze Studio 0.06](https://github.com/tomvita/Breeze-Studio/releases/tag/0.06):
pchost.exe alone is enough, no Python or Studio needed.

| Cheat | What it does |
|---|---|
| Infinite health | Holds health at its maximum |
| Infinite armor | Holds armor at its maximum |
| Infinite ammo | Holds ammo at its maximum |
| Card rerolls 9 | Holds the card rerolls left at 9 |
| 3 dash charges | Sets the dash charges to 3 |
| Gold x10 / Gold x10 off | Gold earned (and the gold at the end of a run) x10; the off cheat puts both back to x1 |
| XP x10 / XP x10 off | XP collected x10; off puts it back to x1 |
| Spell power x10 / Spell power x10 off | Spell power multiplier 10; off puts it back to 1 |
| Cooldowns x0.1 / Cooldowns x0.1 off | Cooldowns (all, ultimate, utility) at a tenth; off puts them back to x1 |

A multiplier stays where the cheat left it after you untick it: tick its **off** cheat for a moment to put it back.

## Use

1. Download `pchost_0.6c.zip` from [Breeze Studio 0.06](https://github.com/tomvita/Breeze-Studio/releases/tag/0.06) and unzip it.
2. Unzip `RevengeOfTheMage_pchost_90D70592625DB9B4.zip` (from this release) into the same folder: it adds
   `pchost_sd\atmosphere\contents\FCD0B1B6D8328083\cheats\90D70592625DB9B4.txt` beside `pchost.exe`.
3. Start the game, then run `pchost RevengeOfTheMage-Win64-Shipping` (or double-click pchost.exe and pick the game).
4. The cheat window opens: tick the cheats you want. They all start off. **Ctrl+Alt+C** shows or hides the window.

`90D70592625DB9B4.txt` is the same cheat file on its own.

Another build (a game update, or another store's release) has another build id: pchost prints the cheat
file path it looks for when it attaches, and if the name there is not `90D70592625DB9B4.txt`, these cheats
do not fit that build.

Single-player game. Do not use pchost on games with online anti-cheat.

## How they were made

Every stat is a Gameplay Ability System attribute of the player, all in one attribute set:
`[[[[[[[[main+AB8D1F0]+228]+38]+0]+30]+350]+6A0]+1080]+0` (GWorld > game instance > local player >
player controller > pawn > AbilitySystemComponent > SpawnedAttributes[0]). Each attribute has a Base
(+8) and a Current (+C) value, and every cheat writes both. Health copies MaxHealth (+90) into
HealthPower (+50), armor MaxArmor (+110) into Armor (+D0), ammo MaxAmmo (+5F0) into CurrentAmmo (+5D0).
Breeze Studio 0.06's Objects > (attributes, GAS) lists them all and makes such cheats.

There is no gold amount cheat: the gold is in a save object reached only through a map whose order
can change, so the multipliers are used instead.

## Tested

On Nov 23 2026, in the game's hub: Infinite health and Infinite armor put the value back to the
maximum after it was lowered; a gold x10 and its off cheat set the multiplier to 10 and back to 1.
None of the cheats has been tried in a run yet: whether the game itself overwrites a written value
during a run (and so whether the multipliers, rerolls and dash charges take effect) is not known.
