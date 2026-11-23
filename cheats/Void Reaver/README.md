# Void Reaver (PC) cheats

For the **GOG** build of Void Reaver on Windows (Unity 6000.3.13f1). The cheats run in
[pchost](https://github.com/tomvita/Breeze-Studio/releases/tag/0.05) (0.6a or later), which
attaches to the game and runs Breeze's cheat VM on it.

| Cheat | What it does |
|---|---|
| CuriumAmount 1M | Holds Curium (the money) at 1,000,000 |
| CurrentLife 200 | Holds the character's life at 200 |

## Use

1. Download `pchost_0.6a.zip` from [Breeze Studio 0.05](https://github.com/tomvita/Breeze-Studio/releases/tag/0.05) and unzip it.
2. Put `AC8F7FB8FBFF674E.txt` in `pchost_sd\atmosphere\contents\FCB61D6A357F9BE2\cheats\` beside
   `pchost.exe` (the release's zip has that folder already: unzip it beside `pchost.exe`).
3. Start the game, then `pchost "Void Reaver"` (or run pchost.exe and pick the game).
4. The cheat window opens: tick the cheats you want. Ctrl+Alt+C shows or hides it.

The file is named by the game's build id (`GameAssembly.dll`'s). Another build, a game update or
the Steam release, has another id: pchost prints the cheat file path it looks for when it
attaches, and if that name is not `AC8F7FB8FBFF674E.txt` these cheats do not fit that build.

Single-player game; do not use pchost on games with online anti-cheat.

## How they were made

Both are pointer chains from IL2CPP static fields, found with Breeze Studio's Objects tab
(Find chain for Unity):

- Curium: `CuriumHandler.instance > currentCuriumAmount` = `[[[main+3E95B58]+B8]+0]+60` (int)
- Life: `GameManager.instance > currentCharacter > CurrentLife` = `[[[[main+3E2E830]+B8]+0]+F8]+CC` (float)
