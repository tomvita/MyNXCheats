# Tutorial on hacking the game with Breeze
## Hacking bar type qty
Let's hack the two bars on screen
![two bars](https://user-images.githubusercontent.com/68505331/198752830-e056eeb2-3205-4f11-966b-5afa1e0732ba.jpg)
### Make a dump
![dump](https://user-images.githubusercontent.com/68505331/198752725-af45a2fa-7a21-4dfd-996c-2f86cbc23274.jpg)
### Reduce the bars by playing the game
Reducing bar is normally the easiest task
![Reduced bar](https://user-images.githubusercontent.com/68505331/198753120-a8d48173-8527-4ab0-8839-751c7f5efd59.jpg)
### Search with u32--
Lucky for us u32-- and u32++ are good for searching both u32 and f32. The most common datatypes. 
![second search for bar reduction](https://user-images.githubusercontent.com/68505331/198753356-16ae8c3f-f6d1-4062-9e04-a4f53f298dbb.jpg)
### Recover the bars and search again
Search with u32++ 
Take note of the result file name
### Reduce the bar and search again
Search with u32--
### Recover the bars and search again
Since full bar is a known value we can take advantage of that with SameB type search
First mark the file when you have full bar. The very first dump you also have full bar but that is a big file so the search is going to be slow
![sameB](https://user-images.githubusercontent.com/68505331/198758703-37f3ec9c-2d88-4129-bf5e-a43513214b67.jpg)
### Do a few more
Get hit u32--, get hit u32 --
### By now you have reduce the candidates to a small amount so we focus the search for each bar
Take note of where we diverge
![point to split the search](https://user-images.githubusercontent.com/68505331/198760759-1a2ecd84-3e4b-4f61-b429-c8903813aa17.jpg)
### Search for HP
Get hit u32--, get hit u32--
Reduce the candidate to small amount
![small candidates for hp](https://user-images.githubusercontent.com/68505331/198760895-33eb1f29-77a4-4b38-81ac-49169e42b5c9.jpg)
### Narrow down to the final HP target
Press L to go to look at the candidates in more details.
Hack them and see what happens. Freezing is a good way to narrow down. Freeze everything to see if the list has the candidate.
This will confirm that we are on the right track.
Unfreezing and freezing until the list becomes small
![Three frozen targets](https://user-images.githubusercontent.com/68505331/198762846-5c8fd61b-acd0-4c0f-8855-7d7f65643ae1.jpg)
### Verify that the target is correct is very important
With the last one check that you actually won't die when it is frozen. Sometimes what you get is only affecting the display and the real one is another.
![one frozen target](https://user-images.githubusercontent.com/68505331/198765730-16349f7b-c7bc-4f06-8045-c199ce47fd5d.jpg)
### Look for code that access the HP address
Rstickclick to goto memory explorer
![memory explorer on HP](https://user-images.githubusercontent.com/68505331/198767629-c3981464-8d1b-4c79-b570-1ecd1b460919.jpg)
ZL+Dpadup to goto gen2 menu "+" to attach, R to start the watch
![gen2 on HP target](https://user-images.githubusercontent.com/68505331/198767669-c2695ce2-5003-4d01-be60-ee9a96519e95.jpg)
![gen2running](https://user-images.githubusercontent.com/68505331/198769338-ca5819e7-23af-4928-9d29-604800b13290.jpg)
Go back to game and play a bit then go back to Breeze.
You have found 12 code that touch this address!
Press - to detach gen2. You will now see the code disassembly.
You can save this result for use later with ZL+RstickRight
![code on hp](https://user-images.githubusercontent.com/68505331/198770040-080c9e70-a6ac-40ae-90d0-2874d6c4505c.jpg)
### Examin the codes
Move the cursor and select the code to see the code segment in detail.
We first look at the one that writes to the address.
![add on hp](https://user-images.githubusercontent.com/68505331/198772762-71f263fa-d5a9-47d7-a7d4-d14a1147b6cf.jpg)




