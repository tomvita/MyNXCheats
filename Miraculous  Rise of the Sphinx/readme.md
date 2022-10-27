Cheat creation tutorial using Breeze
![2022102720033000-974EA1D517BE2D8A7DF45665873FB575](https://user-images.githubusercontent.com/68505331/198279475-d8be2281-f3de-44e6-bb8e-9ffcb6dd7f51.jpg)
There are three cheats in this collection:

1. Moon Jump.
Start by adding freeze game code. At cheat menu press ZR, then Rstick
Now go back to game and jump, press R to freeze while she in mid way in the air.
![2022102720073600-974EA1D517BE2D8A7DF45665873FB575](https://user-images.githubusercontent.com/68505331/198280233-291c65cd-1502-45fd-a760-c64d52ad8e0b.jpg)
Goto Breeze and search with the moon jump prefix. ZL+Rstick to setup the search condition then press X to start the search
![2022102720093200-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198280582-956321c3-32de-4b9f-ab30-563015b69bf7.jpg)
Go back to game and resume. ZL+ZR+L. Now jmp and freeze the game while she falls. 
Goto Breeze and flip the search by pressing ZL+R
![2022102720120900-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198281071-74c44dff-e1ed-4efe-bb3f-d6439bc26eb8.jpg)
![2022102720145400-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198281659-2f589417-9187-4253-84d0-1bfb1d697749.jpg)
Let her rest on the floor and search for 0. Assuming on the floor is 0 makes the search faster it is not the case for every game. If it don't work skip this step.
![2022102720162500-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198282442-6c8e54f3-47fa-471b-8395-036576ff77a3.jpg)
Repeat freezing while up, freezing while down and on the floor.
![2022102720205700-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198282953-b2228a42-3a8b-4e2f-a188-f1653750de98.jpg)
![2022102720211400-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198282977-d01fd320-cf73-4eab-a829-e7b3c1592656.jpg)
![2022102720222600-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198283097-04884cf3-081b-44c3-b134-4e2a8ecb6cfb.jpg)
Now you are left with 72 candidates. Time for next step.
Make jump and freeze while up and do the search.
![2022102720260900-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198283954-3a47bc07-1bcb-4c44-9c1e-ddeb59675754.jpg)
Now is time to test which one is going to keep her moving up.
![2022102720280100-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198284195-e9984da4-74ee-4e3e-a487-eb9a8e49ad11.jpg)
Press L to goto candidate screen on the last result.
Freeze all the candidates.
![2022102720280100-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198284337-9aa3bcab-9385-43a8-adc7-37b1b1eb39f1.jpg)
Go back to game and unfreeze the action ZL+ZR+L. See that she is rising. Which confirm one of the candidate is the right one.
Next use freeze and unfreeze to narrow down until you find the actual address.
Add this address to bookmark then add bookmark to cheat (while she is rising). By now you knwo the rising is a value around 15 float. You can also just put this value before you add to cheat.
Test it by putting a conditinal key to this cheat "B" is the jump key so it make for a good choice.
Test the code and verify you are able to do moon jump.
The address you just found is only going to be valid for a short duration. 
We need to make use of it before it changes or the effort until now needs to be repeated. 
Disable the freeze game code. (don't want to use it to freeze the game anymore)
![2022102720404800-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198287006-76ad17d6-960e-40ca-a706-d176404188aa.jpg)
Press Rstick to go from bookmark to memory explorer
![2022102720405800-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198287026-d9d3ddd9-8b5a-42ee-b9e3-5f2aadce6922.jpg)
At the moment there may be problem with address that is not 16byte aligned. (i.e. last digit needs to be 0 or 8)
![2022102720521100-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198289685-32d173d3-fb02-4f34-95c4-7ec684b58732.jpg)
So we move one to the left.
Press ZL+DpadUp to go from memory explorer to gen2 menu
![2022102720522500-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198290132-5445cd68-0216-4963-8e37-9511876bb287.jpg)
Here you can choose to watch what code access this memory and whether read or write
Press + to attach dmnt.gen2 (the debugger that will capture memory access). Press R to start the watch.
Go back to game and play a bit. While the game code access this memory address it is being recorded.
Now go back to Breeze to see the results.
![2022102720561800-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198290479-9e63057c-658f-43c8-9d8c-043cc786c0c6.jpg)
This screen shows that 18 addresses of code that access the memory address has been captured. Next press - to detach.
![2022102720581000-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198290892-3d175d31-39e1-43d7-85d9-d2fc1c56cb91.jpg)
Now you can see the code that is accessing the memory. Press x to go to the disassumbly of the code.
![2022102721000100-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198291710-840b3329-a848-42d3-9ab8-42ece0133a82.jpg)
![2022102721000400-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198291744-1ea90ee4-8b91-43cd-9043-435b7fd66f08.jpg)
Next we check if this code only access the address that we want. Press L to watch this code.
![2022102721001300-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198291968-5beb7078-6442-41db-a6c1-b09f028af15e.jpg)
![2022102721010400-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198292007-9d1b9dbb-1042-4ec8-b20f-20b580e13627.jpg)
Play the game a bit and come back to Breeze to check the result.
Nice! There is only one address that the code access and comparing it with what we found earlier it is the correct address.
So now we know where we can hook a ASM hack to do moon jump. It is not always that the first one we get is going to work, if it don't work then go down the list until you find one that can work. This one access the correct memory address and only that memory but does the code run at the right time? Only the next step is going to tell.![2022102722361800-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198318328-0e7e766c-a084-40c7-9ee3-4583a13c91d4.jpg)

![2022102721163600-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198295140-3d65bc8d-e68d-432a-b86c-5232aeb4d13c.jpg)
Choose the instruction and add it to cheat. You will be prompted for a name. In this case I name it "asm mj"
A template will be created in the game directory with the name "asm mj.txt". (/switch/breeze/cheats/Miraculous  Rise of the Sphinx/asm mj.txt or /switch/breeze/cheats/0100D06015B58000/asm mj.txt depending on the option you choose in Breeze settings)
Edit this file for the ASM code to use on this address. 
This is how the file looks at the start
"
original: ldr x8, [x19, #0x148]
return: b code1+4
"![2022102722283000-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198314434-f37543e4-1b8d-4caa-9ac9-67ec8d6dd6f1.jpg)

We know the address at [x19, #0x14C] is where we want to put float 15 for her to rise.
Here is the code to do that
"
ldr w8, mj
str w8, [x19, #0x14C]
original: ldr x8, [x19, #0x148]
return: b code1+4
mj: .float 15
"
ldr w8, mj ; we can use w8 as it will be shortly overwritten by the original code, we load it with float 15
str w8, [x19, #0x14C] ; we store the value to the target
original: ldr x8, [x19, #0x148] ; we have to repeat the original so the game will run normal
return: b code1+4 ; return to the game code
mj: .float 15 ; we define the value to load here
After the file is edited go back to Breeze, goto edit cheat and press ZL+DpadUp to assemble what was written in the txt file.
![2022102721313900-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198298460-d2579b0f-0f2e-45ed-817e-27a17f2599ba.jpg)
The first line is the original code which can be use as a off code
![2022102721314500-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198298483-69b08b89-7c1a-40d3-8231-077241ccbd08.jpg)
Save it. 
Add a conditional key to the cheat. 
Edit the cheat so the original code is above the condition key
![2022102721335900-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198299089-b8246eab-b602-4086-b6c7-18a4bb03e5c7.jpg)
![2022102721341200-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198299239-d48d0be0-c480-4726-b851-0942d980838f.jpg)
![2022102721355700-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198299398-391c3989-d535-4269-858c-50f166308a70.jpg)
Moon Jump code is ready for testing.
And it does not work! 
Why it don't work is likely due to the game code is being execute at the wrong time. i.e. not while she was in the air. 
Next we capture only when she is in the air. Make the jump. Quickly press home. Start the capture (R). Go back to the game. Now it starts capturing while she is in the air.
![2022102722004900-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198306243-468c4e47-6100-4eaf-8d67-5d3ba2615cec.jpg)
Now repeat the step we do earlier on the first entry and jackpot. We have the moon jump.
![2022102722130600-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198309663-00754799-fdeb-4c6b-8f66-21d03d89645b.jpg)
![2022102722130500-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198309692-5748ddf0-6749-42ae-b101-81da41becd19.jpg)
This is the working Moon Jump code

2. The orb
This is very easy compared to moon jump 
![2022102722190000-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198312536-cff09d1b-23c2-4563-83d0-b134e665fe5c.jpg)
search again
![2022102722192500-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198312553-fc9c718a-998a-4b08-8f81-f852c93b7d2d.jpg)
hack the candidate
![2022102722205000-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198313145-34e6e4ca-b499-4ecf-bba9-5f3d0e7d44fb.jpg)
found the one
Search for the code by doing the watch on the memory, then watch the code to see that it is only writing to the correct target
![2022102722283000-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198314642-27c0bc88-e2cc-4a04-a553-d900fe4fe800.jpg)
Now it is time to hack the code.
![2022102722321900-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198315757-8919e737-4025-4dc4-929a-089bec106ac2.jpg)
Select the code line and press x
![2022102722333100-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198316127-defc5514-bcb4-4ca2-9071-28e0aa0582d4.jpg)
Scroll up and look what we have here! A add instruction which is very conveniently right above. Maybe we have an easy one here.
Add this to cheat.
![2022102722361800-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198318492-b3be7b8c-e097-4c2f-b653-58066c861ef8.jpg)
Duplicate the line for hacking and keep the original for off code
![2022102722354500-CCFA659F4857F96DDA29AFEDB2E166E6](https://user-images.githubusercontent.com/68505331/198318537-808d3375-5ca8-4658-8a7b-6bce3ca35d5a.jpg)
Add a lsl#8 to get x256









