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
ZL+Dpadup to goto gen2 menu, "+" to attach, R to start the watch
![gen2 on HP target](https://user-images.githubusercontent.com/68505331/198767669-c2695ce2-5003-4d01-be60-ee9a96519e95.jpg)
![gen2running](https://user-images.githubusercontent.com/68505331/198769338-ca5819e7-23af-4928-9d29-604800b13290.jpg)
Go back to game and play a bit then go back to Breeze.
You have found 12 code that touch this address!
Press - to detach gen2. You will now see the code disassembly.
You can save this result for use later with ZL+RstickRight
![code on hp](https://user-images.githubusercontent.com/68505331/198770040-080c9e70-a6ac-40ae-90d0-2874d6c4505c.jpg)
### Examin the codes
Move the cursor and select the code to see the code segment in detail.
We first look at the one that writes to the address. That sub instruction looks very interesting ..
![add on hp](https://user-images.githubusercontent.com/68505331/198772762-71f263fa-d5a9-47d7-a7d4-d14a1147b6cf.jpg)
### Make a in place hack
Add the instruction 
![add to cheat](https://user-images.githubusercontent.com/68505331/198778189-3ec62f48-2101-499b-b6c1-8450d086588e.jpg)
Give it a name
![give it a name](https://user-images.githubusercontent.com/68505331/198778330-b46e8a3e-28fb-4951-b880-8f06c88ee583.jpg)
Goto cheat menu and edit it. Copy the line. Edit the second line. In this case I make it add instead of subtract.
![add hp](https://user-images.githubusercontent.com/68505331/198780491-92cb862d-4a3a-4fcf-baa8-8fbdc83663f0.jpg)
Turn on the code and see what happens.
You have made a HP hack. 
### test that the hack works as intended
Some times code work on both hero and enemy. In this case it didn't otherwise it is back to the drawingboard.
### Explore further to see what other potential hook does
Do whatevery you like, should be fairly safe to hack HP. The most is crashing the game but you may want to do this a bit later as we still have another bar to hack
### Search for magic power bar
Same drill, we continue the search from the point were we diverge.
Reduce the magic by using it the do a u32-- search
![continue for magic bar](https://user-images.githubusercontent.com/68505331/198783410-b9e93dd2-4472-446c-88ed-d690b4685bf0.jpg)
Name it magic
![2022102910420700-50E2A11CE4BDDC72EF99DF78315D4938](https://user-images.githubusercontent.com/68505331/198784269-433ef2dd-b5cf-4b20-96c0-395037e233dd.jpg)
Continue the same drill with this file. Reduce the bar u32--. Reduce the bar u32 --.
![2022102910450600-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198785530-7760bef6-3080-41ed-b76f-9f1f01a5c5d9.jpg)
### Narrow down the candidate until there is only one
Do the freeze to check if one of the candidate is the one
Narrow down to only one
### Use gen2 to find the code that access this memory
![2022102910572200-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198791367-55db8466-d0bb-4cb5-b82c-5ab198cb651f.jpg)
### Look for good spot to hack
This one will fill up the magic bar
![e fill](https://user-images.githubusercontent.com/68505331/198792327-333da307-a5c4-4cfa-85a5-3f350d9fe792.jpg)
This one will stop the magic bar from decreasing
![e nop](https://user-images.githubusercontent.com/68505331/198792385-9a80759c-d060-4c77-abc3-7c469386bb47.jpg)

## Clock
### Unknow search 
Do first dump.
As the clock count down search for u32--
Will take a while but you will get there
### Alternatively bet that it is float representing the time
Search for Rang flt [A..B] (the clock number on display without the decimals) (a larger number). 
### Narrow down and hack the value to see an impact to the game
### Make a code
In this case the memory is in main. So may be static. ZL+Y to add to cheat and you are done if it is static.
Just in case capture code loation and save it should you need to come back to the drawing board.

## Making a code with code cave
This is from the example of the count down clock from above.
![2022102916551800-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198823027-5fbf77d8-1499-44d0-97b1-c35495fb2125.jpg)
What we want to do is to put the value we want into the address pointed by [x19,#0x1890]
So first we hack the existing code to make it jump to another location where there is space to put in our own code.
What we want is simply load the register s2, store it to [x19,#0x1890] and return.
~~~
ldr s2, time
str s2, [x19,#0x1890]
b code1+4
time: .float 30000
~~~
![2022102917093400-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198823431-4d9ef055-4568-4765-85db-34945e6f8320.jpg)
![2022102917094700-50E2A11CE4BDDC72EF99DF78315D4938](https://user-images.githubusercontent.com/68505331/198823436-3d489bce-664e-492d-be3b-08b238923b51.jpg)
Edit the generated "asm time.txt"
~~~
original: ldr s2, [x19, #0x1890]
return: b code1+4
~~~
Original, Breeze made this to save you a little bit of typing

~~~
ldr s2, time
original: str s2, [x19, #0x1890]
return: b code1+4
time: .float 30000
~~~
Final one to be use to assemble the cheat

Goback to Breeze and assemble the cheat
![2022102917161100-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198823754-99b83f25-2413-414c-ad4c-163e5f687b94.jpg)
![2022102917170400-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198823759-6f6c051c-b4ec-4023-8937-a48d10081f54.jpg)
Cheat is ready for testing

## One hit kill
Search for one enemy's HP. Look for one with sufficient HP for you to complete the search. Not much of a problem for this game most most have HP in the thousands.
By now you know your HP is integer and in the thousands so start a search of [A..B] 100 20000 (very conservative number)
Same drill, hit it see that the bar drop u32-- etc etc
Once you found the HP watch it.
Now you have a list of code. Look around for one that apply to the enemy and not your hero.
With that in hand make a code that make the HP small so it becomes one hit kill. This game looks like enemy won't just die when the hit point is zero. Instead it will only die if you hit it but it will become impobile when HP is zero which means you are in trouble to complete any stage that needs them to be all dead.
Set the HP to a small number.
QED.
```
original: ldr w9, [x19, #0x16b0]
cmp w9,#100
b.lt return
mov w9,#100
str w9, [x19, #0x16b0]
return: b code1+4
```
You can adjust the number 100 to anything that suits your play.
![2022102921511100-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198835364-776eb27c-a651-4dd5-bf08-43587ae44f79.jpg)
I also would put some conditional key around the code
![2022102921515100-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198835366-9b125031-ad71-49be-802d-5558cbf620a1.jpg)
Copy the original code above the conditional cond and you are done writing a one hit kill code. Now go test it. 
![2022102921515900-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198835372-5230f7b0-d058-4b87-9d3e-d616b9e6f533.jpg)

## Jump
For this game and for a few others, never jump = 0, jump once = 1, jump twice = 2
Search for it then use what you have learn in this tutorial and make the code.
The cost of doing this search is so low that it just make sense to give it a try everytime.













